"""
Complete End-to-End Application Test
Tests the entire Phase 2 Todo Application flow:
1. User Signup
2. User Signin
3. Task CRUD Operations
4. AI Chatbot Interaction
5. Session Management
"""
import httpx
import json
from datetime import datetime

print("=" * 80)
print("PHASE 2 TODO APPLICATION - COMPLETE END-TO-END TEST")
print("=" * 80)

base_url = "http://localhost:8000"
test_email = f"e2e_test_{datetime.now().strftime('%Y%m%d_%H%M%S')}@example.com"
test_password = "SecurePass123!"
session_token = None

# Create HTTP client with longer timeout
client = httpx.Client(timeout=30.0)

# ============================================================================
# TEST 1: User Signup
# ============================================================================
print("\n[TEST 1/6] User Signup")
print("-" * 80)

signup_response = client.post(
    f"{base_url}/api/auth/signup",
    json={
        "email": test_email,
        "password": test_password,
        "full_name": "E2E Test User"
    }
)

if signup_response.status_code == 201:
    user_data = signup_response.json()
    print(f"[PASS] - User created successfully")
    print(f"   User ID: {user_data['id']}")
    print(f"   Email: {user_data['email']}")
    print(f"   Name: {user_data.get('name', user_data.get('full_name', 'N/A'))}")
else:
    print(f"[FAIL] - Signup failed with status {signup_response.status_code}")
    print(f"   Error: {signup_response.text}")
    exit(1)

# ============================================================================
# TEST 2: User Signin
# ============================================================================
print("\n[TEST 2/6] User Signin")
print("-" * 80)

signin_response = client.post(
    f"{base_url}/api/auth/signin",
    json={
        "email": test_email,
        "password": test_password,
        "remember_me": False
    }
)

if signin_response.status_code == 200:
    session_token = signin_response.cookies.get('session_token')
    signin_data = signin_response.json()
    print(f"[PASS] - Signin successful")
    print(f"   Session token received: {session_token[:20]}...")
    print(f"   User: {signin_data['user']['email']}")
else:
    print(f"[FAIL] - Signin failed with status {signin_response.status_code}")
    print(f"   Error: {signin_response.text}")
    exit(1)

# ============================================================================
# TEST 3: Get Current User (Protected Route)
# ============================================================================
print("\n[TEST 3/6] Protected Route - Get Current User")
print("-" * 80)

me_response = client.get(
    f"{base_url}/api/auth/me",
    cookies={"session_token": session_token}
)

if me_response.status_code == 200:
    me_data = me_response.json()
    print(f"[PASS] - Protected route accessible")
    print(f"   Authenticated as: {me_data['email']}")
else:
    print(f"[FAIL] - Protected route failed with status {me_response.status_code}")
    exit(1)

# ============================================================================
# TEST 4: Task CRUD Operations
# ============================================================================
print("\n[TEST 4/6] Task CRUD Operations")
print("-" * 80)

# Create a task
create_task_response = client.post(
    f"{base_url}/api/tasks",
    json={
        "title": "Test the complete application flow",
        "description": "Verify all Phase 2 features are working",
        "completed": False,
        "priority": "high",
        "category": "testing"
    },
    cookies={"session_token": session_token}
)

if create_task_response.status_code == 201:
    task = create_task_response.json()
    task_id = task['id']
    print(f"[PASS] - Task created")
    print(f"   Task ID: {task_id}")
    print(f"   Title: {task['title']}")
else:
    print(f"[FAIL] - Task creation failed with status {create_task_response.status_code}")
    exit(1)

# Read tasks
read_tasks_response = client.get(
    f"{base_url}/api/tasks",
    cookies={"session_token": session_token}
)

if read_tasks_response.status_code == 200:
    tasks = read_tasks_response.json()
    print(f"[PASS] - Tasks retrieved")
    print(f"   Total tasks: {len(tasks)}")
else:
    print(f"[FAIL] - Task retrieval failed")
    exit(1)

# Note: Task UPDATE and DELETE endpoints are not implemented yet
print(f"[SKIP] - Task update endpoint not implemented (would be PUT /api/tasks/{{id}})")
print(f"[SKIP] - Task delete endpoint not implemented (would be DELETE /api/tasks/{{id}})")
print(f"[INFO] - Current implementation has: GET /api/tasks, GET /api/tasks/{{id}}, POST /api/tasks")

# ============================================================================
# TEST 5: AI Chatbot
# ============================================================================
print("\n[TEST 5/6] AI Chatbot Integration")
print("-" * 80)

# Check chatbot status
status_response = client.get(
    f"{base_url}/api/chatbot/status",
    cookies={"session_token": session_token}
)

if status_response.status_code == 200:
    status = status_response.json()
    print(f"[PASS] - Chatbot status check")
    print(f"   Available: {status['available']}")
    print(f"   Provider: {status.get('provider', 'N/A')}")
    print(f"   Message: {status['message']}")
else:
    print(f"[FAIL] - Chatbot status check failed")
    exit(1)

# Send a message to chatbot
chat_response = client.post(
    f"{base_url}/api/chatbot/chat",
    json={"message": "What can you help me with?"},
    cookies={"session_token": session_token}
)

if chat_response.status_code == 200:
    chat_data = chat_response.json()
    print(f"[PASS] - Chatbot conversation")
    # Remove emojis to avoid Windows console encoding issues
    response_text = chat_data['response'].encode('ascii', 'ignore').decode('ascii')
    print(f"   AI Response (sanitized): {response_text[:80]}...")
else:
    print(f"[FAIL] - Chatbot conversation failed")
    exit(1)

# ============================================================================
# TEST 6: Session Signout
# ============================================================================
print("\n[TEST 6/6] Session Signout")
print("-" * 80)

signout_response = client.post(
    f"{base_url}/api/auth/signout",
    cookies={"session_token": session_token}
)

if signout_response.status_code == 204:
    print(f"[PASS] - User signed out successfully")
else:
    print(f"[FAIL] - Signout failed with status {signout_response.status_code}")
    exit(1)

# Verify session is invalid after signout
verify_response = client.get(
    f"{base_url}/api/auth/me",
    cookies={"session_token": session_token}
)

if verify_response.status_code == 401:
    print(f"[PASS] - Session invalidated correctly")
else:
    print(f"[FAIL] - Session still valid after signout")
    exit(1)

# ============================================================================
# FINAL REPORT
# ============================================================================
print("\n" + "=" * 80)
print("COMPLETE END-TO-END TEST RESULTS")
print("=" * 80)
print("""
[PASS] User Signup              - Working
[PASS] User Signin              - Working
[PASS] Protected Routes         - Working
[PASS] Task Create & Read       - Working
[SKIP] Task Update & Delete     - Not implemented yet
[PASS] AI Chatbot (OpenAI GPT-4) - Working
[PASS] Session Management       - Working

*** PHASE 2 CORE FEATURES OPERATIONAL! ***

Implemented Features:
- User authentication (signup, signin, signout)
- Session-based auth with JWT tokens
- Task creation and listing
- OpenAI GPT-4 chatbot integration
- Protected API endpoints
- Neon PostgreSQL database

Missing Features (to be implemented):
- PUT /api/tasks/{id} (update task)
- DELETE /api/tasks/{id} (delete task)

Application is ready for:
- Local development and testing
- Frontend integration (auth + task create/read + chatbot)
- Task update/delete endpoints need to be added for full CRUD
""")
print("=" * 80)

# Close HTTP client
client.close()
