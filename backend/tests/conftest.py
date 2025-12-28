"""
Pytest configuration and fixtures for backend tests.

Provides database session fixtures and test setup/teardown.
"""

import pytest
import pytest_asyncio


@pytest_asyncio.fixture(scope="function")
async def async_session():
    """
    Create an async database session for testing.

    Uses transactions that are rolled back after each test to ensure isolation.
    """
    from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession, async_sessionmaker
    from sqlmodel import SQLModel
    from app.config import settings

    # Create async engine
    engine = create_async_engine(
        settings.database_url,
        echo=False,
        pool_pre_ping=True,
    )

    # Create tables
    async with engine.begin() as conn:
        await conn.run_sync(SQLModel.metadata.create_all)

    # Create session factory
    async_session_maker = async_sessionmaker(
        engine,
        class_=AsyncSession,
        expire_on_commit=False,
    )

    # Create session
    async with async_session_maker() as session:
        # Begin nested transaction
        async with session.begin():
            yield session
            # Rollback after test
            await session.rollback()

    # Drop tables after all tests
    async with engine.begin() as conn:
        await conn.run_sync(SQLModel.metadata.drop_all)

    await engine.dispose()


@pytest.fixture(scope="function")
def cleanup_uploads(tmp_path):
    """
    Fixture to track and clean up uploaded files during tests.

    Returns a list that test can append file paths to for cleanup.
    """
    cleanup_list = []
    yield cleanup_list

    # Clean up files after test
    import os
    for file_path in cleanup_list:
        if os.path.exists(file_path):
            try:
                os.remove(file_path)
            except:
                pass
