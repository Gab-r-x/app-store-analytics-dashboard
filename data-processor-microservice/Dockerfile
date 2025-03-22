FROM python:3.12-slim

# Set working directory
WORKDIR /app

# Copy requirements and install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy app source code
COPY src/ ./src

# Default command (override when running celery worker or script)
CMD ["python", "src/main.py"]
