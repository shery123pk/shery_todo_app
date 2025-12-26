"""
Authentication Pydantic Schemas
Request/Response models for auth endpoints
Author: Sharmeen Asif
"""

from pydantic import BaseModel, EmailStr, Field
from uuid import UUID
from datetime import datetime
from typing import Optional


class SignupRequest(BaseModel):
    """
    Request model for user signup.

    Attributes:
        email: Valid email address
        password: Plain text password (min 8 chars)
        name: Optional display name
    """

    email: EmailStr = Field(..., description="User's email address")
    password: str = Field(..., min_length=8, description="Password (min 8 characters)")
    name: Optional[str] = Field(None, max_length=255, description="Display name")

    class Config:
        json_schema_extra = {
            "example": {
                "email": "user@example.com",
                "password": "securepass123",
                "name": "John Doe"
            }
        }


class SigninRequest(BaseModel):
    """
    Request model for user signin.

    Attributes:
        email: User's email address
        password: Plain text password
        remember_me: Whether to extend session duration (30 days vs 7 days)
    """

    email: EmailStr = Field(..., description="User's email address")
    password: str = Field(..., description="Password")
    remember_me: bool = Field(default=False, description="Remember me for 30 days")

    class Config:
        json_schema_extra = {
            "example": {
                "email": "user@example.com",
                "password": "securepass123",
                "remember_me": False
            }
        }


class UserResponse(BaseModel):
    """
    Response model for user data (without sensitive fields).

    Attributes:
        id: User's UUID
        email: User's email address
        email_verified: Whether email has been verified
        name: Display name
        created_at: Account creation timestamp
    """

    id: UUID
    email: str
    email_verified: bool
    name: Optional[str]
    created_at: datetime

    class Config:
        from_attributes = True
        json_schema_extra = {
            "example": {
                "id": "550e8400-e29b-41d4-a716-446655440000",
                "email": "user@example.com",
                "email_verified": False,
                "name": "John Doe",
                "created_at": "2025-12-26T10:00:00Z"
            }
        }


class SigninResponse(BaseModel):
    """
    Response model for successful signin.

    Attributes:
        user: User data
        message: Success message
    """

    user: UserResponse
    message: str = "Signed in successfully"

    class Config:
        json_schema_extra = {
            "example": {
                "user": {
                    "id": "550e8400-e29b-41d4-a716-446655440000",
                    "email": "user@example.com",
                    "email_verified": False,
                    "name": "John Doe",
                    "created_at": "2025-12-26T10:00:00Z"
                },
                "message": "Signed in successfully"
            }
        }
