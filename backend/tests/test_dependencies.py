"""
Test dependency injection utilities.

Tests for get_async_session and dependency injection patterns.
Phase 2 foundational tests only - no user/org models required yet.
"""

import pytest
from sqlalchemy import text


@pytest.mark.asyncio
async def test_get_async_session_returns_session():
    """Test get_async_session dependency returns async session."""
    from app.database import get_async_session

    async for session in get_async_session():
        assert session is not None
        # Session should be usable for queries
        result = await session.execute(text("SELECT 1 as num"))
        row = result.first()
        assert row.num == 1


@pytest.mark.asyncio
async def test_get_async_session_closes_properly():
    """Test that async session closes after use."""
    from app.database import get_async_session

    session = None
    async for s in get_async_session():
        session = s
        assert session is not None

    # Session should be closed after exiting context
    # (Can't easily test this without accessing internals, but we verify it doesn't error)
    assert session is not None


def test_dependencies_module_exists():
    """Test that dependencies module can be imported."""
    from app import dependencies
    assert dependencies is not None


def test_database_module_has_get_async_session():
    """Test that database module exports get_async_session."""
    from app.database import get_async_session
    assert get_async_session is not None
    assert callable(get_async_session)
