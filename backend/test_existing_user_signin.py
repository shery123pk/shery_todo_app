"""Test signin with existing frontend test user"""
import httpx

print("=== Testing Signin with Existing User ===")
signin_url = "http://localhost:8000/api/auth/signin"
signin_data = {
    "email": "frontend.test@example.com",
    "password": "FrontendTest123",
    "remember_me": False
}

response = httpx.post(signin_url, json=signin_data)
print(f"Status Code: {response.status_code}")
print(f"Response: {response.text}")

if response.status_code == 200:
    print("\n[SUCCESS] Signin successful!")
    session_token = response.cookies.get('session_token')
    if session_token:
        print(f"Session Cookie: {session_token[:50]}...")

        # Test accessing protected endpoint
        print("\n=== Testing Protected Endpoint /api/auth/me ===")
        me_url = "http://localhost:8000/api/auth/me"
        me_response = httpx.get(me_url, cookies={"session_token": session_token})
        print(f"Status Code: {me_response.status_code}")
        print(f"Response: {me_response.text}")

        if me_response.status_code == 200:
            print("\n[SUCCESS] Protected endpoint accessible with session!")
        else:
            print("\n[FAILED] Protected endpoint denied!")
    else:
        print("\n[WARNING] No session cookie received!")
else:
    print("\n[FAILED] Signin failed!")
