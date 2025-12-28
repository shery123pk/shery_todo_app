"""
Test base SQLModel mixins.

Tests UUID generation, timestamp auto-update, and organization scoping mixin.
"""

import pytest
from datetime import datetime, UTC
from uuid import UUID
from sqlmodel import Field, SQLModel
import asyncio


@pytest.mark.asyncio
async def test_uuid_mixin():
    """Test UUID primary key mixin generates valid UUIDs."""
    from app.models.base import UUIDMixin

    class TestModel(UUIDMixin, SQLModel, table=True):
        __tablename__ = "test_uuid_model"  # type: ignore
        name: str

    # Create instance
    instance = TestModel(name="test")

    # UUID should be generated
    assert instance.id is not None
    assert isinstance(instance.id, UUID)


@pytest.mark.asyncio
async def test_timestamp_mixin():
    """Test timestamp mixin auto-generates created_at and updated_at."""
    from app.models.base import TimestampMixin

    class TestModel(TimestampMixin, SQLModel, table=True):
        __tablename__ = "test_timestamp_model"  # type: ignore
        id: int | None = Field(default=None, primary_key=True)
        name: str

    # Create instance
    instance = TestModel(name="test")

    # Timestamps should be set
    assert instance.created_at is not None
    assert instance.updated_at is not None
    assert isinstance(instance.created_at, datetime)
    assert isinstance(instance.updated_at, datetime)


@pytest.mark.asyncio
async def test_timestamp_auto_update():
    """Test that updated_at is automatically updated on modification."""
    from app.models.base import TimestampMixin
    from app.database import engine, async_session_maker
    from sqlalchemy import select

    class TestModel(TimestampMixin, SQLModel, table=True):
        __tablename__ = "test_timestamp_update"  # type: ignore
        id: int | None = Field(default=None, primary_key=True)
        name: str

    # Create table
    async with engine.begin() as conn:
        await conn.run_sync(SQLModel.metadata.create_all)

    try:
        # Create and save instance
        async with async_session_maker() as session:
            instance = TestModel(name="original")
            session.add(instance)
            await session.commit()
            await session.refresh(instance)

            original_updated_at = instance.updated_at
            instance_id = instance.id

        # Wait a bit
        await asyncio.sleep(0.1)

        # Update instance
        async with async_session_maker() as session:
            statement = select(TestModel).where(TestModel.id == instance_id)
            result = await session.execute(statement)
            instance = result.scalar_one()

            instance.name = "updated"
            session.add(instance)
            await session.commit()
            await session.refresh(instance)

            # updated_at should change
            assert instance.updated_at > original_updated_at

    finally:
        # Cleanup
        async with engine.begin() as conn:
            await conn.run_sync(SQLModel.metadata.drop_all)


@pytest.mark.asyncio
async def test_organization_scoping_mixin():
    """Test organization scoping mixin for multi-tenancy."""
    from app.models.base import OrganizationScopingMixin
    from uuid import uuid4

    class TestModel(OrganizationScopingMixin, SQLModel, table=True):
        __tablename__ = "test_org_scoping"  # type: ignore
        id: int | None = Field(default=None, primary_key=True)
        name: str

    org_id = uuid4()
    instance = TestModel(name="test", organization_id=org_id)

    assert instance.organization_id == org_id
    assert isinstance(instance.organization_id, UUID)


@pytest.mark.asyncio
async def test_combined_base_model():
    """Test model using all base mixins together."""
    from app.models.base import BaseModel

    class TestModel(BaseModel, table=True):
        __tablename__ = "test_combined_base"  # type: ignore
        name: str

    from uuid import uuid4
    org_id = uuid4()

    instance = TestModel(name="test", organization_id=org_id)

    # Should have UUID id
    assert instance.id is not None
    assert isinstance(instance.id, UUID)

    # Should have timestamps
    assert instance.created_at is not None
    assert instance.updated_at is not None

    # Should have organization_id
    assert instance.organization_id == org_id


def test_uuid_is_primary_key():
    """Test that UUID field is configured as primary key."""
    from app.models.base import UUIDMixin

    class TestModel(UUIDMixin, SQLModel, table=True):
        __tablename__ = "test_uuid_pk"  # type: ignore
        name: str

    # Check id field configuration
    id_field = TestModel.model_fields['id']
    assert id_field.default_factory is not None  # UUID generation function


def test_timestamps_timezone_aware():
    """Test that timestamps use UTC timezone."""
    from app.models.base import TimestampMixin

    class TestModel(TimestampMixin, SQLModel, table=True):
        __tablename__ = "test_tz_aware"  # type: ignore
        id: int | None = Field(default=None, primary_key=True)
        name: str

    instance = TestModel(name="test")

    # Timestamps should be timezone-aware (UTC)
    assert instance.created_at.tzinfo is not None
    assert instance.updated_at.tzinfo is not None
