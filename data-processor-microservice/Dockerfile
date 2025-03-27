# Use Python 3.12 as base image
FROM python:3.12-slim

# Set working directory
WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

# Copy configuration and requirements
COPY settings.toml /app/
COPY alembic.ini /app/
COPY requirements.txt /app/
COPY /tests/ /app/
COPY alembic/ /app/alembic/
COPY start.sh /app/start.sh

# Install Python dependencies
RUN pip install --no-cache-dir --upgrade pip \
    && pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY src/ /app/src/

# Set execution permission for start script
RUN chmod +x /app/start.sh

# Set environment variables (can be overridden)
ENV PYTHONPATH=/app/src
ENV C_FORCE_ROOT=1

# Run processor + worker together
CMD ["./start.sh"]
