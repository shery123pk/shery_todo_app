# API Contract: Authentication & User Management

**Feature**: 001-project-management-system
**Resource Group**: /api/auth
**Date**: 2025-12-27

---

## POST /api/auth/signup

**Purpose**: Create a new user account

**Authentication**: None (public endpoint)

**Request**:
```json
{
  "email": "alice@example.com",
  "password": "SecurePass123!",
  "full_name": "Alice Johnson"
}
```

**Request Schema**:
| Field | Type | Required | Constraints |
|-------|------|----------|-------------|
| email | string | Yes | Valid email, lowercase, unique |
| password | string | Yes | Min 8 chars, 1 number or special char |
| full_name | string | Yes | 1-100 characters |

**Response** (201 Created):
```json
{
  "id": "550e8400-e29b-41d4-a716-446655440000",
  "email": "alice@example.com",
  "full_name": "Alice Johnson",
  "email_verified": false,
  "created_at": "2025-12-27T10:00:00Z"
}
```

**Error Responses**:
- 400 Bad Request: Invalid input (validation errors)
  ```json
  {"detail": "Email already registered"}
  ```
- 422 Unprocessable Entity: Validation errors
  ```json
  {
    "detail": [
      {"loc": ["body", "password"], "msg": "Password must be at least 8 characters"}
    ]
  }
  ```

---

## POST /api/auth/signin

**Purpose**: Authenticate user and create session

**Authentication**: None (public endpoint)

**Request**:
```json
{
  "email": "alice@example.com",
  "password": "SecurePass123!",
  "remember_me": false
}
```

**Request Schema**:
| Field | Type | Required | Constraints |
|-------|------|----------|-------------|
| email | string | Yes | Valid email |
| password | string | Yes | Any string |
| remember_me | boolean | No | Default: false |

**Response** (200 OK):
```json
{
  "user": {
    "id": "550e8400-e29b-41d4-a716-446655440000",
    "email": "alice@example.com",
    "full_name": "Alice Johnson",
    "email_verified": true
  },
  "session_expires_at": "2026-01-03T10:00:00Z"
}
```

**Headers Set**:
- `Set-Cookie`: `session_token=<jwt>; HttpOnly; Secure; SameSite=Lax; Max-Age=<seconds>`

**Session Duration**:
- `remember_me=false`: 7 days
- `remember_me=true`: 30 days

**Error Responses**:
- 401 Unauthorized: Invalid credentials
  ```json
  {"detail": "Invalid email or password"}
  ```
- 403 Forbidden: Email not verified
  ```json
  {"detail": "Email not verified. Check your inbox."}
  ```

---

## POST /api/auth/signout

**Purpose**: Invalidate current session

**Authentication**: Required (JWT cookie)

**Request**: None (empty body)

**Response** (204 No Content): Empty response

**Headers Set**:
- `Set-Cookie`: `session_token=; HttpOnly; Secure; SameSite=Lax; Max-Age=0` (clear cookie)

**Error Responses**:
- 401 Unauthorized: No valid session

---

## GET /api/auth/me

**Purpose**: Get current user profile

**Authentication**: Required (JWT cookie)

**Response** (200 OK):
```json
{
  "id": "550e8400-e29b-41d4-a716-446655440000",
  "email": "alice@example.com",
  "full_name": "Alice Johnson",
  "avatar_url": "https://example.com/avatar.jpg",
  "email_verified": true,
  "timezone": "America/New_York",
  "language": "en",
  "created_at": "2025-12-27T10:00:00Z"
}
```

**Error Responses**:
- 401 Unauthorized: No valid session

---

## POST /api/auth/verify-email

**Purpose**: Verify user's email address

**Authentication**: None (token-based)

**Request**:
```json
{
  "token": "8f3e2c1a-9b7d-4e5f-a2c3-6d8e9f0a1b2c"
}
```

**Request Schema**:
| Field | Type | Required | Constraints |
|-------|------|----------|-------------|
| token | string (UUID) | Yes | Valid verification token |

**Response** (200 OK):
```json
{
  "message": "Email verified successfully"
}
```

**Error Responses**:
- 400 Bad Request: Invalid or expired token
  ```json
  {"detail": "Invalid or expired verification token"}
  ```

---

## POST /api/auth/forgot-password

**Purpose**: Request password reset

**Authentication**: None (public endpoint)

**Request**:
```json
{
  "email": "alice@example.com"
}
```

**Response** (200 OK):
```json
{
  "message": "Password reset email sent. Check your inbox."
}
```

**Note**: Always returns 200 OK even if email doesn't exist (security best practice to prevent email enumeration)

---

## POST /api/auth/reset-password

**Purpose**: Reset password with token

**Authentication**: None (token-based)

**Request**:
```json
{
  "token": "8f3e2c1a-9b7d-4e5f-a2c3-6d8e9f0a1b2c",
  "new_password": "NewSecurePass456!"
}
```

**Request Schema**:
| Field | Type | Required | Constraints |
|-------|------|----------|-------------|
| token | string (UUID) | Yes | Valid reset token (1-hour expiration) |
| new_password | string | Yes | Min 8 chars, 1 number or special char |

**Response** (200 OK):
```json
{
  "message": "Password reset successfully"
}
```

**Error Responses**:
- 400 Bad Request: Invalid or expired token
  ```json
  {"detail": "Invalid or expired reset token"}
  ```

---

## PUT /api/auth/profile

**Purpose**: Update user profile

**Authentication**: Required (JWT cookie)

**Request**:
```json
{
  "full_name": "Alice M. Johnson",
  "avatar_url": "https://example.com/new-avatar.jpg",
  "timezone": "Europe/London",
  "language": "en"
}
```

**Request Schema** (all fields optional):
| Field | Type | Required | Constraints |
|-------|------|----------|-------------|
| full_name | string | No | 1-100 characters |
| avatar_url | string | No | Valid URL or null |
| timezone | string | No | Valid IANA timezone |
| language | string | No | ISO 639-1 code |

**Response** (200 OK):
```json
{
  "id": "550e8400-e29b-41d4-a716-446655440000",
  "email": "alice@example.com",
  "full_name": "Alice M. Johnson",
  "avatar_url": "https://example.com/new-avatar.jpg",
  "timezone": "Europe/London",
  "language": "en",
  "updated_at": "2025-12-27T11:00:00Z"
}
```

**Error Responses**:
- 401 Unauthorized: No valid session
- 422 Unprocessable Entity: Validation errors

---

## PUT /api/auth/password

**Purpose**: Change password (authenticated)

**Authentication**: Required (JWT cookie)

**Request**:
```json
{
  "current_password": "SecurePass123!",
  "new_password": "NewSecurePass456!"
}
```

**Request Schema**:
| Field | Type | Required | Constraints |
|-------|------|----------|-------------|
| current_password | string | Yes | Must match current password |
| new_password | string | Yes | Min 8 chars, 1 number or special char |

**Response** (200 OK):
```json
{
  "message": "Password updated successfully"
}
```

**Error Responses**:
- 401 Unauthorized: Invalid current password
  ```json
  {"detail": "Current password is incorrect"}
  ```
- 422 Unprocessable Entity: Validation errors

---

## Authentication Flow

```
1. Signup:
   POST /api/auth/signup
   → Email sent with verification link
   → User receives email with token

2. Email Verification:
   POST /api/auth/verify-email {token}
   → email_verified = true

3. Signin:
   POST /api/auth/signin
   → Session created, JWT cookie set
   → Returns user + session info

4. Authenticated Requests:
   All requests include Cookie: session_token=<jwt>
   → Server validates JWT signature and expiration
   → Server checks session exists in DB and is not expired
   → Request proceeds with user context

5. Signout:
   POST /api/auth/signout
   → Session invalidated in DB
   → Cookie cleared

6. Forgot Password:
   POST /api/auth/forgot-password {email}
   → Email sent with reset link
   → User receives email with token

7. Reset Password:
   POST /api/auth/reset-password {token, new_password}
   → Password updated
   → User can signin with new password
```

---

## Security Considerations

1. **Password Hashing**: bcrypt with cost factor 12
2. **Session Tokens**: JWT signed with HS256, stored as HttpOnly cookies
3. **CSRF Protection**: SameSite=Lax cookies + double-submit cookie pattern
4. **Rate Limiting**:
   - `/api/auth/signin`: 5 attempts per 15 minutes per IP
   - `/api/auth/signup`: 3 attempts per hour per IP
   - `/api/auth/forgot-password`: 3 attempts per hour per email
5. **Email Verification**: Required before full account access
6. **Token Expiration**:
   - Email verification tokens: 24 hours
   - Password reset tokens: 1 hour
   - Session tokens: 7 days (default) or 30 days (remember_me)
