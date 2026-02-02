.PHONY: help install test run-api run-worker run-all docker-up docker-down docker-logs clean lint format

# Default target
help:
	@echo "🚀 Company Intelligence Service - Available Commands"
	@echo "===================================================="
	@echo ""
	@echo "📦 Setup & Installation:"
	@echo "  make install          - Install all dependencies"
	@echo "  make install-test     - Install test dependencies"
	@echo ""
	@echo "🐳 Docker Commands:"
	@echo "  make docker-up        - Start PostgreSQL & RabbitMQ"
	@echo "  make docker-down      - Stop all Docker services"
	@echo "  make docker-restart   - Restart Docker services"
	@echo "  make docker-logs      - View Docker logs"
	@echo "  make docker-clean     - Remove Docker volumes"
	@echo ""
	@echo "🏃 Running Services:"
	@echo "  make run-api          - Start API server only"
	@echo "  make run-worker       - Start worker only"
	@echo "  make run-all          - Start complete system (API + Workers)"
	@echo ""
	@echo "🧪 Testing:"
	@echo "  make test             - Run all tests"
	@echo "  make test-api         - Run API tests only"
	@echo "  make test-services    - Run service tests only"
	@echo "  make test-cov         - Run tests with coverage"
	@echo "  make test-signals     - Run signal/Telegram tests"
	@echo ""
	@echo "🔍 Code Quality:"
	@echo "  make lint             - Run linting checks"
	@echo "  make format           - Format code with black"
	@echo ""
	@echo "🧹 Cleanup:"
	@echo "  make clean            - Clean cache and temp files"
	@echo "  make clean-all        - Clean everything including Docker"
	@echo ""

# Installation
install:
	@echo "📦 Installing dependencies..."
	pip install -r requirements.txt
	pip install -r req.txt
	@echo "✅ Installation complete!"

install-test:
	@echo "📦 Installing test dependencies..."
	pip install -r company_insight_service/tests/requirements-test.txt
	@echo "✅ Test dependencies installed!"

# Docker commands
docker-up:
	@echo "🐳 Starting Docker services..."
	cd company_insight_service && docker-compose up -d
	@echo "⏳ Waiting for services to be ready..."
	@sleep 5
	@echo "✅ Docker services started!"
	@echo "   PostgreSQL: localhost:5432"
	@echo "   RabbitMQ: localhost:5672"
	@echo "   RabbitMQ Management: http://localhost:15672"

docker-down:
	@echo "🛑 Stopping Docker services..."
	cd company_insight_service && docker-compose down
	@echo "✅ Docker services stopped!"

docker-restart: docker-down docker-up

docker-logs:
	@echo "📋 Showing Docker logs..."
	cd company_insight_service && docker-compose logs -f

docker-clean:
	@echo "🧹 Cleaning Docker volumes..."
	cd company_insight_service && docker-compose down -v
	@echo "✅ Docker volumes cleaned!"

# Running services
run-api:
	@echo "🚀 Starting API server..."
	@echo "   API: http://localhost:8000"
	@echo "   Docs: http://localhost:8000/docs"
	@echo ""
	PYTHONPATH=. python -m company_insight_service.run_api

run-worker:
	@echo "⚙️ Starting background worker..."
	PYTHONPATH=. python -m company_insight_service.run_worker

run-all:
	@echo "🚀 Starting complete system..."
	cd company_insight_service && bash scripts/start_parallel.sh

# Testing
test:
	@echo "🧪 Running all tests..."
	PYTHONPATH=. python -m pytest company_insight_service/tests/ -v

test-api:
	@echo "🧪 Running API tests..."
	PYTHONPATH=. python -m pytest company_insight_service/tests/test_api.py -v

test-services:
	@echo "🧪 Running service tests..."
	PYTHONPATH=. python -m pytest company_insight_service/tests/test_services.py -v

test-signals:
	@echo "🧪 Running signal tests..."
	python company_insight_service/tests/test_system.py

test-telegram:
	@echo "🔔 Testing Telegram notifications..."
	PYTHONPATH=. python -m pytest company_insight_service/tests/test_api.py::TestTelegramNotifications -v -s

test-cov:
	@echo "🧪 Running tests with coverage..."
	PYTHONPATH=. python -m pytest company_insight_service/tests/ \
		--cov=company_insight_service \
		--cov-report=term-missing \
		--cov-report=html
	@echo "📊 Coverage report: htmlcov/index.html"

test-watch:
	@echo "👀 Running tests in watch mode..."
	python -m pytest company_insight_service/tests/ -v --looponfail

# Code quality
lint:
	@echo "🔍 Running linting checks..."
	@command -v flake8 >/dev/null 2>&1 || pip install flake8
	flake8 company_insight_service --exclude=__pycache__,*.pyc --max-line-length=120

format:
	@echo "✨ Formatting code..."
	@command -v black >/dev/null 2>&1 || pip install black
	black company_insight_service --exclude='/(\.git|\.venv|__pycache__|\.pytest_cache)/'
	@echo "✅ Code formatted!"


# Cleanup
clean:
	@echo "🧹 Cleaning cache files..."
	find . -type d -name "__pycache__" -exec rm -rf {} + 2>/dev/null || true
	find . -type f -name "*.pyc" -delete
	find . -type f -name "*.pyo" -delete
	find . -type d -name "*.egg-info" -exec rm -rf {} + 2>/dev/null || true
	find . -type d -name ".pytest_cache" -exec rm -rf {} + 2>/dev/null || true
	rm -rf htmlcov .coverage
	@echo "✅ Cache cleaned!"

clean-all: clean docker-clean
	@echo "✅ Everything cleaned!"

# Development helpers
dev-setup: install install-test docker-up
	@echo "✅ Development environment ready!"
	@echo ""
	@echo "Next steps:"
	@echo "  1. Configure .env file"
	@echo "  2. Run: make test"
	@echo "  3. Run: make run-all"

check-env:
	@echo "🔍 Checking environment configuration..."
	@test -f company_insight_service/.env && echo "✅ .env file exists" || echo "❌ .env file missing!"
	@python -c "from company_insight_service.config.settings import settings; print('✅ Settings loaded successfully')" 2>/dev/null || echo "❌ Settings configuration error"

db-init:
	@echo "🗄️ Initializing database..."
	python -c "from company_insight_service.database.models import init_db; init_db(); print('✅ Database initialized')"

# Quick commands
quick-test: docker-up test
	@echo "✅ Quick test complete!"

quick-start: docker-up run-all
	@echo "✅ System started!"

# Status check
status:
	@echo "📊 System Status"
	@echo "==============="
	@echo ""
	@echo "Docker Services:"
	@cd company_insight_service && docker-compose ps || echo "  Not running"
	@echo ""
	@echo "Python Environment:"
	@python --version
	@echo ""
	@echo "Installed Packages:"
	@pip list | grep -E "(fastapi|uvicorn|sqlalchemy|pika|langchain)" || echo "  Core packages not found"
