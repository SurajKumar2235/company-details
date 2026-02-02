#!/bin/bash
# Run all tests with coverage

cd "$(dirname "$0")/.."

echo "🧪 Running Company Intelligence API Tests"
echo "=========================================="

# Install test dependencies
echo "📦 Installing test dependencies..."
pip install -q pytest pytest-asyncio pytest-cov httpx

# Run tests with coverage
echo ""
echo "🏃 Running tests..."
python -m pytest tests/ \
    -v \
    --tb=short \
    --cov=company_insight_service \
    --cov-report=term-missing \
    --cov-report=html \
    "$@"

echo ""
echo "✅ Tests complete!"
echo "📊 Coverage report generated in htmlcov/index.html"
