"""Test signin with wrong password"""
import httpx

url = "http://localhost:8000/api/auth/signin"
data = {
    "email": "testuser@example.com",
    "password": "WrongPassword123",  # Wrong password
    "remember_me": False
}

response = httpx.post(url, json=data)
print(f"Status Code: {response.status_code}")
print(f"Response: {response.text}")
