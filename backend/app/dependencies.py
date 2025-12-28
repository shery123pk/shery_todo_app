"""
FastAPI Dependencies (Async)

Dependency injection for authentication and database sessions using async/await.
Author: Sharmeen Asif
"""

from fastapi import Depends, HTTPException, status, Request
from sqlalchemy.ext.asyncio import AsyncSession
from sqlmodel import select
from typing import Optional, AsyncGenerator
from uuid import UUID

from app.database import get_async_session
from app.models.user import User
from app.security import decode_access_token
from datetime import datetime, UTC


async def get_current_user(
    request: Request,
    session: AsyncSession = Depends(get_async_session),
) -> User:
    """
    Get the currently authenticated user from JWT token in cookie.

    Args:
        request: FastAPI request object (to access cookies)
        session: Async database session

    Returns:
        User object if authenticated

    Raises:
        HTTPException: 401 if not authenticated or token invalid

    Example:
        @app.get("/api/auth/me")
        async def get_me(current_user: User = Depends(get_current_user)):
            return current_user
    """
    # Extract token from cookie
    token = request.cookies.get("access_token")
    if not token:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Not authenticated - no token provided",
            headers={"WWW-Authenticate": "Bearer"},
        )

    # Verify and decode token
    payload = decode_access_token(token)
    if not payload:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid or expired authentication token",
            headers={"WWW-Authenticate": "Bearer"},
        )

    user_id_str: str = payload.get("sub")
    if not user_id_str:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid token - missing subject",
            headers={"WWW-Authenticate": "Bearer"},
        )

    try:
        user_id = UUID(user_id_str)
    except ValueError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid user ID format in token",
            headers={"WWW-Authenticate": "Bearer"},
        )

    # Fetch user from database
    statement = select(User).where(User.id == user_id)
    result = await session.execute(statement)
    user = result.scalar_one_or_none()

    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="User not found",
            headers={"WWW-Authenticate": "Bearer"},
        )

    return user


async def get_current_user_optional(
    request: Request,
    session: AsyncSession = Depends(get_async_session),
) -> Optional[User]:
    """
    Get the currently authenticated user, or None if not authenticated.

    Useful for endpoints that work differently for authenticated vs anonymous users.

    Args:
        request: FastAPI request object
        session: Async database session

    Returns:
        User object if authenticated, None otherwise

    Example:
        @app.get("/api/public")
        async def public_endpoint(
            user: Optional[User] = Depends(get_current_user_optional)
        ):
            if user:
                return {"message": f"Hello {user.name}"}
            return {"message": "Hello anonymous"}
    """
    try:
        return await get_current_user(request, session)
    except HTTPException:
        return None
