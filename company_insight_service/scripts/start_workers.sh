#!/bin/bash
# Start background workers

cd "$(dirname "$0")/.."

# Set PYTHONPATH to parent directory
export PYTHONPATH="$(cd .. && pwd):$PYTHONPATH"

NUM_WORKERS=${1:-4}

echo "Starting $NUM_WORKERS background workers..."

for i in $(seq 1 $NUM_WORKERS); do
    PYTHONPATH="$PYTHONPATH" python -m company_insight_service.run_worker > "logs/worker_$i.log" 2>&1 &
    echo "Started worker $i with PID $!"
done

echo "All workers started"
