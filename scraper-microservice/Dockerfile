# Use Python 3.12 as base image
FROM python:3.12

# Set the working directory inside the container
WORKDIR /app

# Copy the project files into the container
COPY requirements.txt .
COPY src/ /app/src/

# Install dependencies
RUN pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt

# Set environment variables for Celery
ENV CELERY_BROKER_URL=pyamqp://guest@rabbitmq//
ENV CELERY_RESULT_BACKEND=mongodb://mongo:27017/scraper_results

# Define default command (Celery worker)
CMD ["celery", "-A", "tasks.scrape", "worker", "--loglevel=info"]
