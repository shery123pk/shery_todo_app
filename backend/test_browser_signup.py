"""Test browser-like signup form submission"""
import httpx

print("=== Simulating Browser Signup Form Submission ===\n")

# Test with a completely new user
signup_url = "http://localhost:8000/api/auth/signup"
new_user = {
    "email": "browsertest@example.com",
    "password": "BrowserTest123",
    "name": "Browser Test User"
}

# Simulate browser headers
headers = {
    "Content-Type": "application/json",
    "Origin": "http://localhost:3004",
    "Referer": "http://localhost:3004/auth/signup",
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"
}

print(f"Submitting signup form for: {new_user['email']}")
print(f"Origin: {headers['Origin']}\n")

response = httpx.post(signup_url, json=new_user, headers=headers)

print(f"Status Code: {response.status_code}")
print(f"Response Headers:")
print(f"  - Content-Type: {response.headers.get('content-type')}")
print(f"  - Access-Control-Allow-Origin: {response.headers.get('access-control-allow-origin')}")
print(f"\nResponse Body:")
print(response.text)

if response.status_code == 201:
    print("\n[SUCCESS] User created successfully!")

    # Parse the response
    user_data = response.json()
    print(f"\nUser Details:")
    print(f"  - ID: {user_data['id']}")
    print(f"  - Email: {user_data['email']}")
    print(f"  - Name: {user_data['name']}")
    print(f"  - Email Verified: {user_data['email_verified']}")
    print(f"  - Created At: {user_data['created_at']}")

    # Now test signin with this user
    print("\n=== Testing Automatic Signin After Signup ===\n")
    signin_url = "http://localhost:8000/api/auth/signin"
    signin_data = {
        "email": new_user['email'],
        "password": new_user['password'],
        "remember_me": False
    }

    signin_response = httpx.post(signin_url, json=signin_data, headers=headers)
    print(f"Signin Status Code: {signin_response.status_code}")

    if signin_response.status_code == 200:
        print("[SUCCESS] User can sign in immediately after signup!")

        # Check for session cookie
        session_cookie = signin_response.cookies.get('session_token')
        if session_cookie:
            print(f"\nSession Cookie Set: Yes")
            print(f"Cookie Value (first 50 chars): {session_cookie[:50]}...")

            # Test protected endpoint
            print("\n=== Testing Protected Endpoint Access ===\n")
            me_url = "http://localhost:8000/api/auth/me"
            me_response = httpx.get(
                me_url,
                cookies={"session_token": session_cookie},
                headers={"Origin": "http://localhost:3004"}
            )

            print(f"GET /api/auth/me Status: {me_response.status_code}")
            if me_response.status_code == 200:
                print("[SUCCESS] Can access protected endpoints!")
                print(f"User Profile: {me_response.json()['email']}")
            else:
                print("[FAILED] Cannot access protected endpoints")
        else:
            print("[WARNING] No session cookie received!")
    else:
        print(f"[FAILED] Signin failed: {signin_response.text}")

elif response.status_code == 409:
    print("\n[INFO] User already exists - this is expected if running test multiple times")
    print("Testing signin with existing user...")

    # Test signin with existing user
    signin_url = "http://localhost:8000/api/auth/signin"
    signin_data = {
        "email": new_user['email'],
        "password": new_user['password'],
        "remember_me": False
    }

    signin_response = httpx.post(signin_url, json=signin_data, headers=headers)
    print(f"\nSignin Status Code: {signin_response.status_code}")
    if signin_response.status_code == 200:
        print("[SUCCESS] Existing user can sign in!")
    else:
        print(f"[FAILED] Signin failed: {signin_response.text}")
else:
    print(f"\n[FAILED] Signup failed!")
    print(f"Error: {response.text}")
