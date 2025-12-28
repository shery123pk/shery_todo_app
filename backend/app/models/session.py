"""
Session SQLModel Entity
Represents user authentication sessions
Author: Sharmeen Asif
"""

from sqlmodel import SQLModel, Field, Column
from sqlalchemy import TIMESTAMP, ForeignKey as SAForeignKey, text
from uuid import UUID
from datetime import datetime
from typing import Optional

from app.models.base import UUIDMixin


class Session(UUIDMixin, SQLModel, table=True):
    """
    Session entity for managing user authentication tokens.

    Attributes:
        id: UUID primary key (from UUIDMixin)
        user_id: Foreign key to users table (CASCADE delete on user deletion)
        token: Unique access token (JWT or session token)
        refresh_token: Unique refresh token for renewing access tokens
        expires_at: Token expiration timestamp (timezone-aware)
        ip_address: Optional IP address where session was created
        user_agent: Optional browser user agent string
        created_at: Timestamp of session creation (timezone-aware)
    """

    __tablename__ = "sessions"

    # Foreign key to User (CASCADE delete)
    user_id: UUID = Field(
        sa_column=Column(
            SAForeignKey("users.id", ondelete="CASCADE"),
            index=True
        )
    )

    # Tokens (both must be unique)
    token: str = Field(max_length=500, unique=True, index=True)
    refresh_token: str = Field(max_length=500, unique=True, index=True)

    # Expiration
    expires_at: datetime = Field(
        sa_type=TIMESTAMP(timezone=True),
        index=True
    )

    # Optional tracking fields
    ip_address: Optional[str] = Field(default=None, max_length=45)  # IPv6 max length
    user_agent: Optional[str] = Field(default=None, max_length=500)

    # Timestamp (sessions don't update, only created)
    created_at: datetime = Field(
        nullable=False,
        sa_type=TIMESTAMP(timezone=True),
        sa_column_kwargs={"server_default": text("CURRENT_TIMESTAMP")},
    )

    class Config:
        json_schema_extra = {
            "example": {
                "id": "789e0123-e89b-12d3-a456-426614174000",
                "user_id": "550e8400-e29b-41d4-a716-446655440000",
                "token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
                "refresh_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
                "expires_at": "2026-01-02T10:00:00Z",
                "ip_address": "192.168.1.1",
                "user_agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)...",
                "created_at": "2025-12-27T10:00:00Z"
            }
        }
