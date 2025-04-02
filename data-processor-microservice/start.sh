#!/bin/bash

set -e  # Fail on error

echo "📦 Running Alembic migrations..."
alembic -c /app/alembic.ini upgrade head

echo "🚀 Starting Celery worker..."
cd /app/src

# Init worker in background
celery -A celery_worker worker --loglevel=info -Q data_processor &

# Espera o worker iniciar (ajuste o tempo se necessário)
sleep 20

# Dispara a task de geração de labels
echo "🧠 Triggering label generation task..."
python -c "from tasks.generate_labels import generate_app_labels; generate_app_labels.delay()"

# Aguarda o worker
wait
