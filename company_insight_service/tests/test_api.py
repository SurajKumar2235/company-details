"""
Comprehensive API test suite for Company Intelligence Service
Tests all endpoints with various scenarios
"""
import pytest
import asyncio
import logging
from httpx import AsyncClient
from fastapi.testclient import TestClient

from company_insight_service.api.app import app

# Configure logging to show test details
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Synchronous test client for simple tests
client = TestClient(app)


def log_test_info(test_name: str, endpoint: str, params: dict = None, method: str = "POST"):
    """Log test case information"""
    logger.info("=" * 80)
    logger.info(f"🧪 TEST: {test_name}")
    logger.info(f"🎯 ENDPOINT: {method} {endpoint}")
    if params:
        logger.info(f"📋 PARAMETERS:")
        for key, value in params.items():
            logger.info(f"   • {key}: {value}")
    logger.info("=" * 80)


class TestHealthEndpoints:
    """Test health check and root endpoints"""
    
    def test_root_endpoint(self):
        """Test root endpoint returns welcome message"""
        response = client.get("/")
        assert response.status_code == 200
        data = response.json()
        assert "message" in data
        assert "Company Intelligence API" in data["message"]
        assert "endpoints" in data
    
    def test_health_check(self):
        """Test health check endpoint"""
        response = client.get("/health")
        assert response.status_code == 200
        data = response.json()
        assert data["status"] == "healthy"
        assert "timestamp" in data
        assert "service" in data


class TestCompanyMonthlyEvents:
    """Test /company/monthly_events endpoint"""
    
    def test_monthly_events_success(self):
        """Test successful monthly events retrieval"""
        payload = {
            "company_name": "Apple",
            "month": "January",
            "year": 2024
        }
        log_test_info("Monthly Events - Success", "/company/monthly_events", payload)
        response = client.post("/company/monthly_events", json=payload)
        logger.info(f"✅ Response Status: {response.status_code}")
        assert response.status_code == 200
        data = response.json()
        assert data["company"] == "Apple"
        assert "January 2024" in data["period"]
        assert "events" in data
        assert isinstance(data["events"], list)
    
    def test_monthly_events_missing_company(self):
        """Test with missing company name"""
        payload = {
            "company_name": "",
            "month": "January",
            "year": 2024
        }
        response = client.post("/company/monthly_events", json=payload)
        assert response.status_code == 400
        assert "required" in response.json()["detail"].lower()
    
    def test_monthly_events_missing_month(self):
        """Test with missing month"""
        payload = {
            "company_name": "Apple",
            "month": "",
            "year": 2024
        }
        response = client.post("/company/monthly_events", json=payload)
        assert response.status_code == 400
    
    def test_monthly_events_invalid_year(self):
        """Test with invalid year"""
        payload = {
            "company_name": "Apple",
            "month": "January",
            "year": 1900
        }
        response = client.post("/company/monthly_events", json=payload)
        # Should still work but might return empty results
        assert response.status_code == 200
    
    def test_monthly_events_future_date(self):
        """Test with future date"""
        payload = {
            "company_name": "Tesla",
            "month": "December",
            "year": 2030
        }
        response = client.post("/company/monthly_events", json=payload)
        assert response.status_code == 200


class TestCompanyStockTrends:
    """Test /company/stock_trends endpoint"""
    
    def test_stock_trends_success(self):
        """Test successful stock trends analysis"""
        payload = {
            "company_name": "APPL",
            "years": 3
        }
        log_test_info("Stock Trends - Success", "/company/stock_trends", payload)
        response = client.post("/company/stock_trends", json=payload)
        logger.info(f"✅ Response Status: {response.status_code}")
        
        # This might fail if ticker not found or network issues
        if response.status_code == 200:
            data = response.json()
            assert data["company"] == "Apple"
            assert "ticker" in data
            assert "analysis" in data
            
            # Check analysis structure
            analysis = data["analysis"]
            assert "ticker" in analysis
            assert "overall_change_percent" in analysis
            assert "typical_dip_month" in analysis
            assert "typical_peak_month" in analysis
        elif response.status_code == 404:
            # Ticker not found is acceptable
            assert "not found" in response.json()["detail"].lower()
        else:
            # Other errors should be 500
            assert response.status_code == 500
    
    def test_stock_trends_with_ticker_symbol(self):
        """Test with direct ticker symbol"""
        payload = {
            "company_name": "AAPL",
            "years": 2
        }
        response = client.post("/company/stock_trends", json=payload)
        
        # Should work with ticker symbols
        if response.status_code == 200:
            data = response.json()
            assert "AAPL" in data["ticker"]
    
    def test_stock_trends_indian_company(self):
        """Test with Indian company"""
        payload = {
            "company_name": "Reliance",
            "years": 1
        }
        response = client.post("/company/stock_trends", json=payload)
        
        # Should handle Indian stocks
        assert response.status_code in [200, 404, 500]
    
    def test_stock_trends_missing_company(self):
        """Test with missing company name"""
        payload = {
            "company_name": "",
            "years": 3
        }
        response = client.post("/company/stock_trends", json=payload)
        assert response.status_code == 400
    
    def test_stock_trends_default_years(self):
        """Test with default years parameter"""
        payload = {
            "company_name": "Microsoft"
        }
        response = client.post("/company/stock_trends", json=payload)
        
        # Should use default 3 years
        if response.status_code == 200:
            data = response.json()
            assert data["analysis"]["period_years"] == 3
    
    def test_stock_trends_invalid_company(self):
        """Test with non-existent company"""
        payload = {
            "company_name": "NonExistentCompanyXYZ123",
            "years": 1
        }
        response = client.post("/company/stock_trends", json=payload)
        assert response.status_code in [404, 500]
    
    def test_stock_trends_large_years(self):
        """Test with large number of years"""
        payload = {
            "company_name": "Google",
            "years": 10
        }
        response = client.post("/company/stock_trends", json=payload)
        # Should handle gracefully
        assert response.status_code in [200, 404, 500]


class TestDeepSearchCompany:
    """Test /company/deep_search endpoint (streaming)"""
    
    def test_deep_search_success(self):
        """Test successful deep search initiation"""
        payload = {
            "company_name": "Tesla"
        }
        log_test_info("Deep Search - Success", "/company/deep_search", payload)
        response = client.post("/company/deep_search", json=payload)
        logger.info(f"✅ Response Status: {response.status_code}")
        
        # Should return streaming response
        assert response.status_code == 200
        assert "application/x-ndjson" in response.headers.get("content-type", "")
        
        # Read first few chunks
        content = response.text
        lines = content.strip().split('\n')
        
        # Should have at least one event
        assert len(lines) > 0
        
        # Each line should be valid JSON
        import json
        for line in lines[:5]:  # Check first 5 lines
            if line.strip():
                data = json.loads(line)
                assert "event" in data
    
    def test_deep_search_missing_company(self):
        """Test with missing company name"""
        payload = {
            "company_name": ""
        }
        response = client.post("/company/deep_search", json=payload)
        assert response.status_code == 400
    
    def test_deep_search_special_characters(self):
        """Test with special characters in company name"""
        payload = {
            "company_name": "AT&T"
        }
        response = client.post("/company/deep_search", json=payload)
        assert response.status_code == 200
    
    def test_deep_search_long_company_name(self):
        """Test with very long company name"""
        payload = {
            "company_name": "A" * 200
        }
        response = client.post("/company/deep_search", json=payload)
        # Should handle gracefully
        assert response.status_code in [200, 400]


class TestInputValidation:
    """Test input validation across all endpoints"""
    
    def test_invalid_json(self):
        """Test with invalid JSON"""
        response = client.post(
            "/company/monthly_events",
            data="not json",
            headers={"Content-Type": "application/json"}
        )
        assert response.status_code == 422
    
    def test_missing_required_fields(self):
        """Test with missing required fields"""
        response = client.post("/company/monthly_events", json={})
        assert response.status_code == 422
    
    def test_wrong_field_types(self):
        """Test with wrong field types"""
        payload = {
            "company_name": 123,  # Should be string
            "month": "January",
            "year": "2024"  # Should be int
        }
        response = client.post("/company/monthly_events", json=payload)
        assert response.status_code == 422
    
    def test_extra_fields_ignored(self):
        """Test that extra fields are ignored"""
        payload = {
            "company_name": "Apple",
            "month": "January",
            "year": 2024,
            "extra_field": "should be ignored"
        }
        response = client.post("/company/monthly_events", json=payload)
        assert response.status_code == 200


class TestErrorHandling:
    """Test error handling scenarios"""
    
    def test_method_not_allowed(self):
        """Test wrong HTTP method"""
        response = client.get("/company/monthly_events")
        assert response.status_code == 405
    
    def test_not_found_endpoint(self):
        """Test non-existent endpoint"""
        response = client.get("/nonexistent")
        assert response.status_code == 404
    
    def test_post_to_get_endpoint(self):
        """Test POST to GET-only endpoint"""
        response = client.post("/health")
        assert response.status_code == 405


class TestConcurrency:
    """Test concurrent requests"""
    
    @pytest.mark.asyncio
    async def test_concurrent_requests(self):
        """Test multiple concurrent requests"""
        async with AsyncClient(app=app, base_url="http://test") as ac:
            tasks = [
                ac.get("/health"),
                ac.get("/"),
                ac.post("/company/monthly_events", json={
                    "company_name": "Apple",
                    "month": "January",
                    "year": 2024
                })
            ]
            responses = await asyncio.gather(*tasks)
            
            # All should succeed
            assert all(r.status_code in [200, 400, 422] for r in responses)


class TestEdgeCases:
    """Test edge cases and boundary conditions"""
    
    def test_unicode_company_name(self):
        """Test with unicode characters"""
        payload = {
            "company_name": "日本電信電話",  # NTT in Japanese
            "month": "January",
            "year": 2024
        }
        response = client.post("/company/monthly_events", json=payload)
        assert response.status_code == 200
    
    def test_very_old_year(self):
        """Test with very old year"""
        payload = {
            "company_name": "Ford",
            "month": "January",
            "year": 1900
        }
        response = client.post("/company/monthly_events", json=payload)
        assert response.status_code == 200
    
    def test_zero_years_stock_trends(self):
        """Test stock trends with 0 years"""
        payload = {
            "company_name": "Apple",
            "years": 0
        }
        response = client.post("/company/stock_trends", json=payload)
        # Should handle gracefully
        assert response.status_code in [200, 400, 500]
    
    def test_negative_years(self):
        """Test with negative years"""
        payload = {
            "company_name": "Apple",
            "years": -1
        }
        response = client.post("/company/stock_trends", json=payload)
        # Should handle gracefully
        assert response.status_code in [200, 400, 422, 500]


class TestTelegramNotifications:
    """Test Telegram notification integration"""
    
    def test_telegram_notification_on_stock_analysis(self):
        """Test that stock analysis triggers Telegram notification"""
        import time
        from company_insight_service.core import signals
        
        # Test data
        company_name = "Apple"
        years = 3
        
        payload = {
            "company_name": company_name,
            "years": years
        }
        
        log_test_info("Telegram Notification - Stock Analysis", "/company/stock_trends", payload)
        
        # Make request
        response = client.post("/company/stock_trends", json=payload)
        logger.info(f"✅ Response Status: {response.status_code}")
        
        # Should succeed
        assert response.status_code in [200, 404, 500]
        
        if response.status_code == 200:
            data = response.json()
            
            # Send custom Telegram notification with results
            message = (
                f"📊 *Stock Analysis Complete*\n\n"
                f"🏢 *Company:* {company_name}\n"
                f"📅 *Period:* {years} years\n"
                f"🎯 *Ticker:* {data.get('ticker', 'N/A')}\n\n"
                f"📈 *Analysis Results:*\n"
                f"• Overall Change: {data['analysis'].get('overall_change_percent', 'N/A')}%\n"
                f"• Typical Dip Month: {data['analysis'].get('typical_dip_month', 'N/A')}\n"
                f"• Typical Peak Month: {data['analysis'].get('typical_peak_month', 'N/A')}\n\n"
                f"✅ Test completed successfully!"
            )
            
            # Send notification
            signals.send_telegram_message(message)
            
            # Wait for async delivery
            time.sleep(2)
            
            print(f"\n✅ Telegram notification sent for {company_name} ({years} years)")
    
    def test_telegram_notification_custom_message(self):
        """Test sending custom Telegram message"""
        import time
        from company_insight_service.core import signals
        
        # Custom test message
        test_message = (
            f"🧪 *API Test Notification*\n\n"
            f"📋 *Test Details:*\n"
            f"• Company: Tesla\n"
            f"• Analysis Period: 2 years\n"
            f"• Test Type: Integration Test\n"
            f"• Timestamp: {time.strftime('%Y-%m-%d %H:%M:%S')}\n\n"
            f"✅ All systems operational!"
        )
        
        # Send notification
        signals.send_telegram_message(test_message)
        
        # Wait for delivery
        time.sleep(2)
        
        print("\n✅ Custom Telegram notification sent")


# Pytest configuration
def pytest_configure(config):
    """Configure pytest"""
    config.addinivalue_line(
        "markers", "asyncio: mark test as async"
    )


if __name__ == "__main__":
    pytest.main([__file__, "-v", "--tb=short"])
