# Backend Dockerfile for HuggingFace Spaces Deployment
# Author: Sharmeen Asif
# CRITICAL: Must use port 7860 for HuggingFace Spaces

FROM python:3.13-slim

WORKDIR /app

# Install system dependencies
RUN apt-get update && \
    apt-get install -y --no-install-recommends \
    gcc \
    postgresql-client \
    curl && \
    rm -rf /var/lib/apt/lists/*

# Install UV package manager
RUN pip install --no-cache-dir uv

# Copy dependency files
COPY pyproject.toml ./

# Install dependencies
RUN uv pip install --system --no-cache .
RUN uv pip install --system --no-cache ".[dev]"

# Copy application code
COPY app/ ./app/
COPY alembic/ ./alembic/
COPY alembic.ini ./

# Create non-root user for security
RUN useradd -m -u 1000 appuser && \
    chown -R appuser:appuser /app
USER appuser

# Expose port 7860 (HuggingFace Spaces requirement - NON-NEGOTIABLE)
EXPOSE 7860

# Health check endpoint
HEALTHCHECK --interval=30s --timeout=5s --start-period=10s --retries=3 \
    CMD curl --fail http://localhost:7860/health || exit 1

# Run migrations and start server on port 7860
CMD ["sh", "-c", "alembic upgrade head && uvicorn app.main:app --host 0.0.0.0 --port 7860 --workers 1"]
