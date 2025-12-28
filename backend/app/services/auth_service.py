"""
Authentication Service

Handles user authentication operations: signup, signin, signout,
email verification, password reset, and profile management.

Author: Sharmeen Asif
"""

from datetime import datetime, timedelta, UTC
from uuid import UUID, uuid4
from typing import Optional

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from sqlalchemy.exc import IntegrityError

from app.models.user import User
from app.models.session import Session
from app.security import hash_password, verify_password, create_access_token, decode_access_token
from app.config import settings
from app.utils.errors import ValidationError, NotFoundError, UnauthorizedError, ConflictError


class AuthService:
    """Service for authentication operations."""

    def __init__(self, db: AsyncSession):
        self.db = db

    async def signup(
        self,
        email: str,
        password: str,
        full_name: str,
    ) -> User:
        """
        Create a new user account.

        Args:
            email: User's email address (will be normalized to lowercase)
            password: Plain text password (will be hashed with bcrypt)
            full_name: User's full name

        Returns:
            Created User object

        Raises:
            ValidationError: If email/password validation fails
            ConflictError: If email already exists
        """
        # Validate email format
        email = email.lower().strip()
        if not email or '@' not in email:
            raise ValidationError("Invalid email format")

        # Validate password strength
        if len(password) < 8:
            raise ValidationError("Password must be at least 8 characters")

        # Validate full_name
        if not full_name or len(full_name.strip()) < 2:
            raise ValidationError("Full name must be at least 2 characters")

        # Check if email already exists
        stmt = select(User).where(User.email == email)
        result = await self.db.execute(stmt)
        existing_user = result.scalar_one_or_none()

        if existing_user:
            raise ConflictError("Email already registered")

        # Hash password
        hashed_password = hash_password(password)

        # Create user
        user = User(
            email=email,
            hashed_password=hashed_password,
            full_name=full_name.strip(),
            email_verified=False,  # Requires email verification
        )

        self.db.add(user)

        try:
            await self.db.commit()
            await self.db.refresh(user)
        except IntegrityError:
            await self.db.rollback()
            raise ConflictError("Email already registered")

        return user

    async def signin(
        self,
        email: str,
        password: str,
        remember_me: bool = False,
        ip_address: Optional[str] = None,
        user_agent: Optional[str] = None,
    ) -> tuple[User, Session, str, str]:
        """
        Sign in a user and create a session.

        Args:
            email: User's email address
            password: Plain text password
            remember_me: If True, session lasts 30 days instead of 7
            ip_address: Client IP address for session tracking
            user_agent: Client user agent for session tracking

        Returns:
            Tuple of (User, Session, access_token, refresh_token)

        Raises:
            UnauthorizedError: If credentials are invalid
        """
        # Normalize email
        email = email.lower().strip()

        # Find user by email
        stmt = select(User).where(User.email == email)
        result = await self.db.execute(stmt)
        user = result.scalar_one_or_none()

        if not user:
            raise UnauthorizedError("Invalid email or password")

        # Verify password
        if not verify_password(password, user.hashed_password):
            raise UnauthorizedError("Invalid email or password")

        # Create access token (JWT)
        access_token = create_access_token(
            data={"sub": str(user.id), "email": user.email},
            remember_me=remember_me,
        )

        # Create refresh token
        refresh_token = create_access_token(
            data={"sub": str(user.id), "type": "refresh"},
            remember_me=True,  # Refresh tokens always last longer
        )

        # Calculate expiration
        if remember_me:
            expires_delta = timedelta(minutes=settings.access_token_expire_minutes_remember)
        else:
            expires_delta = timedelta(minutes=settings.access_token_expire_minutes)

        expires_at = datetime.now(UTC) + expires_delta

        # Create session record
        session = Session(
            user_id=user.id,
            token=access_token,
            refresh_token=refresh_token,
            expires_at=expires_at,
            ip_address=ip_address,
            user_agent=user_agent,
        )

        self.db.add(session)
        await self.db.commit()
        await self.db.refresh(session)

        return user, session, access_token, refresh_token

    async def signout(self, token: str) -> bool:
        """
        Sign out a user by invalidating their session.

        Args:
            token: Access token from the session

        Returns:
            True if session was deleted, False if not found
        """
        stmt = select(Session).where(Session.token == token)
        result = await self.db.execute(stmt)
        session = result.scalar_one_or_none()

        if session:
            await self.db.delete(session)
            await self.db.commit()
            return True

        return False

    async def get_user_by_id(self, user_id: UUID) -> Optional[User]:
        """Get user by ID."""
        stmt = select(User).where(User.id == user_id)
        result = await self.db.execute(stmt)
        return result.scalar_one_or_none()

    async def get_user_by_email(self, email: str) -> Optional[User]:
        """Get user by email."""
        email = email.lower().strip()
        stmt = select(User).where(User.email == email)
        result = await self.db.execute(stmt)
        return result.scalar_one_or_none()

    async def verify_email(self, user_id: UUID) -> User:
        """
        Mark user's email as verified.

        Args:
            user_id: User ID from verification token

        Returns:
            Updated User object

        Raises:
            NotFoundError: If user not found
        """
        user = await self.get_user_by_id(user_id)

        if not user:
            raise NotFoundError("User not found")

        user.email_verified = True
        await self.db.commit()
        await self.db.refresh(user)

        return user

    async def update_profile(
        self,
        user_id: UUID,
        full_name: Optional[str] = None,
        avatar_url: Optional[str] = None,
        timezone: Optional[str] = None,
        language: Optional[str] = None,
    ) -> User:
        """
        Update user profile information.

        Args:
            user_id: User ID
            full_name: New full name (optional)
            avatar_url: New avatar URL (optional)
            timezone: New timezone (optional)
            language: New language code (optional)

        Returns:
            Updated User object

        Raises:
            NotFoundError: If user not found
        """
        user = await self.get_user_by_id(user_id)

        if not user:
            raise NotFoundError("User not found")

        if full_name is not None:
            if len(full_name.strip()) < 2:
                raise ValidationError("Full name must be at least 2 characters")
            user.full_name = full_name.strip()

        if avatar_url is not None:
            user.avatar_url = avatar_url

        if timezone is not None:
            user.timezone = timezone

        if language is not None:
            user.language = language

        await self.db.commit()
        await self.db.refresh(user)

        return user

    async def change_password(
        self,
        user_id: UUID,
        current_password: str,
        new_password: str,
    ) -> User:
        """
        Change user's password.

        Args:
            user_id: User ID
            current_password: Current password (for verification)
            new_password: New password

        Returns:
            Updated User object

        Raises:
            NotFoundError: If user not found
            UnauthorizedError: If current password is incorrect
            ValidationError: If new password is weak
        """
        user = await self.get_user_by_id(user_id)

        if not user:
            raise NotFoundError("User not found")

        # Verify current password
        if not verify_password(current_password, user.hashed_password):
            raise UnauthorizedError("Current password is incorrect")

        # Validate new password
        if len(new_password) < 8:
            raise ValidationError("Password must be at least 8 characters")

        # Hash and update password
        user.hashed_password = hash_password(new_password)
        await self.db.commit()

        # Invalidate all existing sessions (force re-login everywhere)
        stmt = select(Session).where(Session.user_id == user_id)
        result = await self.db.execute(stmt)
        sessions = result.scalars().all()

        for session in sessions:
            await self.db.delete(session)

        await self.db.commit()
        await self.db.refresh(user)

        return user

    async def refresh_access_token(
        self,
        refresh_token: str,
    ) -> tuple[str, str]:
        """
        Generate new access token using refresh token.

        Args:
            refresh_token: Valid refresh token

        Returns:
            Tuple of (new_access_token, new_refresh_token)

        Raises:
            UnauthorizedError: If refresh token is invalid or expired
        """
        # Decode refresh token
        payload = decode_access_token(refresh_token)

        if not payload or payload.get("type") != "refresh":
            raise UnauthorizedError("Invalid refresh token")

        user_id_str = payload.get("sub")
        if not user_id_str:
            raise UnauthorizedError("Invalid refresh token")

        try:
            user_id = UUID(user_id_str)
        except ValueError:
            raise UnauthorizedError("Invalid refresh token")

        # Find session by refresh token
        stmt = select(Session).where(Session.refresh_token == refresh_token)
        result = await self.db.execute(stmt)
        session = result.scalar_one_or_none()

        if not session:
            raise UnauthorizedError("Session not found")

        # Check if session is expired
        if session.expires_at < datetime.now(UTC):
            await self.db.delete(session)
            await self.db.commit()
            raise UnauthorizedError("Session expired")

        # Get user
        user = await self.get_user_by_id(user_id)
        if not user:
            raise UnauthorizedError("User not found")

        # Create new tokens
        new_access_token = create_access_token(
            data={"sub": str(user.id), "email": user.email},
            remember_me=True,  # Keep same expiration
        )

        new_refresh_token = create_access_token(
            data={"sub": str(user.id), "type": "refresh"},
            remember_me=True,
        )

        # Update session
        session.token = new_access_token
        session.refresh_token = new_refresh_token
        session.expires_at = datetime.now(UTC) + timedelta(
            minutes=settings.access_token_expire_minutes_remember
        )

        await self.db.commit()
        await self.db.refresh(session)

        return new_access_token, new_refresh_token

    def create_verification_token(self, user_id: UUID, token_type: str = "verify") -> str:
        """
        Create a token for email verification or password reset.

        Args:
            user_id: User's UUID
            token_type: Type of token ("verify" or "reset")

        Returns:
            JWT token string (expires in 24 hours)

        Example:
            token = auth_service.create_verification_token(user.id, "verify")
        """
        data = {
            "sub": str(user_id),
            "type": token_type,
            "exp": datetime.now(UTC) + timedelta(hours=24),
        }
        return create_access_token(data, remember_me=False)

    def verify_token(self, token: str, expected_type: str = "verify") -> Optional[UUID]:
        """
        Verify and decode a verification/reset token.

        Args:
            token: JWT token to verify
            expected_type: Expected token type ("verify" or "reset")

        Returns:
            User UUID if valid, None otherwise

        Example:
            user_id = auth_service.verify_token(token, "verify")
        """
        payload = decode_access_token(token)
        if not payload:
            return None

        token_type = payload.get("type")
        if token_type != expected_type:
            return None

        user_id_str = payload.get("sub")
        if not user_id_str:
            return None

        try:
            return UUID(user_id_str)
        except ValueError:
            return None

    async def send_verification_email(self, user: User) -> str:
        """
        Generate verification token and prepare to send email.

        Args:
            user: User object to send verification email to

        Returns:
            Verification token (for testing/frontend to construct URL)

        Note:
            In production, this would trigger actual email sending via EmailService.
            For now, we return the token for the frontend to handle.

        Example:
            token = await auth_service.send_verification_email(user)
            # Frontend constructs: /auth/verify-email?token={token}
        """
        token = self.create_verification_token(user.id, "verify")

        # TODO: Send actual email using EmailService
        # from app.services.email import email_service
        # await email_service.send_verification_email(
        #     to_email=user.email,
        #     user_name=user.full_name,
        #     verification_url=f"{settings.frontend_url}/auth/verify-email?token={token}"
        # )

        return token

    async def verify_email_with_token(self, token: str) -> User:
        """
        Verify email using verification token.

        Args:
            token: Verification token from email link

        Returns:
            User object with email_verified=True

        Raises:
            UnauthorizedError: If token is invalid or expired
            NotFoundError: If user not found

        Example:
            user = await auth_service.verify_email_with_token(token)
        """
        user_id = self.verify_token(token, "verify")
        if not user_id:
            raise UnauthorizedError("Invalid or expired verification token")

        user = await self.get_user_by_id(user_id)
        if not user:
            raise NotFoundError("User not found")

        if user.email_verified:
            return user  # Already verified, no need to update

        user.email_verified = True
        await self.db.commit()
        await self.db.refresh(user)

        return user

    async def forgot_password(self, email: str) -> Optional[str]:
        """
        Generate password reset token for user.

        Args:
            email: User's email address

        Returns:
            Reset token if user exists, None otherwise (for security)

        Note:
            Always returns success even if email doesn't exist (security best practice).
            Actual email sending should happen here.

        Example:
            token = await auth_service.forgot_password("user@example.com")
            if token:
                # Send email with reset link
        """
        email = email.lower().strip()
        user = await self.get_user_by_email(email)

        if not user:
            # For security, don't reveal if email exists
            # Return None but don't raise error
            return None

        # Generate reset token (24 hour expiration)
        reset_token = self.create_verification_token(user.id, "reset")

        # TODO: Send actual password reset email
        # from app.services.email import email_service
        # await email_service.send_password_reset_email(
        #     to_email=user.email,
        #     user_name=user.full_name,
        #     reset_url=f"{settings.frontend_url}/auth/reset-password?token={reset_token}"
        # )

        return reset_token

    async def reset_password(self, token: str, new_password: str) -> User:
        """
        Reset user password using reset token.

        Args:
            token: Password reset token from email
            new_password: New password to set

        Returns:
            User object with updated password

        Raises:
            UnauthorizedError: If token is invalid or expired
            ValidationError: If new password is weak
            NotFoundError: If user not found

        Example:
            user = await auth_service.reset_password(token, "newpassword123")
        """
        # Validate new password
        if len(new_password) < 8:
            raise ValidationError("Password must be at least 8 characters")

        # Verify reset token
        user_id = self.verify_token(token, "reset")
        if not user_id:
            raise UnauthorizedError("Invalid or expired reset token")

        # Get user
        user = await self.get_user_by_id(user_id)
        if not user:
            raise NotFoundError("User not found")

        # Update password
        user.hashed_password = hash_password(new_password)
        await self.db.commit()

        # Invalidate all existing sessions (force re-login)
        stmt = select(Session).where(Session.user_id == user_id)
        result = await self.db.execute(stmt)
        for session in result.scalars().all():
            await self.db.delete(session)
        await self.db.commit()
        await self.db.refresh(user)

        return user
