# Use Python 3.12 as base image
FROM python:3.12

# Set working directory
WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    curl unzip \
    chromium \
    chromium-driver \
    && rm -rf /var/lib/apt/lists/*

# Set environment variables for Chromium
ENV CHROMIUM_BINARY="/usr/bin/chromium"
ENV PATH="/usr/lib/chromium/:${PATH}"

# Copy configuration and application files into the container
COPY settings.toml /app/
COPY requirements.txt .
COPY src/ /app/src/

# Install Python dependencies
RUN pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt

# Set environment variables for Celery
ENV CELERY_BROKER_URL=pyamqp://guest@rabbitmq//
ENV CELERY_RESULT_BACKEND=mongodb://mongo:27017/scraper_results

# Default command
CMD ["celery", "-A", "src.tasks", "worker", "--loglevel=info"]
