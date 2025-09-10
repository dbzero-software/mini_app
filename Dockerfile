# Dockerfile for Mini App with DBZero integration
FROM gcc:13

# Install Python and pip
RUN apt-get update && apt-get install -y \
    python3.11 \
    python3-pip \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

# Set working directory
WORKDIR /app

# Copy requirements and install Python dependencies
COPY requirements.txt .
RUN pip3 install -r requirements.txt --break-system-packages

# Copy and install DBZero package from local packages directory
COPY packages/dbzeroce-0.0.1-cp311-cp311-linux_x86_64.whl .
RUN pip3 install dbzeroce-0.0.1-cp311-cp311-linux_x86_64.whl --break-system-packages

# Copy application code
COPY . .

# Create data directory for DBZero
RUN mkdir -p /mini_app_data

# Expose port
EXPOSE 8080

# Set environment variables
ENV PYTHONPATH=/app
ENV DB_DIR=/mini_app_data/
ENV HOST=0.0.0.0
ENV PORT=8080

# Health check
HEALTHCHECK --interval=30s --timeout=10s --start-period=5s --retries=3 \
    CMD python3 -c "import requests; requests.get('http://localhost:8080/healthcheck')" || exit 1

# Run the application
CMD ["python3", "-m", "uvicorn", "mini_app.main:app", "--host", "0.0.0.0", "--port", "8080"]
