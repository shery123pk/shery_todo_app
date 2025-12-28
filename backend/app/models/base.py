"""
Base SQLModel mixins for all database models.

Provides UUID primary keys, timestamps, and organization scoping for multi-tenancy.
Author: Sharmeen Asif
"""

from sqlmodel import SQLModel, Field
from datetime import datetime
from uuid import UUID, uuid4
from typing import Optional
from sqlalchemy import TIMESTAMP, text


class UUIDMixin(SQLModel):
    """Mixin for UUID primary key."""

    id: UUID = Field(
        default_factory=uuid4,
        primary_key=True,
        index=True,
        nullable=False,
    )


class TimestampMixin(SQLModel):
    """Mixin for automatic timestamp management with timezone support."""

    created_at: datetime = Field(
        nullable=False,
        sa_type=TIMESTAMP(timezone=True),
        sa_column_kwargs={"server_default": text("CURRENT_TIMESTAMP")},
    )
    updated_at: datetime = Field(
        nullable=False,
        sa_type=TIMESTAMP(timezone=True),
        sa_column_kwargs={
            "server_default": text("CURRENT_TIMESTAMP"),
            "onupdate": text("CURRENT_TIMESTAMP"),
        },
    )


class OrganizationScopingMixin(SQLModel):
    """
    Mixin for multi-tenant organization scoping.

    All models with this mixin belong to a specific organization.
    Used for row-level security and data isolation.
    """

    organization_id: UUID = Field(
        foreign_key="organizations.id",
        index=True,
        nullable=False,
    )


class BaseModel(UUIDMixin, TimestampMixin, OrganizationScopingMixin):
    """
    Base model combining all common mixins.

    Use this for models that need:
    - UUID primary key
    - Automatic timestamps (created_at, updated_at)
    - Organization scoping (multi-tenancy)

    Example:
        class Task(BaseModel, table=True):
            title: str
            description: str | None
            # id, created_at, updated_at, organization_id inherited
    """

    pass


class BaseModelNoOrg(UUIDMixin, TimestampMixin):
    """
    Base model without organization scoping.

    Use this for models that are not organization-specific:
    - User (belongs to multiple organizations)
    - Session (user-level, not org-level)
    - Invitation (pre-org membership)

    Example:
        class User(BaseModelNoOrg, table=True):
            email: str
            hashed_password: str
            # id, created_at, updated_at inherited
    """

    pass
