"""
Tests for Authentication Service

Tests signup, signin, signout, profile management, and password operations.
Author: Sharmeen Asif
"""

import pytest
from sqlalchemy.ext.asyncio import AsyncSession
from app.services.auth_service import AuthService
from app.models.user import User
from app.models.session import Session
from app.security import verify_password
from app.utils.errors import ValidationError, NotFoundError, UnauthorizedError, ConflictError


@pytest.mark.asyncio
async def test_signup_success(async_session: AsyncSession):
    """Test successful user signup."""
    auth_service = AuthService(async_session)

    user = await auth_service.signup(
        email="test@example.com",
        password="password123",
        full_name="Test User",
    )

    assert user.id is not None
    assert user.email == "test@example.com"
    assert user.full_name == "Test User"
    assert user.email_verified is False
    assert verify_password("password123", user.hashed_password)


@pytest.mark.asyncio
async def test_signup_duplicate_email(async_session: AsyncSession):
    """Test signup with duplicate email fails."""
    auth_service = AuthService(async_session)

    # Create first user
    await auth_service.signup(
        email="test@example.com",
        password="password123",
        full_name="Test User",
    )

    # Try to create second user with same email
    with pytest.raises(ConflictError, match="Email already registered"):
        await auth_service.signup(
            email="test@example.com",
            password="different123",
            full_name="Another User",
        )


@pytest.mark.asyncio
async def test_signup_invalid_email(async_session: AsyncSession):
    """Test signup with invalid email format fails."""
    auth_service = AuthService(async_session)

    with pytest.raises(ValidationError, match="Invalid email format"):
        await auth_service.signup(
            email="notanemail",
            password="password123",
            full_name="Test User",
        )


@pytest.mark.asyncio
async def test_signup_weak_password(async_session: AsyncSession):
    """Test signup with weak password fails."""
    auth_service = AuthService(async_session)

    with pytest.raises(ValidationError, match="Password must be at least 8 characters"):
        await auth_service.signup(
            email="test@example.com",
            password="short",
            full_name="Test User",
        )


@pytest.mark.asyncio
async def test_signup_short_full_name(async_session: AsyncSession):
    """Test signup with short full name fails."""
    auth_service = AuthService(async_session)

    with pytest.raises(ValidationError, match="Full name must be at least 2 characters"):
        await auth_service.signup(
            email="test@example.com",
            password="password123",
            full_name="A",
        )


@pytest.mark.asyncio
async def test_signin_success(async_session: AsyncSession):
    """Test successful user signin."""
    auth_service = AuthService(async_session)

    # Create user
    await auth_service.signup(
        email="test@example.com",
        password="password123",
        full_name="Test User",
    )

    # Sign in
    user, session, access_token, refresh_token = await auth_service.signin(
        email="test@example.com",
        password="password123",
        remember_me=False,
    )

    assert user.email == "test@example.com"
    assert session.user_id == user.id
    assert access_token is not None
    assert refresh_token is not None
    assert session.token == access_token
    assert session.refresh_token == refresh_token


@pytest.mark.asyncio
async def test_signin_wrong_password(async_session: AsyncSession):
    """Test signin with wrong password fails."""
    auth_service = AuthService(async_session)

    # Create user
    await auth_service.signup(
        email="test@example.com",
        password="password123",
        full_name="Test User",
    )

    # Try to sign in with wrong password
    with pytest.raises(UnauthorizedError, match="Invalid email or password"):
        await auth_service.signin(
            email="test@example.com",
            password="wrongpassword",
        )


@pytest.mark.asyncio
async def test_signin_nonexistent_user(async_session: AsyncSession):
    """Test signin with nonexistent user fails."""
    auth_service = AuthService(async_session)

    with pytest.raises(UnauthorizedError, match="Invalid email or password"):
        await auth_service.signin(
            email="nonexistent@example.com",
            password="password123",
        )


@pytest.mark.asyncio
async def test_signin_remember_me(async_session: AsyncSession):
    """Test signin with remember_me flag."""
    auth_service = AuthService(async_session)

    # Create user
    await auth_service.signup(
        email="test@example.com",
        password="password123",
        full_name="Test User",
    )

    # Sign in with remember_me
    user, session, access_token, refresh_token = await auth_service.signin(
        email="test@example.com",
        password="password123",
        remember_me=True,
    )

    # Session should exist and have longer expiration
    assert session.expires_at is not None


@pytest.mark.asyncio
async def test_signout_success(async_session: AsyncSession):
    """Test successful signout."""
    auth_service = AuthService(async_session)

    # Create user and sign in
    await auth_service.signup(
        email="test@example.com",
        password="password123",
        full_name="Test User",
    )
    user, session, access_token, refresh_token = await auth_service.signin(
        email="test@example.com",
        password="password123",
    )

    # Sign out
    result = await auth_service.signout(access_token)

    assert result is True


@pytest.mark.asyncio
async def test_signout_invalid_token(async_session: AsyncSession):
    """Test signout with invalid token."""
    auth_service = AuthService(async_session)

    result = await auth_service.signout("invalid_token")

    assert result is False


@pytest.mark.asyncio
async def test_update_profile_success(async_session: AsyncSession):
    """Test successful profile update."""
    auth_service = AuthService(async_session)

    # Create user
    user = await auth_service.signup(
        email="test@example.com",
        password="password123",
        full_name="Test User",
    )

    # Update profile
    updated_user = await auth_service.update_profile(
        user_id=user.id,
        full_name="Updated Name",
        avatar_url="https://example.com/avatar.jpg",
        timezone="America/New_York",
        language="en",
    )

    assert updated_user.full_name == "Updated Name"
    assert updated_user.avatar_url == "https://example.com/avatar.jpg"
    assert updated_user.timezone == "America/New_York"
    assert updated_user.language == "en"


@pytest.mark.asyncio
async def test_update_profile_partial(async_session: AsyncSession):
    """Test partial profile update (only some fields)."""
    auth_service = AuthService(async_session)

    # Create user
    user = await auth_service.signup(
        email="test@example.com",
        password="password123",
        full_name="Test User",
    )

    # Update only full_name
    updated_user = await auth_service.update_profile(
        user_id=user.id,
        full_name="New Name",
    )

    assert updated_user.full_name == "New Name"
    assert updated_user.avatar_url is None
    assert updated_user.timezone is None
    assert updated_user.language is None


@pytest.mark.asyncio
async def test_update_profile_invalid_full_name(async_session: AsyncSession):
    """Test profile update with invalid full name fails."""
    auth_service = AuthService(async_session)

    # Create user
    user = await auth_service.signup(
        email="test@example.com",
        password="password123",
        full_name="Test User",
    )

    # Try to update with short full name
    with pytest.raises(ValidationError, match="Full name must be at least 2 characters"):
        await auth_service.update_profile(
            user_id=user.id,
            full_name="A",
        )


@pytest.mark.asyncio
async def test_change_password_success(async_session: AsyncSession):
    """Test successful password change."""
    auth_service = AuthService(async_session)

    # Create user and sign in
    user = await auth_service.signup(
        email="test@example.com",
        password="oldpassword123",
        full_name="Test User",
    )
    user1, session1, _, _ = await auth_service.signin(
        email="test@example.com",
        password="oldpassword123",
    )

    # Change password
    updated_user = await auth_service.change_password(
        user_id=user.id,
        current_password="oldpassword123",
        new_password="newpassword456",
    )

    # Verify new password works
    assert verify_password("newpassword456", updated_user.hashed_password)

    # Verify old session is invalidated
    result = await auth_service.signout(session1.token)
    assert result is False  # Session should be deleted


@pytest.mark.asyncio
async def test_change_password_wrong_current_password(async_session: AsyncSession):
    """Test password change with wrong current password fails."""
    auth_service = AuthService(async_session)

    # Create user
    user = await auth_service.signup(
        email="test@example.com",
        password="password123",
        full_name="Test User",
    )

    # Try to change password with wrong current password
    with pytest.raises(UnauthorizedError, match="Current password is incorrect"):
        await auth_service.change_password(
            user_id=user.id,
            current_password="wrongpassword",
            new_password="newpassword456",
        )


@pytest.mark.asyncio
async def test_change_password_weak_new_password(async_session: AsyncSession):
    """Test password change with weak new password fails."""
    auth_service = AuthService(async_session)

    # Create user
    user = await auth_service.signup(
        email="test@example.com",
        password="password123",
        full_name="Test User",
    )

    # Try to change to weak password
    with pytest.raises(ValidationError, match="Password must be at least 8 characters"):
        await auth_service.change_password(
            user_id=user.id,
            current_password="password123",
            new_password="short",
        )


@pytest.mark.asyncio
async def test_refresh_access_token_success(async_session: AsyncSession):
    """Test successful token refresh."""
    auth_service = AuthService(async_session)

    # Create user and sign in
    await auth_service.signup(
        email="test@example.com",
        password="password123",
        full_name="Test User",
    )
    user, session, access_token, refresh_token = await auth_service.signin(
        email="test@example.com",
        password="password123",
    )

    # Refresh token
    new_access_token, new_refresh_token = await auth_service.refresh_access_token(
        refresh_token=refresh_token,
    )

    assert new_access_token is not None
    assert new_refresh_token is not None
    assert new_access_token != access_token  # Should be different
    assert new_refresh_token != refresh_token  # Should be different


@pytest.mark.asyncio
async def test_refresh_access_token_invalid_token(async_session: AsyncSession):
    """Test token refresh with invalid refresh token fails."""
    auth_service = AuthService(async_session)

    with pytest.raises(UnauthorizedError):
        await auth_service.refresh_access_token(
            refresh_token="invalid_token",
        )


@pytest.mark.asyncio
async def test_get_user_by_email(async_session: AsyncSession):
    """Test get user by email."""
    auth_service = AuthService(async_session)

    # Create user
    created_user = await auth_service.signup(
        email="test@example.com",
        password="password123",
        full_name="Test User",
    )

    # Get user by email
    found_user = await auth_service.get_user_by_email("test@example.com")

    assert found_user is not None
    assert found_user.id == created_user.id
    assert found_user.email == created_user.email


@pytest.mark.asyncio
async def test_get_user_by_email_not_found(async_session: AsyncSession):
    """Test get user by email when user doesn't exist."""
    auth_service = AuthService(async_session)

    user = await auth_service.get_user_by_email("nonexistent@example.com")

    assert user is None


@pytest.mark.asyncio
async def test_verify_email_success(async_session: AsyncSession):
    """Test email verification."""
    auth_service = AuthService(async_session)

    # Create user
    user = await auth_service.signup(
        email="test@example.com",
        password="password123",
        full_name="Test User",
    )

    assert user.email_verified is False

    # Verify email
    verified_user = await auth_service.verify_email(user.id)

    assert verified_user.email_verified is True
