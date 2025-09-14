FROM python:3.11-slim

WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    gcc \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements first (for better caching)
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY synthetic_data_agent.py .
COPY app.py .

# Create output directory for generated files
RUN mkdir -p /app/output

# Expose port for web interface
EXPOSE 8080

# Run the web application
CMD ["python", "app.py"]
