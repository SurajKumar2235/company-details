"""
Company data gathering service
Consolidates all company-related data collection
"""
import logging
from typing import Dict

from company_insight_service.services.search import (
    get_latest_news,
    get_research_info,
    get_product_info,
    get_sales_data_search
)

logger = logging.getLogger(__name__)


def gather_company_data(company_name: str) -> Dict:
    """
    Gather comprehensive company data from multiple sources
    
    Args:
        company_name: Name of the company
    
    Returns:
        Dict containing news, products, research, and sales data
    """
    logger.info(f"Gathering comprehensive data for: {company_name}")
    
    return {
        "company": company_name,
        "news": get_latest_news(company_name),
        "products": get_product_info(company_name),
        "research": get_research_info(company_name),
        "sales_data": {
            "search_results": get_sales_data_search(company_name),
            "note": "For precise structure, integration with paid financial APIs is recommended."
        }
    }
