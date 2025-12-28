"""Test signin endpoint"""
import httpx

url = "http://localhost:8000/api/auth/signin"
data = {
    "email": "testuser@example.com",
    "password": "Test123456",
    "remember_me": False
}

response = httpx.post(url, json=data)
print(f"Status Code: {response.status_code}")
print(f"Response: {response.text}")
print(f"Cookies: {response.cookies}")
