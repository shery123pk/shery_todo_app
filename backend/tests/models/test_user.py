"""
Test User model.

Tests for User model field validation, email normalization, and defaults.
"""

import pytest
from datetime import datetime, UTC
from uuid import UUID
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from app.models.user import User


@pytest.mark.asyncio
async def test_user_model_exists():
    """Test that User model can be imported."""
    assert User is not None


@pytest.mark.asyncio
async def test_user_creation_basic(async_session: AsyncSession):
    """Test creating a basic user with required fields."""
    user = User(
        email="test@example.com",
        hashed_password="hashed_password_here",
        full_name="John Doe"
    )

    async_session.add(user)
    await async_session.commit()
    await async_session.refresh(user)

    assert user.id is not None
    assert isinstance(user.id, UUID)
    assert user.email == "test@example.com"
    assert user.hashed_password == "hashed_password_here"
    assert user.full_name == "John Doe"


@pytest.mark.asyncio
async def test_user_email_lowercase_normalization(async_session: AsyncSession):
    """Test that email is automatically converted to lowercase."""
    user = User(
        email="Test.User@EXAMPLE.COM",
        hashed_password="hashed_password",
        full_name="Test User"
    )

    async_session.add(user)
    await async_session.commit()
    await async_session.refresh(user)

    # Email should be normalized to lowercase
    assert user.email == "test.user@example.com"


@pytest.mark.asyncio
async def test_user_email_verified_default_false(async_session: AsyncSession):
    """Test that email_verified defaults to False."""
    user = User(
        email="newuser@example.com",
        hashed_password="password_hash",
        full_name="New User"
    )

    async_session.add(user)
    await async_session.commit()
    await async_session.refresh(user)

    assert user.email_verified is False


@pytest.mark.asyncio
async def test_user_email_verified_can_be_set_true(async_session: AsyncSession):
    """Test that email_verified can be explicitly set to True."""
    user = User(
        email="verified@example.com",
        hashed_password="password_hash",
        full_name="Verified User",
        email_verified=True
    )

    async_session.add(user)
    await async_session.commit()
    await async_session.refresh(user)

    assert user.email_verified is True


@pytest.mark.asyncio
async def test_user_optional_fields(async_session: AsyncSession):
    """Test user with all optional fields set."""
    user = User(
        email="fulluser@example.com",
        hashed_password="password_hash",
        full_name="Full User",
        avatar_url="https://example.com/avatar.jpg",
        timezone="America/New_York",
        language="en-US"
    )

    async_session.add(user)
    await async_session.commit()
    await async_session.refresh(user)

    assert user.avatar_url == "https://example.com/avatar.jpg"
    assert user.timezone == "America/New_York"
    assert user.language == "en-US"


@pytest.mark.asyncio
async def test_user_optional_fields_nullable(async_session: AsyncSession):
    """Test that optional fields can be None."""
    user = User(
        email="minimal@example.com",
        hashed_password="password_hash",
        full_name="Minimal User"
    )

    async_session.add(user)
    await async_session.commit()
    await async_session.refresh(user)

    assert user.avatar_url is None
    assert user.timezone is None
    assert user.language is None


@pytest.mark.asyncio
async def test_user_timestamps_auto_set(async_session: AsyncSession):
    """Test that timestamps are automatically set."""
    user = User(
        email="timestamps@example.com",
        hashed_password="password_hash",
        full_name="Timestamp User"
    )

    async_session.add(user)
    await async_session.commit()
    await async_session.refresh(user)

    assert user.created_at is not None
    assert isinstance(user.created_at, datetime)
    assert user.updated_at is not None
    assert isinstance(user.updated_at, datetime)

    # Timestamps should be close to now
    now = datetime.now(UTC)
    assert (now - user.created_at).total_seconds() < 5
    assert (now - user.updated_at).total_seconds() < 5


@pytest.mark.asyncio
async def test_user_timestamps_timezone_aware(async_session: AsyncSession):
    """Test that timestamps are timezone-aware (UTC)."""
    user = User(
        email="tz@example.com",
        hashed_password="password_hash",
        full_name="TZ User"
    )

    async_session.add(user)
    await async_session.commit()
    await async_session.refresh(user)

    # Timestamps should be timezone-aware
    assert user.created_at.tzinfo is not None
    assert user.updated_at.tzinfo is not None


@pytest.mark.asyncio
async def test_user_email_unique(async_session: AsyncSession):
    """Test that email must be unique."""
    from sqlalchemy.exc import IntegrityError

    user1 = User(
        email="unique@example.com",
        hashed_password="password1",
        full_name="User One"
    )

    async_session.add(user1)
    await async_session.commit()

    # Try to create another user with same email
    user2 = User(
        email="unique@example.com",
        hashed_password="password2",
        full_name="User Two"
    )

    async_session.add(user2)

    with pytest.raises(IntegrityError):
        await async_session.commit()

    await async_session.rollback()


@pytest.mark.asyncio
async def test_user_full_name_required(async_session: AsyncSession):
    """Test that full_name is required."""
    from sqlalchemy.exc import IntegrityError
    from pydantic import ValidationError

    # Pydantic validation should catch this
    with pytest.raises((ValidationError, TypeError)):
        user = User(
            email="noname@example.com",
            hashed_password="password_hash"
            # Missing full_name
        )


@pytest.mark.asyncio
async def test_user_updated_at_changes_on_update(async_session: AsyncSession):
    """Test that updated_at changes when user is updated."""
    import asyncio

    user = User(
        email="updatetest@example.com",
        hashed_password="password_hash",
        full_name="Update Test"
    )

    async_session.add(user)
    await async_session.commit()
    await async_session.refresh(user)

    original_updated_at = user.updated_at

    # Wait a moment to ensure timestamp will be different
    await asyncio.sleep(0.1)

    # Update user
    user.full_name = "Updated Name"
    await async_session.commit()
    await async_session.refresh(user)

    # updated_at should have changed
    assert user.updated_at > original_updated_at


@pytest.mark.asyncio
async def test_user_email_validation(async_session: AsyncSession):
    """Test email format validation."""
    from pydantic import ValidationError

    # Invalid email should be caught by Pydantic
    with pytest.raises(ValidationError):
        user = User(
            email="not-an-email",
            hashed_password="password_hash",
            full_name="Invalid Email"
        )


# ============================================================================
# Session Model Tests (T040)
# ============================================================================

from app.models.session import Session


@pytest.mark.asyncio
async def test_session_model_exists():
    """Test that Session model can be imported."""
    assert Session is not None


@pytest.mark.asyncio
async def test_session_creation_basic(async_session: AsyncSession):
    """Test creating a basic session."""
    from datetime import timedelta

    # Create user first
    user = User(
        email="sessionuser@example.com",
        hashed_password="password_hash",
        full_name="Session User"
    )
    async_session.add(user)
    await async_session.commit()
    await async_session.refresh(user)

    # Create session
    expires_at = datetime.now(UTC) + timedelta(days=7)
    session = Session(
        user_id=user.id,
        token="session_token_123",
        refresh_token="refresh_token_123",
        expires_at=expires_at,
        ip_address="192.168.1.1",
        user_agent="Mozilla/5.0..."
    )

    async_session.add(session)
    await async_session.commit()
    await async_session.refresh(session)

    assert session.id is not None
    assert isinstance(session.id, UUID)
    assert session.user_id == user.id
    assert session.token == "session_token_123"
    assert session.refresh_token == "refresh_token_123"
    assert session.expires_at == expires_at


@pytest.mark.asyncio
async def test_session_token_unique(async_session: AsyncSession):
    """Test that session token must be unique."""
    from sqlalchemy.exc import IntegrityError
    from datetime import timedelta

    # Create user
    user = User(
        email="tokenuser@example.com",
        hashed_password="password_hash",
        full_name="Token User"
    )
    async_session.add(user)
    await async_session.commit()
    await async_session.refresh(user)

    # Create first session
    session1 = Session(
        user_id=user.id,
        token="unique_token",
        refresh_token="refresh1",
        expires_at=datetime.now(UTC) + timedelta(days=7)
    )
    async_session.add(session1)
    await async_session.commit()

    # Try to create second session with same token
    session2 = Session(
        user_id=user.id,
        token="unique_token",  # Duplicate token
        refresh_token="refresh2",
        expires_at=datetime.now(UTC) + timedelta(days=7)
    )
    async_session.add(session2)

    with pytest.raises(IntegrityError):
        await async_session.commit()

    await async_session.rollback()


@pytest.mark.asyncio
async def test_session_refresh_token_unique(async_session: AsyncSession):
    """Test that refresh_token must be unique."""
    from sqlalchemy.exc import IntegrityError
    from datetime import timedelta

    # Create user
    user = User(
        email="refreshuser@example.com",
        hashed_password="password_hash",
        full_name="Refresh User"
    )
    async_session.add(user)
    await async_session.commit()
    await async_session.refresh(user)

    # Create first session
    session1 = Session(
        user_id=user.id,
        token="token1",
        refresh_token="unique_refresh_token",
        expires_at=datetime.now(UTC) + timedelta(days=7)
    )
    async_session.add(session1)
    await async_session.commit()

    # Try to create second session with same refresh_token
    session2 = Session(
        user_id=user.id,
        token="token2",
        refresh_token="unique_refresh_token",  # Duplicate refresh_token
        expires_at=datetime.now(UTC) + timedelta(days=7)
    )
    async_session.add(session2)

    with pytest.raises(IntegrityError):
        await async_session.commit()

    await async_session.rollback()


@pytest.mark.asyncio
async def test_session_cascade_delete_on_user_delete(async_session: AsyncSession):
    """Test that session is deleted when user is deleted (CASCADE)."""
    from datetime import timedelta

    # Create user
    user = User(
        email="cascadeuser@example.com",
        hashed_password="password_hash",
        full_name="Cascade User"
    )
    async_session.add(user)
    await async_session.commit()
    await async_session.refresh(user)

    user_id = user.id

    # Create session for user
    session = Session(
        user_id=user.id,
        token="cascade_token",
        refresh_token="cascade_refresh",
        expires_at=datetime.now(UTC) + timedelta(days=7)
    )
    async_session.add(session)
    await async_session.commit()
    await async_session.refresh(session)

    session_id = session.id

    # Delete user
    await async_session.delete(user)
    await async_session.commit()

    # Session should also be deleted (CASCADE)
    result = await async_session.execute(
        select(Session).where(Session.id == session_id)
    )
    deleted_session = result.scalar_one_or_none()

    assert deleted_session is None


@pytest.mark.asyncio
async def test_session_optional_fields_nullable(async_session: AsyncSession):
    """Test that ip_address and user_agent can be None."""
    from datetime import timedelta

    # Create user
    user = User(
        email="minimal_session@example.com",
        hashed_password="password_hash",
        full_name="Minimal Session User"
    )
    async_session.add(user)
    await async_session.commit()
    await async_session.refresh(user)

    # Create session without optional fields
    session = Session(
        user_id=user.id,
        token="minimal_token",
        refresh_token="minimal_refresh",
        expires_at=datetime.now(UTC) + timedelta(days=7)
    )
    async_session.add(session)
    await async_session.commit()
    await async_session.refresh(session)

    assert session.ip_address is None
    assert session.user_agent is None


@pytest.mark.asyncio
async def test_session_expiration_validation(async_session: AsyncSession):
    """Test session expiration timestamp validation."""
    from datetime import timedelta

    # Create user
    user = User(
        email="expirationuser@example.com",
        hashed_password="password_hash",
        full_name="Expiration User"
    )
    async_session.add(user)
    await async_session.commit()
    await async_session.refresh(user)

    # Create session with future expiration
    future_expiration = datetime.now(UTC) + timedelta(days=30)
    session = Session(
        user_id=user.id,
        token="expiration_token",
        refresh_token="expiration_refresh",
        expires_at=future_expiration
    )
    async_session.add(session)
    await async_session.commit()
    await async_session.refresh(session)

    assert session.expires_at == future_expiration

    # Check if session is expired
    now = datetime.now(UTC)
    is_expired = session.expires_at < now
    assert is_expired is False  # Should not be expired


@pytest.mark.asyncio
async def test_session_created_at_auto_set(async_session: AsyncSession):
    """Test that created_at is automatically set."""
    from datetime import timedelta

    # Create user
    user = User(
        email="created_at_user@example.com",
        hashed_password="password_hash",
        full_name="Created At User"
    )
    async_session.add(user)
    await async_session.commit()
    await async_session.refresh(user)

    # Create session
    session = Session(
        user_id=user.id,
        token="created_at_token",
        refresh_token="created_at_refresh",
        expires_at=datetime.now(UTC) + timedelta(days=7)
    )
    async_session.add(session)
    await async_session.commit()
    await async_session.refresh(session)

    assert session.created_at is not None
    assert isinstance(session.created_at, datetime)

    # Should be close to now
    now = datetime.now(UTC)
    assert (now - session.created_at).total_seconds() < 5
