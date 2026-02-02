# Project Restructuring Plan

## Current Structure Issues
- All modules in root directory (flat structure)
- No separation of concerns
- Tests mixed with source code
- No clear API routing separation

## New Proposed Structure

```
company_insight_service/
├── __init__.py
├── config/
│   ├── __init__.py
│   └── settings.py              # Configuration management
│
├── core/
│   ├── __init__.py
│   ├── signals.py               # Database event listeners
│   └── messaging.py             # Telegram/notification utilities
│
├── database/
│   ├── __init__.py
│   ├── models.py                # SQLAlchemy models
│   └── session.py               # Database session management
│
├── services/
│   ├── __init__.py
│   ├── search.py                # Web search functionality
│   ├── scraping.py              # Web scraping
│   ├── sentiment.py             # Sentiment analysis
│   ├── stock.py                 # Stock analysis
│   └── company.py               # Company data gathering
│
├── workers/
│   ├── __init__.py
│   ├── consumer.py              # RabbitMQ consumer
│   └── queue_utils.py           # Queue utilities
│
├── workflows/
│   ├── __init__.py
│   └── company_research.py      # LangGraph workflows
│
├── api/
│   ├── __init__.py
│   ├── app.py                   # FastAPI app initialization
│   ├── dependencies.py          # API dependencies
│   └── routes/
│       ├── __init__.py
│       ├── company.py           # Company endpoints
│       ├── stock.py             # Stock endpoints
│       └── health.py            # Health check endpoints
│
├── tests/
│   ├── __init__.py
│   ├── conftest.py              # Pytest fixtures
│   ├── test_signals.py          # Signal tests
│   ├── test_services.py         # Service tests
│   ├── test_api.py              # API endpoint tests
│   └── test_integration.py      # Integration tests
│
├── scripts/
│   ├── start_api.sh
│   ├── start_workers.sh
│   └── start_parallel.sh
│
├── docker-compose.yml
├── requirements.txt
└── README.md
```

## Migration Steps

1. Create new directory structure
2. Move and refactor modules
3. Update imports
4. Create __init__.py files
5. Update entry points
6. Test everything
