"""
Test backend project structure and dependencies.

This test verifies that all required modules and dependencies
are properly installed and can be imported.
"""

import pytest


def test_import_fastapi():
    """Test that FastAPI can be imported."""
    try:
        import fastapi
        assert fastapi.__version__
    except ImportError:
        pytest.fail("FastAPI not installed")


def test_import_sqlmodel():
    """Test that SQLModel can be imported."""
    try:
        import sqlmodel
        assert sqlmodel
    except ImportError:
        pytest.fail("SQLModel not installed")


def test_import_alembic():
    """Test that Alembic can be imported."""
    try:
        import alembic
        assert alembic.__version__
    except ImportError:
        pytest.fail("Alembic not installed")


def test_import_pydantic():
    """Test that Pydantic can be imported."""
    try:
        import pydantic
        assert pydantic.__version__
    except ImportError:
        pytest.fail("Pydantic not installed")


def test_import_passlib():
    """Test that passlib (for bcrypt) can be imported."""
    try:
        from passlib.hash import bcrypt
        assert bcrypt
    except ImportError:
        pytest.fail("passlib[bcrypt] not installed")


def test_import_jose():
    """Test that python-jose (for JWT) can be imported."""
    try:
        from jose import jwt
        assert jwt
    except ImportError:
        pytest.fail("python-jose not installed")


def test_import_aiofiles():
    """Test that aiofiles can be imported."""
    try:
        import aiofiles
        assert aiofiles
    except ImportError:
        pytest.fail("aiofiles not installed")


def test_import_aiosmtplib():
    """Test that aiosmtplib can be imported."""
    try:
        import aiosmtplib
        assert aiosmtplib
    except ImportError:
        pytest.fail("aiosmtplib not installed")


def test_import_asyncpg():
    """Test that asyncpg can be imported."""
    try:
        import asyncpg
        assert asyncpg.__version__
    except ImportError:
        pytest.fail("asyncpg not installed")


def test_app_directory_exists():
    """Test that app directory exists and has __init__.py."""
    import os
    from pathlib import Path

    backend_dir = Path(__file__).parent.parent
    app_dir = backend_dir / "app"

    assert app_dir.exists(), "app directory does not exist"
    assert (app_dir / "__init__.py").exists(), "app/__init__.py does not exist"


def test_alembic_directory_exists():
    """Test that alembic directory exists."""
    import os
    from pathlib import Path

    backend_dir = Path(__file__).parent.parent
    alembic_dir = backend_dir / "alembic"
    alembic_ini = backend_dir / "alembic.ini"

    assert alembic_dir.exists(), "alembic directory does not exist"
    assert alembic_ini.exists(), "alembic.ini does not exist"


def test_python_version():
    """Test that Python version is 3.13+."""
    import sys

    assert sys.version_info >= (3, 13), f"Python 3.13+ required, got {sys.version_info}"
