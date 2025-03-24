# Use Python 3.12 as base image
FROM python:3.12-slim

# Set working directory
WORKDIR /app

# Install system dependencies if needed (can be extended later)
RUN apt-get update && apt-get install -y \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

# Copy configuration and requirements
COPY settings.toml /app/
COPY alembic.ini /app/
COPY requirements.txt /app/
COPY /tests/ /app/
COPY alembic/ /app/alembic/

# Install Python dependencies
RUN pip install --no-cache-dir --upgrade pip \
    && pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY src/ /app/src/

# Set environment variables for Celery (optional defaults, can be overridden in docker-compose)
ENV CELERY_BROKER_URL=pyamqp://guest@rabbitmq//
ENV CELERY_RESULT_BACKEND=db+mongodb://mongo:27017/scraper_results

# Default command (can be overridden in docker-compose)
CMD ["python", "src/main.py"]
