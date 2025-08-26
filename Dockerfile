# Base image
FROM python:3.11-slim

# Set workdir
WORKDIR /app

# Install system deps (for psycopg2 / postgres client)
RUN apt-get update && apt-get install -y \
    libpq-dev gcc && \
    rm -rf /var/lib/apt/lists/*

# Install python deps
COPY requirements.txt .
RUN pip install -r requirements.txt

# Copy project files
COPY . .

# Expose port (gunicorn will bind here)
EXPOSE 8000

# Default command (compose overrides this anyway)
CMD ["gunicorn", "onlineartgallery.wsgi:application", "--bind", "0.0.0.0:8000"]
