#!/bin/bash
# Comprehensive project commands script
# Alternative to Makefile for systems without make

set -e

PROJECT_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$PROJECT_ROOT"

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Helper functions
print_header() {
    echo -e "${BLUE}===================================================${NC}"
    echo -e "${BLUE}$1${NC}"
    echo -e "${BLUE}===================================================${NC}"
}

print_success() {
    echo -e "${GREEN}✅ $1${NC}"
}

print_error() {
    echo -e "${RED}❌ $1${NC}"
}

print_info() {
    echo -e "${YELLOW}ℹ️  $1${NC}"
}

# Command functions
cmd_help() {
    print_header "Company Intelligence Service - Commands"
    echo ""
    echo "Usage: ./commands.sh [command]"
    echo ""
    echo "📦 Setup & Installation:"
    echo "  install          - Install all dependencies"
    echo "  install-test     - Install test dependencies"
    echo ""
    echo "🐳 Docker Commands:"
    echo "  docker-up        - Start PostgreSQL & RabbitMQ"
    echo "  docker-down      - Stop all Docker services"
    echo "  docker-restart   - Restart Docker services"
    echo "  docker-logs      - View Docker logs"
    echo "  docker-clean     - Remove Docker volumes"
    echo ""
    echo "🏃 Running Services:"
    echo "  run-api          - Start API server only"
    echo "  run-worker       - Start worker only"
    echo "  run-all          - Start complete system"
    echo ""
    echo "🧪 Testing:"
    echo "  test             - Run all tests"
    echo "  test-api         - Run API tests only"
    echo "  test-services    - Run service tests only"
    echo "  test-cov         - Run tests with coverage"
    echo "  test-signals     - Run signal tests"
    echo ""
    echo "🧹 Cleanup:"
    echo "  clean            - Clean cache files"
    echo "  clean-all        - Clean everything"
    echo ""
    echo "🔍 Utilities:"
    echo "  status           - Check system status"
    echo "  check-env        - Verify environment"
    echo ""
}

cmd_install() {
    print_header "Installing Dependencies"
    pip install -r requirements.txt
    pip install -r req.txt
    print_success "Installation complete!"
}

cmd_install_test() {
    print_header "Installing Test Dependencies"
    pip install -r company_insight_service/tests/requirements-test.txt
    print_success "Test dependencies installed!"
}

cmd_docker_up() {
    print_header "Starting Docker Services"
    cd company_insight_service
    docker-compose up -d
    cd ..
    print_info "Waiting for services to be ready..."
    sleep 5
    print_success "Docker services started!"
    echo ""
    echo "   PostgreSQL: localhost:5432"
    echo "   RabbitMQ: localhost:5672"
    echo "   RabbitMQ Management: http://localhost:15672"
}

cmd_docker_down() {
    print_header "Stopping Docker Services"
    cd company_insight_service
    docker-compose down
    cd ..
    print_success "Docker services stopped!"
}

cmd_docker_restart() {
    cmd_docker_down
    cmd_docker_up
}

cmd_docker_logs() {
    print_header "Docker Logs"
    cd company_insight_service
    docker-compose logs -f
}

cmd_docker_clean() {
    print_header "Cleaning Docker Volumes"
    cd company_insight_service
    docker-compose down -v
    cd ..
    print_success "Docker volumes cleaned!"
}

cmd_run_api() {
    print_header "Starting API Server"
    echo "   API: http://localhost:8000"
    echo "   Docs: http://localhost:8000/docs"
    echo ""
    python -m company_insight_service.run_api
}

cmd_run_worker() {
    print_header "Starting Background Worker"
    python -m company_insight_service.run_worker
}

cmd_run_all() {
    print_header "Starting Complete System"
    cd company_insight_service
    bash scripts/start_parallel.sh
}

cmd_test() {
    print_header "Running All Tests"
    python -m pytest company_insight_service/tests/ -v
}

cmd_test_api() {
    print_header "Running API Tests"
    python -m pytest company_insight_service/tests/test_api.py -v
}

cmd_test_services() {
    print_header "Running Service Tests"
    python -m pytest company_insight_service/tests/test_services.py -v
}

cmd_test_signals() {
    print_header "Running Signal Tests"
    python company_insight_service/tests/test_system.py
}

cmd_test_cov() {
    print_header "Running Tests with Coverage"
    python -m pytest company_insight_service/tests/ \
        --cov=company_insight_service \
        --cov-report=term-missing \
        --cov-report=html
    print_success "Coverage report: htmlcov/index.html"
}

cmd_clean() {
    print_header "Cleaning Cache Files"
    find . -type d -name "__pycache__" -exec rm -rf {} + 2>/dev/null || true
    find . -type f -name "*.pyc" -delete
    find . -type f -name "*.pyo" -delete
    find . -type d -name "*.egg-info" -exec rm -rf {} + 2>/dev/null || true
    find . -type d -name ".pytest_cache" -exec rm -rf {} + 2>/dev/null || true
    rm -rf htmlcov .coverage
    print_success "Cache cleaned!"
}

cmd_clean_all() {
    cmd_clean
    cmd_docker_clean
    print_success "Everything cleaned!"
}

cmd_status() {
    print_header "System Status"
    echo ""
    echo "Docker Services:"
    cd company_insight_service
    docker-compose ps || echo "  Not running"
    cd ..
    echo ""
    echo "Python Environment:"
    python --version
    echo ""
    echo "Key Packages:"
    pip list | grep -E "(fastapi|uvicorn|sqlalchemy|pika|langchain)" || echo "  Not installed"
}

cmd_check_env() {
    print_header "Environment Check"
    if [ -f "company_insight_service/.env" ]; then
        print_success ".env file exists"
    else
        print_error ".env file missing!"
    fi
    
    python -c "from company_insight_service.config.settings import settings; print('✅ Settings loaded')" 2>/dev/null || print_error "Settings error"
}

# Main command dispatcher
COMMAND=${1:-help}

case "$COMMAND" in
    help) cmd_help ;;
    install) cmd_install ;;
    install-test) cmd_install_test ;;
    docker-up) cmd_docker_up ;;
    docker-down) cmd_docker_down ;;
    docker-restart) cmd_docker_restart ;;
    docker-logs) cmd_docker_logs ;;
    docker-clean) cmd_docker_clean ;;
    run-api) cmd_run_api ;;
    run-worker) cmd_run_worker ;;
    run-all) cmd_run_all ;;
    test) cmd_test ;;
    test-api) cmd_test_api ;;
    test-services) cmd_test_services ;;
    test-signals) cmd_test_signals ;;
    test-cov) cmd_test_cov ;;
    clean) cmd_clean ;;
    clean-all) cmd_clean_all ;;
    status) cmd_status ;;
    check-env) cmd_check_env ;;
    *)
        print_error "Unknown command: $COMMAND"
        echo ""
        cmd_help
        exit 1
        ;;
esac
