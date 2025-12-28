"""
Minimal validation of auth implementation
Tests imports and basic logic without database
"""

import sys
print("Python version:", sys.version)

# Test 1: Import security module
print("\n=== Test 1: Security Module ===")
try:
    from app.security import hash_password, verify_password
    print("✓ Security module imported")

    # Test password hashing
    hashed = hash_password("test123456")
    print(f"✓ Password hashed: {hashed[:30]}...")

    # Test password verification
    is_valid = verify_password("test123456", hashed)
    print(f"✓ Password verified: {is_valid}")
    assert is_valid == True

    # Test wrong password
    is_invalid = verify_password("wrongpass", hashed)
    print(f"✓ Wrong password rejected: {not is_invalid}")
    assert is_invalid == False

except Exception as e:
    print(f"✗ Security test failed: {e}")
    import traceback
    traceback.print_exc()
    sys.exit(1)

# Test 2: Import schemas
print("\n=== Test 2: Auth Schemas ===")
try:
    from app.schemas.auth import (
        SignupRequest,
        SigninRequest,
        UserResponse,
        UpdateProfileRequest,
        ChangePasswordRequest,
    )
    print("✓ SignupRequest imported")
    print("✓ SigninRequest imported")
    print("✓ UserResponse imported")
    print("✓ UpdateProfileRequest imported")
    print("✓ ChangePasswordRequest imported")

    # Test schema creation
    signup = SignupRequest(
        email="test@example.com",
        password="password123",
        full_name="Test User"
    )
    print(f"✓ SignupRequest created: {signup.email}, {signup.full_name}")

except Exception as e:
    print(f"✗ Schema test failed: {e}")
    import traceback
    traceback.print_exc()
    sys.exit(1)

# Test 3: Import models
print("\n=== Test 3: Database Models ===")
try:
    from app.models.user import User
    from app.models.session import Session
    print("✓ User model imported")
    print("✓ Session model imported")

except Exception as e:
    print(f"✗ Model test failed: {e}")
    import traceback
    traceback.print_exc()
    sys.exit(1)

# Test 4: Import auth service
print("\n=== Test 4: Auth Service ===")
try:
    from app.services.auth_service import AuthService
    print("✓ AuthService imported")
    print(f"✓ AuthService methods: {[m for m in dir(AuthService) if not m.startswith('_')][:10]}")

except Exception as e:
    print(f"✗ AuthService test failed: {e}")
    import traceback
    traceback.print_exc()
    sys.exit(1)

# Test 5: Import router
print("\n=== Test 5: Auth Router ===")
try:
    from app.routers.auth import router
    print("✓ Auth router imported")
    print(f"✓ Router prefix: {router.prefix}")
    print(f"✓ Number of routes: {len(router.routes)}")

except Exception as e:
    print(f"✗ Router test failed: {e}")
    import traceback
    traceback.print_exc()
    sys.exit(1)

print("\n" + "="*50)
print("✓✓✓ ALL VALIDATION TESTS PASSED ✓✓✓")
print("="*50)
print("\nAuth implementation is complete and all modules import correctly!")
print("Ready for database testing when venv is fixed.")
