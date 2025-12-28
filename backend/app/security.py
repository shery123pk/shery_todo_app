"""
Security Utilities

Password hashing with bcrypt and JWT token management for authentication.
Author: Sharmeen Asif
"""

from jose import JWTError, jwt
import bcrypt
from datetime import datetime, timedelta, UTC
from typing import Optional
from uuid import UUID
from app.config import settings


# Password Hashing Functions

def hash_password(password: str) -> str:
    """
    Hash a password using bcrypt (cost factor 12).

    Args:
        password: Plain text password

    Returns:
        Bcrypt hashed password string

    Example:
        hashed = hash_password("securepass123")
        # Returns: "$2b$12$..."
    """
    # Convert password to bytes and hash with bcrypt
    password_bytes = password.encode('utf-8')
    salt = bcrypt.gensalt(rounds=12)
    hashed = bcrypt.hashpw(password_bytes, salt)
    # Return as string for database storage
    return hashed.decode('utf-8')


def verify_password(plain_password: str, hashed_password: str) -> bool:
    """
    Verify a password against a bcrypt hash.

    Args:
        plain_password: Plain text password to verify
        hashed_password: Bcrypt hash to verify against

    Returns:
        True if password matches, False otherwise

    Example:
        is_valid = verify_password("securepass123", "$2b$12$...")
        # Returns: True or False
    """
    # Convert both to bytes for bcrypt comparison
    password_bytes = plain_password.encode('utf-8')
    hashed_bytes = hashed_password.encode('utf-8')
    return bcrypt.checkpw(password_bytes, hashed_bytes)


# JWT Token Functions

def create_access_token(
    data: dict,
    remember_me: bool = False,
) -> str:
    """
    Create a JWT access token for authentication.

    Args:
        data: Data to encode in token (must include "sub" for user ID)
        remember_me: If True, use extended expiration (30 days vs 7 days)

    Returns:
        Encoded JWT token string

    Example:
        token = create_access_token(
            data={"sub": "550e8400-e29b-41d4-a716-446655440000"},
            remember_me=True
        )
        # Returns: "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9..."
    """
    # Copy data to avoid modifying original
    to_encode = data.copy()

    # Determine expiration time
    if remember_me:
        expires_delta = timedelta(minutes=settings.access_token_expire_minutes_remember)
    else:
        expires_delta = timedelta(minutes=settings.access_token_expire_minutes)

    expire = datetime.now(UTC) + expires_delta

    # Add standard claims
    to_encode.update({
        "exp": expire,  # Expiration time
        "iat": datetime.now(UTC),  # Issued at
        "type": "access"  # Token type
    })

    # Encode and return token
    encoded_jwt = jwt.encode(
        to_encode,
        settings.jwt_secret,
        algorithm=settings.jwt_algorithm,
    )

    return encoded_jwt


def decode_access_token(token: str) -> Optional[dict]:
    """
    Decode and verify a JWT access token.

    Args:
        token: JWT token string to decode

    Returns:
        Decoded token payload dict, or None if invalid/expired

    Example:
        payload = decode_access_token("eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...")
        # Returns: {"sub": "550e8400-...", "exp": 1234567890, ...}
        # Or: None (if invalid)
    """
    try:
        payload = jwt.decode(
            token,
            settings.jwt_secret,
            algorithms=[settings.jwt_algorithm],
        )
        return payload
    except JWTError:
        return None


def get_user_id_from_token(token: str) -> Optional[UUID]:
    """
    Extract user ID from a JWT token.

    Args:
        token: JWT token string

    Returns:
        User UUID if valid, None otherwise

    Example:
        user_id = get_user_id_from_token("eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...")
        # Returns: UUID("550e8400-e29b-41d4-a716-446655440000") or None
    """
    payload = decode_access_token(token)
    if not payload:
        return None

    user_id_str = payload.get("sub")
    if not user_id_str:
        return None

    try:
        return UUID(user_id_str)
    except ValueError:
        return None
