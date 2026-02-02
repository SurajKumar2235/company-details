"""
Sentiment analysis using TextBlob and Google Gemini
"""
import logging
import json
from textblob import TextBlob
from typing import Tuple, Dict, Optional, List
import concurrent.futures

from google import genai

from company_insight_service.config.settings import settings
from company_insight_service.services.scraping import scrape_url_content

logger = logging.getLogger(__name__)

# Configure Gemini Client
gemini_client = None
if settings.GEMINI_API_KEY:
    try:
        gemini_client = genai.Client(api_key=settings.GEMINI_API_KEY)
        logger.info("Gemini client initialized successfully")
    except Exception as e:
        logger.error(f"Failed to initialize Gemini Client: {e}")
else:
    logger.warning("GEMINI_API_KEY not found. Gemini features will be disabled.")


def analyze_sentiment(text: str) -> Tuple[float, str]:
    """
    Simple sentiment analysis using TextBlob
    
    Args:
        text: Text to analyze
    
    Returns:
        Tuple of (score, label) where score is -1 to 1
    """
    if not text:
        return 0, "Neutral"
        
    analysis = TextBlob(text)
    score = analysis.sentiment.polarity
    
    if score > 0.1:
        label = "Positive"
    elif score < -0.1:
        label = "Negative"
    else:
        label = "Neutral"
        
    return score, label


def analyze_with_gemini(text: str, context_query: str) -> Optional[Dict]:
    """
    Analyze text using Gemini API for sentiment and similarity
    
    Args:
        text: Text to analyze
        context_query: Context/search query for relevance scoring
    
    Returns:
        Dict with sentiment_score, sentiment_label, similarity_score, summary
        or None if Gemini is not available
    """
    if not gemini_client:
        logger.warning("Gemini Client not initialized, falling back to basic analysis.")
        return None

    try:
        prompt = f"""
        Analyze the following text content extracted from a webpage.
        Context/Search Query: "{context_query}"
        
        Text to Analyze:
        "{text[:2000]}"... (truncated)
        
        Task:
        1. Determine the Sentiment Score between -1.0 (Negative) and 1.0 (Positive).
        2. Assign a Sentiment Label (Positive, Negative, Neutral).
        3. Determine a Relevance/Similarity Score between 0.0 (Irrelevant) and 1.0 (Highly Relevant) indicating how well this text matches the intent of the Context Query.
        
        Return ONLY valid JSON in this format:
        {{
            "sentiment_score": float,
            "sentiment_label": string,
            "similarity_score": float,
            "summary": "Brief 1-sentence summary of the review/opinion"
        }}
        """
        
        response = gemini_client.models.generate_content(
            model="gemini-1.5-flash",
            contents=prompt
        )
        
        # Clean response to ensure it's valid JSON
        content = response.text.strip()
        if content.startswith("```json"):
            content = content[7:-3]
        elif content.startswith("```"):
            content = content[3:-3]
            
        return json.loads(content)
        
    except Exception as e:
        logger.error(f"Gemini analysis failed: {e}")
        return None


def analyze_products(company_name: str) -> List[Dict]:
    """
    Search for products, scrape details, and analyze sentiment concurrently
    
    Args:
        company_name: Name of the company
    
    Returns:
        List of analyzed products with sentiment scores
    """
    from company_insight_service.services.search import search_web
    
    logger.info(f"Analyzing products for: {company_name}")
    search_query = f"{company_name} consumer product reviews sentiment"
    results = search_web(search_query, max_results=5)
    
    analyzed_products = []
    
    with concurrent.futures.ThreadPoolExecutor(max_workers=5) as executor:
        # Map scrape function to urls
        future_to_url = {executor.submit(scrape_url_content, r['link']): r for r in results}
        
        for future in concurrent.futures.as_completed(future_to_url):
            r = future_to_url[future]
            content = ""
            
            try:
                content = future.result()
            except Exception as e:
                logger.warning(f"Scrape failed for {r['link']}: {e}")
            
            # Fallback to snippet if scraping yielded little text
            if len(content) < 100:
                logger.debug(f"Low content scraped for {r['link']}, using snippet.")
                content = r.get('snippet', '') + " " + r.get('title', '')
            
            if content:
                # Try Gemini first
                gemini_result = analyze_with_gemini(content, search_query)
                
                if gemini_result:
                    analyzed_products.append({
                        "title": r['title'],
                        "link": r['link'],
                        "sentiment_score": gemini_result.get("sentiment_score", 0),
                        "sentiment_label": gemini_result.get("sentiment_label", "Neutral"),
                        "similarity_score": gemini_result.get("similarity_score", 0),
                        "summary": gemini_result.get("summary", content[:300] + "...")
                    })
                else:
                    # Fallback to TextBlob
                    score, label = analyze_sentiment(content)
                    analyzed_products.append({
                        "title": r['title'],
                        "link": r['link'],
                        "sentiment_score": round(score, 2),
                        "sentiment_label": label,
                        "similarity_score": None,
                        "summary": (content[:300] + "...") if len(content) > 300 else content
                    })
                
    return analyzed_products
