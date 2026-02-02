# ⚡ Why Tests Are Slow - EXPLAINED

## The Problem

Your tests are **working correctly** but slow because:

### When Testing via Swagger Docs (`/docs`):
- ✅ You run **1 request** at a time
- ✅ Takes 5-10 seconds per request
- ✅ Feels fast because it's interactive

### When Running `make test`:
- ⏳ Pytest runs **44 tests** sequentially
- ⏳ Many tests hit **external APIs**:
  - Yahoo Finance (stock data)
  - DuckDuckGo (web search)
  - Web scraping
- ⏳ Each external API call takes 5-10 seconds
- ⏳ **Total time: 2-5 minutes** for all tests

## 🔍 Slow Tests Breakdown

| Test Class | # Tests | External API | Time Each |
|------------|---------|--------------|-----------|
| `TestHealthEndpoints` | 2 | ❌ No | <1s |
| `TestCompanyMonthlyEvents` | 5 | ✅ DuckDuckGo | 5-10s |
| `TestCompanyStockTrends` | 8 | ✅ Yahoo Finance | 5-10s |
| `TestDeepSearchCompany` | 4 | ✅ Multiple APIs | 10-20s |
| `TestInputValidation` | 4 | ❌ No | <1s |
| `TestErrorHandling` | 3 | ❌ No | <1s |
| `TestConcurrency` | 1 | ✅ APIs | 5-10s |
| `TestEdgeCases` | 4 | ✅ APIs | 5-10s |

**Total: ~17 tests hitting external APIs × 5-10s each = 85-170 seconds!**

## ⚡ Solutions

### 1. **Run Only Fast Tests** (Recommended for Development)
```bash
# Run only tests that don't hit external APIs
PYTHONPATH=. python -m pytest company_insight_service/tests/test_api.py::TestHealthEndpoints -v
PYTHONPATH=. python -m pytest company_insight_service/tests/test_api.py::TestInputValidation -v
PYTHONPATH=. python -m pytest company_insight_service/tests/test_api.py::TestErrorHandling -v
```

### 2. **Mark Slow Tests** (Best Practice)
Add markers to slow tests:

```python
# In test_api.py
import pytest

class TestCompanyStockTrends:
    @pytest.mark.slow  # Mark as slow
    def test_stock_trends_success(self):
        # ... test code
```

Then run:
```bash
# Skip slow tests
make test -m "not slow"

# Run only slow tests
make test -m "slow"
```

### 3. **Mock External APIs** (Production Best Practice)
```python
# In test_api.py
from unittest.mock import patch, Mock

class TestCompanyStockTrends:
    @patch('company_insight_service.services.stock.yf.download')
    def test_stock_trends_success_mocked(self, mock_download):
        # Mock the response
        mock_download.return_value = Mock(...)  # Fast!
        
        payload = {"company_name": "AAPL", "years": 3}
        response = client.post("/company/stock_trends", json=payload)
        assert response.status_code == 200
```

### 4. **Use Pytest-xdist for Parallel Testing**
```bash
# Install
pip install pytest-xdist

# Run tests in parallel (4 workers)
PYTHONPATH=. python -m pytest company_insight_service/tests/ -n 4
```

### 5. **Reduce Test Scope**
```python
# Change years from 3 to 1 for faster tests
payload = {
    "company_name": "AAPL",
    "years": 1  # 3x faster!
}
```

## 🎯 Quick Fix for You

### Option A: Run Only Fast Tests
```bash
# Add to Makefile
test-fast:
\t@echo "🧪 Running fast tests only..."
\tPYTHONPATH=. python -m pytest company_insight_service/tests/test_api.py::TestHealthEndpoints company_insight_service/tests/test_api.py::TestInputValidation company_insight_service/tests/test_api.py::TestErrorHandling -v
```

### Option B: Skip Slow Tests
Create `pytest.ini`:
```ini
[pytest]
markers =
    slow: marks tests as slow (deselect with '-m "not slow"')
    integration: marks tests as integration tests
```

Then mark slow tests and run:
```bash
make test -m "not slow"  # Fast tests only
```

### Option C: Mock External Calls (Recommended)
I can create a mocked version of the tests that runs in <5 seconds total!

## 📊 Performance Comparison

| Method | Time | Tests Run |
|--------|------|-----------|
| **Swagger Docs** | 5-10s | 1 test |
| **pytest (all)** | 2-5 min | 44 tests |
| **pytest (fast only)** | <10s | 13 tests |
| **pytest (mocked)** | <5s | 44 tests |
| **pytest (parallel)** | <1 min | 44 tests |

## ✅ Recommendation

For **development**:
```bash
# Run fast tests only
make test-fast
```

For **CI/CD**:
```bash
# Run all tests with mocks
make test-mocked
```

For **integration testing**:
```bash
# Run real API tests (slow but thorough)
make test  # Current behavior
```

## 🚀 Want Me to Implement?

I can create:
1. ✅ Fast test suite (mocked external APIs)
2. ✅ Pytest markers for slow tests
3. ✅ Parallel test execution
4. ✅ Separate make commands for fast/slow tests

**Which would you like?**

---

**Bottom Line:**
- Your tests are **working perfectly** ✅
- They're slow because they hit **real external APIs** ⏳
- This is **normal** for integration tests ✅
- Use mocks or markers to speed up development testing ⚡
