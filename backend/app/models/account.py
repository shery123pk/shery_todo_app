"""
Account SQLModel Entity
Represents OAuth provider accounts linked to users
Author: Sharmeen Asif
"""

from sqlmodel import SQLModel, Field
from uuid import UUID, uuid4
from datetime import datetime
from typing import Optional


class Account(SQLModel, table=True):
    """
    Account entity for OAuth provider integration.

    Supports linking multiple OAuth accounts (Google, GitHub, etc.) to a single user.

    Attributes:
        id: UUID primary key
        user_id: Foreign key to users table (CASCADE delete)
        provider: OAuth provider name (google, github, etc.)
        provider_account_id: Unique ID from the OAuth provider
        access_token: OAuth access token (optional)
        refresh_token: OAuth refresh token (optional)
        expires_at: Token expiration timestamp (optional)
        created_at: Timestamp of account link
        updated_at: Timestamp of last update
    """

    __tablename__ = "accounts"

    id: UUID = Field(default_factory=uuid4, primary_key=True)
    user_id: UUID = Field(
        foreign_key="users.id",
        index=True,
        nullable=False,
        ondelete="CASCADE"
    )
    provider: str = Field(max_length=50, nullable=False, index=True)
    provider_account_id: str = Field(max_length=255, nullable=False)
    access_token: Optional[str] = Field(default=None, max_length=500)
    refresh_token: Optional[str] = Field(default=None, max_length=500)
    expires_at: Optional[datetime] = Field(default=None)
    created_at: datetime = Field(default_factory=datetime.utcnow, nullable=False)
    updated_at: datetime = Field(
        default_factory=datetime.utcnow,
        nullable=False,
        sa_column_kwargs={"onupdate": datetime.utcnow}
    )

    class Config:
        json_schema_extra = {
            "example": {
                "id": "abc01234-e89b-12d3-a456-426614174000",
                "user_id": "550e8400-e29b-41d4-a716-446655440000",
                "provider": "google",
                "provider_account_id": "1234567890",
                "expires_at": "2026-01-02T10:00:00Z",
                "created_at": "2025-12-26T10:00:00Z",
                "updated_at": "2025-12-26T10:00:00Z"
            }
        }
