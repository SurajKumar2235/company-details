# 🔔 Telegram Notification Tests

## New Tests Added!

I've added comprehensive Telegram notification tests to `test_api.py`.

### What the Tests Do

#### 1. **Stock Analysis Notification** (`test_telegram_notification_on_stock_analysis`)
- Runs stock analysis for a company
- Formats the results beautifully
- Sends to Telegram with:
  - Company name
  - Analysis period (years)
  - Ticker symbol
  - Overall change percentage
  - Typical dip month
  - Typical peak month

#### 2. **Custom Message Test** (`test_telegram_notification_custom_message`)
- Sends a custom formatted test message
- Includes timestamp
- Tests the Telegram integration directly

## 🚀 How to Run

### Option 1: Using Make (Recommended)
```bash
make test-telegram
```

### Option 2: Using Script
```bash
bash company_insight_service/scripts/test_telegram.sh
```

### Option 3: Direct Pytest
```bash
PYTHONPATH=. python -m pytest company_insight_service/tests/test_api.py::TestTelegramNotifications -v -s
```

## 📋 What You'll See

### In Terminal:
```
🔔 Testing Telegram notifications...
test_telegram_notification_on_stock_analysis PASSED
✅ Telegram notification sent for Apple (3 years)

test_telegram_notification_custom_message PASSED
✅ Custom Telegram notification sent
```

### In Telegram:
You'll receive 2 messages:

**Message 1: Stock Analysis Results**
```
📊 *Stock Analysis Complete*

🏢 *Company:* Apple
📅 *Period:* 3 years
🎯 *Ticker:* AAPL

📈 *Analysis Results:*
• Overall Change: 45.2%
• Typical Dip Month: January
• Typical Peak Month: December

✅ Test completed successfully!
```

**Message 2: Custom Test Message**
```
🧪 *API Test Notification*

📋 *Test Details:*
• Company: Tesla
• Analysis Period: 2 years
• Test Type: Integration Test
• Timestamp: 2026-01-31 23:42:00

✅ All systems operational!
```

## ⚙️ Configuration

Make sure your `.env` file has:
```env
TELEGRAM_BOT_TOKEN=your_bot_token_here
TELEGRAM_CHAT_ID=your_chat_id_here
```

## 🎯 Test Features

✅ **Real API Integration** - Tests actual stock analysis
✅ **Formatted Messages** - Beautiful Markdown formatting
✅ **Company & Year Info** - Includes all requested details
✅ **Async Delivery** - Non-blocking Telegram sends
✅ **Error Handling** - Graceful failures if Telegram not configured

## 📊 Example Usage

### Test with Different Companies
Edit `test_api.py` line 383:
```python
company_name = "Tesla"  # Or any company
years = 2              # Or any number
```

### Test with Real-time Data
The test uses live stock data, so results will vary based on:
- Current market conditions
- Historical performance
- Time period selected

## 🔍 Debugging

If notifications don't arrive:

1. **Check Telegram credentials**
   ```bash
   make check-env
   ```

2. **View logs**
   ```bash
   # Look for Telegram-related messages
   make test-telegram 2>&1 | grep -i telegram
   ```

3. **Test credentials directly**
   ```bash
   python -c "from company_insight_service.core import signals; import asyncio; asyncio.run(signals.test_telegram_setup())"
   ```

## ✨ Benefits

- ✅ **Automated Testing** - No manual Telegram testing needed
- ✅ **Real Data** - Tests with actual stock analysis
- ✅ **Beautiful Formatting** - Professional-looking messages
- ✅ **Easy to Extend** - Add more notification tests easily

## 🎓 How It Works

```python
# 1. Run stock analysis
response = client.post("/company/stock_trends", json=payload)

# 2. Format results
message = f"📊 *Stock Analysis Complete*\n..."

# 3. Send to Telegram
signals.send_telegram_message(message)

# 4. Wait for delivery
time.sleep(2)
```

## 🚀 Next Steps

Run the test now:
```bash
make test-telegram
```

Then check your Telegram! 📱

---

**Happy Testing! 🎉**
