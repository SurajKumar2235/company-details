# Testing Guide

## 📋 Test Suite Overview

The project includes comprehensive tests for all API endpoints and services:

### Test Files
- **`test_api.py`** - API endpoint tests (200+ test cases)
- **`test_services.py`** - Service layer unit tests
- **`test_system.py`** - System integration tests (Telegram signals)
- **`conftest.py`** - Pytest configuration and fixtures

## 🚀 Running Tests

### Run All Tests
```bash
cd company_insight_service
bash scripts/run_tests.sh
```

### Run Specific Test File
```bash
pytest tests/test_api.py -v
```

### Run Specific Test Class
```bash
pytest tests/test_api.py::TestHealthEndpoints -v
```

### Run Specific Test
```bash
pytest tests/test_api.py::TestHealthEndpoints::test_root_endpoint -v
```

### Run with Coverage
```bash
pytest tests/ --cov=company_insight_service --cov-report=html
```

### Run Only Fast Tests
```bash
pytest tests/ -m "not slow"
```

## 📊 Test Categories

### 1. Health Endpoints (`TestHealthEndpoints`)
- ✅ Root endpoint
- ✅ Health check endpoint

### 2. Monthly Events (`TestCompanyMonthlyEvents`)
- ✅ Successful retrieval
- ✅ Missing company name
- ✅ Missing month
- ✅ Invalid year
- ✅ Future dates

### 3. Stock Trends (`TestCompanyStockTrends`)
- ✅ Successful analysis
- ✅ Direct ticker symbols
- ✅ Indian companies
- ✅ Missing company
- ✅ Default parameters
- ✅ Invalid companies
- ✅ Large time ranges

### 4. Deep Search (`TestDeepSearchCompany`)
- ✅ Streaming response
- ✅ Missing company
- ✅ Special characters
- ✅ Long company names

### 5. Input Validation (`TestInputValidation`)
- ✅ Invalid JSON
- ✅ Missing required fields
- ✅ Wrong field types
- ✅ Extra fields handling

### 6. Error Handling (`TestErrorHandling`)
- ✅ Wrong HTTP methods
- ✅ Non-existent endpoints
- ✅ Method not allowed

### 7. Concurrency (`TestConcurrency`)
- ✅ Concurrent requests
- ✅ Async operations

### 8. Edge Cases (`TestEdgeCases`)
- ✅ Unicode characters
- ✅ Very old dates
- ✅ Zero/negative values
- ✅ Boundary conditions

## 🔧 Test Configuration

### Fixtures Available
```python
# In conftest.py
- sample_company_data: Mock company data
- mock_settings: Mock application settings
- test_client: FastAPI test client
```

### Custom Markers
```python
@pytest.mark.slow      # Slow tests
@pytest.mark.integration  # Integration tests
@pytest.mark.unit      # Unit tests
@pytest.mark.api       # API tests
```

## 📈 Coverage Goals

- **API Endpoints**: 100% coverage
- **Services**: 80%+ coverage
- **Overall**: 85%+ coverage

## 🐛 Debugging Tests

### Run with Verbose Output
```bash
pytest tests/ -vv
```

### Show Print Statements
```bash
pytest tests/ -s
```

### Stop on First Failure
```bash
pytest tests/ -x
```

### Run Last Failed Tests
```bash
pytest tests/ --lf
```

### Debug with PDB
```bash
pytest tests/ --pdb
```

## 📝 Writing New Tests

### Example Test Structure
```python
class TestNewFeature:
    """Test new feature"""
    
    def test_success_case(self, test_client):
        """Test successful operation"""
        response = test_client.post("/endpoint", json={...})
        assert response.status_code == 200
        assert "expected_key" in response.json()
    
    def test_error_case(self, test_client):
        """Test error handling"""
        response = test_client.post("/endpoint", json={...})
        assert response.status_code == 400
```

## 🔄 CI/CD Integration

### GitHub Actions Example
```yaml
- name: Run tests
  run: |
    pip install -r requirements.txt
    pip install -r tests/requirements-test.txt
    pytest tests/ --cov=company_insight_service
```

## 📊 Test Results

After running tests, you'll see:
- ✅ Pass/Fail status for each test
- 📊 Coverage percentage
- 🕐 Execution time
- 📄 HTML coverage report in `htmlcov/`

## 🎯 Best Practices

1. **Isolate Tests**: Each test should be independent
2. **Use Fixtures**: Reuse common setup code
3. **Mock External Calls**: Don't rely on external APIs
4. **Test Edge Cases**: Include boundary conditions
5. **Clear Names**: Test names should describe what they test
6. **Fast Tests**: Keep unit tests fast, mark slow tests

## 🚨 Common Issues

### Import Errors
```bash
# Make sure you're in the right directory
cd /path/to/test_kube
python -m pytest company_insight_service/tests/
```

### Missing Dependencies
```bash
pip install -r company_insight_service/tests/requirements-test.txt
```

### Database Errors
```bash
# Ensure test database is configured
# Tests use in-memory SQLite by default
```

## 📚 Resources

- [Pytest Documentation](https://docs.pytest.org/)
- [FastAPI Testing](https://fastapi.tiangolo.com/tutorial/testing/)
- [Coverage.py](https://coverage.readthedocs.io/)
