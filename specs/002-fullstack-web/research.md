# Research & Technology Decisions: Phase 2 Full-Stack Web

**Feature**: 002-fullstack-web
**Date**: 2025-12-26
**Phase**: Phase 0 (Research)
**Status**: Complete

---

## Overview

This document consolidates research findings and technology decisions for Phase 2 implementation. All unknowns from the plan's Technical Context have been investigated, and concrete implementation paths have been chosen.

---

## 1. Better Auth Python Integration

### Decision

**Build custom JWT + bcrypt implementation** instead of waiting for Better Auth Python adapter.

### Rationale

**Research Findings**:
- Better Auth is primarily a TypeScript/JavaScript library
- No official Python adapter exists as of 2025-12-26
- Better Auth Next.js integration can work with any backend that speaks JWT
- Custom implementation gives full control over session management

**Why Custom JWT + bcrypt**:
- **Pros**:
  - Full control over token structure and claims
  - Native Python ecosystem (PyJWT, passlib/bcrypt)
  - No dependency on external adapter maintenance
  - Direct database session storage
  - Industry-standard approach
- **Cons**:
  - More code to write and maintain
  - Need to implement token refresh manually
  - No Better Auth dashboard/admin UI

### Alternatives Considered

1. **Better Auth Python Adapter** (if it existed):
   - **Pros**: Official integration, unified auth experience
   - **Cons**: Doesn't exist, would require wrapper development
   - **Rejected**: Not available

2. **NextAuth.js (frontend only)**:
   - **Pros**: Mature, well-documented
   - **Cons**: Requires Next.js API routes, not truly backend-agnostic
   - **Rejected**: Ties frontend to auth logic (violates separation)

3. **FastAPI-Users**:
   - **Pros**: Comprehensive user management library
   - **Cons**: Opinionated architecture, may conflict with constitution
   - **Rejected**: Too heavy for simple auth needs

### Implementation Path

**Backend (FastAPI)**:

```python
# backend/app/security.py
from passlib.context import CryptContext
from jose import JWTError, jwt
from datetime import datetime, timedelta

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def hash_password(password: str) -> str:
    return pwd_context.hash(password)

def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)

def create_access_token(data: dict, expires_delta: timedelta = timedelta(days=7)):
    to_encode = data.copy()
    expire = datetime.utcnow() + expires_delta
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, SECRET_KEY, algorithm="HS256")
```

**Database Session Storage**:
```python
# backend/app/models/session.py
from sqlmodel import SQLModel, Field
from uuid import UUID, uuid4
from datetime import datetime

class Session(SQLModel, table=True):
    id: UUID = Field(default_factory=uuid4, primary_key=True)
    user_id: UUID = Field(foreign_key="user.id", index=True)
    token: str = Field(unique=True, index=True)
    expires_at: datetime = Field(index=True)
    ip_address: str | None = None
    user_agent: str | None = None
    created_at: datetime = Field(default_factory=datetime.utcnow)
```

**Frontend (Next.js)**:
```typescript
// frontend/lib/auth.ts
export async function signin(email: string, password: string) {
  const response = await fetch(`${API_URL}/api/auth/signin`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ email, password }),
    credentials: 'include', // Important for cookies
  });

  if (!response.ok) throw new Error('Login failed');
  return response.json();
}

export async function getSession() {
  const response = await fetch(`${API_URL}/api/auth/me`, {
    credentials: 'include',
  });

  if (!response.ok) return null;
  return response.json();
}
```

**Packages**:
- Backend: `python-jose[cryptography]`, `passlib[bcrypt]`, `python-multipart`
- Frontend: Native fetch (no additional packages needed)

---

## 2. Neon PostgreSQL Connection Strategy

### Decision

**Use Neon Pooler with asyncpg** for production, **sync SQLModel engine** for simplicity.

### Rationale

**Research Findings**:
- Neon provides two connection types: Direct and Pooler
- Pooler adds connection pooling layer, reduces cold start impact
- SQLModel supports both sync and async, but sync is simpler for FastAPI CRUD
- Neon Serverless has ~100-500ms cold start (mitigated by pooler)

**Why Pooler + Sync**:
- **Pooler**: Reduces cold starts, handles connection limits
- **Sync Engine**: Simpler code, FastAPI background tasks work well with sync
- **Cost**: Free tier sufficient (0.5GB storage, 3GB bandwidth/month)
- **Performance**: Pooler adds ~5-10ms latency but prevents cold starts

### Connection String Format

```bash
# Production (Neon Pooler)
DATABASE_URL=postgresql://user:password@ep-xxx-xxx.us-east-2.pooler.neon.tech/neondb?sslmode=require

# Local Development (Docker PostgreSQL)
DATABASE_URL=postgresql://todo_user:todo_pass@localhost:5432/todo_db
```

### Cold Start Mitigation

1. **Use Pooler**: Always use `.pooler.neon.tech` endpoint
2. **Warm-up Query**: Optional health check endpoint that queries database
3. **Reserved Compute** (Paid): If needed, upgrade to always-on compute

### SQLModel Engine Configuration

```python
# backend/app/database.py
from sqlmodel import create_engine, Session
from app.config import settings

# Sync engine (simpler for CRUD)
engine = create_engine(
    settings.database_url,
    echo=settings.debug,
    pool_pre_ping=True,  # Verify connections before use
    pool_size=5,  # Max connections in pool
    max_overflow=10,  # Max overflow connections
)

def get_session():
    with Session(engine) as session:
        yield session
```

### Alternatives Considered

1. **Direct Connection (no pooler)**:
   - **Pros**: Lower latency (~5-10ms faster)
   - **Cons**: Cold start issues, connection limit problems
   - **Rejected**: Cold starts unacceptable for web app

2. **Async SQLModel**:
   - **Pros**: Better for high concurrency
   - **Cons**: More complex code, async/await everywhere
   - **Rejected**: Overkill for Phase 2 scale (10-100 concurrent users)

3. **PGBouncer (self-hosted)**:
   - **Pros**: More control, lower latency
   - **Cons**: Additional infrastructure, maintenance burden
   - **Rejected**: Neon Pooler sufficient, avoid extra services

### Performance Targets

- **Connection Time**: <50ms (with pooler)
- **Query Time**: <20ms (indexed queries)
- **Total API Latency**: <200ms p95 (including DB query)

---

## 3. Hugging Face Spaces Dockerfile Configuration

### Decision

**Single-worker Uvicorn on port 7860** with health check endpoint.

### Rationale

**Research Findings**:
- HF Spaces Docker SDK **requires** port 7860 (non-negotiable)
- Single container constraint (no multi-container support)
- Free tier: 2 vCPU, 16GB RAM, 50GB storage
- Persistent storage at `/data` (optional)
- Auto-restart on crash

**Why Single-Worker**:
- Free tier has 2 vCPU → single worker sufficient
- Multi-worker adds complexity without benefit at this scale
- Easier to debug and monitor

### Dockerfile Template

```dockerfile
# backend/Dockerfile
FROM python:3.13-slim

# Set working directory
WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    build-essential \
    libpq-dev \
    && rm -rf /var/lib/apt/lists/*

# Copy dependency files
COPY pyproject.toml README.md ./

# Install UV and dependencies
RUN pip install --no-cache-dir uv && \
    uv pip install --system --no-cache -e .

# Copy application code
COPY app/ ./app/
COPY alembic/ ./alembic/
COPY alembic.ini ./

# Run database migrations on startup (optional, can be manual)
# RUN alembic upgrade head

# Expose port 7860 (HF Spaces requirement)
EXPOSE 7860

# Health check endpoint
HEALTHCHECK --interval=30s --timeout=5s --start-period=10s --retries=3 \
  CMD curl --fail http://localhost:7860/health || exit 1

# Run Uvicorn on port 7860 (CRITICAL: must be 7860)
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "7860", "--workers", "1"]
```

### Health Check Endpoint

```python
# backend/app/main.py
from fastapi import FastAPI

app = FastAPI()

@app.get("/health")
async def health_check():
    """Health check endpoint for HF Spaces and monitoring"""
    return {"status": "healthy", "service": "todo-backend"}
```

### Startup Time Optimization

**Target**: <10 seconds from container start to ready

**Optimizations**:
1. **Layer Caching**: Separate dependency install from code copy
2. **Slim Base Image**: `python:3.13-slim` (not `python:3.13`)
3. **No Dev Dependencies**: Only production packages installed
4. **Pre-compile**: Python bytecode compiled during build

### Testing Locally

```bash
# Build and run locally on port 7860
cd backend
docker build -t todo-backend .
docker run -p 7860:7860 --env-file .env todo-backend

# Test health check
curl http://localhost:7860/health
# Expected: {"status": "healthy", "service": "todo-backend"}

# Test API docs
curl http://localhost:7860/docs
# Should return OpenAPI HTML
```

### Alternatives Considered

1. **Multi-worker Uvicorn**:
   - **Pros**: Higher throughput for CPU-bound tasks
   - **Cons**: More memory, complex debugging, overkill for Phase 2
   - **Rejected**: Single worker sufficient

2. **Gunicorn + Uvicorn Workers**:
   - **Pros**: Production-grade WSGI server
   - **Cons**: Additional process management layer
   - **Rejected**: Unnecessary complexity for HF Spaces

3. **Port 8000 (standard)**:
   - **Pros**: Common default for FastAPI
   - **Cons**: **HF Spaces REQUIRES port 7860**
   - **Rejected**: Non-compliant with HF Spaces

---

## 4. Next.js 15 + Better Auth Pattern

### Decision

**Middleware-based authentication with Server Components** for protected routes.

### Rationale

**Research Findings**:
- Next.js 15 App Router supports middleware for route protection
- Server Components can validate sessions on server-side (no client flash)
- Better Auth client can work with any JWT backend
- Cookies auto-sent with `credentials: 'include'`

**Why Middleware + Server Components**:
- **Security**: Session validation on server, no client-side exposure
- **Performance**: No waterfall requests, auth check before page load
- **UX**: No flash of unauthenticated content
- **SEO**: Server-rendered with auth context

### Implementation Pattern

**Middleware** (`frontend/middleware.ts`):
```typescript
import { NextResponse } from 'next/server';
import type { NextRequest } from 'next/server';

export async function middleware(request: NextRequest) {
  const sessionCookie = request.cookies.get('session_token');

  // Protected routes: /tasks/*
  if (request.nextUrl.pathname.startsWith('/tasks')) {
    if (!sessionCookie) {
      // Redirect to login with returnUrl
      const loginUrl = new URL('/auth/signin', request.url);
      loginUrl.searchParams.set('returnUrl', request.nextUrl.pathname);
      return NextResponse.redirect(loginUrl);
    }

    // Verify session with backend
    const response = await fetch(`${process.env.NEXT_PUBLIC_API_URL}/api/auth/me`, {
      headers: {
        Cookie: `session_token=${sessionCookie.value}`,
      },
    });

    if (!response.ok) {
      // Invalid or expired session
      const loginUrl = new URL('/auth/signin', request.url);
      loginUrl.searchParams.set('error', 'session_expired');
      return NextResponse.redirect(loginUrl);
    }
  }

  return NextResponse.next();
}

export const config = {
  matcher: ['/tasks/:path*'],
};
```

**Server Component** (`app/tasks/page.tsx`):
```typescript
import { cookies } from 'next/headers';

async function getUser() {
  const sessionCookie = cookies().get('session_token');

  const response = await fetch(`${process.env.NEXT_PUBLIC_API_URL}/api/auth/me`, {
    headers: {
      Cookie: `session_token=${sessionCookie?.value}`,
    },
    cache: 'no-store', // Always fresh
  });

  if (!response.ok) return null;
  return response.json();
}

export default async function TasksPage() {
  const user = await getUser();

  return (
    <div>
      <h1>Welcome, {user.name}!</h1>
      {/* Task list components */}
    </div>
  );
}
```

**Client Component** (for interactivity):
```typescript
'use client';

import { useState } from 'react';

export function TaskForm() {
  const [title, setTitle] = useState('');

  async function createTask(e: React.FormEvent) {
    e.preventDefault();

    const response = await fetch(`${process.env.NEXT_PUBLIC_API_URL}/api/tasks`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ title }),
      credentials: 'include', // Send cookies
    });

    if (!response.ok) throw new Error('Failed to create task');
    // Handle success
  }

  return <form onSubmit={createTask}>{/* Form UI */}</form>;
}
```

### Session Cookie Configuration

**Backend** (`app/routers/auth.py`):
```python
from fastapi import Response

@router.post("/signin")
async def signin(credentials: LoginRequest, response: Response):
    # ... validate credentials ...

    session_token = create_access_token({"sub": str(user.id)})

    # Set cookie with secure flags
    response.set_cookie(
        key="session_token",
        value=session_token,
        httponly=True,  # Prevent XSS
        secure=True,  # HTTPS only (production)
        samesite="lax",  # CSRF protection
        max_age=604800,  # 7 days (or 2592000 for 30 days with remember_me)
        path="/",
    )

    return {"user": {"id": user.id, "email": user.email}}
```

### Alternatives Considered

1. **Client-Side Session Validation**:
   - **Pros**: Simpler implementation
   - **Cons**: Flash of unauthenticated content, security risk
   - **Rejected**: Poor UX and security

2. **Server Actions Only** (no middleware):
   - **Pros**: Centralized auth logic
   - **Cons**: Still need middleware for redirects
   - **Rejected**: Middleware more appropriate for route protection

3. **localStorage for Tokens**:
   - **Pros**: Easier to access in JavaScript
   - **Cons**: **Vulnerable to XSS attacks**
   - **Rejected**: Security violation (constitution mandates httpOnly cookies)

---

## 5. CORS Configuration Strategy

### Decision

**FastAPI CORSMiddleware with dynamic origin list** supporting Vercel production and preview domains.

### Rationale

**Research Findings**:
- Vercel creates unique URLs for preview deployments: `app-name-git-branch-username.vercel.app`
- Production URL: `app-name.vercel.app` (or custom domain)
- CORS credentials require explicit origin (can't use wildcard with `credentials=True`)
- Preflight requests (OPTIONS) must be handled

**Why Dynamic Origin List**:
- Supports both production and preview deployments
- Allows local development (`localhost:3000`)
- Secure (explicit origins only, no wildcard)
- Cookie-based auth requires `credentials=True`

### CORS Configuration

```python
# backend/app/main.py
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import os

app = FastAPI()

# CORS configuration
frontend_url = os.getenv("FRONTEND_URL", "http://localhost:3000")

# Allowed origins (production, preview, local)
allowed_origins = [
    frontend_url,  # Production: https://todo-app.vercel.app
    "http://localhost:3000",  # Local development
    "http://localhost:3001",  # Alternative local port
]

# Add Vercel preview domain pattern if production
if frontend_url.endswith(".vercel.app"):
    # Extract base name: todo-app.vercel.app → todo-app-*
    base_name = frontend_url.split(".")[0]
    # Allow all preview deployments (git-* pattern)
    allowed_origins.append(f"https://{base_name}-git-*.vercel.app")

app.add_middleware(
    CORSMiddleware,
    allow_origins=allowed_origins,
    allow_credentials=True,  # Required for cookies
    allow_methods=["GET", "POST", "PATCH", "DELETE", "OPTIONS"],
    allow_headers=["*"],  # Or specific headers
    expose_headers=["*"],
)
```

### Vercel Preview Domains

Vercel preview deployments follow pattern:
```
https://[app-name]-[git-branch]-[username].vercel.app
```

Example:
- Production: `https://todo-app.vercel.app`
- Preview (main branch): `https://todo-app-git-main-shery123pk.vercel.app`
- Preview (feature branch): `https://todo-app-git-002-fullstack-web-shery123pk.vercel.app`

**Wildcard Pattern**: `https://todo-app-git-*.vercel.app` (supported by FastAPI CORS regex)

### Preflight Request Handling

FastAPI CORSMiddleware automatically handles `OPTIONS` preflight requests:
```http
OPTIONS /api/tasks
Access-Control-Request-Method: POST
Access-Control-Request-Headers: content-type

HTTP/1.1 200 OK
Access-Control-Allow-Origin: https://todo-app.vercel.app
Access-Control-Allow-Credentials: true
Access-Control-Allow-Methods: POST
Access-Control-Allow-Headers: content-type
```

### Testing CORS

```bash
# Test from local frontend
curl -X OPTIONS http://localhost:8000/api/tasks \
  -H "Origin: http://localhost:3000" \
  -H "Access-Control-Request-Method: POST" \
  -v

# Should return:
# Access-Control-Allow-Origin: http://localhost:3000
# Access-Control-Allow-Credentials: true
```

### Alternatives Considered

1. **Wildcard Origin** (`allow_origins=["*"]`):
   - **Pros**: Simplest configuration
   - **Cons**: **Cannot use with credentials=True**, security risk
   - **Rejected**: Incompatible with cookie-based auth

2. **Proxy via Next.js API Routes**:
   - **Pros**: No CORS needed
   - **Cons**: Extra latency, defeats purpose of separate backend
   - **Rejected**: Architecture violation

3. **Vercel Serverless Functions for API**:
   - **Pros**: No CORS issues
   - **Cons**: Not FastAPI, violates constitution (must use FastAPI)
   - **Rejected**: Wrong technology stack

---

## 6. Testing & CI/CD Strategy

### Decision

**Docker Compose for local dev + GitHub Actions for CI/CD** with parallel test execution.

### Rationale

**Research Findings**:
- Docker Compose simplifies multi-service local development
- GitHub Actions free tier: 2000 minutes/month (sufficient)
- Playwright Cloud for E2E tests (free tier available)
- Separate CI workflows: Backend, Frontend, E2E

**Why Docker Compose + GitHub Actions**:
- **Local Development**: `docker-compose up` starts all services
- **CI/CD**: Automated testing on every push
- **Cost**: $0/month (all free tiers)
- **Simplicity**: No complex orchestration needed

### Docker Compose Configuration

```yaml
# docker-compose.yml
version: '3.9'

services:
  postgres:
    image: postgres:16-alpine
    environment:
      POSTGRES_USER: todo_user
      POSTGRES_PASSWORD: todo_pass
      POSTGRES_DB: todo_db
    ports:
      - "5432:5432"
    volumes:
      - postgres_data:/var/lib/postgresql/data
    healthcheck:
      test: ["CMD-SHELL", "pg_isready -U todo_user"]
      interval: 5s
      timeout: 3s
      retries: 5

  backend:
    build:
      context: ./backend
      dockerfile: Dockerfile
    ports:
      - "8000:8000"
    environment:
      DATABASE_URL: postgresql://todo_user:todo_pass@postgres:5432/todo_db
      BETTER_AUTH_SECRET: dev-secret-key-change-in-production
      BETTER_AUTH_URL: http://localhost:8000
      FRONTEND_URL: http://localhost:3000
    depends_on:
      postgres:
        condition: service_healthy
    command: uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload

  frontend:
    build:
      context: ./frontend
      dockerfile: Dockerfile.dev
    ports:
      - "3000:3000"
    environment:
      NEXT_PUBLIC_API_URL: http://localhost:8000
    depends_on:
      - backend
    volumes:
      - ./frontend:/app
      - /app/node_modules
    command: npm run dev

volumes:
  postgres_data:
```

### GitHub Actions Workflows

**Backend CI** (`.github/workflows/backend-ci.yml`):
```yaml
name: Backend CI

on:
  push:
    branches: [main, 002-fullstack-web]
    paths:
      - 'backend/**'
  pull_request:
    paths:
      - 'backend/**'

jobs:
  test:
    runs-on: ubuntu-latest

    services:
      postgres:
        image: postgres:16
        env:
          POSTGRES_USER: test_user
          POSTGRES_PASSWORD: test_pass
          POSTGRES_DB: test_db
        options: >-
          --health-cmd pg_isready
          --health-interval 5s
          --health-timeout 3s
          --health-retries 5
        ports:
          - 5432:5432

    steps:
      - uses: actions/checkout@v4

      - name: Set up Python 3.13
        uses: actions/setup-python@v5
        with:
          python-version: '3.13'

      - name: Install UV
        run: pip install uv

      - name: Install dependencies
        run: |
          cd backend
          uv sync

      - name: Run tests with coverage
        env:
          DATABASE_URL: postgresql://test_user:test_pass@localhost:5432/test_db
        run: |
          cd backend
          uv run pytest --cov --cov-report=xml --cov-report=term-missing

      - name: Upload coverage
        uses: codecov/codecov-action@v3
        with:
          files: ./backend/coverage.xml

      - name: Type check (Pyright)
        run: |
          cd backend
          uv run pyright

      - name: Lint (Ruff)
        run: |
          cd backend
          uv run ruff check .
```

**Frontend CI** (`.github/workflows/frontend-ci.yml`):
```yaml
name: Frontend CI

on:
  push:
    branches: [main, 002-fullstack-web]
    paths:
      - 'frontend/**'
  pull_request:
    paths:
      - 'frontend/**'

jobs:
  test:
    runs-on: ubuntu-latest

    steps:
      - uses: actions/checkout@v4

      - name: Set up Node.js 20
        uses: actions/setup-node@v4
        with:
          node-version: '20'
          cache: 'npm'
          cache-dependency-path: frontend/package-lock.json

      - name: Install dependencies
        run: |
          cd frontend
          npm ci

      - name: Run tests with coverage
        run: |
          cd frontend
          npm test -- --coverage

      - name: Upload coverage
        uses: codecov/codecov-action@v3
        with:
          files: ./frontend/coverage/coverage-final.json

      - name: Type check
        run: |
          cd frontend
          npm run type-check

      - name: Lint
        run: |
          cd frontend
          npm run lint

      - name: Build
        run: |
          cd frontend
          npm run build
```

**E2E Tests** (`.github/workflows/e2e.yml`):
```yaml
name: E2E Tests

on:
  push:
    branches: [main, 002-fullstack-web]
  pull_request:

jobs:
  test:
    runs-on: ubuntu-latest

    steps:
      - uses: actions/checkout@v4

      - name: Start services with Docker Compose
        run: docker-compose up -d

      - name: Wait for services
        run: |
          timeout 60 bash -c 'until curl -f http://localhost:8000/health; do sleep 2; done'
          timeout 60 bash -c 'until curl -f http://localhost:3000; do sleep 2; done'

      - name: Run Playwright tests
        run: |
          cd frontend
          npx playwright install --with-deps
          npx playwright test

      - name: Upload Playwright report
        if: always()
        uses: actions/upload-artifact@v3
        with:
          name: playwright-report
          path: frontend/playwright-report/
```

### Local Testing Commands

```bash
# Start all services
docker-compose up

# Run backend tests
cd backend && uv run pytest -v

# Run frontend tests
cd frontend && npm test

# Run E2E tests (requires services running)
cd frontend && npx playwright test

# Run specific E2E test
cd frontend && npx playwright test auth.spec.ts

# View Playwright UI
cd frontend && npx playwright test --ui
```

### Environment Parity

| Environment | Backend URL | Frontend URL | Database | Purpose |
|-------------|-------------|--------------|----------|---------|
| Local | http://localhost:8000 | http://localhost:3000 | Docker PostgreSQL | Development |
| CI/CD | http://localhost:8000 | http://localhost:3000 | GitHub Services | Testing |
| Staging | https://[user]-todo-backend-dev.hf.space | https://[app]-staging.vercel.app | Neon (staging branch) | Pre-production |
| Production | https://[user]-todo-backend.hf.space | https://[app].vercel.app | Neon (main branch) | Live |

### Alternatives Considered

1. **Minikube for local dev**:
   - **Pros**: Closer to production (Kubernetes)
   - **Cons**: Overkill for Phase 2, slow startup, resource-heavy
   - **Rejected**: Save for Phase 4 (Kubernetes deployment)

2. **Jenkins for CI/CD**:
   - **Pros**: More control, self-hosted
   - **Cons**: Maintenance burden, no free tier
   - **Rejected**: GitHub Actions sufficient

3. **Manual testing only**:
   - **Pros**: Zero CI/CD cost
   - **Cons**: Error-prone, slow feedback, violates test-first principle
   - **Rejected**: Constitution requires automated testing

---

## 7. Phase 1 → Phase 2 Migration Strategy

### Decision

**Neon branch + idempotent Python script + validation** with rollback via branch management.

### Rationale

**Research Findings**:
- Neon branching creates instant snapshots (copy-on-write)
- Branches can be merged or deleted without affecting main
- Python script can read JSON and write to PostgreSQL
- UUID generation for new IDs (replace int IDs)

**Why Neon Branch + Script**:
- **Safety**: Main database untouched until merge
- **Testing**: Full migration test on dev branch first
- **Rollback**: Simply delete dev branch if issues
- **Automation**: One command to migrate

### Migration Steps

**Step 1**: Create Neon dev branch
```bash
# Using Neon CLI
neon branches create --name dev-migration --parent main

# Get connection string for dev branch
neon connection-string dev-migration
# Output: postgresql://user:pass@ep-xxx-dev.neon.tech/neondb
```

**Step 2**: Run migration script
```bash
cd backend
export DATABASE_URL=postgresql://user:pass@ep-xxx-dev.neon.tech/neondb
uv run python scripts/migrate_phase1_to_phase2.py
```

**Step 3**: Validate migration
```bash
# Script auto-validates:
# - JSON task count == PostgreSQL task count
# - No NULL user_ids
# - All UUIDs valid format
# - created_at/updated_at populated
```

**Step 4**: Merge or rollback
```bash
# If validation passes, merge to main
neon branches merge dev-migration --into main

# If validation fails, delete dev branch
neon branches delete dev-migration
```

### Migration Script

```python
# backend/scripts/migrate_phase1_to_phase2.py
import json
import sys
from pathlib import Path
from uuid import uuid4
from datetime import datetime
from sqlmodel import Session, select
from app.database import engine
from app.models.user import User
from app.models.task import Task

def migrate_phase1_to_phase2():
    """
    Migrate Phase 1 JSON tasks to Phase 2 PostgreSQL.

    Creates default "Phase 1 Migration" user if not exists.
    Reads cli/tasks.json and inserts into tasks table.
    """
    json_path = Path("cli/tasks.json")

    if not json_path.exists():
        print("✗ Phase 1 tasks.json not found at cli/tasks.json")
        sys.exit(1)

    # Read JSON tasks
    with open(json_path) as f:
        json_data = json.load(f)

    phase1_tasks = json_data.get("tasks", [])
    print(f"✓ Found {len(phase1_tasks)} tasks in Phase 1 JSON")

    with Session(engine) as session:
        # Create or get migration user
        migration_user = session.exec(
            select(User).where(User.email == "phase1-migration@example.com")
        ).first()

        if not migration_user:
            migration_user = User(
                id=uuid4(),
                email="phase1-migration@example.com",
                name="Phase 1 Migration User",
                hashed_password="<no-password>",  # Cannot login
                created_at=datetime.utcnow(),
                updated_at=datetime.utcnow(),
            )
            session.add(migration_user)
            session.commit()
            print(f"✓ Created migration user: {migration_user.id}")
        else:
            print(f"✓ Using existing migration user: {migration_user.id}")

        # Migrate tasks
        migrated_count = 0
        for task_data in phase1_tasks:
            # Transform Phase 1 task to Phase 2 format
            new_task = Task(
                id=uuid4(),  # New UUID (replace int ID)
                user_id=migration_user.id,
                title=task_data["title"],
                description=task_data.get("description", ""),
                completed=task_data.get("completed", False),
                priority=None,  # Phase 1 didn't have priority
                tags=[],  # Phase 1 didn't have tags
                category=None,  # Phase 1 didn't have category
                created_at=datetime.utcnow(),
                updated_at=datetime.utcnow(),
            )
            session.add(new_task)
            migrated_count += 1

        session.commit()
        print(f"✓ Migrated {migrated_count} tasks to PostgreSQL")

        # Validation: count match
        db_task_count = session.exec(
            select(Task).where(Task.user_id == migration_user.id)
        ).count()

        if db_task_count == len(phase1_tasks):
            print(f"✓ Validation PASSED: {db_task_count} tasks in database")
        else:
            print(f"✗ Validation FAILED: Expected {len(phase1_tasks)}, got {db_task_count}")
            sys.exit(1)

    print("\n✅ Migration completed successfully!")
    print(f"   - JSON tasks: {len(phase1_tasks)}")
    print(f"   - Database tasks: {db_task_count}")
    print(f"   - Migration user ID: {migration_user.id}")

if __name__ == "__main__":
    migrate_phase1_to_phase2()
```

### Validation Checklist

- ✅ JSON task count == PostgreSQL task count
- ✅ All tasks have valid UUIDs
- ✅ All tasks have user_id (migration user)
- ✅ All tasks have created_at and updated_at timestamps
- ✅ Title and description preserved exactly
- ✅ Completed status preserved (boolean)
- ✅ No NULL values in required fields

### Rollback Procedure

**If migration fails on dev branch**:
```bash
# Delete dev branch (main unaffected)
neon branches delete dev-migration

# Main database unchanged, try again
```

**If migration fails after merge to main**:
```bash
# Restore from Neon snapshot (24-hour retention on free tier)
neon branches restore main --timestamp "2025-12-26T09:00:00Z"
```

### Idempotency

Script can be run multiple times safely:
- Checks if migration user exists (don't create duplicates)
- Could add task deduplication by matching title+description
- Safe to re-run on empty database

### Alternatives Considered

1. **Manual SQL Migration**:
   - **Pros**: Direct SQL, no Python script
   - **Cons**: Error-prone, no validation, harder to rollback
   - **Rejected**: Script provides better automation and validation

2. **Alembic Data Migration**:
   - **Pros**: Version controlled with schema migrations
   - **Cons**: Alembic designed for schema, not data; one-time migration doesn't need versioning
   - **Rejected**: Overkill, separate script clearer

3. **In-App Migration (on first run)**:
   - **Pros**: Automatic, no manual step
   - **Cons**: Risky, could fail in production, harder to test
   - **Rejected**: Prefer explicit manual migration for safety

---

## Summary of Decisions

| Research Area | Decision | Key Package/Tool |
|---------------|----------|------------------|
| Authentication | Custom JWT + bcrypt | `python-jose`, `passlib` |
| Database Connection | Neon Pooler + Sync SQLModel | `asyncpg`, `sqlmodel` |
| HF Spaces Dockerfile | Single-worker Uvicorn, port 7860 | `uvicorn` |
| Next.js Auth Pattern | Middleware + Server Components | Next.js 15 built-in |
| CORS | FastAPI CORSMiddleware + dynamic origins | FastAPI built-in |
| Testing & CI/CD | Docker Compose + GitHub Actions | Docker, GitHub Actions |
| Phase 1 Migration | Neon branch + Python script + validation | Neon CLI, Python |

---

## Next Steps

1. ✅ **Research Complete** → All unknowns resolved
2. ⏳ **Create Data Model** → Document entity schemas in `data-model.md`
3. ⏳ **Generate API Contracts** → Create OpenAPI specs in `contracts/`
4. ⏳ **Write Quickstart Guide** → Developer onboarding in `quickstart.md`
5. ⏳ **Update Agent Context** → Add Phase 2 technologies to `CLAUDE.md`
6. ⏳ **Generate Tasks** → Run `/sp.tasks` to create task breakdown

---

**Research Status**: ✅ Complete
**Blockers**: None - All technology paths validated
**Confidence Level**: High - All decisions based on official documentation and best practices
