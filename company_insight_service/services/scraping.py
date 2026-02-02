"""
Web scraping functionality
"""
import logging
import requests
from bs4 import BeautifulSoup

from company_insight_service.config.settings import settings

logger = logging.getLogger(__name__)


def scrape_url_content(url: str) -> str:
    """
    Extract text content from a URL
    
    Args:
        url: URL to scrape
    
    Returns:
        Extracted text content (limited to SCRAPE_MAX_CHARS)
    """
    logger.debug(f"Scraping URL: {url}")
    
    try:
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
            'Accept-Language': 'en-US,en;q=0.9',
        }
        
        response = requests.get(url, headers=headers, timeout=settings.SCRAPE_TIMEOUT)
        
        if response.status_code == 200:
            soup = BeautifulSoup(response.text, 'html.parser')
            
            # Remove script, style, nav, footer, header elements
            for script in soup(["script", "style", "nav", "footer", "header"]):
                script.extract()
                
            text = soup.get_text()
            
            # Clean up text
            lines = (line.strip() for line in text.splitlines())
            chunks = (phrase.strip() for line in lines for phrase in line.split("  "))
            text = '\n'.join(chunk for chunk in chunks if chunk)
            
            return text[:settings.SCRAPE_MAX_CHARS]
            
    except Exception as e:
        logger.warning(f"Failed to scrape {url}: {e}")
        
    return ""
