#!/bin/bash
# Start complete system (infrastructure + API + workers)

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$SCRIPT_DIR/.."

# Set PYTHONPATH to parent directory
export PYTHONPATH="$(cd .. && pwd):$PYTHONPATH"

echo "==================================="
echo "Company Intelligence System Startup"
echo "==================================="

# 1. Start infrastructure
echo ""
echo "1️⃣ Starting infrastructure (PostgreSQL + RabbitMQ)..."
docker-compose up -d

echo "   Waiting for services to be ready..."
sleep 5

# 2. Create logs directory
mkdir -p logs

# 3. Start background workers
echo ""
echo "2️⃣ Starting background workers..."
NUM_WORKERS=${1:-4}

for i in $(seq 1 $NUM_WORKERS); do
    PYTHONPATH="$PYTHONPATH" python -m company_insight_service.run_worker > "logs/worker_$i.log" 2>&1 &
    echo "   Started worker $i with PID $!"
done

# 4. Start API server
echo ""
echo "3️⃣ Starting API server..."
echo "   API will be available at http://localhost:8000"
echo "   API docs at http://localhost:8000/docs"
echo ""

PYTHONPATH="$PYTHONPATH" python -m company_insight_service.run_api
