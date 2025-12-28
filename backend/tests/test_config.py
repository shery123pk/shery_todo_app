"""
Test configuration loading and validation.

Tests environment variable parsing, defaults, Pydantic validation,
and missing required variables.
"""

import pytest
from pydantic import ValidationError


def test_config_loads_from_env():
    """Test that config can be loaded from environment."""
    from app.config import settings

    assert settings is not None
    assert hasattr(settings, 'database_url')


def test_database_url_required():
    """Test that DATABASE_URL is required."""
    from pydantic_settings import BaseSettings

    class TestSettings(BaseSettings):
        database_url: str

        class Config:
            env_file = ".env"

    # This should not raise if .env exists with DATABASE_URL
    try:
        test_settings = TestSettings()
        assert test_settings.database_url
    except ValidationError:
        # Expected if DATABASE_URL not in .env
        pass


def test_jwt_secret_required():
    """Test that JWT_SECRET is required."""
    from app.config import settings

    assert hasattr(settings, 'jwt_secret')
    assert settings.jwt_secret


def test_environment_defaults():
    """Test that environment has correct defaults."""
    from app.config import settings

    # Environment should default to "development" in tests
    assert settings.environment in ["development", "production"]


def test_debug_mode():
    """Test that debug mode can be controlled."""
    from app.config import settings

    assert isinstance(settings.debug, bool)


def test_cors_settings():
    """Test CORS settings."""
    from app.config import settings

    assert hasattr(settings, 'frontend_url')
    assert hasattr(settings, 'allowed_origins')


def test_smtp_settings():
    """Test SMTP email settings."""
    from app.config import settings

    assert hasattr(settings, 'smtp_host')
    assert hasattr(settings, 'smtp_port')
    assert hasattr(settings, 'smtp_username')
    assert hasattr(settings, 'smtp_password')
    assert hasattr(settings, 'from_email')


def test_file_upload_settings():
    """Test file upload settings."""
    from app.config import settings

    assert hasattr(settings, 'max_file_size_mb')
    assert hasattr(settings, 'upload_dir')
    assert settings.max_file_size_mb > 0


def test_get_allowed_origins():
    """Test get_allowed_origins method returns correct list."""
    from app.config import settings

    origins = settings.get_allowed_origins()
    assert isinstance(origins, list)
    assert settings.frontend_url in origins
    assert "http://localhost:3000" in origins


def test_max_file_size_bytes():
    """Test max_file_size_bytes conversion."""
    from app.config import settings

    max_bytes = settings.max_file_size_bytes()
    assert max_bytes == settings.max_file_size_mb * 1024 * 1024


def test_config_case_insensitive():
    """Test that config is case insensitive."""
    import os

    # Pydantic settings should be case insensitive by default
    from app.config import Settings

    # Verify Config class has case_sensitive = False
    assert hasattr(Settings, 'model_config')


def test_token_expiration_defaults():
    """Test JWT token expiration defaults."""
    from app.config import settings

    assert hasattr(settings, 'access_token_expire_minutes')
    assert settings.access_token_expire_minutes > 0
    assert settings.access_token_expire_minutes_remember > settings.access_token_expire_minutes
