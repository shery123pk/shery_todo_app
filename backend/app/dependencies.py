"""
FastAPI Dependencies
Dependency injection for authentication and database sessions
Author: Sharmeen Asif
"""

from fastapi import Depends, HTTPException, status, Cookie
from sqlmodel import Session, select
from typing import Optional
from uuid import UUID

from app.database import get_session
from app.models.user import User
from app.models.session import Session as DBSession
from app.security import get_user_id_from_token
from datetime import datetime


async def get_current_user(
    session_token: Optional[str] = Cookie(None),
    db: Session = Depends(get_session)
) -> User:
    """
    Get the currently authenticated user from session cookie.

    Args:
        session_token: JWT token from httpOnly cookie
        db: Database session

    Returns:
        User object if authenticated

    Raises:
        HTTPException: 401 if not authenticated or token invalid

    Example:
        @app.get("/api/auth/me")
        def get_me(current_user: User = Depends(get_current_user)):
            return current_user
    """
    # Check if token exists
    if not session_token:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Not authenticated",
            headers={"WWW-Authenticate": "Bearer"},
        )

    # Decode token and extract user ID
    user_id = get_user_id_from_token(session_token)
    if not user_id:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid authentication token",
            headers={"WWW-Authenticate": "Bearer"},
        )

    # Verify session exists in database and is not expired
    db_session = db.exec(
        select(DBSession)
        .where(DBSession.token == session_token)
        .where(DBSession.expires_at > datetime.utcnow())
    ).first()

    if not db_session:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Session expired or invalid",
            headers={"WWW-Authenticate": "Bearer"},
        )

    # Fetch user from database
    user = db.get(User, user_id)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="User not found",
            headers={"WWW-Authenticate": "Bearer"},
        )

    return user


async def get_current_user_optional(
    session_token: Optional[str] = Cookie(None),
    db: Session = Depends(get_session)
) -> Optional[User]:
    """
    Get the currently authenticated user, or None if not authenticated.

    Useful for endpoints that work differently for authenticated vs anonymous users.

    Args:
        session_token: JWT token from httpOnly cookie
        db: Database session

    Returns:
        User object if authenticated, None otherwise

    Example:
        @app.get("/api/public")
        def public_endpoint(user: Optional[User] = Depends(get_current_user_optional)):
            if user:
                return {"message": f"Hello {user.name}"}
            return {"message": "Hello anonymous"}
    """
    if not session_token:
        return None

    try:
        return await get_current_user(session_token, db)
    except HTTPException:
        return None
