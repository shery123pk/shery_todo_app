"""
Database Configuration and Connection Management

Async database connection using SQLModel with asyncpg for Neon PostgreSQL.
Author: Sharmeen Asif
"""

from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession, async_sessionmaker
from sqlmodel import SQLModel
from app.config import settings
from typing import AsyncGenerator


# Create async engine with connection pooling
engine = create_async_engine(
    settings.database_url,
    echo=settings.debug,
    pool_pre_ping=True,  # Verify connections before use (important for Neon)
    pool_size=5,  # Max number of permanent connections
    max_overflow=10,  # Max number of overflow connections
    pool_recycle=3600,  # Recycle connections after 1 hour (Neon closes idle connections)
)

# Create async session factory
async_session_maker = async_sessionmaker(
    engine,
    class_=AsyncSession,
    expire_on_commit=False,
)


async def get_async_session() -> AsyncGenerator[AsyncSession, None]:
    """
    Dependency for getting an async database session.

    Yields:
        AsyncSession: SQLModel async database session

    Example:
        @app.get("/items")
        async def get_items(session: AsyncSession = Depends(get_async_session)):
            statement = select(Item)
            result = await session.execute(statement)
            items = result.scalars().all()
            return items
    """
    async with async_session_maker() as session:
        yield session


async def create_db_and_tables() -> None:
    """
    Create all database tables.

    Note: In production, use Alembic migrations instead.
    This is useful for testing and development only.
    """
    async with engine.begin() as conn:
        await conn.run_sync(SQLModel.metadata.create_all)


async def init_db() -> None:
    """
    Initialize database on application startup.

    Creates tables if they don't exist (development only).
    In production, this should be handled by Alembic migrations.
    """
    if settings.debug:
        await create_db_and_tables()
