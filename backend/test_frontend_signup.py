"""Test frontend signup flow with a new user"""
import httpx

# Test signup with a new user
signup_url = "http://localhost:8000/api/auth/signup"
new_user_data = {
    "email": "frontend.test@example.com",
    "password": "FrontendTest123",
    "name": "Frontend Test User"
}

print("=== Testing Signup ===")
response = httpx.post(signup_url, json=new_user_data)
print(f"Status Code: {response.status_code}")
print(f"Response: {response.text}")

if response.status_code == 201:
    print("\n[SUCCESS] Signup successful!")

    # Now test signin
    print("\n=== Testing Signin ===")
    signin_url = "http://localhost:8000/api/auth/signin"
    signin_data = {
        "email": "frontend.test@example.com",
        "password": "FrontendTest123",
        "remember_me": False
    }

    signin_response = httpx.post(signin_url, json=signin_data)
    print(f"Status Code: {signin_response.status_code}")
    print(f"Response: {signin_response.text}")

    if signin_response.status_code == 200:
        print("\n[SUCCESS] Signin successful!")
        print(f"Session Cookie: {signin_response.cookies.get('session_token')[:50]}...")
    else:
        print("\n[FAILED] Signin failed!")
else:
    print("\n[FAILED] Signup failed!")
