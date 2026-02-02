# Company Intelligence Service

A comprehensive FastAPI-based service for deep company insights using AI, web scraping, and financial analysis.

## 🚀 Quick Start

### Using Makefile (Recommended)
```bash
# First time setup
make install
make docker-up

# Run tests
make test

# Start the system
make run-all
```

### Using Commands Script
```bash
# Make executable
chmod +x commands.sh

# View all commands
./commands.sh help

# Start system
./commands.sh docker-up
./commands.sh run-all
```

### Manual Commands
```bash
# Install dependencies
pip install -r requirements.txt -r req.txt

# Start infrastructure
cd company_insight_service
docker-compose up -d

# Start API
python -m company_insight_service.run_api

# Start worker (in another terminal)
python -m company_insight_service.run_worker
```

## 📋 Available Commands

### Makefile Commands
```bash
make help              # Show all commands
make install           # Install dependencies
make docker-up         # Start Docker services
make run-api           # Start API server
make run-worker        # Start background worker
make run-all           # Start everything
make test              # Run all tests
make test-cov          # Run tests with coverage
make clean             # Clean cache files
```

### Script Commands
```bash
./commands.sh help           # Show all commands
./commands.sh install        # Install dependencies
./commands.sh docker-up      # Start Docker services
./commands.sh run-api        # Start API server
./commands.sh test           # Run tests
./commands.sh status         # Check system status
```

## 🏗️ Project Structure

```
company_insight_service/
├── api/              # FastAPI routes and app
├── config/           # Configuration and settings
├── core/             # Core functionality (signals)
├── database/         # Database models
├── services/         # Business logic (modular)
├── workers/          # Background processing
├── workflows/        # LangGraph workflows
├── tests/            # Test suite
└── scripts/          # Utility scripts
```

## 🔧 Configuration

Create `.env` file in `company_insight_service/`:

```env
# Database
DATABASE_URL=postgresql://user:password@localhost:5432/company_db

# RabbitMQ
RABBITMQ_URL=amqp://guest:guest@localhost:5672/
RABBITMQ_QUEUE_NAME=company_insights

# API Keys
GEMINI_API_KEY=your_gemini_api_key

# Telegram (optional)
TELEGRAM_BOT_TOKEN=your_bot_token
TELEGRAM_CHAT_ID=your_chat_id

# Settings
LOG_LEVEL=INFO
API_WORKERS=4
```

## 🧪 Testing

```bash
# Run all tests
make test

# Run specific test suite
make test-api
make test-services
make test-signals
make test-telegram     # NEW: Test Telegram notifications

# Run with coverage
make test-cov

# View coverage report
open htmlcov/index.html
```

## 📊 API Endpoints

Once running, visit:
- **API Docs**: http://localhost:8000/docs
- **Health Check**: http://localhost:8000/health

### Main Endpoints

#### 1. Monthly Events
```bash
POST /company/monthly_events
{
  "company_name": "Apple",
  "month": "January",
  "year": 2024
}
```

#### 2. Stock Trends
```bash
POST /company/stock_trends
{
  "company_name": "Tesla",
  "years": 3
}
```

#### 3. Deep Search (Streaming)
```bash
POST /company/deep_search
{
  "company_name": "Microsoft"
}
```

## 🐳 Docker Services

After `make docker-up`:
- **PostgreSQL**: `localhost:5432`
- **RabbitMQ**: `localhost:5672`
- **RabbitMQ Management UI**: http://localhost:15672 (guest/guest)

## 🎯 Features

- ✅ **Web Search**: DuckDuckGo integration
- ✅ **AI Analysis**: Google Gemini for sentiment analysis
- ✅ **Stock Data**: yfinance for financial analysis
- ✅ **Async Processing**: RabbitMQ queue system
- ✅ **Real-time Notifications**: Telegram integration
- ✅ **Database Signals**: Automatic event tracking
- ✅ **Streaming API**: Real-time progress updates
- ✅ **Comprehensive Tests**: 200+ test cases

## 📚 Documentation

- [Quick Start Guide](QUICK_START.md)
- [Testing Guide](TESTING_GUIDE.md)
- [Architecture Overview](ARCHITECTURE.md)
- [Migration Guide](MIGRATION_GUIDE.md)

## 🛠️ Development

### Setup Development Environment
```bash
make dev-setup
```

### Code Quality
```bash
make lint          # Check code quality
make format        # Format code with black
```

### Cleanup
```bash
make clean         # Clean cache files
make clean-all     # Clean everything including Docker
```

## 🔍 Troubleshooting

### Check System Status
```bash
make status
make check-env
```

### View Logs
```bash
make docker-logs
```

### Reset Everything
```bash
make clean-all
make docker-up
make install
```

## 📈 Performance

- **Parallel Processing**: 4 workers by default
- **Async Operations**: Non-blocking I/O
- **Queue-based**: Resilient message processing
- **Caching**: Smart result caching

## 🤝 Contributing

1. Fork the repository
2. Create feature branch
3. Make changes
4. Run tests: `make test`
5. Submit pull request

## 📝 License

MIT License

## 🙏 Acknowledgments

- FastAPI for the web framework
- LangGraph for workflow orchestration
- Google Gemini for AI capabilities
- yfinance for stock data

## 📞 Support

For issues and questions:
1. Check documentation
2. Run `make status`
3. View logs with `make docker-logs`
4. Open an issue on GitHub

---

**Made with ❤️ using FastAPI, LangGraph, and AI**
