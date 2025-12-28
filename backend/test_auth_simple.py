"""
Simple standalone test for auth service
Verifies basic signup and signin functionality
"""

import asyncio
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession, async_sessionmaker
from sqlmodel import SQLModel

# Import our models and services
from app.models.user import User
from app.models.session import Session
from app.services.auth_service import AuthService
from app.config import settings
from app.security import verify_password


async def test_auth():
    """Test basic auth operations"""
    print("=== Testing Auth Service ===\n")

    # Create async engine
    engine = create_async_engine(
        settings.database_url,
        echo=False,
        pool_pre_ping=True,
    )

    # Create tables
    async with engine.begin() as conn:
        await conn.run_sync(SQLModel.metadata.create_all)

    # Create session
    async_session_maker = async_sessionmaker(
        engine,
        class_=AsyncSession,
        expire_on_commit=False,
    )

    async with async_session_maker() as session:
        async with session.begin():
            auth_service = AuthService(session)

            # Test 1: Signup
            print("Test 1: Signup")
            try:
                user = await auth_service.signup(
                    email="testuser@example.com",
                    password="password123",
                    full_name="Test User"
                )
                print(f"✓ User created: {user.email} (ID: {user.id})")
                print(f"  Full name: {user.full_name}")
                print(f"  Email verified: {user.email_verified}")
                assert user.email == "testuser@example.com"
                assert user.full_name == "Test User"
                assert verify_password("password123", user.hashed_password)
            except Exception as e:
                print(f"✗ Signup failed: {e}")
                raise

            # Test 2: Signin
            print("\nTest 2: Signin")
            try:
                user, session_obj, access_token, refresh_token = await auth_service.signin(
                    email="testuser@example.com",
                    password="password123",
                    remember_me=False
                )
                print(f"✓ User signed in: {user.email}")
                print(f"  Session ID: {session_obj.id}")
                print(f"  Access token: {access_token[:50]}...")
                print(f"  Refresh token: {refresh_token[:50]}...")
                assert user.email == "testuser@example.com"
                assert access_token is not None
                assert refresh_token is not None
            except Exception as e:
                print(f"✗ Signin failed: {e}")
                raise

            # Test 3: Update Profile
            print("\nTest 3: Update Profile")
            try:
                updated_user = await auth_service.update_profile(
                    user_id=user.id,
                    full_name="Updated Name",
                    timezone="America/New_York",
                    language="en"
                )
                print(f"✓ Profile updated")
                print(f"  New full name: {updated_user.full_name}")
                print(f"  Timezone: {updated_user.timezone}")
                print(f"  Language: {updated_user.language}")
                assert updated_user.full_name == "Updated Name"
                assert updated_user.timezone == "America/New_York"
            except Exception as e:
                print(f"✗ Profile update failed: {e}")
                raise

            # Test 4: Change Password
            print("\nTest 4: Change Password")
            try:
                await auth_service.change_password(
                    user_id=user.id,
                    current_password="password123",
                    new_password="newpassword456"
                )
                print(f"✓ Password changed successfully")

                # Verify new password works
                user2, session2, _, _ = await auth_service.signin(
                    email="testuser@example.com",
                    password="newpassword456"
                )
                print(f"✓ Can sign in with new password")
                assert user2.email == "testuser@example.com"
            except Exception as e:
                print(f"✗ Password change failed: {e}")
                raise

            print("\n=== All Tests Passed! ===")

    # Cleanup
    async with engine.begin() as conn:
        await conn.run_sync(SQLModel.metadata.drop_all)

    await engine.dispose()


if __name__ == "__main__":
    asyncio.run(test_auth())
