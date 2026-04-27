# Dockerfile
# Standardized production environment for HermuXclaw-CORE

FROM python:3.11-slim

# Set working directory
WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    build-essential \
    libpq-dev \
    && rm -rf /var/lib/apt/lists/*

# Install Python dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application source
COPY . .

# Expose Dashboard Port
EXPOSE 8013

# Default Command: Start the Orchestrator
CMD ["python", "core/orchestrator.py"]
