# syntax=docker/dockerfile:1
FROM python:3.11-slim

# Prevents Python from writing .pyc files and enables output flushing
ENV PYTHONDONTWRITEBYTECODE=1         PYTHONUNBUFFERED=1

# System deps (gcc for mysql-connector if needed)
RUN apt-get update \
	&& apt-get install -y --no-install-recommends \
	   build-essential \
	   curl \
	   ca-certificates \
	&& rm -rf /var/lib/apt/lists/*

WORKDIR /app

# Install Python deps first (better layer caching)
COPY requirements.txt /app/requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Copy source
COPY . /app

# Expose Flask port
EXPOSE 5000

# Default envs (overridden by docker-compose)
ENV FLASK_ENV=production

# Start using Gunicorn
CMD ["gunicorn", "-w", "2", "-b", "0.0.0.0:5000", "app:create_app()"]
