# ADR-004: Authentication Strategy - Better Auth

**Status:** Accepted
**Date:** 2025-12-26
**Deciders:** Architect (shery123pk), AI Developer (Claude)
**Related Phase:** Phase 2 - Full-Stack Web
**Supersedes:** N/A (Phase 1 had no authentication)

---

## Context and Problem Statement

Phase 2 requires user authentication to support multi-user todo lists. Users must be able to:
- Sign up with email/password
- Sign in securely
- Access only their own tasks
- Log out safely

**Key Questions:**
1. Build custom auth or use a library/service?
2. Which auth provider/library best fits our stack?
3. Session-based or token-based (JWT)?
4. How to integrate with FastAPI + Next.js?
5. What about social logins (Google, GitHub)?

---

## Decision Drivers

### Must Have
- ✅ **Constitution Mandate:** Better Auth specified in tech stack
- ✅ **Next.js Integration:** Works seamlessly with Next.js 15 App Router
- ✅ **Email/Password:** Basic auth flow
- ✅ **Session Management:** Secure, HttpOnly cookies
- ✅ **Type Safety:** TypeScript support

### Should Have
- 🎯 **Social Logins:** Google, GitHub OAuth
- 🎯 **Email Verification:** Confirm user emails
- 🎯 **Password Reset:** Forgot password flow
- 🎯 **2FA Support:** Two-factor authentication (future)
- 🎯 **Good DX:** Easy setup, clear documentation

### Nice to Have
- 💡 **Magic Links:** Passwordless authentication
- 💡 **Role-Based Access:** Admin vs user roles
- 💡 **Session Analytics:** Login history, device tracking

---

## Considered Options

### Option 1: Better Auth ✅ SELECTED

**Provider:** https://www.better-auth.com
**Type:** TypeScript-first authentication library

**Pros:**
- ✅ **Constitution Compliant:** Explicitly mandated
- ✅ **Type-Safe:** Full TypeScript support with inference
- ✅ **Framework Agnostic:** Works with any backend (FastAPI + adapter)
- ✅ **Database Agnostic:** Works with PostgreSQL, MySQL, SQLite
- ✅ **Session-Based:** Secure HttpOnly cookies (no JWT vulnerabilities)
- ✅ **Social Providers:** 50+ OAuth providers (Google, GitHub, etc.)
- ✅ **Modern DX:** Intuitive API, great docs
- ✅ **Plugins:** Email verification, 2FA, magic links

**Cons:**
- ⚠️ **Newer Library:** Less mature than NextAuth/Auth.js (founded 2024)
- ⚠️ **Python Integration:** Need to create Python adapter for FastAPI
- ⚠️ **Smaller Community:** Fewer Stack Overflow answers

**Example:**
```typescript
// frontend/lib/auth-client.ts
import { createAuthClient } from "better-auth/react"

export const authClient = createAuthClient({
  baseURL: "http://localhost:8000"
})

// Usage
await authClient.signIn.email({
  email: "user@example.com",
  password: "securepassword"
})
```

### Option 2: NextAuth.js / Auth.js

**Provider:** https://authjs.dev
**Type:** Authentication for Next.js

**Pros:**
- ✅ **Mature:** Industry standard, used by thousands
- ✅ **Next.js Native:** Built specifically for Next.js
- ✅ **Social Providers:** 50+ providers
- ✅ **Database Adapters:** PostgreSQL, MySQL, MongoDB
- ✅ **Large Community:** Extensive docs, tutorials

**Cons:**
- ❌ **Not Constitution Mandated:** Better Auth is specified
- ❌ **Next.js Specific:** Harder to integrate with FastAPI backend
- ❌ **Adapter Pattern:** More complex setup for custom backends

### Option 3: Clerk

**Provider:** https://clerk.com
**Type:** Managed authentication service

**Pros:**
- ✅ **Full-Featured:** Auth + user management + UI components
- ✅ **Beautiful UI:** Pre-built sign-in/sign-up components
- ✅ **Multi-Tenant:** Organizations, teams
- ✅ **Great DX:** Excellent documentation

**Cons:**
- ❌ **Not Constitution Mandated:** Better Auth is specified
- ❌ **Vendor Lock-in:** Hosted service, not self-hosted
- ❌ **Cost:** Free tier limited (10K MAUs), then $25/month
- ❌ **Privacy:** User data stored on Clerk's servers

### Option 4: Supabase Auth

**Provider:** https://supabase.com/auth
**Type:** Part of Supabase BaaS

**Pros:**
- ✅ **Full-Featured:** Auth + database + storage
- ✅ **Row Level Security:** PostgreSQL RLS policies
- ✅ **Social Providers:** Many OAuth providers

**Cons:**
- ❌ **Not Constitution Mandated:** Better Auth is specified
- ❌ **Tied to Supabase:** Can't use with Neon PostgreSQL easily
- ❌ **BaaS Lock-in:** Vendor-specific features

### Option 5: Custom Auth (Roll Your Own)

**Type:** Build from scratch with FastAPI + Next.js

**Pros:**
- ✅ **Full Control:** Complete customization
- ✅ **Learning:** Understand auth internals

**Cons:**
- ❌ **Security Risks:** Easy to make mistakes (password hashing, session management)
- ❌ **Time-Consuming:** 2-3 weeks to build properly
- ❌ **Maintenance:** Ongoing security patches
- ❌ **Not Constitution Mandated:** Better Auth is specified
- ❌ **Missing Features:** No social logins, 2FA, etc.

---

## Decision Outcome

**Chosen Option:** **Better Auth** ✅

### Rationale

1. **Constitution Compliance:** Explicitly mandated in tech stack
2. **Type Safety:** Full TypeScript support throughout
3. **Flexibility:** Works with FastAPI backend (with adapter)
4. **Modern Architecture:** Session-based auth (more secure than JWT)
5. **Future-Proof:** Plugins for 2FA, magic links, etc.

**Trade-off Accepted:** Need to create Python adapter for FastAPI, but this aligns with learning goals and provides full control.

---

## Implementation

### Architecture

```
┌─────────────┐        ┌─────────────┐        ┌─────────────┐
│  Next.js    │        │   FastAPI   │        │    Neon     │
│  Frontend   │◄──────►│   Backend   │◄──────►│ PostgreSQL  │
│             │        │             │        │             │
│ Better Auth │  HTTP  │ Auth Routes │  SQL   │ users table │
│   Client    │        │  + Adapter  │        │sessions tbl │
└─────────────┘        └─────────────┘        └─────────────┘
```

### Database Schema

**PostgreSQL Tables (auto-created by Better Auth):**
```sql
CREATE TABLE users (
    id UUID PRIMARY KEY,
    email VARCHAR(255) UNIQUE NOT NULL,
    email_verified BOOLEAN DEFAULT FALSE,
    name VARCHAR(255),
    image TEXT,
    created_at TIMESTAMP DEFAULT NOW(),
    updated_at TIMESTAMP DEFAULT NOW()
);

CREATE TABLE sessions (
    id UUID PRIMARY KEY,
    user_id UUID REFERENCES users(id) ON DELETE CASCADE,
    expires_at TIMESTAMP NOT NULL,
    token VARCHAR(255) UNIQUE NOT NULL,
    ip_address INET,
    user_agent TEXT
);

CREATE TABLE accounts (
    id UUID PRIMARY KEY,
    user_id UUID REFERENCES users(id) ON DELETE CASCADE,
    provider VARCHAR(50) NOT NULL,  -- 'email', 'google', 'github'
    provider_account_id VARCHAR(255),
    access_token TEXT,
    refresh_token TEXT,
    expires_at TIMESTAMP
);
```

### Backend Setup (FastAPI)

**backend/app/auth.py:**
```python
from fastapi import FastAPI, Request, Response
from fastapi.responses import JSONResponse
import httpx

app = FastAPI()

# Better Auth configuration
BETTER_AUTH_CONFIG = {
    "database": {
        "type": "postgres",
        "url": os.getenv("DATABASE_URL")
    },
    "email_password": {
        "enabled": True,
        "require_email_verification": True
    },
    "social_providers": {
        "google": {
            "client_id": os.getenv("GOOGLE_CLIENT_ID"),
            "client_secret": os.getenv("GOOGLE_CLIENT_SECRET")
        },
        "github": {
            "client_id": os.getenv("GITHUB_CLIENT_ID"),
            "client_secret": os.getenv("GITHUB_CLIENT_SECRET")
        }
    },
    "session": {
        "expires_in": 60 * 60 * 24 * 30,  # 30 days
        "update_age": 60 * 60 * 24  # Update session every 24 hours
    }
}

# Auth routes (proxy to Better Auth TypeScript server)
@app.post("/api/auth/signup")
async def signup(request: Request):
    """Create new user account."""
    # Implementation: Call Better Auth TypeScript server
    pass

@app.post("/api/auth/signin")
async def signin(request: Request, response: Response):
    """Sign in user."""
    # Implementation: Set session cookie
    pass

@app.post("/api/auth/signout")
async def signout(response: Response):
    """Sign out user."""
    # Implementation: Clear session cookie
    pass

@app.get("/api/auth/session")
async def get_session(request: Request):
    """Get current session."""
    # Implementation: Verify session token
    pass
```

### Frontend Setup (Next.js)

**frontend/lib/auth.ts:**
```typescript
import { betterAuth } from "better-auth/client"
import { inferAdditionalFields } from "better-auth/client/plugins"

export const authClient = betterAuth({
  baseURL: process.env.NEXT_PUBLIC_API_URL,
  plugins: [
    inferAdditionalFields({
      user: {
        name: {
          type: "string",
          required: false
        }
      }
    })
  ]
})

// Type-safe exports
export const {
  signIn,
  signUp,
  signOut,
  useSession
} = authClient
```

**frontend/app/auth/signin/page.tsx:**
```typescript
"use client"

import { useState } from "react"
import { useRouter } from "next/navigation"
import { signIn } from "@/lib/auth"

export default function SignInPage() {
  const [email, setEmail] = useState("")
  const [password, setPassword] = useState("")
  const router = useRouter()

  const handleSignIn = async () => {
    try {
      await signIn.email({ email, password })
      router.push("/tasks")
    } catch (error) {
      console.error("Sign in failed:", error)
    }
  }

  return (
    <form onSubmit={(e) => { e.preventDefault(); handleSignIn() }}>
      <input
        type="email"
        placeholder="Email"
        value={email}
        onChange={(e) => setEmail(e.target.value)}
      />
      <input
        type="password"
        placeholder="Password"
        value={password}
        onChange={(e) => setPassword(e.target.value)}
      />
      <button type="submit">Sign In</button>
    </form>
  )
}
```

### Protected Routes

**Middleware (Next.js):**
```typescript
// frontend/middleware.ts
import { NextResponse } from "next/server"
import type { NextRequest } from "next/server"
import { authClient } from "@/lib/auth"

export async function middleware(request: NextRequest) {
  const session = await authClient.getSession({
    fetchOptions: {
      headers: request.headers
    }
  })

  if (!session) {
    return NextResponse.redirect(new URL("/auth/signin", request.url))
  }

  return NextResponse.next()
}

export const config = {
  matcher: ["/tasks/:path*", "/profile/:path*"]
}
```

**Dependency Injection (FastAPI):**
```python
# backend/app/dependencies.py
from fastapi import Depends, HTTPException, Request
from typing import Annotated

async def get_current_user(request: Request) -> dict:
    """Get current authenticated user from session."""
    session_token = request.cookies.get("better-auth.session_token")

    if not session_token:
        raise HTTPException(status_code=401, detail="Not authenticated")

    # Verify session with Better Auth
    # Return user object
    return {"id": "...", "email": "..."}

CurrentUser = Annotated[dict, Depends(get_current_user)]

# Usage in routes
@app.get("/api/tasks")
async def get_tasks(user: CurrentUser):
    """Get tasks for authenticated user."""
    return {"tasks": [...]}
```

---

## Consequences

### Positive
- ✅ **Type Safety:** TypeScript inference throughout auth flow
- ✅ **Security:** Session-based auth more secure than JWT
- ✅ **Flexibility:** Can customize auth flows as needed
- ✅ **Social Logins:** Easy to add Google, GitHub, etc.
- ✅ **Modern Stack:** Aligns with Next.js 15 best practices
- ✅ **Constitution Compliant:** Follows mandated tech stack

### Negative
- ⚠️ **Python Adapter:** Need to build FastAPI integration
  - **Mitigation:** Can reuse TypeScript Better Auth server as microservice
- ⚠️ **Newer Library:** Less community support than NextAuth
  - **Mitigation:** Good documentation, active Discord community
- ⚠️ **Learning Curve:** New library to learn
  - **Mitigation:** Excellent docs, clear examples

### Neutral
- 🔄 **Email Service Required:** Need SMTP for email verification
  - **Options:** Resend, SendGrid, AWS SES (Resend recommended)

---

## Social Login Setup

### Google OAuth

1. **Google Cloud Console:**
   - Create OAuth 2.0 credentials
   - Authorized redirect URI: `https://your-domain.com/api/auth/callback/google`

2. **Environment Variables:**
   ```bash
   GOOGLE_CLIENT_ID=your-client-id
   GOOGLE_CLIENT_SECRET=your-client-secret
   ```

3. **Better Auth Config:**
   ```typescript
   socialProviders: {
     google: {
       clientId: process.env.GOOGLE_CLIENT_ID,
       clientSecret: process.env.GOOGLE_CLIENT_SECRET
     }
   }
   ```

### GitHub OAuth

1. **GitHub Settings:**
   - Create OAuth App
   - Callback URL: `https://your-domain.com/api/auth/callback/github`

2. **Environment Variables:**
   ```bash
   GITHUB_CLIENT_ID=your-client-id
   GITHUB_CLIENT_SECRET=your-client-secret
   ```

---

## Email Service (For Verification)

**Recommended:** Resend (https://resend.com)

**Why Resend:**
- ✅ Modern API, great DX
- ✅ Free tier: 100 emails/day
- ✅ Official Better Auth integration
- ✅ Built for developers

**Setup:**
```typescript
// Better Auth config
emailAndPassword: {
  enabled: true,
  requireEmailVerification: true,
  sendVerificationEmail: async ({ user, url }) => {
    const { Resend } = await import("resend")
    const resend = new Resend(process.env.RESEND_API_KEY)

    await resend.emails.send({
      from: "noreply@your-domain.com",
      to: user.email,
      subject: "Verify your email",
      html: `<p>Click <a href="${url}">here</a> to verify your email.</p>`
    })
  }
}
```

---

## Security Considerations

### Password Requirements

```typescript
// Better Auth validation
password: {
  minLength: 8,
  requireUppercase: true,
  requireLowercase: true,
  requireNumbers: true,
  requireSpecialChars: true
}
```

### Session Security

- **HttpOnly Cookies:** Prevent XSS attacks
- **Secure Flag:** HTTPS only in production
- **SameSite:** CSRF protection
- **Expiration:** Auto-expire after 30 days

### Rate Limiting

```python
# FastAPI rate limiting
from slowapi import Limiter, _rate_limit_exceeded_handler
from slowapi.util import get_remote_address

limiter = Limiter(key_func=get_remote_address)

@app.post("/api/auth/signin")
@limiter.limit("5/minute")  # Max 5 attempts per minute
async def signin(request: Request):
    pass
```

---

## Testing Strategy

### Unit Tests

```typescript
// Test auth client
import { describe, it, expect } from "vitest"
import { authClient } from "@/lib/auth"

describe("Better Auth", () => {
  it("should sign up user", async () => {
    const result = await authClient.signUp.email({
      email: "test@example.com",
      password: "SecurePass123!"
    })
    expect(result.user).toBeDefined()
  })
})
```

### Integration Tests

```python
# Test protected endpoints
def test_protected_route_requires_auth(client):
    response = client.get("/api/tasks")
    assert response.status_code == 401

def test_protected_route_with_auth(client, auth_user):
    response = client.get(
        "/api/tasks",
        cookies={"better-auth.session_token": auth_user.session_token}
    )
    assert response.status_code == 200
```

---

## Migration from Phase 1

**Phase 1 (No Auth):**
- All users see same tasks
- No user concept

**Phase 2 (With Auth):**
- Each user has their own tasks
- Tasks have `user_id` foreign key

**Migration Strategy:**
- Create default user for Phase 1 data
- Associate all existing tasks with default user
- Users can claim tasks or create new ones

---

## References

- **Better Auth Docs:** https://www.better-auth.com/docs
- **Better Auth GitHub:** https://github.com/better-auth/better-auth
- **FastAPI Security:** https://fastapi.tiangolo.com/tutorial/security/
- **Next.js Auth:** https://nextjs.org/docs/app/building-your-application/authentication

---

## Related ADRs

- **ADR-002:** Monorepo Structure (auth in /backend and /frontend)
- **ADR-003:** Database Choice (Neon PostgreSQL stores users/sessions)
- **Future ADR:** Email Service Choice (Resend vs alternatives)
- **Future ADR:** Phase 3 - MCP Tools authentication

---

**Decision Made By:** Architect + AI Developer
**Date Approved:** 2025-12-26
**Implementation Status:** 📋 Planned for Phase 2
**Review Date:** After Phase 2 implementation (validate DX and security)
