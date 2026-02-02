"""
Pytest configuration and fixtures
"""
import pytest
import sys
from pathlib import Path

# Add project root to path
project_root = Path(__file__).parent.parent.parent
sys.path.insert(0, str(project_root))


@pytest.fixture
def sample_company_data():
    """Sample company data for testing"""
    return {
        "company_name": "Test Company",
        "ticker": "TEST",
        "news": [
            {"title": "News 1", "link": "https://example.com/1", "snippet": "snippet 1"}
        ],
        "product_sentiment": [
            {
                "title": "Product Review",
                "link": "https://example.com/review",
                "sentiment_score": 0.8,
                "sentiment_label": "Positive",
                "summary": "Great product"
            }
        ],
        "stock_analysis": {
            "ticker": "TEST",
            "overall_change_percent": 15.5,
            "typical_dip_month": "January",
            "typical_peak_month": "December"
        }
    }


@pytest.fixture
def mock_settings():
    """Mock settings for testing"""
    from unittest.mock import Mock
    settings = Mock()
    settings.DATABASE_URL = "sqlite:///:memory:"
    settings.RABBITMQ_URL = "amqp://guest:guest@localhost:5672/"
    settings.RABBITMQ_QUEUE_NAME = "test_queue"
    settings.GEMINI_API_KEY = "test_key"
    settings.TELEGRAM_BOT_TOKEN = "test_token"
    settings.TELEGRAM_CHAT_ID = "test_chat_id"
    settings.LOG_LEVEL = "INFO"
    settings.DEFAULT_SEARCH_MAX_RESULTS = 5
    settings.SCRAPE_TIMEOUT = 5
    settings.SCRAPE_MAX_CHARS = 5000
    return settings


@pytest.fixture
def test_client():
    """FastAPI test client"""
    from fastapi.testclient import TestClient
    from company_insight_service.api.app import app
    return TestClient(app)


# Pytest markers
def pytest_configure(config):
    """Configure custom pytest markers"""
    config.addinivalue_line(
        "markers", "slow: marks tests as slow (deselect with '-m \"not slow\"')"
    )
    config.addinivalue_line(
        "markers", "integration: marks tests as integration tests"
    )
    config.addinivalue_line(
        "markers", "unit: marks tests as unit tests"
    )
    config.addinivalue_line(
        "markers", "api: marks tests as API tests"
    )
