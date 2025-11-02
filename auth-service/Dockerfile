FROM python:3.13-slim

# Environment setup
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

WORKDIR /app

# ✅ Install system build dependencies FIRST
RUN apt-get update && apt-get install -y curl && apt-get install -y --no-install-recommends \
    build-essential \
    gcc \
    g++ \
    libffi-dev \
    libssl-dev \
    python3-dev \
    && rm -rf /var/lib/apt/lists/*

# Copy and install Python dependencies
COPY requirements.txt .
RUN pip install --upgrade pip && pip install --no-cache-dir -r requirements.txt

# Copy your app
COPY . .

# Expose port
EXPOSE 8000

# Run FastAPI in dev mode
# CMD ["fastapi", "dev", "app/main.py", "--host", "0.0.0.0", "--port", "8000"]