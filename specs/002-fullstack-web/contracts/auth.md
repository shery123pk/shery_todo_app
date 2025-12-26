# Authentication API Contract

**Feature**: 002-fullstack-web
**Base URL**: `/api/auth`
**Authentication**: Public endpoints (no auth required except `/me`)
**Date**: 2025-12-26

---

## Endpoints

### POST /api/auth/signup

**Description**: Register a new user account with email and password.

**Authentication**: None (public endpoint)

**Request Headers**:
```http
Content-Type: application/json
```

**Request Body**:
```json
{
  "email": "user@example.com",
  "password": "securepass123",
  "name": "John Doe"  // optional
}
```

**Request Schema**:
```typescript
interface SignupRequest {
  email: string;           // RFC 5322 valid email, max 255 chars
  password: string;        // Min 8 chars, max 100 chars
  name?: string;           // Optional, max 255 chars
}
```

**Success Response (201 Created)**:
```json
{
  "id": "550e8400-e29b-41d4-a716-446655440000",
  "email": "user@example.com",
  "name": "John Doe",
  "email_verified": false,
  "created_at": "2025-12-26T10:00:00Z"
}
```

**Response Schema**:
```typescript
interface UserRead {
  id: string;              // UUID
  email: string;
  name: string | null;
  email_verified: boolean;
  created_at: string;      // ISO 8601 UTC timestamp
}
```

**Error Responses**:

**400 Bad Request** - Invalid input:
```json
{
  "detail": "Please enter a valid email address"
}
```

```json
{
  "detail": "Password must be at least 8 characters"
}
```

**409 Conflict** - Duplicate email:
```json
{
  "detail": "An account with this email already exists"
}
```

**Validation Rules**:
- Email: Valid RFC 5322 format, converted to lowercase
- Password: 8-100 characters (before hashing)
- Name: Optional, max 255 characters

**Example Usage**:
```bash
curl -X POST http://localhost:8000/api/auth/signup \
  -H "Content-Type: application/json" \
  -d '{
    "email": "newuser@example.com",
    "password": "mysecurepass123",
    "name": "Jane Doe"
  }'
```

---

### POST /api/auth/signin

**Description**: Login with email and password, receive session cookie.

**Authentication**: None (public endpoint)

**Request Headers**:
```http
Content-Type: application/json
```

**Request Body**:
```json
{
  "email": "user@example.com",
  "password": "securepass123",
  "remember_me": false  // optional, default false
}
```

**Request Schema**:
```typescript
interface SigninRequest {
  email: string;
  password: string;
  remember_me?: boolean;   // If true, 30-day session; else 7-day session
}
```

**Success Response (200 OK)**:
```json
{
  "user": {
    "id": "550e8400-e29b-41d4-a716-446655440000",
    "email": "user@example.com",
    "name": "John Doe"
  }
}
```

**Response Headers**:
```http
Set-Cookie: session_token=<JWT_TOKEN>; HttpOnly; Secure; SameSite=Lax; Path=/; Max-Age=604800
```

**Cookie Attributes**:
- `HttpOnly`: True (prevent XSS access)
- `Secure`: True (HTTPS only in production)
- `SameSite`: Lax (CSRF protection)
- `Max-Age`: 604800 seconds (7 days) or 2592000 seconds (30 days with remember_me)
- `Path`: / (available for all routes)

**Error Responses**:

**400 Bad Request** - Missing fields:
```json
{
  "detail": "Email and password are required"
}
```

**401 Unauthorized** - Invalid credentials:
```json
{
  "detail": "Invalid email or password"
}
```

**429 Too Many Requests** - Rate limit exceeded:
```json
{
  "detail": "Too many login attempts. Please try again later."
}
```

**Rate Limiting**:
- Max 5 login attempts per IP per minute
- Response: 429 Too Many Requests
- Retry after: 60 seconds

**Example Usage**:
```bash
curl -X POST http://localhost:8000/api/auth/signin \
  -H "Content-Type: application/json" \
  -c cookies.txt \
  -d '{
    "email": "user@example.com",
    "password": "securepass123",
    "remember_me": true
  }'
```

---

### POST /api/auth/signout

**Description**: Logout current user and clear session cookie.

**Authentication**: Required (session token)

**Request Headers**:
```http
Cookie: session_token=<TOKEN>
```

**Request Body**: None (empty)

**Success Response (204 No Content)**:
No response body.

**Response Headers**:
```http
Set-Cookie: session_token=; HttpOnly; Secure; SameSite=Lax; Path=/; Max-Age=0
```

**Error Responses**:

**401 Unauthorized** - No session or invalid session:
```json
{
  "detail": "Not authenticated"
}
```

**Example Usage**:
```bash
curl -X POST http://localhost:8000/api/auth/signout \
  -b cookies.txt \
  -c cookies.txt
```

---

### GET /api/auth/me

**Description**: Get currently authenticated user's profile.

**Authentication**: Required (session token)

**Request Headers**:
```http
Cookie: session_token=<TOKEN>
```

**Success Response (200 OK)**:
```json
{
  "id": "550e8400-e29b-41d4-a716-446655440000",
  "email": "user@example.com",
  "name": "John Doe",
  "email_verified": false,
  "created_at": "2025-12-26T10:00:00Z"
}
```

**Response Schema**:
```typescript
interface UserRead {
  id: string;
  email: string;
  name: string | null;
  email_verified: boolean;
  created_at: string;
}
```

**Error Responses**:

**401 Unauthorized** - No session, invalid token, or expired token:
```json
{
  "detail": "Not authenticated"
}
```

**401 Unauthorized** - Expired session:
```json
{
  "detail": "Session expired. Please log in again."
}
```

**Example Usage**:
```bash
curl -X GET http://localhost:8000/api/auth/me \
  -b cookies.txt
```

---

## Authentication Flow

### Registration Flow
```
User Input (email, password)
       ↓
POST /api/auth/signup
       ↓
Validate email format & uniqueness
       ↓
Hash password (bcrypt, cost factor 12)
       ↓
Create user in database
       ↓
Return user object (201 Created)
       ↓
Redirect to /auth/signin
```

### Login Flow
```
User Input (email, password)
       ↓
POST /api/auth/signin
       ↓
Find user by email (case-insensitive)
       ↓
Verify password (bcrypt compare)
       ↓
Generate JWT session token
       ↓
Store session in database
       ↓
Set httpOnly cookie with token
       ↓
Return user object (200 OK)
       ↓
Redirect to /tasks
```

### Session Validation Flow
```
Request to protected endpoint
       ↓
Extract session_token from cookie
       ↓
Decode JWT token
       ↓
Check if session exists in database
       ↓
Check if session expired (expires_at > now)
       ↓
If valid: Allow request + attach user to context
If invalid: Return 401 Unauthorized
```

### Logout Flow
```
POST /api/auth/signout
       ↓
Extract session_token from cookie
       ↓
Delete session from database
       ↓
Clear session_token cookie (Max-Age=0)
       ↓
Return 204 No Content
       ↓
Redirect to /auth/signin
```

---

## Security Considerations

### Password Security
- ✅ Passwords hashed with bcrypt (cost factor 12)
- ✅ Never stored in plaintext
- ✅ Never logged (use `SecretStr` in Pydantic)
- ✅ Never exposed in API responses

### Session Security
- ✅ Tokens stored in httpOnly cookies (prevent XSS)
- ✅ Secure flag enabled in production (HTTPS only)
- ✅ SameSite=Lax prevents CSRF attacks
- ✅ Session expiry enforced (7 or 30 days)
- ✅ Expired sessions auto-deleted via background job

### Rate Limiting
- ✅ 5 login attempts per IP per minute
- ✅ 429 Too Many Requests response
- ✅ Prevents brute-force attacks

### Error Messages
- ✅ "Invalid email or password" (identical for both cases)
- ✅ Prevents user enumeration attacks
- ✅ No specific "User not found" or "Wrong password" messages

---

## Database Operations

### Signup
```sql
INSERT INTO users (id, email, email_verified, name, hashed_password, created_at, updated_at)
VALUES ($1, $2, false, $3, $4, now(), now())
ON CONFLICT (email) DO NOTHING
RETURNING id, email, name, email_verified, created_at;
```

### Signin
```sql
-- Find user
SELECT id, email, name, hashed_password FROM users
WHERE email = lower($1);

-- Create session
INSERT INTO sessions (id, user_id, token, expires_at, ip_address, user_agent, created_at)
VALUES ($1, $2, $3, $4, $5, $6, now());
```

### Signout
```sql
DELETE FROM sessions
WHERE token = $1;
```

### Get Current User
```sql
-- Validate session
SELECT user_id, expires_at FROM sessions
WHERE token = $1
  AND expires_at > now();

-- Get user
SELECT id, email, name, email_verified, created_at FROM users
WHERE id = $2;
```

---

## Frontend Integration

### React Hook Example

```typescript
// frontend/lib/auth.ts
export async function signup(email: string, password: string, name?: string) {
  const response = await fetch(`${API_URL}/api/auth/signup`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ email, password, name }),
  });

  if (!response.ok) {
    const error = await response.json();
    throw new Error(error.detail);
  }

  return response.json();
}

export async function signin(email: string, password: string, rememberMe: boolean = false) {
  const response = await fetch(`${API_URL}/api/auth/signin`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ email, password, remember_me: rememberMe }),
    credentials: 'include', // IMPORTANT: Send cookies
  });

  if (!response.ok) {
    const error = await response.json();
    throw new Error(error.detail);
  }

  return response.json();
}

export async function signout() {
  const response = await fetch(`${API_URL}/api/auth/signout`, {
    method: 'POST',
    credentials: 'include',
  });

  if (!response.ok) {
    const error = await response.json();
    throw new Error(error.detail);
  }
}

export async function getCurrentUser() {
  const response = await fetch(`${API_URL}/api/auth/me`, {
    credentials: 'include',
  });

  if (!response.ok) return null;
  return response.json();
}
```

---

## Testing Checklist

### Unit Tests
- ✅ Password hashing function
- ✅ Password verification function
- ✅ JWT token generation and validation
- ✅ Email normalization (lowercase)

### Integration Tests
- ✅ Signup with valid data → 201 Created
- ✅ Signup with duplicate email → 409 Conflict
- ✅ Signup with invalid email → 400 Bad Request
- ✅ Signup with short password → 400 Bad Request
- ✅ Signin with correct credentials → 200 OK + cookie
- ✅ Signin with wrong password → 401 Unauthorized
- ✅ Signin with non-existent email → 401 Unauthorized
- ✅ Signin with 6+ attempts → 429 Too Many Requests
- ✅ Signout → 204 No Content + cookie cleared
- ✅ Get current user with valid session → 200 OK
- ✅ Get current user with invalid session → 401 Unauthorized
- ✅ Get current user with expired session → 401 Unauthorized

### Security Tests
- ✅ Session cookie has httpOnly flag
- ✅ Session cookie has secure flag (production)
- ✅ Session cookie has SameSite=Lax
- ✅ Password never logged or exposed
- ✅ Error messages don't reveal user existence

---

**Status**: ✅ Complete
**Next**: Task CRUD API contract
