"""Final comprehensive browser signup flow test"""
import httpx
import time

print("=" * 70)
print("BROWSER SIGNUP FORM SUBMISSION TEST")
print("=" * 70)

# Test with a unique user
timestamp = int(time.time())
test_user = {
    "email": f"user{timestamp}@example.com",
    "password": "SecurePassword123",
    "name": f"Test User {timestamp}"
}

# Browser-like headers
headers = {
    "Content-Type": "application/json",
    "Origin": "http://localhost:3004",
    "Referer": "http://localhost:3004/auth/signup",
    "Accept": "application/json",
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"
}

print("\n[1/5] TESTING SIGNUP FORM SUBMISSION")
print("-" * 70)
print(f"Email: {test_user['email']}")
print(f"Name: {test_user['name']}")
print(f"Origin: http://localhost:3004")

signup_response = httpx.post(
    "http://localhost:8000/api/auth/signup",
    json=test_user,
    headers=headers,
    timeout=10.0
)

print(f"\nStatus: {signup_response.status_code} {signup_response.reason_phrase}")
print(f"CORS Header: {signup_response.headers.get('access-control-allow-origin', 'NOT SET')}")

if signup_response.status_code == 201:
    print("[PASS] User created successfully!")
    user_data = signup_response.json()
    print(f"User ID: {user_data['id']}")
else:
    print(f"[FAIL] Signup failed: {signup_response.text}")
    exit(1)

print("\n[2/5] TESTING SIGNIN WITH NEW ACCOUNT")
print("-" * 70)

signin_response = httpx.post(
    "http://localhost:8000/api/auth/signin",
    json={
        "email": test_user['email'],
        "password": test_user['password'],
        "remember_me": False
    },
    headers=headers,
    timeout=10.0
)

print(f"Status: {signin_response.status_code}")
print(f"CORS Header: {signin_response.headers.get('access-control-allow-origin', 'NOT SET')}")

if signin_response.status_code == 200:
    print("[PASS] Signin successful!")
    session_token = signin_response.cookies.get('session_token')
    if session_token:
        print(f"Session cookie received (length: {len(session_token)} chars)")
    else:
        print("[FAIL] No session cookie!")
        exit(1)
else:
    print(f"[FAIL] Signin failed: {signin_response.text}")
    exit(1)

print("\n[3/5] TESTING PROTECTED ENDPOINT ACCESS")
print("-" * 70)

me_response = httpx.get(
    "http://localhost:8000/api/auth/me",
    cookies={"session_token": session_token},
    headers={"Origin": "http://localhost:3004"},
    timeout=10.0
)

print(f"Status: {me_response.status_code}")
print(f"CORS Header: {me_response.headers.get('access-control-allow-origin', 'NOT SET')}")

if me_response.status_code == 200:
    print("[PASS] Protected endpoint accessible!")
    profile = me_response.json()
    print(f"Profile Email: {profile['email']}")
    print(f"Profile Name: {profile['name']}")
else:
    print("[FAIL] Cannot access protected endpoint")
    exit(1)

print("\n[4/5] TESTING WRONG PASSWORD")
print("-" * 70)

wrong_signin = httpx.post(
    "http://localhost:8000/api/auth/signin",
    json={
        "email": test_user['email'],
        "password": "WrongPassword123",
        "remember_me": False
    },
    headers=headers,
    timeout=10.0
)

print(f"Status: {wrong_signin.status_code}")

if wrong_signin.status_code == 401:
    print("[PASS] Wrong password correctly rejected!")
    print(f"Error: {wrong_signin.json()['detail']}")
else:
    print("[FAIL] Wrong password not rejected properly")
    exit(1)

print("\n[5/5] TESTING DUPLICATE EMAIL")
print("-" * 70)

duplicate_signup = httpx.post(
    "http://localhost:8000/api/auth/signup",
    json=test_user,
    headers=headers,
    timeout=10.0
)

print(f"Status: {duplicate_signup.status_code}")

if duplicate_signup.status_code == 409:
    print("[PASS] Duplicate email correctly rejected!")
    print(f"Error: {duplicate_signup.json()['detail']}")
else:
    print("[FAIL] Duplicate email not rejected properly")
    exit(1)

print("\n" + "=" * 70)
print("ALL TESTS PASSED!")
print("=" * 70)
print("\nThe signup form submission works perfectly in browser simulation!")
print("\nYou can now test in a real browser:")
print(f"  1. Open: http://localhost:3004/auth/signup")
print(f"  2. Fill in the form")
print(f"  3. Submit")
print(f"  4. You should be redirected and authenticated")
print("\n" + "=" * 70)
