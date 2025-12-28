"""
User SQLModel Entity
Represents authenticated users in the system
Author: Sharmeen Asif
"""

from sqlmodel import SQLModel, Field
from typing import Optional
from pydantic import field_validator, EmailStr

from app.models.base import UUIDMixin, TimestampMixin


class User(UUIDMixin, TimestampMixin, SQLModel, table=True):
    """
    User entity for authentication and profile management.

    Attributes:
        id: UUID primary key (from UUIDMixin)
        email: Unique email address (indexed, normalized to lowercase)
        hashed_password: Bcrypt hashed password
        full_name: User's full name (required)
        email_verified: Whether email has been verified (default: False)
        avatar_url: Optional URL to user's avatar image
        timezone: Optional IANA timezone (e.g., "America/New_York")
        language: Optional language code (e.g., "en-US")
        created_at: Timestamp of account creation (from TimestampMixin)
        updated_at: Timestamp of last update (from TimestampMixin)
    """

    __tablename__ = "users"

    # Required fields
    email: str = Field(max_length=255, unique=True, index=True)
    hashed_password: str = Field(max_length=255)
    full_name: str = Field(max_length=255)

    # Boolean flags
    email_verified: bool = Field(default=False)

    # Optional fields
    avatar_url: Optional[str] = Field(default=None, max_length=500)
    timezone: Optional[str] = Field(default=None, max_length=50)
    language: Optional[str] = Field(default=None, max_length=10)

    @field_validator('email', mode='before')
    @classmethod
    def normalize_email(cls, v: str) -> str:
        """Normalize email to lowercase."""
        if isinstance(v, str):
            return v.lower().strip()
        return v

    class Config:
        json_schema_extra = {
            "example": {
                "id": "550e8400-e29b-41d4-a716-446655440000",
                "email": "user@example.com",
                "hashed_password": "$2b$12$...",
                "full_name": "John Doe",
                "email_verified": False,
                "avatar_url": "https://example.com/avatar.jpg",
                "timezone": "America/New_York",
                "language": "en-US",
                "created_at": "2025-12-27T10:00:00Z",
                "updated_at": "2025-12-27T10:00:00Z"
            }
        }
