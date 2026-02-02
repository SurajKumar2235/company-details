"""
Services package - Exposes all service modules
"""
from company_insight_service.services.search import (
    search_web,
    get_latest_news,
    get_research_info,
    get_monthly_events,
    get_product_info,
    get_sales_data_search
)

from company_insight_service.services.scraping import scrape_url_content

from company_insight_service.services.sentiment import (
    analyze_sentiment,
    analyze_with_gemini,
    analyze_products
)

from company_insight_service.services.stock import (
    get_stock_data_analysis,
    find_ticker
)

from company_insight_service.services.company import gather_company_data

__all__ = [
    # Search
    'search_web',
    'get_latest_news',
    'get_research_info',
    'get_monthly_events',
    'get_product_info',
    'get_sales_data_search',
    
    # Scraping
    'scrape_url_content',
    
    # Sentiment
    'analyze_sentiment',
    'analyze_with_gemini',
    'analyze_products',
    
    # Stock
    'get_stock_data_analysis',
    'find_ticker',
    
    # Company
    'gather_company_data',
]
