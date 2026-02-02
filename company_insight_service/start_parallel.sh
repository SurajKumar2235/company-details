#!/bin/bash
# Start script for parallel execution

# Get the directory where the script is located
SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" &> /dev/null && pwd )"
# Project Root is one level up
PROJECT_ROOT="$SCRIPT_DIR/.."

# Ensure we are in the service directory for docker-compose
cd "$SCRIPT_DIR"

# 1. Start RabbitMQ (if not running)
echo "Starting RabbitMQ..."
docker-compose up -d rabbitmq

# Wait a moment for RabbitMQ to be ready (rudimentary)
sleep 5

# 2. Start Background Workers (Parallel Consumers)
# We need to run python from the project root so the module import works
echo "Switching to Project Root: $PROJECT_ROOT"
cd "$PROJECT_ROOT"

echo "Starting 4 background workers..."
for i in {1..4}
do
   # logs redirected to individual files for debugging
   python -m company_insight_service.worker > "$SCRIPT_DIR/worker_$i.log" 2>&1 &
   echo "Started worker $i with PID $!"
done

# 3. Start API (Parallel Producers/Handlers)
echo "Starting API with multiple workers..."
python -m company_insight_service.main
