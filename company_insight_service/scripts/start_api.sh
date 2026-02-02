#!/bin/bash
# Start API server

cd "$(dirname "$0")/.."

# Set PYTHONPATH to parent directory
export PYTHONPATH="$(cd .. && pwd):$PYTHONPATH"

echo "Starting Company Intelligence API..."
python -m company_insight_service.run_api
