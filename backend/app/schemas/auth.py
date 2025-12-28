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
        full_name: User's full name (required)
    """

    email: EmailStr = Field(..., description="User's email address")
    password: str = Field(..., min_length=8, description="Password (min 8 characters)")
    full_name: str = Field(..., min_length=2, max_length=255, description="Full name")

    class Config:
        json_schema_extra = {
            "example": {
                "email": "user@example.com",
                "password": "securepass123",
                "full_name": "John Doe"
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
        full_name: User's full name
        avatar_url: Profile picture URL
        timezone: User's timezone
        language: Preferred language code
        created_at: Account creation timestamp
        updated_at: Last update timestamp
    """

    id: UUID
    email: str
    email_verified: bool
    full_name: str
    avatar_url: Optional[str] = None
    timezone: Optional[str] = None
    language: Optional[str] = None
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True
        json_schema_extra = {
            "example": {
                "id": "550e8400-e29b-41d4-a716-446655440000",
                "email": "user@example.com",
                "email_verified": False,
                "full_name": "John Doe",
                "avatar_url": "https://example.com/avatar.jpg",
                "timezone": "UTC",
                "language": "en",
                "created_at": "2025-12-26T10:00:00Z",
                "updated_at": "2025-12-27T10:00:00Z"
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
                    "full_name": "John Doe",
                    "avatar_url": None,
                    "timezone": None,
                    "language": None,
                    "created_at": "2025-12-26T10:00:00Z",
                    "updated_at": "2025-12-26T10:00:00Z"
                },
                "message": "Signed in successfully"
            }
        }


class UpdateProfileRequest(BaseModel):
    """
    Request model for updating user profile.

    All fields are optional - only provided fields will be updated.

    Attributes:
        full_name: User's full name
        avatar_url: Profile picture URL
        timezone: User's timezone (e.g., "America/New_York", "UTC")
        language: Preferred language code (e.g., "en", "es")
    """

    full_name: Optional[str] = Field(None, min_length=2, max_length=255, description="Full name")
    avatar_url: Optional[str] = Field(None, max_length=500, description="Avatar URL")
    timezone: Optional[str] = Field(None, max_length=50, description="Timezone")
    language: Optional[str] = Field(None, max_length=10, description="Language code")

    class Config:
        json_schema_extra = {
            "example": {
                "full_name": "Jane Smith",
                "avatar_url": "https://example.com/avatar.jpg",
                "timezone": "America/New_York",
                "language": "en"
            }
        }


class ChangePasswordRequest(BaseModel):
    """
    Request model for changing user password.

    Requires current password for verification and new password.
    All existing sessions will be invalidated after password change.

    Attributes:
        current_password: Current password for verification
        new_password: New password (min 8 characters)
    """

    current_password: str = Field(..., description="Current password")
    new_password: str = Field(..., min_length=8, description="New password (min 8 characters)")

    class Config:
        json_schema_extra = {
            "example": {
                "current_password": "oldpassword123",
                "new_password": "newsecurepass456"
            }
        }


class VerifyEmailRequest(BaseModel):
    """
    Request model for email verification.

    Attributes:
        token: Email verification token from email link
    """

    token: str = Field(..., description="Email verification token")

    class Config:
        json_schema_extra = {
            "example": {
                "token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9..."
            }
        }


class ForgotPasswordRequest(BaseModel):
    """
    Request model for forgot password.

    Sends password reset email to user if email exists.
    Always returns success for security (no email enumeration).

    Attributes:
        email: User's email address
    """

    email: EmailStr = Field(..., description="Email address to send reset link")

    class Config:
        json_schema_extra = {
            "example": {
                "email": "user@example.com"
            }
        }


class ResetPasswordRequest(BaseModel):
    """
    Request model for password reset.

    Uses token from email to reset password.
    All existing sessions will be invalidated.

    Attributes:
        token: Password reset token from email
        new_password: New password (min 8 characters)
    """

    token: str = Field(..., description="Password reset token")
    new_password: str = Field(..., min_length=8, description="New password (min 8 characters)")

    class Config:
        json_schema_extra = {
            "example": {
                "token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
                "new_password": "newsecurepass123"
            }
        }
