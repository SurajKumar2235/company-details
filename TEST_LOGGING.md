# 📊 Test Execution Logging

## What You'll See Now

When running tests, you'll see detailed information about:
- ✅ Which test case is running
- ✅ Which endpoint it's hitting
- ✅ What parameters are being sent
- ✅ Response status code

## Example Output

### Running Tests
```bash
make test-api
```

### What You'll See:

```
================================================================================
🧪 TEST: Monthly Events - Success
🎯 ENDPOINT: POST /company/monthly_events
📋 PARAMETERS:
   • company_name: Apple
   • month: January
   • year: 2024
================================================================================
✅ Response Status: 200

================================================================================
🧪 TEST: Stock Trends - Success
🎯 ENDPOINT: POST /company/stock_trends
📋 PARAMETERS:
   • company_name: APPL
   • years: 3
================================================================================
2026-01-31 23:45:00 - INFO - Finding ticker for: APPL
2026-01-31 23:45:05 - INFO - Verified direct ticker: APPL.BO
2026-01-31 23:45:05 - INFO - Analyzing stock for ticker: APPL.BO over 3 years
✅ Response Status: 200

================================================================================
🧪 TEST: Deep Search - Success
🎯 ENDPOINT: POST /company/deep_search
📋 PARAMETERS:
   • company_name: Tesla
================================================================================
✅ Response Status: 200

================================================================================
🧪 TEST: Telegram Notification - Stock Analysis
🎯 ENDPOINT: POST /company/stock_trends
📋 PARAMETERS:
   • company_name: Apple
   • years: 3
================================================================================
✅ Response Status: 200
✅ Telegram notification sent for Apple (3 years)
```

## Benefits

### 1. **Clear Test Identification**
You can instantly see which test is running:
```
🧪 TEST: Stock Trends - Success
```

### 2. **Endpoint Visibility**
Know exactly which API endpoint is being tested:
```
🎯 ENDPOINT: POST /company/stock_trends
```

### 3. **Parameter Tracking**
See all parameters being sent:
```
📋 PARAMETERS:
   • company_name: APPL
   • years: 3
```

### 4. **Response Status**
Immediate feedback on success/failure:
```
✅ Response Status: 200
```

## Running with Verbose Output

### See Everything
```bash
# With pytest verbose mode
PYTHONPATH=. python -m pytest company_insight_service/tests/test_api.py -v -s

# Or with make
make test-api
```

### Filter Specific Tests
```bash
# Only stock trends tests
PYTHONPATH=. python -m pytest company_insight_service/tests/test_api.py::TestCompanyStockTrends -v -s

# Only Telegram tests
make test-telegram
```

## Log Levels

The logging is configured to show:
- **INFO**: Test execution details
- **WARNING**: Potential issues
- **ERROR**: Failures

### Customize Log Level
```python
# In test_api.py, change:
logging.basicConfig(
    level=logging.DEBUG,  # More detailed
    # or
    level=logging.WARNING,  # Less verbose
)
```

## Example: Full Test Run

```bash
$ make test-telegram

🔔 Testing Telegram notifications...
PYTHONPATH=. python -m pytest company_insight_service/tests/test_api.py::TestTelegramNotifications -v -s

================================================================================
🧪 TEST: Telegram Notification - Stock Analysis
🎯 ENDPOINT: POST /company/stock_trends
📋 PARAMETERS:
   • company_name: Apple
   • years: 3
================================================================================
2026-01-31 23:45:10 - INFO - Finding ticker for: Apple
2026-01-31 23:45:11 - INFO - Verified direct ticker: AAPL
2026-01-31 23:45:11 - INFO - Analyzing stock for ticker: AAPL over 3 years
2026-01-31 23:45:16 - INFO - Fetching stock data for AAPL from 3 years ago to now
2026-01-31 23:45:18 - INFO - yfinance successfully downloaded data for AAPL
✅ Response Status: 200
2026-01-31 23:45:18 - INFO - ✉️ Telegram notification sent

✅ Telegram notification sent for Apple (3 years)
PASSED

test_telegram_notification_custom_message 
✅ Custom Telegram notification sent
PASSED

======================== 2 passed in 12.34s ========================
```

## What's Logged

### For Each Test:
1. **Test Name** - Human-readable description
2. **HTTP Method** - POST, GET, etc.
3. **Endpoint** - Full API path
4. **Parameters** - All request data
5. **Response Status** - HTTP status code
6. **Additional Info** - Service-specific logs

### Service Logs:
- Stock ticker discovery
- Data fetching progress
- Analysis results
- Telegram notifications
- Error messages

## Debugging Made Easy

### Find Failing Tests
```bash
# Run and see which test fails
make test-api 2>&1 | grep -A 5 "TEST:"
```

### Track Specific Endpoint
```bash
# See all calls to stock_trends
make test-api 2>&1 | grep -A 10 "stock_trends"
```

### Monitor Parameters
```bash
# See what parameters are being sent
make test-api 2>&1 | grep -A 5 "PARAMETERS"
```

## 🎯 Quick Reference

| What You Want | Command |
|---------------|---------|
| See all test details | `make test-api` |
| See specific test | `pytest test_api.py::TestName -v -s` |
| Quiet mode | `pytest test_api.py -q` |
| Show print statements | `pytest test_api.py -s` |
| Stop on first failure | `pytest test_api.py -x` |

## ✨ Benefits

✅ **Transparency** - See exactly what's being tested
✅ **Debugging** - Quickly identify issues
✅ **Learning** - Understand API usage
✅ **Monitoring** - Track test execution
✅ **Documentation** - Self-documenting tests

---

**Now you can see exactly what each test is doing! 🎉**
