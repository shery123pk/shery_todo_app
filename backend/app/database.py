"""
Database Configuration and Connection Management
Uses SQLModel with sync engine for Neon PostgreSQL
Author: Sharmeen Asif
"""

from sqlmodel import create_engine, Session, SQLModel
from app.config import settings
from typing import Generator


# Create sync engine with connection pooling
engine = create_engine(
    settings.database_url,
    echo=settings.debug,
    pool_pre_ping=True,  # Verify connections before use (important for Neon)
    pool_size=5,  # Max number of permanent connections
    max_overflow=10,  # Max number of overflow connections
    pool_recycle=3600,  # Recycle connections after 1 hour
)


def get_session() -> Generator[Session, None, None]:
    """
    Dependency for getting a database session.

    Yields:
        Session: SQLModel database session

    Example:
        @app.get("/items")
        def get_items(session: Session = Depends(get_session)):
            items = session.exec(select(Item)).all()
            return items
    """
    with Session(engine) as session:
        yield session


def create_db_and_tables() -> None:
    """
    Create all database tables.

    Note: In production, use Alembic migrations instead.
    This is useful for testing and development only.
    """
    SQLModel.metadata.create_all(engine)


def init_db() -> None:
    """
    Initialize database on application startup.

    Creates tables if they don't exist (development only).
    In production, this should be handled by Alembic migrations.
    """
    if settings.debug:
        create_db_and_tables()
