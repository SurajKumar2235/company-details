#!/bin/bash

source .venv/bin/activate
cd company_insight_service && docker-compose up -ds
uvicorn main:app --host 0.0.0.0 --port 8000 --reload