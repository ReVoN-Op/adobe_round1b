FROM python:3.9-slim

# Set working directory
WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    gcc \
    g++ \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements first for better caching
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY . .

# Create directories
RUN mkdir -p /app/data/input /app/data/output /app/models

# Download and cache the embedding model
RUN python -c "from sentence_transformers import SentenceTransformer; SentenceTransformer('all-MiniLM-L6-v2')"

# Set environment variables
ENV PYTHONPATH=/app
ENV MODEL_CACHE_DIR=/app/models

# Expose port (if needed for API)
EXPOSE 8000

# Default command
CMD ["python", "main.py"]