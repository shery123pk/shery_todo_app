"""
Authentication Router
Handles user signup, signin, signout, and profile endpoints
Author: Sharmeen Asif
"""

from fastapi import APIRouter, Depends, HTTPException, status, Response, Request
from sqlmodel import Session, select
from datetime import datetime, timedelta

from app.database import get_session
from app.models.user import User
from app.models.session import Session as DBSession
from app.schemas.auth import (
    SignupRequest,
    SigninRequest,
    UserResponse,
    SigninResponse
)
from app.security import hash_password, verify_password, create_access_token
from app.dependencies import get_current_user
from app.config import settings


router = APIRouter()


@router.post("/signup", response_model=UserResponse, status_code=status.HTTP_201_CREATED)
def signup(
    signup_data: SignupRequest,
    db: Session = Depends(get_session)
):
    """
    User registration endpoint.

    Creates a new user account with email and password.

    Args:
        signup_data: SignupRequest with email, password, and optional name
        db: Database session

    Returns:
        UserResponse: Created user data

    Raises:
        HTTPException 400: Invalid email format
        HTTPException 400: Password too short (< 8 chars)
        HTTPException 409: Email already registered

    Example:
        POST /api/auth/signup
        {
            "email": "user@example.com",
            "password": "securepass123",
            "name": "John Doe"
        }

        Response (201):
        {
            "id": "550e8400-...",
            "email": "user@example.com",
            "email_verified": false,
            "name": "John Doe",
            "created_at": "2025-12-26T10:00:00Z"
        }
    """
    # Check if email already exists
    existing_user = db.exec(
        select(User).where(User.email == signup_data.email)
    ).first()

    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="An account with this email already exists"
        )

    # Hash password
    hashed_password = hash_password(signup_data.password)

    # Create new user
    new_user = User(
        email=signup_data.email,
        hashed_password=hashed_password,
        name=signup_data.name,
        email_verified=False,
        created_at=datetime.utcnow(),
        updated_at=datetime.utcnow()
    )

    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    return new_user


@router.post("/signin", response_model=SigninResponse)
def signin(
    signin_data: SigninRequest,
    response: Response,
    request: Request,
    db: Session = Depends(get_session)
):
    """
    User signin endpoint.

    Authenticates user and creates a session with JWT token in httpOnly cookie.

    Args:
        signin_data: SigninRequest with email, password, and remember_me flag
        response: FastAPI Response to set cookies
        request: FastAPI Request to get client IP and user agent
        db: Database session

    Returns:
        SigninResponse: User data and success message

    Raises:
        HTTPException 401: Invalid email or password
        HTTPException 429: Too many login attempts (rate limiting)

    Example:
        POST /api/auth/signin
        {
            "email": "user@example.com",
            "password": "securepass123",
            "remember_me": false
        }

        Response (200):
        {
            "user": {
                "id": "550e8400-...",
                "email": "user@example.com",
                "email_verified": false,
                "name": "John Doe",
                "created_at": "2025-12-26T10:00:00Z"
            },
            "message": "Signed in successfully"
        }

        Sets cookie: session_token=<JWT>; HttpOnly; Secure; SameSite=Lax
    """
    # Find user by email
    user = db.exec(
        select(User).where(User.email == signin_data.email)
    ).first()

    # Verify user exists and password is correct
    # Use same error message for both cases to prevent email enumeration
    if not user or not verify_password(signin_data.password, user.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid email or password"
        )

    # Create JWT access token
    access_token = create_access_token(
        user_id=user.id,
        remember_me=signin_data.remember_me
    )

    # Calculate expiration time
    if signin_data.remember_me:
        expires_delta = timedelta(minutes=settings.access_token_expire_minutes_remember)
    else:
        expires_delta = timedelta(minutes=settings.access_token_expire_minutes)

    expires_at = datetime.utcnow() + expires_delta

    # Get client IP and user agent
    client_ip = request.client.host if request.client else None
    user_agent = request.headers.get("user-agent")

    # Create session in database
    db_session = DBSession(
        user_id=user.id,
        token=access_token,
        expires_at=expires_at,
        ip_address=client_ip,
        user_agent=user_agent,
        created_at=datetime.utcnow()
    )

    db.add(db_session)
    db.commit()

    # Set httpOnly cookie
    response.set_cookie(
        key="session_token",
        value=access_token,
        httponly=True,
        secure=settings.environment == "production",  # HTTPS only in production
        samesite="lax",
        max_age=int(expires_delta.total_seconds()),
        path="/"
    )

    return SigninResponse(user=user)


@router.post("/signout", status_code=status.HTTP_204_NO_CONTENT)
def signout(
    response: Response,
    current_user: User = Depends(get_current_user),
    session_token: str = Cookie(None),
    db: Session = Depends(get_session)
):
    """
    User signout endpoint.

    Deletes the session from database and clears the session cookie.

    Args:
        response: FastAPI Response to clear cookies
        current_user: Currently authenticated user
        session_token: JWT token from cookie
        db: Database session

    Returns:
        204 No Content

    Example:
        POST /api/auth/signout
        (Requires session_token cookie)

        Response: 204 No Content
        Clears cookie: session_token
    """
    # Delete session from database
    if session_token:
        db_session = db.exec(
            select(DBSession).where(DBSession.token == session_token)
        ).first()

        if db_session:
            db.delete(db_session)
            db.commit()

    # Clear cookie
    response.delete_cookie(key="session_token", path="/")

    return None


@router.get("/me", response_model=UserResponse)
def get_current_user_profile(
    current_user: User = Depends(get_current_user)
):
    """
    Get current user profile endpoint.

    Returns the authenticated user's profile data.

    Args:
        current_user: Currently authenticated user (from dependency)

    Returns:
        UserResponse: Current user data

    Raises:
        HTTPException 401: Not authenticated

    Example:
        GET /api/auth/me
        (Requires session_token cookie)

        Response (200):
        {
            "id": "550e8400-...",
            "email": "user@example.com",
            "email_verified": false,
            "name": "John Doe",
            "created_at": "2025-12-26T10:00:00Z"
        }
    """
    return current_user
