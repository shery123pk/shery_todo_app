"""
Test FastAPI app initialization.

Tests CORS configuration, middleware registration, router mounting,
and exception handlers.
"""

import pytest
from fastapi.testclient import TestClient


def test_app_creation():
    """Test that FastAPI app is created."""
    from app.main import app

    assert app is not None
    assert app.title
    assert app.version


def test_cors_middleware():
    """Test that CORS middleware is configured."""
    from app.main import app

    # Check if CORSMiddleware is in middleware stack
    middleware_types = [type(m).__name__ for m in app.user_middleware]
    assert 'CORSMiddleware' in middleware_types


def test_cors_configuration():
    """Test CORS configuration with allowed origins."""
    from app.main import app
    from app.config import settings

    # Verify CORS is configured with frontend URL
    assert settings.frontend_url


def test_health_endpoint():
    """Test /health endpoint."""
    from app.main import app

    client = TestClient(app)
    response = client.get("/health")

    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "healthy"
    assert "version" in data


def test_root_endpoint():
    """Test root / endpoint."""
    from app.main import app

    client = TestClient(app)
    response = client.get("/")

    assert response.status_code == 200
    data = response.json()
    assert "message" in data
    assert "docs" in data


def test_docs_available():
    """Test that OpenAPI docs are available."""
    from app.main import app

    client = TestClient(app)

    # Swagger UI
    response = client.get("/docs")
    assert response.status_code == 200

    # ReDoc
    response = client.get("/redoc")
    assert response.status_code == 200

    # OpenAPI schema
    response = client.get("/openapi.json")
    assert response.status_code == 200


def test_cors_allows_credentials():
    """Test that CORS allows credentials (for cookies)."""
    from app.main import app

    client = TestClient(app)
    response = client.options(
        "/health",
        headers={
            "Origin": "http://localhost:3000",
            "Access-Control-Request-Method": "GET",
        },
    )

    # Should have Access-Control-Allow-Credentials header
    assert "access-control-allow-credentials" in response.headers


def test_cors_allows_methods():
    """Test that CORS allows required HTTP methods."""
    from app.main import app

    client = TestClient(app)
    response = client.options(
        "/health",
        headers={
            "Origin": "http://localhost:3000",
            "Access-Control-Request-Method": "POST",
        },
    )

    assert response.status_code == 200


def test_exception_handler_404():
    """Test 404 exception handler."""
    from app.main import app

    client = TestClient(app)
    response = client.get("/nonexistent-route")

    assert response.status_code == 404


def test_openapi_schema():
    """Test that OpenAPI schema is correctly generated."""
    from app.main import app

    client = TestClient(app)
    response = client.get("/openapi.json")

    assert response.status_code == 200
    schema = response.json()
    assert "openapi" in schema
    assert "info" in schema
    assert schema["info"]["title"]
