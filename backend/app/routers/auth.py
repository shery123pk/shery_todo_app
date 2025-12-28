"""
Authentication Router

Handles user authentication endpoints: signup, signin, signout,
email verification, password reset, and profile management.

Author: Sharmeen Asif
"""

from fastapi import APIRouter, Depends, HTTPException, status, Response, Request
from sqlalchemy.ext.asyncio import AsyncSession

from app.database import get_async_session
from app.services.auth_service import AuthService
from app.dependencies import get_current_user
from app.models.user import User
from app.config import settings
from app.schemas.auth import (
    SignupRequest,
    SigninRequest,
    UserResponse,
    SigninResponse,
    UpdateProfileRequest,
    ChangePasswordRequest,
    VerifyEmailRequest,
    ForgotPasswordRequest,
    ResetPasswordRequest,
)
from app.utils.errors import ValidationError, NotFoundError, UnauthorizedError, ConflictError


router = APIRouter(tags=["Authentication"])


@router.post("/signup", response_model=UserResponse, status_code=status.HTTP_201_CREATED)
async def signup(
    signup_data: SignupRequest,
    db: AsyncSession = Depends(get_async_session),
):
    """
    Create a new user account.

    Validates email uniqueness, password strength, and creates user.
    Returns user data (excluding password).

    Args:
        signup_data: Email, password, and full name

    Returns:
        UserResponse: Created user data

    Raises:
        400: Invalid email format or weak password
        409: Email already registered
    """
    auth_service = AuthService(db)

    try:
        user = await auth_service.signup(
            email=signup_data.email,
            password=signup_data.password,
            full_name=signup_data.full_name,
        )

        # TODO: Send verification email
        # await send_verification_email(user.email, verification_token)

        return user

    except ValidationError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e),
        )
    except ConflictError as e:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail=str(e),
        )


@router.post("/signin", response_model=SigninResponse)
async def signin(
    signin_data: SigninRequest,
    response: Response,
    request: Request,
    db: AsyncSession = Depends(get_async_session),
):
    """
    Sign in a user and create a session.

    Verifies credentials, creates session, and sets HttpOnly cookie.

    Args:
        signin_data: Email, password, and remember_me flag
        response: FastAPI Response object to set cookies
        request: FastAPI Request object to get client info

    Returns:
        SigninResponse: User data and success message

    Raises:
        401: Invalid credentials
    """
    auth_service = AuthService(db)

    try:
        # Get client info
        ip_address = request.client.host if request.client else None
        user_agent = request.headers.get("user-agent")

        user, session, access_token, refresh_token = await auth_service.signin(
            email=signin_data.email,
            password=signin_data.password,
            remember_me=signin_data.remember_me,
            ip_address=ip_address,
            user_agent=user_agent,
        )

        # Set access token in HttpOnly cookie
        max_age = 30 * 24 * 60 * 60 if signin_data.remember_me else 7 * 24 * 60 * 60  # 30 days or 7 days
        response.set_cookie(
            key="access_token",
            value=access_token,
            httponly=True,
            secure=True,  # HTTPS only
            samesite="lax",
            max_age=max_age,
        )

        # Set refresh token in separate HttpOnly cookie
        response.set_cookie(
            key="refresh_token",
            value=refresh_token,
            httponly=True,
            secure=True,
            samesite="lax",
            max_age=30 * 24 * 60 * 60,  # 30 days
        )

        return SigninResponse(
            user=user,
            message="Sign in successful",
        )

    except UnauthorizedError as e:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=str(e),
        )


@router.post("/signout", status_code=status.HTTP_200_OK)
async def signout(
    response: Response,
    request: Request,
    db: AsyncSession = Depends(get_async_session),
):
    """
    Sign out the current user.

    Invalidates the session and clears cookies.

    Args:
        response: FastAPI Response object to clear cookies
        request: FastAPI Request object to get token

    Returns:
        Success message
    """
    auth_service = AuthService(db)

    # Get token from cookie
    token = request.cookies.get("access_token")

    if token:
        await auth_service.signout(token)

    # Clear cookies
    response.delete_cookie(key="access_token")
    response.delete_cookie(key="refresh_token")

    return {"message": "Sign out successful"}


@router.get("/me", response_model=UserResponse)
async def get_current_user_profile(
    current_user: User = Depends(get_current_user),
):
    """
    Get the current authenticated user's profile.

    Requires valid session token in cookie.

    Returns:
        UserResponse: Current user data

    Raises:
        401: Not authenticated
    """
    return current_user


@router.put("/profile", response_model=UserResponse)
async def update_profile(
    profile_data: UpdateProfileRequest,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_async_session),
):
    """
    Update the current user's profile.

    Allows updating full_name, avatar_url, timezone, and language.

    Args:
        profile_data: Profile fields to update
        current_user: Current authenticated user

    Returns:
        UserResponse: Updated user data

    Raises:
        400: Invalid input data
        401: Not authenticated
    """
    auth_service = AuthService(db)

    try:
        user = await auth_service.update_profile(
            user_id=current_user.id,
            full_name=profile_data.full_name,
            avatar_url=profile_data.avatar_url,
            timezone=profile_data.timezone,
            language=profile_data.language,
        )

        return user

    except ValidationError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e),
        )
    except NotFoundError as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(e),
        )


@router.put("/password", status_code=status.HTTP_200_OK)
async def change_password(
    password_data: ChangePasswordRequest,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_async_session),
    response: Response = None,
):
    """
    Change the current user's password.

    Verifies current password, updates to new password,
    and invalidates all existing sessions (forces re-login).

    Args:
        password_data: Current and new password
        current_user: Current authenticated user

    Returns:
        Success message

    Raises:
        400: Weak new password
        401: Current password incorrect or not authenticated
    """
    auth_service = AuthService(db)

    try:
        await auth_service.change_password(
            user_id=current_user.id,
            current_password=password_data.current_password,
            new_password=password_data.new_password,
        )

        # Clear cookies (force re-login)
        if response:
            response.delete_cookie(key="access_token")
            response.delete_cookie(key="refresh_token")

        return {"message": "Password changed successfully. Please sign in again."}

    except ValidationError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e),
        )
    except UnauthorizedError as e:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=str(e),
        )
    except NotFoundError as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(e),
        )


@router.post("/refresh", status_code=status.HTTP_200_OK)
async def refresh_token(
    request: Request,
    response: Response,
    db: AsyncSession = Depends(get_async_session),
):
    """
    Refresh access token using refresh token.

    Gets new access and refresh tokens using the refresh token from cookie.

    Args:
        request: FastAPI Request to get refresh token cookie
        response: FastAPI Response to set new cookies

    Returns:
        Success message

    Raises:
        401: Invalid or expired refresh token
    """
    auth_service = AuthService(db)

    # Get refresh token from cookie
    refresh_token = request.cookies.get("refresh_token")

    if not refresh_token:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="No refresh token provided",
        )

    try:
        new_access_token, new_refresh_token = await auth_service.refresh_access_token(
            refresh_token=refresh_token,
        )

        # Set new tokens in cookies
        response.set_cookie(
            key="access_token",
            value=new_access_token,
            httponly=True,
            secure=True,
            samesite="lax",
            max_age=30 * 24 * 60 * 60,
        )

        response.set_cookie(
            key="refresh_token",
            value=new_refresh_token,
            httponly=True,
            secure=True,
            samesite="lax",
            max_age=30 * 24 * 60 * 60,
        )

        return {"message": "Token refreshed successfully"}

    except UnauthorizedError as e:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=str(e),
        )


@router.post("/verify-email", response_model=UserResponse)
async def verify_email(
    verify_data: VerifyEmailRequest,
    db: AsyncSession = Depends(get_async_session),
):
    """
    Verify user's email address using verification token.

    Marks the user's email as verified in the database.

    Args:
        verify_data: Contains verification token from email link

    Returns:
        UserResponse: User data with email_verified=True

    Raises:
        401: Invalid or expired verification token
        404: User not found
    """
    auth_service = AuthService(db)

    try:
        user = await auth_service.verify_email_with_token(verify_data.token)
        return user

    except UnauthorizedError as e:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=str(e),
        )
    except NotFoundError as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(e),
        )


@router.post("/forgot-password", status_code=status.HTTP_200_OK)
async def forgot_password(
    forgot_data: ForgotPasswordRequest,
    db: AsyncSession = Depends(get_async_session),
):
    """
    Request password reset email.

    Sends password reset link to user's email if account exists.
    Always returns success for security (prevents email enumeration).

    Args:
        forgot_data: Contains email address

    Returns:
        Success message (always, even if email doesn't exist)

    Note:
        For development, returns the reset token in response.
        In production, this would only send email and return generic success.
    """
    auth_service = AuthService(db)

    # Generate reset token (returns None if email doesn't exist)
    reset_token = await auth_service.forgot_password(forgot_data.email)

    # For security, always return success message
    # In development, also return token for testing
    response_data = {
        "message": "If an account exists with this email, a password reset link has been sent."
    }

    # Only include token in development mode
    if reset_token and settings.environment == "development":
        response_data["reset_token"] = reset_token  # For testing only

    return response_data


@router.post("/reset-password", status_code=status.HTTP_200_OK)
async def reset_password(
    reset_data: ResetPasswordRequest,
    db: AsyncSession = Depends(get_async_session),
):
    """
    Reset user password using reset token.

    Uses token from email to set new password.
    Invalidates all existing sessions (forces re-login).

    Args:
        reset_data: Contains reset token and new password

    Returns:
        Success message

    Raises:
        400: Weak new password
        401: Invalid or expired reset token
        404: User not found
    """
    auth_service = AuthService(db)

    try:
        await auth_service.reset_password(
            token=reset_data.token,
            new_password=reset_data.new_password,
        )

        return {"message": "Password reset successfully. Please sign in with your new password."}

    except ValidationError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e),
        )
    except UnauthorizedError as e:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=str(e),
        )
    except NotFoundError as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(e),
        )
