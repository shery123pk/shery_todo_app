# Implementation Plan: Professional Multi-Tenant Project Management System

**Branch**: `001-project-management-system` | **Date**: 2025-12-27 | **Spec**: [spec.md](./spec.md)
**Input**: Feature specification from `/specs/001-project-management-system/spec.md`

**Note**: This template is filled in by the `/sp.plan` command. See `.specify/templates/commands/plan.md` for the execution workflow.

## Summary

This plan implements a production-grade, multi-tenant project management platform (similar to Jira/Linear/Trello) to replace the simple todo app. The system supports organizations (workspaces), projects, Kanban boards, tasks with rich metadata, role-based permissions, file attachments, comments, activity logging, and user authentication.

**Core Requirements**:
- Multi-tenant architecture with complete data isolation by organization
- Role-based access control (RBAC) at organization and project levels
- Kanban boards with drag-and-drop task management
- Sequential task numbering per project (WEB-1, WEB-2, etc.)
- File attachments up to 10MB per file
- Markdown support in task descriptions and comments
- @mentions for user notifications
- Email verification and password reset flows

**Technical Approach** (from constitution and design decisions):
- Backend: FastAPI with SQLModel ORM, Neon PostgreSQL, Better Auth JWT
- Frontend: Next.js 15 App Router, TypeScript strict mode, Tailwind CSS
- Architecture: Row-level multi-tenancy, UUID primary keys, position-based drag-and-drop ordering
- Testing: pytest (backend), Vitest (frontend), >80% coverage requirement

## Technical Context

**Language/Version**:
- Backend: Python 3.13+ (per constitution Phase 2+)
- Frontend: TypeScript 5.0+ (strict mode)

**Primary Dependencies**:
- Backend: FastAPI 0.110+, SQLModel (SQLAlchemy 2.0 + Pydantic v2), Better Auth, python-jose (JWT), aiofiles, aiosmtplib
- Frontend: Next.js 15+ (App Router), React 18+, Tailwind CSS v3, shadcn/ui, TanStack Query v5, Zustand, @dnd-kit/core, React Hook Form, Zod
- Shared: Neon PostgreSQL 15+ (serverless), UV (Python package manager)

**Storage**:
- Database: Neon PostgreSQL (serverless) with row-level security for multi-tenancy
- File Attachments: Local filesystem (MVP) → AWS S3 or Backblaze B2 (production)
- Sessions: Database-backed with JWT tokens in HttpOnly cookies

**Testing**:
- Backend: pytest with httpx (async client), >80% coverage
- Frontend: Vitest + React Testing Library, >80% coverage
- E2E: Playwright for critical user flows
- Contract Testing: Pydantic validation on all API boundaries

**Target Platform**:
- Backend: Linux server (containerized for deployment)
- Frontend: Modern browsers (Chrome 90+, Firefox 88+, Safari 14+, Edge 90+)
- Responsive design: Desktop (1920x1080, 1366x768), Tablet (768x1024), Mobile (375x667, 414x896)

**Project Type**: Web application (full-stack monorepo with separate frontend/ and backend/ directories)

**Performance Goals** (from spec success criteria):
- API response time: <200ms p95 for reads, <500ms p95 for writes
- Page load (FCP): <1.5 seconds
- Board render: <500ms for 100 tasks, <2s for 500 tasks
- Drag-and-drop: 60fps (16ms per frame) smooth animation
- Search results: <1 second for queries across 10,000 tasks
- File upload (5MB): <10 seconds on standard broadband

**Constraints**:
- Multi-tenant row-level security enforced on ALL queries
- Session expiration: 7 days (default), 30 days with "Remember Me"
- File upload limits: 10MB per file, 20 files per task
- Rate limiting: 100 req/min per IP, 500 req/min per authenticated user
- Password hashing: bcrypt with cost factor 12
- Email verification required before email notifications sent
- Backward compatibility: All Phase 2 todo app features must remain functional

**Scale/Scope**:
- Target users: 100 organizations × 50 users = 5,000 total users (MVP)
- Target tasks: 1,000 tasks per project, 10,000 tasks per organization
- Database: Single Postgres instance (MVP), read replicas (production)
- Concurrent users: 50 per organization (MVP), 200 per organization (production)
- Uptime SLO: 99.5% (MVP), 99.9% (production)

## Constitution Check

*GATE: Must pass before Phase 0 research. Re-check after Phase 1 design.*

### ✅ Spec-Driven Development (Article I)
- [x] Approved spec exists at `specs/001-project-management-system/spec.md`
- [x] Spec includes user stories, acceptance criteria, edge cases, test scenarios
- [x] Following SDD workflow: `/sp.specify` → `/sp.plan` (current) → `/sp.tasks` → `/sp.implement`
- [x] No implementation started before approved spec

### ✅ AI as Sole Developer (Article II)
- [x] Human (Architect) authored and approved spec
- [x] AI (Claude) generating plan, will generate tasks, code, tests
- [x] Clear role separation maintained

### ✅ Semantic Code Editing (Article III)
- [x] Plan acknowledges LSP-aware editing requirement for all code changes
- [x] Will use Pyright for Python, tsserver for TypeScript
- [x] No blind regex or text-based edits planned

### ✅ Full Traceability (Article IV)
- [x] Spec → Plan → Tasks → Code linkage established
- [x] PHRs will be created in `history/prompts/001-project-management-system/`
- [x] ADRs will be suggested for architectural decisions (multi-tenancy, auth, file storage)

### ✅ Test-First & Evolutionary Safeguards (Article V)
- [x] Test coverage target: >80% per constitution
- [x] Tests will be generated with/before code
- [x] Regression suite required: Phase 2 todo app must remain functional
- [x] E2E tests planned for critical flows (auth, task creation, board interaction)

### ✅ Technology Stack Compliance (Article: Technology Stack & Standards)
- [x] Backend: Python 3.13+, FastAPI, SQLModel, Pydantic ✓
- [x] Frontend: Next.js 15+, TypeScript strict, Tailwind CSS ✓
- [x] Database: Neon PostgreSQL ✓
- [x] Auth: Better Auth with JWT ✓
- [x] Package Management: UV for Python ✓
- [x] Testing: pytest (backend), Vitest (frontend) ✓
- [x] Dependency Injection: FastAPI DI patterns ✓

### ✅ Domain Model Evolution (Article: Unified Domain Model)
- [x] Preserves Phase 1 core fields: id (UUID), title, description, completed
- [x] Preserves Phase 2 additions: priority, tags, category, timestamps
- [x] Extends with: organization_id, project_id, board_id, column_id, assignee_id, reporter_id, due_date, position, labels
- [x] Maintains invariant: `id` never mutates, `completed` is binary
- [x] Migration plan required for Phase 2 → Project Management System transition

### ⚠️ Backward Compatibility (Article: Phase Evolution Roadmap)
- [x] **CRITICAL**: Phase 2 todo app features must remain functional
- [x] Strategy: Treat existing `tasks` table as project tasks within a "Personal" organization
- [x] Migration: Auto-create default organization for existing users
- [x] Testing: Regression tests for all Phase 2 endpoints (/api/tasks, /api/auth, /api/chatbot)

### 📋 Architectural Decisions Requiring ADRs

Based on Article: Architectural Decision Records, the following decisions meet significance criteria (Impact + Alternatives + Scope):

1. **Multi-Tenant Architecture Pattern**
   - Impact: Long-term consequences for data isolation, query performance, security
   - Alternatives: Row-level security vs separate databases vs schema-based
   - Scope: Cross-cutting, affects all data access patterns
   - **Recommendation**: Document in ADR before implementation

2. **Sequential Task Numbering Implementation**
   - Impact: Concurrency handling, database constraints, user experience
   - Alternatives: Database sequences, atomic counters, UUID fallback
   - Scope: Affects task creation, URLs, user communication
   - **Recommendation**: Document in ADR before implementation

3. **File Storage Strategy**
   - Impact: Scalability, cost, security, backup/restore
   - Alternatives: Local filesystem, S3, Backblaze B2, database BLOBs
   - Scope: Affects deployment, data portability, disaster recovery
   - **Recommendation**: Document in ADR before implementation

### ✅ Forbidden Practices Check
- [x] No manual code writing planned (AI-generated only)
- [x] No hard-coded secrets (using .env files)
- [x] No direct DB access from frontend (API layer enforced)
- [x] No unparameterized queries (SQLModel ORM)
- [x] No vendor lock-in (standard PostgreSQL, standard REST APIs)
- [x] No blind regex edits (LSP-aware tools required)

### Constitution Compliance Summary

**Status**: ✅ PASS - Ready to proceed with Phase 0 research

**Violations**: None

**Deferred Decisions**: 3 ADRs recommended before implementation (multi-tenancy, task numbering, file storage)

## Project Structure

### Documentation (this feature)

```text
specs/[###-feature]/
├── plan.md              # This file (/sp.plan command output)
├── research.md          # Phase 0 output (/sp.plan command)
├── data-model.md        # Phase 1 output (/sp.plan command)
├── quickstart.md        # Phase 1 output (/sp.plan command)
├── contracts/           # Phase 1 output (/sp.plan command)
└── tasks.md             # Phase 2 output (/sp.tasks command - NOT created by /sp.plan)
```

### Source Code (repository root)

```text
backend/
├── app/
│   ├── models/              # SQLModel entities
│   │   ├── user.py          # User, Session, Notification
│   │   ├── organization.py  # Organization, OrganizationMember, Invitation
│   │   ├── project.py       # Project, ProjectMember
│   │   ├── board.py         # Board, Column
│   │   ├── task.py          # Task
│   │   ├── comment.py       # Comment
│   │   ├── attachment.py    # Attachment
│   │   └── activity.py      # ActivityLog
│   ├── routers/             # FastAPI route handlers
│   │   ├── auth.py          # /api/auth/* (signup, signin, signout, verify, reset)
│   │   ├── organizations.py # /api/organizations/*
│   │   ├── invitations.py   # /api/invitations/*
│   │   ├── projects.py      # /api/organizations/{slug}/projects, /api/projects/*
│   │   ├── boards.py        # /api/projects/{key}/boards, /api/boards/*
│   │   ├── columns.py       # /api/boards/{id}/columns, /api/columns/*
│   │   ├── tasks.py         # /api/projects/{key}/tasks, /api/tasks/*
│   │   ├── comments.py      # /api/tasks/{id}/comments, /api/comments/*
│   │   ├── attachments.py   # /api/tasks/{id}/attachments, /api/attachments/*
│   │   ├── notifications.py # /api/notifications/*
│   │   ├── dashboard.py     # /api/organizations/{slug}/dashboard, /api/users/me/tasks
│   │   └── search.py        # /api/organizations/{slug}/search
│   ├── services/            # Business logic
│   │   ├── auth_service.py
│   │   ├── email_service.py
│   │   ├── file_service.py
│   │   ├── notification_service.py
│   │   └── task_numbering_service.py
│   ├── dependencies.py      # FastAPI dependency injection
│   ├── database.py          # Database connection and session management
│   ├── config.py            # Settings (Pydantic BaseSettings)
│   └── main.py              # FastAPI app initialization
├── tests/
│   ├── conftest.py          # pytest fixtures
│   ├── test_auth.py
│   ├── test_organizations.py
│   ├── test_projects.py
│   ├── test_boards.py
│   ├── test_tasks.py
│   ├── test_comments.py
│   ├── test_attachments.py
│   └── test_regression.py   # Ensure Phase 2 todo app still works
├── alembic/                 # Database migrations
│   └── versions/
├── pyproject.toml           # UV dependencies
└── README.md

frontend/
├── app/                     # Next.js App Router
│   ├── layout.tsx           # Root layout
│   ├── page.tsx             # Landing/dashboard page
│   ├── auth/
│   │   ├── signin/          # Sign in page
│   │   ├── signup/          # Sign up page
│   │   ├── verify/          # Email verification page
│   │   └── reset/           # Password reset page
│   ├── [orgSlug]/           # Organization workspace
│   │   ├── layout.tsx       # Org-level layout with sidebar
│   │   ├── page.tsx         # Org dashboard
│   │   ├── settings/        # Org settings
│   │   ├── members/         # Org members management
│   │   └── [projectKey]/    # Project workspace
│   │       ├── page.tsx     # Project dashboard
│   │       ├── board/       # Kanban board view
│   │       ├── settings/    # Project settings
│   │       └── members/     # Project members
│   └── me/                  # User profile and tasks
│       ├── tasks/           # My Tasks view
│       ├── profile/         # User profile settings
│       └── notifications/   # Notification center
├── components/
│   ├── ui/                  # shadcn/ui components
│   ├── layout/              # Layout components (navbar, sidebar, footer)
│   ├── auth/                # Auth-related components
│   ├── board/               # Kanban board components (Column, TaskCard, etc.)
│   ├── task/                # Task detail modal, task forms
│   ├── comment/             # Comment thread, comment form
│   └── common/              # Shared components (Avatar, Badge, etc.)
├── lib/
│   ├── api.ts               # API client (fetch wrappers)
│   ├── auth.ts              # Auth utilities
│   ├── hooks/               # Custom React hooks
│   └── utils.ts             # Utility functions
├── stores/                  # Zustand stores
│   ├── authStore.ts
│   ├── uiStore.ts
│   └── boardStore.ts
├── types/                   # TypeScript type definitions
│   ├── api.ts               # API response types
│   └── models.ts            # Domain model types
├── tests/
│   ├── components/          # Component tests (Vitest + React Testing Library)
│   └── e2e/                 # E2E tests (Playwright)
├── public/                  # Static assets
├── package.json
├── tsconfig.json
├── tailwind.config.ts
└── README.md

shared/                      # Shared configuration and documentation
├── docs/
│   └── api-contracts/       # OpenAPI/REST API documentation
└── .env.example             # Example environment variables
```

**Structure Decision**:

This is a **Web Application** (full-stack monorepo) with separate `backend/` and `frontend/` directories as per constitution Phase 2+ requirements.

**Key Design Decisions**:

1. **Backend Structure**:
   - Models organized by domain entity (user, organization, project, board, task, etc.)
   - Routers follow RESTful resource hierarchy
   - Services layer for business logic (auth, email, file storage, task numbering)
   - FastAPI dependency injection for auth and database sessions

2. **Frontend Structure**:
   - Next.js 15 App Router with parallel routes for org/project navigation
   - Dynamic routes: `[orgSlug]/[projectKey]` for clean URLs
   - Component organization: UI primitives, layout, features, domain-specific
   - Zustand for client state, TanStack Query for server state

3. **Testing Strategy**:
   - Backend: pytest with fixtures for auth, DB, and API testing
   - Frontend: Vitest for component tests, Playwright for E2E
   - Regression tests ensure Phase 2 todo app endpoints still work

4. **Migration Plan** (backward compatibility):
   - Create default "Personal" organization for existing users
   - Map existing `tasks` table to project tasks within default org
   - Preserve `/api/tasks` endpoint for Phase 2 compatibility

## Complexity Tracking

> **Fill ONLY if Constitution Check has violations that must be justified**

**Status**: N/A - No constitution violations detected. All complexity is justified by functional requirements in the spec.
