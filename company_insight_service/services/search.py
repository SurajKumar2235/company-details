"""
Web search functionality using DuckDuckGo
"""
import logging
from typing import List, Dict

try:
    from ddgs import DDGS
except ImportError:
    from duckduckgo_search import DDGS

from company_insight_service.config.settings import settings

logger = logging.getLogger(__name__)


def search_web(query: str, max_results: int = None) -> List[Dict]:
    """
    Search the web using DuckDuckGo
    
    Args:
        query: Search query string
        max_results: Maximum number of results (defaults to settings value)
    
    Returns:
        List of search results with title, link, and snippet
    """
    if max_results is None:
        max_results = settings.DEFAULT_SEARCH_MAX_RESULTS
        
    results = []
    logger.info(f"Searching web for: {query}")
    
    try:
        with DDGS() as ddgs:
            search_results = list(ddgs.text(query, max_results=max_results))
            for r in search_results:
                results.append({
                    "title": r.get("title"),
                    "link": r.get("href"),
                    "snippet": r.get("body")
                })
    except Exception as e:
        logger.error(f"Error searching for {query}: {e}")
        
    return results


def get_latest_news(company_name: str) -> List[Dict]:
    """Get latest news for a company"""
    return search_web(f"{company_name} company latest news", max_results=5)


def get_research_info(company_name: str) -> List[Dict]:
    """Get market research and analysis for a company"""
    return search_web(f"{company_name} company market research analysis", max_results=3)


def get_monthly_events(company_name: str, month: str, year: int) -> List[Dict]:
    """
    Find specific events that happened for a company in a given month and year
    """
    query = f"{company_name} {month} {year} news"
    logger.info(f"Searching for monthly events: {query}")
    return search_web(query, max_results=settings.MONTHLY_EVENTS_MAX_RESULTS)


def get_product_info(company_name: str) -> List[Dict]:
    """Find official product pages or summaries"""
    return search_web(f"{company_name} company main products and services", max_results=4)


def get_sales_data_search(company_name: str) -> List[Dict]:
    """Search for sales/revenue information"""
    return search_web(f"{company_name} company annual revenue sales financial report 2024", max_results=3)
