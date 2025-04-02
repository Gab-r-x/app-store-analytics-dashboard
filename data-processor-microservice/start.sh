#!/bin/bash

set -e  # Fail on error

echo "📦 Running Alembic migrations..."
alembic -c /app/alembic.ini upgrade head

echo "🚀 Starting Celery worker..."
cd /app/src
exec celery -A celery_worker worker --loglevel=info -Q data_processor


