# Quick Reference Guide

## 🚀 Quick Start Commands

### First Time Setup
```bash
# 1. Install dependencies
make install

# 2. Start infrastructure
make docker-up

# 3. Run tests
make test

# 4. Start the system
make run-all
```

## 📋 Common Commands

### Docker Management
```bash
make docker-up          # Start PostgreSQL & RabbitMQ
make docker-down        # Stop services
make docker-restart     # Restart services
make docker-logs        # View logs
```

### Running Services
```bash
make run-api           # API only (http://localhost:8000)
make run-worker        # Worker only
make run-all           # Everything (API + Workers)
```

### Testing
```bash
make test              # All tests
make test-api          # API tests only
make test-services     # Service tests only
make test-cov          # With coverage report
make test-signals      # Telegram signal tests
```

### Development
```bash
make clean             # Clean cache files
make lint              # Check code quality
make format            # Format code
make status            # Check system status
```

## 🎯 Common Workflows

### Daily Development
```bash
# Start your day
make docker-up
make run-api

# In another terminal
make run-worker

# Run tests before committing
make test
```

### Testing Workflow
```bash
# Quick test
make quick-test

# Full test with coverage
make test-cov

# Test specific component
make test-api
```

### Deployment Preparation
```bash
# Clean and test
make clean
make test-cov
make lint

# Start fresh
make docker-restart
make run-all
```

## 🐳 Docker Services

After `make docker-up`:
- **PostgreSQL**: `localhost:5432`
- **RabbitMQ**: `localhost:5672`
- **RabbitMQ UI**: `http://localhost:15672` (guest/guest)

## 📊 API Endpoints

After `make run-api`:
- **API**: `http://localhost:8000`
- **Docs**: `http://localhost:8000/docs`
- **Health**: `http://localhost:8000/health`

## 🔧 Troubleshooting

### Port Already in Use
```bash
make docker-down
# Kill process using port 8000
lsof -ti:8000 | xargs kill -9
make run-api
```

### Clean Everything
```bash
make clean-all
make docker-up
make install
```

### Check Status
```bash
make status
make check-env
```

## 💡 Pro Tips

1. **Use `make help`** to see all available commands
2. **Run `make dev-setup`** for first-time setup
3. **Use `make quick-test`** for rapid testing
4. **Check `make status`** if something's not working
5. **Run `make clean`** regularly to avoid cache issues

## 📚 More Information

- Full documentation: `README.md`
- Testing guide: `TESTING_GUIDE.md`
- Architecture: `ARCHITECTURE.md`
- Migration guide: `MIGRATION_GUIDE.md`
