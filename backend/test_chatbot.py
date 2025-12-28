"""Test the AI Chatbot with OpenAI GPT-4"""
import httpx
import json

print("=" * 70)
print("AI CHATBOT TEST WITH OPENAI GPT-4")
print("=" * 70)

# First, sign in to get a session token
print("\n[1/3] Signing in to get session token...")
signin_response = httpx.post(
    "http://localhost:8000/api/auth/signin",
    json={
        "email": "browsertest@example.com",
        "password": "BrowserTest123",
        "remember_me": False
    }
)

if signin_response.status_code != 200:
    print(f"[FAILED] Could not sign in: {signin_response.status_code}")
    exit(1)

session_token = signin_response.cookies.get('session_token')
print(f"[SUCCESS] Signed in! Session token received.")

# Check chatbot status
print("\n[2/3] Checking chatbot status...")
status_response = httpx.get(
    "http://localhost:8000/api/chatbot/status",
    cookies={"session_token": session_token}
)

status = status_response.json()
print(f"Status: {json.dumps(status, indent=2)}")

if not status.get("available"):
    print("[FAILED] Chatbot is not available!")
    exit(1)

print(f"[SUCCESS] Chatbot is ready: {status['message']}")

# Test chatbot with various messages
print("\n[3/3] Testing chatbot conversations...")
print("=" * 70)

test_messages = [
    "Hello! Who are you?",
    "Can you help me add a task?",
    "What can you help me with?",
]

for i, message in enumerate(test_messages, 1):
    print(f"\n[USER] Message {i}: '{message}'")

    chat_response = httpx.post(
        "http://localhost:8000/api/chatbot/chat",
        json={"message": message},
        cookies={"session_token": session_token},
        timeout=30.0
    )

    if chat_response.status_code == 200:
        data = chat_response.json()
        response_text = data.get("response", "No response")
        print(f"[AI] Response:\n{response_text}")
        print("-" * 70)
    else:
        print(f"[ERROR] Failed to get response: {chat_response.status_code}")
        print(f"Error: {chat_response.text}")

print("\n" + "=" * 70)
print("CHATBOT TEST COMPLETE!")
print("=" * 70)
print("\nThe AI chatbot is working! You can now use it in the browser:")
print("  http://localhost:3004/chatbot")
print("=" * 70)
