"""
Session SQLModel Entity
Represents user authentication sessions
Author: Sharmeen Asif
"""

from sqlmodel import SQLModel, Field
from uuid import UUID, uuid4
from datetime import datetime
from typing import Optional


class Session(SQLModel, table=True):
    """
    Session entity for managing user authentication tokens.

    Attributes:
        id: UUID primary key
        user_id: Foreign key to users table (CASCADE delete)
        token: Unique JWT token (indexed for fast lookup)
        expires_at: Token expiration timestamp
        ip_address: IP address where session was created
        user_agent: Browser user agent string
        created_at: Timestamp of session creation
    """

    __tablename__ = "sessions"

    id: UUID = Field(default_factory=uuid4, primary_key=True)
    user_id: UUID = Field(
        foreign_key="users.id",
        index=True,
        nullable=False,
        ondelete="CASCADE"
    )
    token: str = Field(max_length=500, unique=True, index=True, nullable=False)
    expires_at: datetime = Field(nullable=False, index=True)
    ip_address: Optional[str] = Field(default=None, max_length=45)  # IPv6 max length
    user_agent: Optional[str] = Field(default=None, max_length=500)
    created_at: datetime = Field(default_factory=datetime.utcnow, nullable=False)

    class Config:
        json_schema_extra = {
            "example": {
                "id": "789e0123-e89b-12d3-a456-426614174000",
                "user_id": "550e8400-e29b-41d4-a716-446655440000",
                "token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
                "expires_at": "2026-01-02T10:00:00Z",
                "ip_address": "192.168.1.1",
                "user_agent": "Mozilla/5.0...",
                "created_at": "2025-12-26T10:00:00Z"
            }
        }
