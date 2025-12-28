"""
Test database connection and session management.

Tests async engine creation, session management, connection pooling,
and Neon PostgreSQL connection.
"""

import pytest
from sqlmodel import SQLModel, Field
from sqlalchemy.ext.asyncio import AsyncSession
from typing import AsyncGenerator


@pytest.mark.asyncio
async def test_async_engine_creation():
    """Test that async engine can be created."""
    from app.database import engine

    assert engine is not None
    assert hasattr(engine, 'begin')
    assert hasattr(engine, 'connect')


@pytest.mark.asyncio
async def test_async_session_management():
    """Test that async sessions can be created and closed."""
    from app.database import async_session_maker

    async with async_session_maker() as session:
        assert isinstance(session, AsyncSession)
        assert session.is_active


@pytest.mark.asyncio
async def test_connection_pooling():
    """Test that connection pooling is configured."""
    from app.database import engine

    # Check pool configuration
    pool = engine.pool
    assert pool is not None
    assert pool.size() >= 0  # Pool exists and can report size


@pytest.mark.asyncio
async def test_get_async_session_dependency():
    """Test the async session dependency."""
    from app.database import get_async_session

    session_gen = get_async_session()
    assert session_gen is not None

    # Get session from generator
    session = await session_gen.__anext__()
    assert isinstance(session, AsyncSession)

    # Cleanup
    try:
        await session_gen.__anext__()
    except StopAsyncIteration:
        pass  # Expected


@pytest.mark.asyncio
async def test_database_url_format():
    """Test that DATABASE_URL uses asyncpg driver."""
    from app.config import settings

    assert settings.database_url.startswith('postgresql+asyncpg://'), \
        "DATABASE_URL must use asyncpg driver for async operations"


@pytest.mark.asyncio
async def test_simple_query():
    """Test a simple database query."""
    from app.database import async_session_maker
    from sqlalchemy import text

    async with async_session_maker() as session:
        result = await session.execute(text("SELECT 1 as num"))
        row = result.first()
        assert row is not None
        assert row.num == 1


class TestModel(SQLModel, table=True):
    """Test model for database operations."""
    __tablename__ = "test_models"  # type: ignore

    id: int | None = Field(default=None, primary_key=True)
    name: str


@pytest.mark.asyncio
async def test_model_operations():
    """Test basic CRUD operations with async session."""
    from app.database import engine, async_session_maker
    from sqlalchemy import select

    # Create table
    async with engine.begin() as conn:
        await conn.run_sync(SQLModel.metadata.create_all)

    # Create record
    async with async_session_maker() as session:
        test_item = TestModel(name="test")
        session.add(test_item)
        await session.commit()
        await session.refresh(test_item)
        assert test_item.id is not None

    # Read record
    async with async_session_maker() as session:
        statement = select(TestModel).where(TestModel.name == "test")
        result = await session.execute(statement)
        found_item = result.scalar_one_or_none()
        assert found_item is not None
        assert found_item.name == "test"

    # Cleanup
    async with engine.begin() as conn:
        await conn.run_sync(SQLModel.metadata.drop_all)
