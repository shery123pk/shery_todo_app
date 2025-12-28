"""Test signup endpoint"""
import httpx

url = "http://localhost:8000/api/auth/signup"
data = {
    "email": "testuser@example.com",
    "password": "Test123456",
    "name": "Test User"
}

response = httpx.post(url, json=data)
print(f"Status Code: {response.status_code}")
print(f"Response: {response.text}")
