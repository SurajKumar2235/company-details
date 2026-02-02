"""
Stock analysis and ticker discovery functionality
"""
import logging
import re
import json
import traceback
from typing import Optional, Dict
from collections import Counter
import calendar

import yfinance as yf
import pandas as pd

from company_insight_service.config.settings import settings
from company_insight_service.services.search import search_web
from company_insight_service.services.sentiment import gemini_client

logger = logging.getLogger(__name__)

def get_stock_data_analysis(ticker: str, years: int = 3) -> Optional[Dict]:
    """
    Fetch stock data for N years and analyze trends
    
    Args:
        ticker: Stock ticker symbol
        years: Number of years to analyze
    
    Returns:
        Dict with analysis results or None if failed
    """
    logger.info(f"Analyzing stock for ticker: {ticker} over {years} years")
    
    if not ticker:
        return None
    logger.info(f"Fetching stock data for {ticker} from {years} years ago to now")
    end_date = pd.Timestamp.now()
    start_date = end_date - pd.DateOffset(years=years)
    
    try:
        # Download stock data
        data = yf.download(ticker, start=start_date, end=end_date, progress=False)
        logger.info(f"yfinance successfully downloaded data for {ticker}. Data preview:\n{data.head()}")
        if data.empty:
            logger.warning(f"yfinance returned no data for ticker: {ticker}")
            return None
            
        # Log success and show data preview in terminal
        logger.info(f"yfinance successfully returned data for {ticker}. Data preview:\n{data.head()}")
            
        # Handle yfinance MultiIndex structure
        if isinstance(data.columns, pd.MultiIndex):
            try:
                data = data.xs(ticker, level=1, axis=1)
            except Exception:
                pass
                
        if 'Close' not in data:
            logger.warning(f"'Close' column missing in data for {ticker}")
            return None

        close_series = data['Close']
        if isinstance(close_series, pd.DataFrame):
            close_series = close_series.iloc[:, 0]

        # Analyze monthly patterns
        monthly_avg = close_series.groupby(close_series.index.month).mean()
        best_month = monthly_avg.idxmax()
        worst_month = monthly_avg.idxmin()
        
        best_month_name = calendar.month_name[best_month]
        worst_month_name = calendar.month_name[worst_month]
        
        latest_price = close_series.iloc[-1]
        start_price = close_series.iloc[0]
        
        # Ensure scalar values
        if hasattr(latest_price, 'item'):
            latest_price = latest_price.item()
        if hasattr(start_price, 'item'):
            start_price = start_price.item()
            
        overall_change = ((latest_price - start_price) / start_price) * 100
        
        return {
            "ticker": ticker,
            "period_years": years,
            "overall_change_percent": round(float(overall_change), 2),
            "typical_dip_month": worst_month_name,
            "typical_peak_month": best_month_name,
            "latest_price": round(float(latest_price), 2),
            "data_points": len(close_series)
        }
        
    except Exception as e:
        logger.error(f"Error analyzing stock {ticker}: {e}")
        logger.debug(traceback.format_exc())
        return None


def find_ticker(company_name: str) -> Optional[str]:
    """
    Find stock ticker symbol for a company
    
    Uses multiple strategies with 20-second timeout:
    1. Direct ticker validation
    2. Web search with regex patterns
    3. Gemini AI extraction
    4. Frequency-based validation
    
    Args:
        company_name: Company name or potential ticker
    
    Returns:
        Validated ticker symbol or None (returns within 20 seconds)
    """
    import time
    start_time = time.time()
    MAX_SEARCH_TIME = 20  # Maximum 20 seconds for ticker search
    
    logger.info(f"Finding ticker for: {company_name} (max {MAX_SEARCH_TIME}s)")
    
    # Strategy 1: Check if input is already a valid ticker
    if 2 <= len(company_name) <= 12 and company_name.replace('.', '').isalnum():
        logger.debug(f"Checking {company_name} as direct ticker")
        
        variations = [company_name.upper()]
        if "." not in company_name:
            variations.extend([
                f"{company_name.upper()}.NS",
                f"{company_name.upper()}.BO"
            ])
            
        for var in variations:
            try:
                if not yf.Ticker(var).history(period="1d").empty:
                    logger.info(f"Verified direct ticker: {var}")
                    return var
            except:
                pass


    # Strategy 2: Search for ticker using web search (with timeout)
    elapsed = time.time() - start_time
    if elapsed > MAX_SEARCH_TIME:
        logger.warning(f"⏱️ Ticker search timeout ({MAX_SEARCH_TIME}s) - stopping search")
        return None
    
    logger.info(f"Starting web search (elapsed: {elapsed:.1f}s)")
    queries = [
        f"{company_name} stock ticker symbol",
        f"what is the stock ticker for {company_name}",
    ]
    
    potential_tickers = []
    all_results = []
    
    for q in queries:
        # Check timeout before each query
        elapsed = time.time() - start_time
        if elapsed > MAX_SEARCH_TIME:
            logger.warning(f"⏱️ Timeout reached during web search ({elapsed:.1f}s)")
            break
        
        results = search_web(q, max_results=2)
        all_results.extend(results)
        
        for r in results:
            text = (r['title'] + " " + r['snippet']).upper()
            text = text.replace(":", " ").replace("-", " ")
            
            logger.debug(f"Ticker search text: {text[:100]}...")
            
            # Extract potential tickers using regex patterns
            matches_parenthesis = re.findall(r'\(([A-Z]{1,5})\)', text)
            for m in matches_parenthesis:
                if m not in ['NYSE', 'NASDAQ', 'INC', 'CORP', 'LTD', 'USA', 'UNK', 'STOCK']:
                    potential_tickers.append(m)
            
            matches_ticker_keyword = re.findall(r'TICKER\s+([A-Z]{1,5})', text)
            potential_tickers.extend(matches_ticker_keyword)
            
            matches_stock_keyword = re.findall(r'STOCK\s+([A-Z]{1,5})', text)
            potential_tickers.extend(matches_stock_keyword)
            
            matches_exchange = re.findall(r'(?:NASDAQ|NYSE)\s+([A-Z]{1,5})', text)
            potential_tickers.extend(matches_exchange)
            
    # Strategy 3: Use Gemini to extract ticker (with timeout check)
    elapsed = time.time() - start_time
    if elapsed > MAX_SEARCH_TIME:
        logger.warning(f"⏱️ Timeout reached before Gemini call ({elapsed:.1f}s)")
        return None
    
    if gemini_client and all_results:
        try:
            prompt_context = "\n".join([f"{r['title']}: {r['snippet']}" for r in all_results])
            ticker_prompt = f"""
            Identify the stock exchange ticker symbol for the company "{company_name}" based on the search results below.
            
            Search Results:
            {prompt_context}
            
            Rules:
            1. Return only the ticker symbol (e.g., "AAPL", "RELIANCE", "SBIN").
            2. If the company is listed on Indian exchanges (NSE/BSE), prefer the base symbol (e.g., return "SBIN", not "SBIN.NS").
            3. Ignore noise words like "PRICE", "QUOTE", "STOCK", "SYMBOL".
            4. If multiple tickers exist, pick the most primary/liquid one.
            5. Return JSON format: {{"ticker": "SYMBOL"}} or {{"ticker": null}} if not found.
            """
            
            response = gemini_client.models.generate_content(
                model="gemini-1.5-flash",
                contents=ticker_prompt
            )
            
            cleaned_text = response.text.replace('```json', '').replace('```', '').strip()
            data = json.loads(cleaned_text)
            candidate = data.get("ticker")
            
            if candidate:
                logger.info(f"Gemini suggested ticker: {candidate}")
                
                # Validate suggested ticker
                suffixes = ["", ".NS", ".BO"]
                for suffix in suffixes:
                    trial_ticker = candidate + suffix
                    try:
                        if not yf.Ticker(trial_ticker).history(period="1d").empty:
                            logger.info(f"Verified Gemini ticker: {trial_ticker}")
                            return trial_ticker
                    except:
                        pass
                        
        except Exception as e:
            logger.error(f"Gemini ticker extraction failed: {e}")

    # Strategy 4: Frequency-based validation
    if potential_tickers:
        noise = {
            'THE', 'FOR', 'AND', 'INC', 'CORP', 'LTD', 'PLC', 'USD', 'COM',
            'PRICE', 'QUOTE', 'STOCK', 'SYMBOL', 'TICKER', 'MARKET', 'SHARE',
            'TRADE', 'VALUE', 'CLOSE', 'OPEN', 'HIGH', 'LOW', 'VOL', 'DATE',
            'TIME', 'YEAR', 'MONTH', 'WEEK', 'DAY', 'EXCHA', 'TRADI', 'TICKE',
            'SYMBO', 'CHANGE', 'PERCENT', 'COMPAN', 'GROUP', 'INDIA', 'BANK'
        }
        filtered = [t for t in potential_tickers if t not in noise]
        
        if filtered:
            most_common = Counter(filtered).most_common(3)
            
            for candidate, _ in most_common:
                logger.info(f"Verifying candidate ticker: {candidate}")
                
                suffixes = ["", ".NS", ".BO"]
                for suffix in suffixes:
                    trial_ticker = candidate + suffix
                    try:
                        hist = yf.Ticker(trial_ticker).history(period="1d")
                        if not hist.empty:
                            logger.info(f"Verified ticker: {trial_ticker}")
                            return trial_ticker
                    except:
                        pass
        
    elapsed = time.time() - start_time
    logger.warning(f"❌ No valid ticker found for '{company_name}' (searched for {elapsed:.1f}s)")
    return None
