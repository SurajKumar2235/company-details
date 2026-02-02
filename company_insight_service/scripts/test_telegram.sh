#!/bin/bash
# Test Telegram notifications

cd "$(dirname "$0")/.."

echo "🔔 Testing Telegram Notifications"
echo "=================================="
echo ""
echo "This will:"
echo "1. Run stock analysis for Apple (3 years)"
echo "2. Send formatted results to Telegram"
echo "3. Send a custom test message"
echo ""
echo "Make sure your Telegram credentials are configured in .env"
echo ""

# Set PYTHONPATH
export PYTHONPATH="$(cd .. && pwd):$PYTHONPATH"

# Run only Telegram tests
PYTHONPATH="$PYTHONPATH" python -m pytest tests/test_api.py::TestTelegramNotifications -v -s

echo ""
echo "✅ Check your Telegram for notifications!"
