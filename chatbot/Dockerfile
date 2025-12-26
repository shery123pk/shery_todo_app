# Chatbot Dockerfile
# Phase III: AI-Powered Todo Chatbot
# Author: Sharmeen Asif

FROM python:3.13-slim

WORKDIR /app

# Install UV package manager
RUN pip install --no-cache-dir uv

# Copy dependency files
COPY pyproject.toml ./

# Install dependencies
RUN uv pip install --system --no-cache .

# Copy application code
COPY app/ ./app/

# Create non-root user
RUN useradd -m -u 1000 chatbotuser && \
    chown -R chatbotuser:chatbotuser /app
USER chatbotuser

# Run chatbot
CMD ["python", "-m", "app.main"]
