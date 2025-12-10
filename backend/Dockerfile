FROM python:3.14-slim

WORKDIR /app

# Install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY app/ ./app/
COPY data/ ./data/

# Create db directory with proper permissions BEFORE switching user
RUN mkdir -p /app/db && chmod 777 /app/db

# Run as non-root user
RUN useradd -m -u 1000 appuser && chown -R appuser:appuser /app
USER appuser

CMD ["fastapi", "run", "app/main.py", "--proxy-headers", "--forwarded-allow-ips", "172.20.0.0/16", "--port", "8000"]
