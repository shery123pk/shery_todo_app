"""
User SQLModel Entity
Represents authenticated users in the system
Author: Sharmeen Asif
"""

from sqlmodel import SQLModel, Field
from uuid import UUID, uuid4
from datetime import datetime
from typing import Optional


class User(SQLModel, table=True):
    """
    User entity for authentication and profile management.

    Attributes:
        id: UUID primary key
        email: Unique email address (indexed for fast lookup)
        email_verified: Whether email has been verified
        name: Optional display name
        hashed_password: Bcrypt hashed password
        created_at: Timestamp of account creation
        updated_at: Timestamp of last update
    """

    __tablename__ = "users"

    id: UUID = Field(default_factory=uuid4, primary_key=True)
    email: str = Field(max_length=255, unique=True, index=True, nullable=False)
    email_verified: bool = Field(default=False, nullable=False)
    name: Optional[str] = Field(default=None, max_length=255)
    hashed_password: str = Field(max_length=255, nullable=False)
    created_at: datetime = Field(default_factory=datetime.utcnow, nullable=False)
    updated_at: datetime = Field(
        default_factory=datetime.utcnow,
        nullable=False,
        sa_column_kwargs={"onupdate": datetime.utcnow}
    )

    class Config:
        json_schema_extra = {
            "example": {
                "id": "550e8400-e29b-41d4-a716-446655440000",
                "email": "user@example.com",
                "email_verified": False,
                "name": "John Doe",
                "created_at": "2025-12-26T10:00:00Z",
                "updated_at": "2025-12-26T10:00:00Z"
            }
        }
