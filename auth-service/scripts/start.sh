#!/bin/bash
set -e

echo "Running Alembic migrations..."
alembic upgrade head

echo "Starting FastAPI..."
exec fastapi dev app/main.py --host 0.0.0.0 --port 8000
