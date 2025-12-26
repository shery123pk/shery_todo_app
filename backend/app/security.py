"""
Security Utilities
Password hashing with bcrypt and JWT token management
Author: Sharmeen Asif
"""

from passlib.context import CryptContext
from jose import JWTError, jwt
from datetime import datetime, timedelta
from typing import Optional
from uuid import UUID
from app.config import settings


# Password hashing context
pwd_context = CryptContext(
    schemes=["bcrypt"],
    deprecated="auto",
    bcrypt__rounds=settings.bcrypt_rounds
)


# Password Hashing Functions

def hash_password(password: str) -> str:
    """
    Hash a password using bcrypt.

    Args:
        password: Plain text password

    Returns:
        Bcrypt hashed password string

    Example:
        hashed = hash_password("securepass123")
        # Returns: "$2b$12$..."
    """
    return pwd_context.hash(password)


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
    return pwd_context.verify(plain_password, hashed_password)


# JWT Token Functions

def create_access_token(
    user_id: UUID,
    remember_me: bool = False,
    additional_data: Optional[dict] = None
) -> str:
    """
    Create a JWT access token for authentication.

    Args:
        user_id: User's UUID to encode in token
        remember_me: If True, use extended expiration (30 days vs 7 days)
        additional_data: Optional additional claims to include in token

    Returns:
        Encoded JWT token string

    Example:
        token = create_access_token(
            user_id=UUID("550e8400-e29b-41d4-a716-446655440000"),
            remember_me=True
        )
        # Returns: "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9..."
    """
    # Determine expiration time
    if remember_me:
        expires_delta = timedelta(minutes=settings.access_token_expire_minutes_remember)
    else:
        expires_delta = timedelta(minutes=settings.access_token_expire_minutes)

    expire = datetime.utcnow() + expires_delta

    # Build token payload
    to_encode = {
        "sub": str(user_id),  # Subject (user ID)
        "exp": expire,  # Expiration time
        "iat": datetime.utcnow(),  # Issued at
        "type": "access"  # Token type
    }

    # Add additional claims if provided
    if additional_data:
        to_encode.update(additional_data)

    # Encode and return token
    encoded_jwt = jwt.encode(
        to_encode,
        settings.better_auth_secret,
        algorithm="HS256"
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
            settings.better_auth_secret,
            algorithms=["HS256"]
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
