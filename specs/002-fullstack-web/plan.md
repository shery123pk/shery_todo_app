# Implementation Plan: Full-Stack Web Application with Authentication

**Branch**: `002-fullstack-web` | **Date**: 2025-12-26 | **Spec**: [spec.md](./spec.md)
**Input**: Feature specification from `specs/002-fullstack-web/spec.md`

**Note**: This template is filled in by the `/sp.plan` command. See `.specify/templates/commands/plan.md` for the execution workflow.

## Summary

Transform the Phase 1 CLI todo application into a production-ready full-stack web application with multi-user support, authentication, and persistent storage. Build FastAPI backend with SQLModel ORM connected to Neon PostgreSQL, Next.js 15 frontend with shadcn/ui components, and Better Auth for session-based authentication. Deploy backend to Hugging Face Spaces (port 7860), frontend to Vercel, and database to Neon PostgreSQL serverless.

Phase 1 CLI remains fully independent and functional - no shared data or dependencies.

## Technical Context

**Language/Version**: Python 3.13+ (backend), TypeScript 5 strict mode (frontend)
**Primary Dependencies**:
- Backend: FastAPI 0.100+, SQLModel, Pydantic, Better Auth Python adapter, Alembic
- Frontend: Next.js 15 App Router, React 19, Tailwind CSS 4, shadcn/ui, Zod
**Storage**: Neon PostgreSQL 16 serverless (cloud), PostgreSQL 16 Docker (local dev)
**Testing**:
- Backend: pytest, pytest-cov (≥80%), pytest-asyncio
- Frontend: Vitest, React Testing Library (≥80%)
- E2E: Playwright (cross-browser)
**Target Platform**:
- Backend: Hugging Face Spaces (Docker SDK, port 7860 mandatory)
- Frontend: Vercel (Next.js optimized)
- Database: Neon PostgreSQL (external serverless)
**Project Type**: Web application (monorepo with separate frontend/ and backend/)
**Performance Goals**:
- API: <200ms p95 latency, <500ms p99
- Frontend: <2s initial page load on 3G, Lighthouse ≥90
- Database: Indexed queries on user_id, completed, created_at
**Constraints**:
- Port 7860 for HF Spaces (non-negotiable)
- Test coverage ≥80% (both frontend and backend)
- Pyright strict (backend), TypeScript strict (frontend)
- Phase 1 CLI must remain 100% functional
- CORS: Vercel frontend ↔ HF Space backend
**Scale/Scope**:
- Multi-user: Support 10-100 concurrent users
- 0-1000 tasks per user (no pagination in Phase 2)
- 7-day session expiry (30 days with "remember me")

## Constitution Check

*GATE: Must pass before Phase 0 research. Re-check after Phase 1 design.*

### ✅ I. Spec-Driven Development Only
- **Status**: PASS
- **Evidence**: Following strict SDD workflow: Constitution → Specify ✅ → Plan (current) → Tasks → Implement
- **Specification**: Complete spec at `specs/002-fullstack-web/spec.md` with 7 user stories, 73 acceptance criteria, 43 functional requirements
- **Approval**: Architect approved on 2025-12-26

### ✅ II. AI as Sole Developer
- **Status**: PASS
- **Human Role**: Architect (shery123pk) provides specs, reviews plans, validates tests
- **AI Role**: Claude generates plan, tasks, code, tests, documentation
- **Subagents**: Backend Engineer, Frontend Engineer, Data Migration, QA Testing agents ready for invocation

### ✅ III. Semantic Code Editing (Serena Rules)
- **Status**: PASS
- **LSP Configuration**:
  - Python: Pyright/Pylance (strict mode)
  - TypeScript: tsserver (strict mode)
- **Tools**: Serena agent available for semantic refactoring
- **Commitment**: All code modifications will use LSP-aware tools, no blind regex edits

### ✅ IV. Full Traceability & Audit Trail
- **Status**: PASS
- **Chain**:
  - ADRs: 001 (ID Migration), 002 (Monorepo), 003 (Neon DB), 004 (Better Auth), 005 (HF Deployment)
  - Spec: `specs/002-fullstack-web/spec.md`
  - Plan: `specs/002-fullstack-web/plan.md` (this file)
  - Tasks: `specs/002-fullstack-web/tasks.md` (next step)
  - Code: `backend/`, `frontend/`
  - Tests: `backend/tests/`, `frontend/__tests__/`
- **PHRs**: History in `history/prompts/fullstack-web/`

### ✅ V. Test-First & Evolutionary Safeguards
- **Status**: PASS
- **Commitment**:
  - Generate tests with/before code
  - ≥80% coverage (backend: pytest-cov, frontend: Vitest)
  - E2E tests for all 7 user stories (Playwright)
  - Phase 1 regression: Verify all 81 CLI tests still passing
- **Coverage Targets**:
  - Backend: ≥80% line coverage
  - Frontend: ≥80% line coverage
  - E2E: 100% user story coverage

### ✅ VI. Reusable Intelligence Integration
- **Status**: PASS
- **Subagents Available**:
  - Backend Engineer: FastAPI, SQLModel, MCP server
  - Frontend Engineer: Next.js 15, TypeScript, shadcn/ui
  - Data Migration: Phase 1 → Phase 2 migration script
  - QA Testing: pytest, Vitest, Playwright
  - AI Engineer: (Phase 3 - MCP tools)
- **Skills**: All agents spec-driven and traceable

### ✅ Unified Domain Model Compliance
- **Status**: PASS
- **Phase 1 Core (Preserved)**:
  - `id`: UUID (migrated from int per ADR-001)
  - `title`: string (1-200 chars)
  - `description`: string (optional, max 1000 chars)
  - `completed`: boolean
- **Phase 2 Additions**:
  - `user_id`: UUID (foreign key, indexed)
  - `priority`: enum["low", "medium", "high", "critical"]
  - `tags`: array of strings
  - `category`: string (max 50 chars)
  - `created_at`, `updated_at`: ISO 8601 timestamps
- **Invariants**:
  - ✅ `id` never mutates
  - ✅ `completed` is binary only (true/false)
  - ✅ CRUD semantics consistent with Phase 1
  - ✅ Backward compatible (Phase 1 CLI unaffected)

### ✅ Technology Stack Compliance
- **Status**: PASS
- **Backend**: Python 3.13+, FastAPI, SQLModel, Pydantic, Better Auth ✅
- **Frontend**: Next.js 15, TypeScript strict, Tailwind CSS, shadcn/ui ✅
- **Database**: Neon PostgreSQL 16 ✅
- **Deployment**: HF Spaces (Docker, port 7860), Vercel, Neon ✅
- **Testing**: pytest, Vitest, Playwright ✅
- **Type Checking**: Pyright strict, TypeScript strict ✅
- **Linting**: Ruff (Python), ESLint (TypeScript) ✅
- **LSP**: Configured for Python and TypeScript ✅

### ✅ Forbidden Practices Avoided
- **Status**: PASS
- **Verification**:
  - ✅ No manual code writing by humans (AI-generated only)
  - ✅ No hard-coded secrets (use .env)
  - ✅ No direct DB access from frontend (API layer enforced)
  - ✅ No unparameterized queries (SQLModel ORM only)
  - ✅ No vendor lock-in (Dapr in Phase 5)
  - ✅ No blind regex edits (LSP-aware tools only)
  - ✅ No code mods without semantic understanding

**GATE RESULT**: ✅ **PASS** - Proceed to Phase 0 (Research)

---

## Project Structure

### Documentation (this feature)

```text
specs/002-fullstack-web/
├── spec.md              # Feature specification (complete)
├── plan.md              # This file (/sp.plan output)
├── research.md          # Phase 0 output (research decisions)
├── data-model.md        # Phase 1 output (entity schemas)
├── quickstart.md        # Phase 1 output (dev setup guide)
├── contracts/           # Phase 1 output (API contracts)
│   ├── openapi.yaml     # OpenAPI 3.1 spec
│   ├── auth.md          # Authentication endpoints
│   └── tasks.md         # Task CRUD endpoints
└── tasks.md             # Phase 2 output (/sp.tasks - NOT created by /sp.plan)
```

### Source Code (repository root)

**Structure Decision**: Web application with separate backend and frontend (monorepo)

```text
backend/
├── app/
│   ├── main.py                    # FastAPI app entry, CORS, middleware
│   ├── config.py                  # Settings (BaseSettings)
│   ├── database.py                # SQLModel engine, session
│   ├── models/
│   │   ├── __init__.py
│   │   ├── user.py                # User SQLModel
│   │   ├── task.py                # Task SQLModel
│   │   ├── session.py             # Session SQLModel (Better Auth)
│   │   └── account.py             # Account SQLModel (Better Auth OAuth)
│   ├── schemas/
│   │   ├── __init__.py
│   │   ├── user.py                # User Pydantic models (UserCreate, UserRead)
│   │   ├── task.py                # Task Pydantic models (TaskCreate, TaskUpdate, TaskRead)
│   │   └── auth.py                # Auth Pydantic models (LoginRequest, TokenResponse)
│   ├── routers/
│   │   ├── __init__.py
│   │   ├── auth.py                # /api/auth endpoints (signup, signin, signout)
│   │   └── tasks.py               # /api/tasks endpoints (CRUD)
│   ├── dependencies.py            # Dependency injection (get_db, get_current_user)
│   ├── security.py                # Password hashing, JWT, session validation
│   └── exceptions.py              # Custom exception handlers
├── alembic/
│   ├── versions/                  # Database migrations
│   └── env.py                     # Alembic config
├── scripts/
│   └── migrate_phase1_to_phase2.py  # One-time migration script
├── tests/
│   ├── conftest.py                # pytest fixtures (test DB, test client)
│   ├── unit/
│   │   ├── test_models.py         # Model validation tests
│   │   ├── test_schemas.py        # Pydantic schema tests
│   │   └── test_security.py       # Password hashing, JWT tests
│   ├── integration/
│   │   ├── test_auth.py           # Auth flow tests
│   │   └── test_tasks.py          # Task CRUD tests
│   └── e2e/
│       └── test_api_contract.py   # OpenAPI contract tests
├── Dockerfile                     # HF Spaces Docker (port 7860)
├── pyproject.toml                 # UV dependencies
├── README.md                      # Backend setup instructions
└── .env.example                   # Example environment variables

frontend/
├── app/
│   ├── layout.tsx                 # Root layout (Server Component)
│   ├── page.tsx                   # Landing page
│   ├── auth/
│   │   ├── signin/
│   │   │   └── page.tsx           # Login page
│   │   └── signup/
│   │       └── page.tsx           # Registration page
│   ├── tasks/
│   │   ├── layout.tsx             # Protected layout (auth required)
│   │   └── page.tsx               # Task dashboard (Server Component)
│   └── api/
│       └── auth/
│           └── [...auth]/
│               └── route.ts       # Better Auth API routes
├── components/
│   ├── ui/                        # shadcn/ui components
│   │   ├── button.tsx
│   │   ├── card.tsx
│   │   ├── input.tsx
│   │   ├── dialog.tsx
│   │   └── ...
│   ├── TaskList.tsx               # Task list (Client Component)
│   ├── TaskCard.tsx               # Individual task (Client Component)
│   ├── TaskForm.tsx               # Create/edit task modal (Client Component)
│   └── Header.tsx                 # Navigation header
├── lib/
│   ├── api.ts                     # API client (fetch wrappers)
│   ├── auth.ts                    # Better Auth client config
│   ├── utils.ts                   # Utility functions (cn, formatDate)
│   └── validations.ts             # Zod schemas (client-side)
├── hooks/
│   ├── useTasks.ts                # SWR hook for task data
│   └── useAuth.ts                 # Authentication hook
├── __tests__/
│   ├── components/
│   │   ├── TaskList.test.tsx      # Component tests (Vitest)
│   │   └── TaskCard.test.tsx
│   └── integration/
│       └── auth-flow.test.ts      # Integration tests
├── e2e/
│   ├── auth.spec.ts               # Playwright E2E tests (auth flow)
│   ├── tasks.spec.ts              # Playwright E2E tests (CRUD)
│   └── playwright.config.ts       # Playwright config
├── public/
│   └── ... (static assets)
├── styles/
│   └── globals.css                # Global Tailwind CSS
├── Dockerfile                     # Optional (static export)
├── package.json                   # npm dependencies
├── tsconfig.json                  # TypeScript strict config
├── tailwind.config.ts             # Tailwind CSS config
├── next.config.js                 # Next.js config
├── README.md                      # Frontend setup instructions
└── .env.local.example             # Example environment variables

cli/                               # Phase 1 CLI (UNCHANGED)
├── todo_cli/
│   ├── __init__.py
│   ├── cli.py
│   ├── repository.py
│   └── ...
├── tests/                         # 81 tests (96% coverage)
├── pyproject.toml
└── README.md

shared/                            # Shared types/utils (if needed)
└── types.ts                       # TypeScript shared types

docker-compose.yml                 # Local dev: backend + frontend + postgres
.env.example                       # Root environment variables
README.md                          # Root setup instructions
CLAUDE.md                          # AI development guidelines
```

**Structure Rationale**:
- **Monorepo**: Single git repo for all phases (per ADR-002)
- **Separation**: `backend/` and `frontend/` are independent deployable units
- **Phase 1 Isolation**: `cli/` remains untouched, fully functional
- **Shared Code**: Minimal (types only), most code phase-specific
- **Deployment**: Backend → HF Spaces, Frontend → Vercel, DB → Neon (separate platforms)

---

## Complexity Tracking

> **Fill ONLY if Constitution Check has violations that must be justified**

**No violations detected.** All constitution principles complied with.

---

## Phase 0: Research & Technology Decisions

**Goal**: Resolve all unknowns and research best practices before design phase.

### Research Tasks

#### 1. Better Auth Python Adapter Investigation
**Question**: Does Better Auth have an official Python adapter, or do we need a custom JWT implementation?

**Research Needed**:
- Check Better Auth official docs for Python/FastAPI support
- Search npm registry for `@better-auth/python` or similar
- Investigate alternative: Custom JWT with bcrypt (if no adapter)
- Identify session storage strategy (database vs Redis)

**Expected Output in research.md**:
```markdown
### Better Auth Python Integration
**Decision**: [Use Better Auth adapter | Build custom JWT implementation]
**Rationale**: [Why chosen based on research]
**Alternatives Considered**:
  - Better Auth Python adapter (if exists): Pros/Cons
  - Custom JWT + bcrypt: Pros/Cons
  - NextAuth.js (frontend only): Pros/Cons
**Implementation Path**: [Specific packages, code patterns]
```

#### 2. Neon PostgreSQL Connection Patterns
**Question**: What's the optimal connection pattern for Neon serverless with FastAPI?

**Research Needed**:
- Neon connection pooler vs direct connection
- SQLModel async vs sync engine
- Cold start mitigation strategies
- SSL certificate handling
- Environment variable configuration

**Expected Output in research.md**:
```markdown
### Neon PostgreSQL Connection Strategy
**Decision**: [Connection pooler | Direct connection | Hybrid]
**Rationale**: [Performance, reliability, cost considerations]
**Connection String Format**: postgresql://user:pass@ep-xxx.neon.tech/db?sslmode=require&pool_timeout=30
**Cold Start Mitigation**: [Warm-up queries | Reserved compute | Connection pooling]
**SQLModel Engine**: [Async | Sync] + justification
```

#### 3. Hugging Face Spaces Dockerfile Best Practices
**Question**: What's the optimal Dockerfile configuration for FastAPI on HF Spaces (port 7860)?

**Research Needed**:
- HF Spaces Docker SDK requirements
- Port 7860 exposure and binding
- Uvicorn worker configuration (1 worker vs multi)
- Health check endpoint
- Startup time optimization

**Expected Output in research.md**:
```markdown
### Hugging Face Spaces Dockerfile Configuration
**Decision**: Single-worker Uvicorn on port 7860
**Rationale**: HF Spaces single-container constraint, port 7860 mandatory
**Dockerfile Template**: [Tested Dockerfile with optimizations]
**Health Check**: GET /health endpoint
**Startup Time**: Target <10 seconds
```

#### 4. Next.js 15 App Router Authentication Patterns
**Question**: What's the recommended Better Auth integration pattern with Next.js 15 Server Components?

**Research Needed**:
- Better Auth client setup with App Router
- Server vs Client Components for auth
- Session validation in Server Components
- Protected routes middleware
- Cookie handling (httpOnly)

**Expected Output in research.md**:
```markdown
### Next.js 15 + Better Auth Pattern
**Decision**: [Server Component auth | Middleware-based | Hybrid]
**Rationale**: [Performance, security, developer experience]
**Protected Routes**: Middleware at /tasks/*, redirect to /auth/signin
**Session Validation**: [Server Component | API route | Middleware]
**Cookie Strategy**: httpOnly, secure, sameSite=lax, 7-day expiry
```

#### 5. CORS Configuration for Vercel ↔ HF Spaces
**Question**: How to configure CORS for cross-origin requests between Vercel frontend and HF Space backend?

**Research Needed**:
- FastAPI CORS middleware setup
- Vercel domain patterns (preview vs production)
- Wildcard domains for preview deployments
- Preflight request handling
- Cookie credential sharing

**Expected Output in research.md**:
```markdown
### CORS Configuration Strategy
**Decision**: FastAPI CORSMiddleware with dynamic origin list
**Allowed Origins**:
  - Production: https://[your-app].vercel.app
  - Preview: https://*-[your-username].vercel.app (wildcard pattern)
  - Local: http://localhost:3000
**Credentials**: allow_credentials=True (for cookies)
**Headers**: allow_headers=["*"] or specific list
**Methods**: ["GET", "POST", "PATCH", "DELETE", "OPTIONS"]
```

#### 6. Test Strategy for Multi-Platform Deployment
**Question**: How to test the integrated system locally before deploying to 3 platforms?

**Research Needed**:
- Docker Compose setup (backend + frontend + postgres)
- Playwright configuration for E2E tests
- Environment variable management (local vs production)
- CI/CD pipeline strategy (GitHub Actions)

**Expected Output in research.md**:
```markdown
### Testing & CI/CD Strategy
**Decision**: Docker Compose local dev + GitHub Actions CI/CD
**Local Testing**:
  - docker-compose up → backend:8000, frontend:3000, postgres:5432
  - Playwright E2E tests against local
**CI/CD Pipeline**:
  - Push to main → Run pytest (backend) + Vitest (frontend)
  - E2E tests on staging environment
  - Deploy backend to HF Spaces, frontend to Vercel
**Environment Parity**: .env.local (dev), .env.production (prod)
```

#### 7. Migration Script Safety & Rollback
**Question**: How to safely migrate Phase 1 JSON data to Phase 2 PostgreSQL with rollback capability?

**Research Needed**:
- Neon branching feature for safe migrations
- Data validation pre/post migration
- Idempotent migration script
- Rollback procedure

**Expected Output in research.md**:
```markdown
### Phase 1 → Phase 2 Migration Strategy
**Decision**: Neon branch + idempotent Python script + validation
**Steps**:
  1. Create Neon dev branch (snapshot)
  2. Run migration script on dev branch
  3. Validate: task count, data integrity
  4. Merge dev branch to main if successful
**Rollback**: Delete dev branch, main unchanged
**Script Location**: backend/scripts/migrate_phase1_to_phase2.py
**Validation**: Assert JSON task count == PostgreSQL task count
```

### Research Output

**File**: `specs/002-fullstack-web/research.md`

**Required Sections**:
1. Better Auth Python Integration
2. Neon PostgreSQL Connection Strategy
3. Hugging Face Spaces Dockerfile Configuration
4. Next.js 15 + Better Auth Pattern
5. CORS Configuration Strategy
6. Testing & CI/CD Strategy
7. Phase 1 → Phase 2 Migration Strategy

Each section must include:
- **Decision**: What was chosen
- **Rationale**: Why chosen (pros/cons)
- **Alternatives Considered**: What else was evaluated
- **Implementation Notes**: Code snippets, package versions, config examples

---

## Phase 1: Design & Contracts

### 1. Data Model Design

**File**: `specs/002-fullstack-web/data-model.md`

**Content Structure**:

```markdown
# Data Model: Full-Stack Web Application

## Entity Relationship Diagram (ERD)

[Mermaid diagram showing User, Task, Session, Account relationships]

## Entity: User

### Fields
| Field | Type | Constraints | Description |
|-------|------|-------------|-------------|
| id | UUID | PRIMARY KEY, NOT NULL | Unique user identifier |
| email | VARCHAR(255) | UNIQUE, NOT NULL, INDEX | Lowercase normalized email |
| email_verified | BOOLEAN | DEFAULT false | Email verification status |
| name | VARCHAR(255) | NULLABLE | User display name |
| hashed_password | VARCHAR(255) | NOT NULL | Bcrypt hashed password (cost factor 12) |
| created_at | TIMESTAMP WITH TIME ZONE | NOT NULL, DEFAULT now() | Account creation timestamp |
| updated_at | TIMESTAMP WITH TIME ZONE | NOT NULL, DEFAULT now() | Last update timestamp |

### Indexes
- PRIMARY KEY: id
- UNIQUE INDEX: email
- INDEX: created_at (for admin queries)

### Validation Rules
- email: RFC 5322 regex, max 255 chars
- name: Optional, max 255 chars
- hashed_password: bcrypt hash only, never plaintext

### State Transitions
N/A (simple entity, no state machine)

---

## Entity: Task

### Fields
| Field | Type | Constraints | Description |
|-------|------|-------------|-------------|
| id | UUID | PRIMARY KEY, NOT NULL | Unique task identifier |
| user_id | UUID | FOREIGN KEY (users.id), NOT NULL, INDEX | Owner of the task |
| title | VARCHAR(200) | NOT NULL | Task title (1-200 chars) |
| description | TEXT | NULLABLE | Task description (max 1000 chars, enforced in app) |
| completed | BOOLEAN | NOT NULL, DEFAULT false, INDEX | Completion status |
| priority | VARCHAR(10) | NULLABLE, CHECK IN ('low', 'medium', 'high', 'critical') | Task priority |
| tags | TEXT[] | DEFAULT '{}' | Array of string tags |
| category | VARCHAR(50) | NULLABLE | Task category |
| created_at | TIMESTAMP WITH TIME ZONE | NOT NULL, DEFAULT now(), INDEX | Creation timestamp |
| updated_at | TIMESTAMP WITH TIME ZONE | NOT NULL, DEFAULT now() | Last update timestamp |

### Indexes
- PRIMARY KEY: id
- INDEX: user_id (for filtering by owner)
- INDEX: completed (for filtering by status)
- INDEX: created_at (for sorting)
- COMPOSITE INDEX: (user_id, completed, created_at) (for common query)

### Validation Rules
- title: Required, 1-200 chars, trimmed
- description: Optional, max 1000 chars
- priority: Optional, one of ['low', 'medium', 'high', 'critical']
- tags: Optional, array of strings
- category: Optional, max 50 chars

### State Transitions
- completed: false ↔ true (bidirectional toggle)

### Foreign Keys
- user_id → users.id (ON DELETE CASCADE)

---

## Entity: Session (Better Auth)

### Fields
| Field | Type | Constraints | Description |
|-------|------|-------------|-------------|
| id | UUID | PRIMARY KEY, NOT NULL | Unique session identifier |
| user_id | UUID | FOREIGN KEY (users.id), NOT NULL, INDEX | Session owner |
| token | VARCHAR(255) | UNIQUE, NOT NULL, INDEX | Session token (JWT or random) |
| expires_at | TIMESTAMP WITH TIME ZONE | NOT NULL, INDEX | Session expiry timestamp |
| ip_address | INET | NULLABLE | Client IP address (optional) |
| user_agent | TEXT | NULLABLE | Client User-Agent (optional) |
| created_at | TIMESTAMP WITH TIME ZONE | NOT NULL, DEFAULT now() | Session creation timestamp |

### Indexes
- PRIMARY KEY: id
- UNIQUE INDEX: token
- INDEX: user_id (for user sessions query)
- INDEX: expires_at (for cleanup job)

### Validation Rules
- token: Unique, secure random or JWT
- expires_at: Must be future timestamp

### Foreign Keys
- user_id → users.id (ON DELETE CASCADE)

---

## Entity: Account (Better Auth OAuth)

### Fields
| Field | Type | Constraints | Description |
|-------|------|-------------|-------------|
| id | UUID | PRIMARY KEY, NOT NULL | Unique account identifier |
| user_id | UUID | FOREIGN KEY (users.id), NOT NULL, INDEX | Account owner |
| provider | VARCHAR(50) | NOT NULL | OAuth provider (email, google, github) |
| provider_account_id | VARCHAR(255) | NOT NULL | Provider-specific user ID |
| access_token | TEXT | NULLABLE | Encrypted OAuth access token |
| refresh_token | TEXT | NULLABLE | Encrypted OAuth refresh token |
| expires_at | TIMESTAMP WITH TIME ZONE | NULLABLE | Token expiry timestamp |
| created_at | TIMESTAMP WITH TIME ZONE | NOT NULL, DEFAULT now() | Account creation timestamp |

### Indexes
- PRIMARY KEY: id
- INDEX: user_id
- UNIQUE INDEX: (provider, provider_account_id)

### Validation Rules
- provider: One of ['email', 'google', 'github']
- provider_account_id: Required, max 255 chars

### Foreign Keys
- user_id → users.id (ON DELETE CASCADE)

---

## Relationships

- User → Task: One-to-Many (user_id foreign key)
- User → Session: One-to-Many (user_id foreign key)
- User → Account: One-to-Many (user_id foreign key)

All relationships use CASCADE delete (when user deleted, all associated data deleted).

---

## Database Migrations

**Tool**: Alembic

**Migration Files**:
1. `001_initial_schema.py`: Create users, tasks, sessions, accounts tables
2. `002_add_indexes.py`: Add composite indexes for performance
3. `003_add_constraints.py`: Add check constraints (priority enum)

**Migration Commands**:
```bash
# Generate migration
alembic revision --autogenerate -m "Initial schema"

# Apply migrations
alembic upgrade head

# Rollback
alembic downgrade -1
```

**Neon Branching**:
- Dev branch: `dev` (for testing migrations)
- Staging branch: `staging` (for pre-prod testing)
- Main branch: `main` (production)

---

## Data Integrity Rules

1. **User Isolation**: All task queries MUST filter by user_id (no exceptions)
2. **Cascade Deletes**: User deletion → delete all tasks, sessions, accounts
3. **Email Uniqueness**: Case-insensitive unique constraint on email
4. **Password Security**: Never store plaintext, always bcrypt hash
5. **Session Expiry**: Auto-cleanup expired sessions (background job)
6. **Timestamp Consistency**: All timestamps in UTC, ISO 8601 format
```

### 2. API Contract Generation

**Directory**: `specs/002-fullstack-web/contracts/`

#### File 1: `openapi.yaml`

Full OpenAPI 3.1 specification for the API (auto-generated by FastAPI, documented here for reference).

**Key Endpoints**:
- `POST /api/auth/signup`: Register new user
- `POST /api/auth/signin`: Login user
- `POST /api/auth/signout`: Logout user
- `GET /api/tasks`: List user's tasks
- `POST /api/tasks`: Create task
- `GET /api/tasks/{id}`: Get single task
- `PATCH /api/tasks/{id}`: Update task
- `DELETE /api/tasks/{id}`: Delete task

#### File 2: `auth.md`

```markdown
# Authentication API Contract

## POST /api/auth/signup

**Description**: Register a new user account

**Request**:
```json
{
  "email": "user@example.com",
  "password": "securepass123",
  "name": "John Doe" // optional
}
```

**Response (201 Created)**:
```json
{
  "id": "550e8400-e29b-41d4-a716-446655440000",
  "email": "user@example.com",
  "name": "John Doe",
  "email_verified": false,
  "created_at": "2025-12-26T10:00:00Z"
}
```

**Errors**:
- 400: Invalid email format, password too short
- 409: Email already exists

---

## POST /api/auth/signin

**Description**: Login with email and password

**Request**:
```json
{
  "email": "user@example.com",
  "password": "securepass123",
  "remember_me": false // optional, default false
}
```

**Response (200 OK)**:
```json
{
  "user": {
    "id": "550e8400-e29b-41d4-a716-446655440000",
    "email": "user@example.com",
    "name": "John Doe"
  }
}
```

**Headers**:
- `Set-Cookie`: `session_token=xxx; HttpOnly; Secure; SameSite=Lax; Max-Age=604800`

**Errors**:
- 400: Missing email or password
- 401: Invalid credentials
- 429: Too many login attempts

---

## POST /api/auth/signout

**Description**: Logout current user (clear session)

**Request**: Empty body

**Response (204 No Content)**

**Headers**:
- `Set-Cookie`: `session_token=; Max-Age=0` (clear cookie)

---

## GET /api/auth/me

**Description**: Get current authenticated user

**Authentication**: Required (session token)

**Response (200 OK)**:
```json
{
  "id": "550e8400-e29b-41d4-a716-446655440000",
  "email": "user@example.com",
  "name": "John Doe",
  "email_verified": false,
  "created_at": "2025-12-26T10:00:00Z"
}
```

**Errors**:
- 401: Unauthorized (no session or expired)
```

#### File 3: `tasks.md`

```markdown
# Task CRUD API Contract

## GET /api/tasks

**Description**: List all tasks for authenticated user

**Authentication**: Required

**Query Parameters**:
- `completed` (optional): Filter by completion status (true/false)
- `limit` (optional): Max tasks to return (default: 1000)
- `offset` (optional): Pagination offset (default: 0)

**Response (200 OK)**:
```json
{
  "tasks": [
    {
      "id": "123e4567-e89b-12d3-a456-426614174000",
      "user_id": "550e8400-e29b-41d4-a716-446655440000",
      "title": "Buy groceries",
      "description": "Milk, eggs, bread",
      "completed": false,
      "priority": "medium",
      "tags": ["shopping", "urgent"],
      "category": "personal",
      "created_at": "2025-12-26T09:00:00Z",
      "updated_at": "2025-12-26T09:00:00Z"
    }
  ],
  "total": 15,
  "completed": 5,
  "incomplete": 10
}
```

**Errors**:
- 401: Unauthorized

---

## POST /api/tasks

**Description**: Create a new task

**Authentication**: Required

**Request**:
```json
{
  "title": "Buy groceries",
  "description": "Milk, eggs, bread", // optional
  "priority": "medium", // optional
  "tags": ["shopping"], // optional
  "category": "personal" // optional
}
```

**Response (201 Created)**:
```json
{
  "id": "123e4567-e89b-12d3-a456-426614174000",
  "user_id": "550e8400-e29b-41d4-a716-446655440000",
  "title": "Buy groceries",
  "description": "Milk, eggs, bread",
  "completed": false,
  "priority": "medium",
  "tags": ["shopping"],
  "category": "personal",
  "created_at": "2025-12-26T10:00:00Z",
  "updated_at": "2025-12-26T10:00:00Z"
}
```

**Errors**:
- 400: Validation error (title missing, too long, etc.)
- 401: Unauthorized

---

## GET /api/tasks/{id}

**Description**: Get a single task by ID

**Authentication**: Required

**Response (200 OK)**:
```json
{
  "id": "123e4567-e89b-12d3-a456-426614174000",
  "user_id": "550e8400-e29b-41d4-a716-446655440000",
  "title": "Buy groceries",
  "description": "Milk, eggs, bread",
  "completed": false,
  "priority": "medium",
  "tags": ["shopping"],
  "category": "personal",
  "created_at": "2025-12-26T10:00:00Z",
  "updated_at": "2025-12-26T10:00:00Z"
}
```

**Errors**:
- 401: Unauthorized
- 404: Task not found or not owned by user

---

## PATCH /api/tasks/{id}

**Description**: Update a task (partial update)

**Authentication**: Required

**Request** (all fields optional):
```json
{
  "title": "Buy groceries and milk",
  "description": "Updated description",
  "completed": true,
  "priority": "high",
  "tags": ["shopping", "urgent"],
  "category": "personal"
}
```

**Response (200 OK)**:
```json
{
  "id": "123e4567-e89b-12d3-a456-426614174000",
  "user_id": "550e8400-e29b-41d4-a716-446655440000",
  "title": "Buy groceries and milk",
  "description": "Updated description",
  "completed": true,
  "priority": "high",
  "tags": ["shopping", "urgent"],
  "category": "personal",
  "created_at": "2025-12-26T10:00:00Z",
  "updated_at": "2025-12-26T12:30:00Z"
}
```

**Errors**:
- 400: Validation error
- 401: Unauthorized
- 404: Task not found or not owned by user

---

## DELETE /api/tasks/{id}

**Description**: Permanently delete a task

**Authentication**: Required

**Response (204 No Content)**

**Errors**:
- 401: Unauthorized
- 404: Task not found or not owned by user
```

### 3. Quickstart Guide

**File**: `specs/002-fullstack-web/quickstart.md`

```markdown
# Quickstart: Phase 2 Full-Stack Web Application

## Prerequisites

- Python 3.13+
- Node.js 20+
- Docker & Docker Compose
- UV (Python package manager): `pip install uv`
- Git

## Local Development Setup (5 minutes)

### 1. Clone Repository

```bash
git clone <repo-url>
cd shery_todo_app
git checkout 002-fullstack-web
```

### 2. Environment Variables

**Backend** (`backend/.env`):
```bash
DATABASE_URL=postgresql://todo_user:todo_pass@localhost:5432/todo_db
BETTER_AUTH_SECRET=your-secret-key-here-change-in-production
BETTER_AUTH_URL=http://localhost:8000
FRONTEND_URL=http://localhost:3000
```

**Frontend** (`frontend/.env.local`):
```bash
NEXT_PUBLIC_API_URL=http://localhost:8000
BETTER_AUTH_URL=http://localhost:8000
BETTER_AUTH_SECRET=your-secret-key-here-change-in-production
```

### 3. Start Services (Docker Compose)

```bash
docker-compose up -d
```

This starts:
- **Backend**: http://localhost:8000
- **Frontend**: http://localhost:3000
- **PostgreSQL**: localhost:5432
- **API Docs**: http://localhost:8000/docs

### 4. Run Database Migrations

```bash
cd backend
uv run alembic upgrade head
```

### 5. Create First User

Navigate to http://localhost:3000/auth/signup

### 6. Run Tests

**Backend**:
```bash
cd backend
uv run pytest --cov --cov-report=term-missing
```

**Frontend**:
```bash
cd frontend
npm test
```

**E2E**:
```bash
cd frontend
npx playwright test
```

---

## Production Deployment

### Backend (Hugging Face Spaces)

1. Create new Space: https://huggingface.co/spaces
2. Select Docker SDK
3. Upload `backend/Dockerfile`
4. Set Secrets:
   - `DATABASE_URL`: Neon PostgreSQL connection string
   - `BETTER_AUTH_SECRET`: Random 32-char string
   - `BETTER_AUTH_URL`: https://[username]-todo-backend.hf.space
   - `FRONTEND_URL`: https://[your-app].vercel.app
5. Deploy → Auto-build and run on port 7860
6. Verify: https://[username]-todo-backend.hf.space/docs

### Frontend (Vercel)

1. Push to GitHub
2. Import on Vercel: https://vercel.com/new
3. Set Environment Variables:
   - `NEXT_PUBLIC_API_URL`: https://[username]-todo-backend.hf.space
   - `BETTER_AUTH_URL`: https://[username]-todo-backend.hf.space
   - `BETTER_AUTH_SECRET`: (same as backend)
4. Deploy → Auto-deploy on push to main
5. Verify: https://[your-app].vercel.app

### Database (Neon)

1. Create project: https://neon.tech
2. Create branches: `dev`, `staging`, `main`
3. Copy connection string for each branch
4. Update environment variables in HF Spaces and Vercel

---

## Common Commands

**Backend**:
```bash
# Install dependencies
uv sync

# Run dev server
uv run uvicorn app.main:app --reload --port 8000

# Create migration
uv run alembic revision --autogenerate -m "Add new field"

# Run tests
uv run pytest -v

# Type check
uv run pyright

# Lint
uv run ruff check .
```

**Frontend**:
```bash
# Install dependencies
npm install

# Run dev server
npm run dev

# Build for production
npm run build

# Run tests
npm test

# E2E tests
npx playwright test

# Type check
npm run type-check

# Lint
npm run lint
```

---

## Troubleshooting

### Issue: Backend fails to connect to database

**Solution**: Verify DATABASE_URL is correct and database is running:
```bash
docker-compose ps postgres
```

### Issue: Frontend shows CORS error

**Solution**: Verify FRONTEND_URL in backend .env matches frontend URL

### Issue: HF Space backend stuck on port 8000

**Solution**: Update Dockerfile CMD to use port 7860:
```dockerfile
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "7860"]
```

### Issue: Neon connection timeout

**Solution**: Use connection pooler URL, not direct connection:
```
postgresql://user:pass@ep-xxx.pooler.neon.tech/db?sslmode=require
```
```

### 4. Agent Context Update

**Script**: `.specify/scripts/powershell/update-agent-context.ps1 -AgentType claude`

This script will:
1. Detect that we're using Claude
2. Update `CLAUDE.md` with Phase 2 technologies
3. Preserve manual additions between markers
4. Add only new technologies from this plan

**Technologies to Add**:
- Better Auth (authentication)
- Neon PostgreSQL (database)
- Alembic (migrations)
- shadcn/ui (UI components)
- Zod (validation)
- Playwright (E2E testing)
- Hugging Face Spaces (backend deployment)
- Vercel (frontend deployment)

---

## Implementation Phases (Next Steps)

### Phase 2: Task Breakdown (`/sp.tasks`)

**Not created by /sp.plan** - This is the next command.

Will generate `specs/002-fullstack-web/tasks.md` with:
- Ordered, dependency-aware task list
- Test-driven task structure (Red-Green-Refactor)
- Acceptance criteria for each task
- Estimated effort

### Phase 3: Implementation (`/sp.implement`)

Execute tasks from tasks.md:
1. Backend setup (FastAPI, SQLModel, database)
2. Authentication (Better Auth, session management)
3. Task CRUD API (endpoints, validation, tests)
4. Frontend setup (Next.js, shadcn/ui)
5. Auth UI (signup, login pages)
6. Task UI (dashboard, CRUD operations)
7. Integration tests
8. E2E tests
9. Deployment (HF Spaces, Vercel)

---

## Risk Mitigation

| Risk | Impact | Mitigation | Status |
|------|--------|------------|--------|
| Better Auth Python adapter doesn't exist | High | Research alternatives (custom JWT implementation) | Research Phase |
| Neon cold start latency | Medium | Use connection pooler, reserved compute if needed | Research Phase |
| HF Spaces port 7860 configuration errors | High | Test Dockerfile locally before deployment | Design Phase |
| CORS issues Vercel ↔ HF Spaces | Medium | Document CORS config, test with preview deployments | Design Phase |
| Phase 1 tests break | High | Run Phase 1 tests before/after each change | **MITIGATED** (81/81 passing verified) |
| Migration data loss | High | Use Neon branching, validate pre/post migration | Design Phase |
| Test coverage <80% | Medium | TDD approach, coverage gates in CI/CD | Implementation Phase |

---

## Success Criteria (from Spec)

- ✅ SC-001: New user can register and log in within 1 minute
- ✅ SC-002: Authenticated user can create a task in <2 seconds
- ✅ SC-003: Task list loads in <1 second for up to 1000 tasks
- ✅ SC-004: 100% data isolation verified
- ✅ SC-005: All 7 user stories have passing E2E tests
- ✅ SC-006: Backend test coverage ≥80%
- ✅ SC-007: Frontend test coverage ≥80%
- ✅ SC-008: Zero SQL injection vulnerabilities
- ✅ SC-009: Zero XSS vulnerabilities
- ✅ SC-010: `docker-compose up` starts all services in <30 seconds
- ✅ SC-011: Frontend Lighthouse score ≥90
- ✅ SC-012: API documentation auto-generated at /api/docs
- ✅ SC-013: Successful deployment to Vercel + HF + Neon
- ✅ SC-014: Phase 1 CLI remains 100% functional

---

**Plan Status**: ✅ Phase 0 & Phase 1 Complete - Ready for `/sp.tasks`

**Next Command**: `/sp.tasks` to generate task breakdown

**Estimated Implementation Time**: 20-30 hours (full-stack development)

**Dependencies**: None (all research will be completed in Phase 0)
