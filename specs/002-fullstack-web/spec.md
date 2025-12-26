# Phase 2 Specification: Full-Stack Web Application with Authentication and Task CRUD

**Feature ID:** 002-fullstack-web
**Version:** 1.0.0
**Phase:** Phase II – Full-Stack Web Application
**Status:** Draft → Ready for /sp.plan
**Linked Constitution:** @.specify/memory/constitution.md
**Linked Phase 1 Spec:** @specs/001-cli-todo-app/spec.md
**Points:** 150 (Hackathon II)
**Date:** 2025-12-26
**Author:** Architect (shery123pk) + AI Developer (Claude)

---

## Problem Statement

Transform the Phase 1 CLI todo application into a modern, multi-user full-stack web application with persistent storage and user authentication. The system must support secure user registration/login and provide a responsive web interface for managing personal tasks (CRUD operations) while enforcing strict data isolation between users.

All implementation must follow Spec-Driven Development using Claude Code and Spec-Kit Plus. Humans act as architects only – no manual code writing.

This phase preserves all Phase 1 semantics (task fields, validation rules, operation behavior) while extending with authentication, persistence, and web interfaces.

**Critical Requirement**: Phase 1 CLI must remain fully functional as a standalone application. Phase 2 adds web capabilities but does not replace or break Phase 1.

---

## Key Entities

### User
- `id`: UUID (primary key, immutable)
- `email`: string (unique, indexed, lowercase normalized)
- `email_verified`: boolean (default false)
- `name`: string (optional, max 255 characters)
- `hashed_password`: string (bcrypt hashed, never exposed)
- `created_at`: ISO 8601 timestamp (UTC)
- `updated_at`: ISO 8601 timestamp (UTC)

### Task (extends Phase 1 core)
- `id`: UUID (primary key, immutable) - **Changed from int in Phase 1** per ADR-001
- `user_id`: UUID (foreign key → users.id, indexed, NOT NULL)
- `title`: string (required, 1–200 characters)
- `description`: string (optional, max 1000 characters)
- `completed`: boolean (default false, indexed)
- `priority`: enum["low", "medium", "high", "critical"] (optional, default null)
- `tags`: array of strings (optional, default empty array)
- `category`: string (optional, max 50 characters)
- `created_at`: ISO 8601 timestamp (UTC, indexed)
- `updated_at`: ISO 8601 timestamp (UTC)

### Session (Better Auth)
- `id`: UUID (primary key)
- `user_id`: UUID (foreign key → users.id)
- `token`: string (unique, indexed)
- `expires_at`: ISO 8601 timestamp
- `ip_address`: inet (optional)
- `user_agent`: string (optional)

### Account (Better Auth - OAuth)
- `id`: UUID (primary key)
- `user_id`: UUID (foreign key → users.id)
- `provider`: string ("email", "google", "github")
- `provider_account_id`: string (unique per provider)
- `access_token`: text (encrypted)
- `refresh_token`: text (encrypted)
- `expires_at`: ISO 8601 timestamp

---

## User Stories & Acceptance Criteria

### User Story 1 – User Registration (Priority: P1)

**As a new user,** I want to sign up with email and password so I can create an account and start managing my tasks.

**Acceptance Criteria:**

1. **AC-1.1**: Valid email + password (≥8 chars) → account created, password hashed with bcrypt (cost factor 12), redirect to login with success message "Account created successfully! Please log in."
2. **AC-1.2**: Invalid email format → error "Please enter a valid email address" (validated against RFC 5322 regex)
3. **AC-1.3**: Password <8 characters → error "Password must be at least 8 characters"
4. **AC-1.4**: Duplicate email (case-insensitive) → error "An account with this email already exists"
5. **AC-1.5**: Email automatically normalized to lowercase before storage
6. **AC-1.6**: Password never stored in plaintext, never logged, never exposed in API responses
7. **AC-1.7**: Registration form accessible without authentication
8. **AC-1.8**: Link to login page: "Already have an account? Log in"

**Test Scenarios:**
```gherkin
Scenario: Successful registration
  Given I am on the registration page
  When I enter email "user@example.com" and password "securepass123"
  And I click "Sign Up"
  Then I should see "Account created successfully"
  And I should be redirected to "/auth/signin"
  And the password should be bcrypt hashed in the database

Scenario: Duplicate email
  Given user "existing@example.com" already exists
  When I try to register with "existing@example.com"
  Then I should see error "An account with this email already exists"
  And I should remain on the registration page
```

---

### User Story 2 – User Login (Priority: P1)

**As a registered user,** I want to log in with my credentials so I can access my personal task dashboard.

**Acceptance Criteria:**

1. **AC-2.1**: Correct credentials → Better Auth session created, httpOnly cookie set (7-day expiry), redirect to "/tasks"
2. **AC-2.2**: Incorrect password or non-existent email → error "Invalid email or password" (identical message to prevent user enumeration)
3. **AC-2.3**: Valid session token after browser close/reopen (within 7 days) → remain authenticated, no re-login required
4. **AC-2.4**: Session cookie attributes: httpOnly=true, secure=true (production), sameSite=lax, path=/
5. **AC-2.5**: Rate limiting: Max 5 login attempts per IP per minute (429 Too Many Requests after limit)
6. **AC-2.6**: Login form accessible without authentication
7. **AC-2.7**: Link to registration: "Don't have an account? Sign up"
8. **AC-2.8**: "Remember me" option extends session to 30 days

**Test Scenarios:**
```gherkin
Scenario: Successful login
  Given user "user@example.com" with password "securepass123" exists
  When I enter correct credentials and click "Sign In"
  Then I should see "Welcome back!"
  And I should be redirected to "/tasks"
  And session cookie should be set with httpOnly flag

Scenario: Failed login (wrong password)
  Given user "user@example.com" exists
  When I enter email "user@example.com" and wrong password
  Then I should see "Invalid email or password"
  And no session should be created
```

---

### User Story 3 – View All My Tasks (Priority: P2)

**As a logged-in user,** I want to view all my tasks so I can see what needs to be done.

**Acceptance Criteria:**

1. **AC-3.1**: Dashboard at "/tasks" shows only tasks belonging to authenticated user (filtered by user_id)
2. **AC-3.2**: Tasks sorted by created_at DESC (newest first) by default
3. **AC-3.3**: Each task displays: title, description (truncated to 100 chars with "..." if longer), completion status, created date (relative: "2 days ago")
4. **AC-3.4**: Completed tasks visually distinguished with strikethrough title + green checkmark icon
5. **AC-3.5**: Incomplete tasks show empty checkbox
6. **AC-3.6**: No tasks → empty state with illustration + message: "You don't have any tasks yet. Create your first task to get started!" + "Add Task" button
7. **AC-3.7**: Other users' tasks NEVER visible regardless of URL manipulation
8. **AC-3.8**: Page shows total count: "X tasks (Y completed)"
9. **AC-3.9**: Loading state: skeleton UI while fetching tasks
10. **AC-3.10**: Error state: "Failed to load tasks. Please try again." with retry button

**Test Scenarios:**
```gherkin
Scenario: View my tasks only
  Given I am logged in as "user1@example.com"
  And user1 has 3 tasks
  And user2 has 5 tasks
  When I visit "/tasks"
  Then I should see exactly 3 tasks
  And all tasks should belong to user1
  And I should not see user2's tasks

Scenario: Empty task list
  Given I am logged in with no tasks
  When I visit "/tasks"
  Then I should see "You don't have any tasks yet"
  And I should see "Add Task" button
```

---

### User Story 4 – Create New Task (Priority: P2)

**As a logged-in user,** I want to create a new task with title and optional description.

**Acceptance Criteria:**

1. **AC-4.1**: "Add Task" button opens modal/form with fields: title (required), description (optional)
2. **AC-4.2**: Valid title (1–200 chars) + optional description (≤1000 chars) → task saved with:
   - Auto-generated UUID for id
   - user_id set to authenticated user
   - created_at and updated_at set to current UTC timestamp
   - completed defaults to false
3. **AC-4.3**: Task appears at top of list immediately (optimistic UI update)
4. **AC-4.4**: Success message: "Task created successfully!"
5. **AC-4.5**: Empty title → error "Title is required" (client + server validation)
6. **AC-4.6**: Title >200 chars → error "Title must be 200 characters or less"
7. **AC-4.7**: Description >1000 chars → error "Description must be 1000 characters or less"
8. **AC-4.8**: Empty description allowed (stored as empty string)
9. **AC-4.9**: Unauthenticated user → redirect to "/auth/signin"
10. **AC-4.10**: Form resets after successful creation
11. **AC-4.11**: ESC key or "Cancel" button closes form without creating
12. **AC-4.12**: Duplicate titles allowed (no uniqueness constraint)

**Test Scenarios:**
```gherkin
Scenario: Create task with title only
  Given I am logged in
  When I click "Add Task"
  And I enter title "Buy groceries"
  And I click "Create"
  Then I should see "Task created successfully"
  And task "Buy groceries" should appear at the top of my list
  And the task should have my user_id

Scenario: Create task with title and description
  Given I am logged in
  When I create task with title "Buy groceries" and description "Milk, eggs, bread"
  Then both fields should be saved correctly
  And the task should be visible immediately
```

---

### User Story 5 – Mark Task Complete/Incomplete (Priority: P3)

**As a logged-in user,** I want to toggle completion status with one click.

**Acceptance Criteria:**

1. **AC-5.1**: Click checkbox → status flips (true ↔ false)
2. **AC-5.2**: Optimistic UI update: visual change immediate (before server confirmation)
3. **AC-5.3**: updated_at timestamp updated on server
4. **AC-5.4**: Changes persisted to database
5. **AC-5.5**: Page refresh → status persists
6. **AC-5.6**: Completed task → checkbox checked, title strikethrough, move to bottom (optional)
7. **AC-5.7**: Incomplete task → checkbox unchecked, normal title
8. **AC-5.8**: Task not owned by user → 404 error (not 403)
9. **AC-5.9**: If toggle fails (network error), revert UI with error message
10. **AC-5.10**: Keyboard accessible: Space or Enter toggles checkbox

**Test Scenarios:**
```gherkin
Scenario: Mark task complete
  Given I have an incomplete task "Buy groceries"
  When I click the checkbox
  Then the task should be marked complete immediately
  And the title should have strikethrough
  And the database should reflect completed=true

Scenario: Toggle back to incomplete
  Given I have a completed task
  When I click the checkbox again
  Then the task should be marked incomplete
  And the strikethrough should be removed
```

---

### User Story 6 – Update Task (Priority: P3)

**As a logged-in user,** I want to edit title/description of my tasks.

**Acceptance Criteria:**

1. **AC-6.1**: Click "Edit" button/icon → opens edit form with current values pre-filled
2. **AC-6.2**: Modify title and/or description → click "Save" → changes persisted
3. **AC-6.3**: updated_at timestamp updated
4. **AC-6.4**: Changes visible immediately after save
5. **AC-6.5**: Empty title on save → error "Title is required"
6. **AC-6.6**: Title >200 chars → error "Title must be 200 characters or less"
7. **AC-6.7**: Description >1000 chars → error "Description must be 1000 characters or less"
8. **AC-6.8**: Task not owned by user → 404 error
9. **AC-6.9**: "Cancel" button → discards changes, closes form
10. **AC-6.10**: Inline editing: click title/description to edit directly (optional)
11. **AC-6.11**: Completed status preserved during edit
12. **AC-6.12**: ESC key cancels edit

**Test Scenarios:**
```gherkin
Scenario: Update task title
  Given I have task "Buy groceries"
  When I click "Edit" and change title to "Buy groceries and milk"
  And I click "Save"
  Then the task title should update to "Buy groceries and milk"
  And updated_at should be current timestamp

Scenario: Cancel edit
  Given I start editing a task
  When I modify the title but click "Cancel"
  Then the original values should be preserved
  And no API call should be made
```

---

### User Story 7 – Delete Task (Priority: P4)

**As a logged-in user,** I want to permanently delete tasks I no longer need.

**Acceptance Criteria:**

1. **AC-7.1**: Click "Delete" button/icon → confirmation dialog appears
2. **AC-7.2**: Dialog message: "Are you sure you want to delete this task? This action cannot be undone."
3. **AC-7.3**: Dialog buttons: "Delete" (destructive red) and "Cancel"
4. **AC-7.4**: Click "Delete" → task permanently removed from database (hard delete, not soft delete)
5. **AC-7.5**: Success message: "Task deleted successfully"
6. **AC-7.6**: Task immediately removed from UI (optimistic update)
7. **AC-7.7**: Click "Cancel" → dialog closes, task remains
8. **AC-7.8**: Task not owned by user → 404 error
9. **AC-7.9**: Page refresh → deletion persists
10. **AC-7.10**: If delete fails, show error and restore task in UI
11. **AC-7.11**: ESC key cancels delete dialog

**Test Scenarios:**
```gherkin
Scenario: Delete task with confirmation
  Given I have task "Old task"
  When I click "Delete"
  Then I should see confirmation dialog
  When I click "Delete" in dialog
  Then task should be removed from database
  And task should disappear from UI
  And I should see "Task deleted successfully"

Scenario: Cancel delete
  Given I have task "Important task"
  When I click "Delete" but then click "Cancel"
  Then the task should remain unchanged
  And no deletion should occur
```

---

## Edge Cases & Security Scenarios

### Authentication Edge Cases

1. **Expired Session**:
   - **Scenario**: User's session expires while browsing
   - **Expected**: Redirect to login with message "Your session has expired. Please log in again."
   - **Test**: Set session expiry to past date, attempt protected route access

2. **No Session on Protected Route**:
   - **Scenario**: Unauthenticated user accesses "/tasks" directly
   - **Expected**: Immediate redirect to "/auth/signin" with returnUrl parameter
   - **Test**: Clear cookies, navigate to "/tasks"

3. **Concurrent Sessions**:
   - **Scenario**: User logs in on multiple devices
   - **Expected**: All sessions remain valid until individual expiry (not single-session)
   - **Test**: Login from 2 browsers, verify both work

4. **Session Hijacking Prevention**:
   - **Scenario**: Attacker steals session cookie
   - **Expected**: HttpOnly + Secure flags prevent XSS theft, session tied to IP/User-Agent (optional)
   - **Test**: Try to use session cookie from different IP

### Task Operation Edge Cases

5. **URL Manipulation (Unauthorized Access)**:
   - **Scenario**: User tries to access `/api/tasks/{other_user_task_id}` via URL
   - **Expected**: 404 Not Found (not 403 Forbidden to prevent info leakage)
   - **Test**: Create task as user1, attempt GET as user2 → 404

6. **Boundary Value Testing**:
   - **Scenario**: Title exactly 200 chars, description exactly 1000 chars
   - **Expected**: Accepted and saved correctly
   - **Test**: Create task with max-length strings

7. **Special Characters & HTML Input**:
   - **Scenario**: User enters `<script>alert('XSS')</script>` in title
   - **Expected**: Sanitized/escaped before rendering (prevent XSS)
   - **Test**: Inject various XSS payloads, verify sanitization

8. **SQL Injection Attempts**:
   - **Scenario**: User enters `'; DROP TABLE tasks; --` in title
   - **Expected**: Treated as literal string via parameterized queries, no SQL execution
   - **Test**: Attempt SQL injection payloads in all input fields

9. **Concurrent Updates (Race Condition)**:
   - **Scenario**: User edits same task in 2 browser tabs simultaneously
   - **Expected**: Last write wins (no optimistic locking in Phase 2)
   - **Test**: Update task from 2 tabs, verify final state

10. **Network Failure During Create/Update**:
    - **Scenario**: Network drops while creating task
    - **Expected**: UI shows error "Failed to save task. Please try again.", task not created
    - **Test**: Simulate network failure, verify retry mechanism

11. **Empty/Whitespace-Only Title**:
    - **Scenario**: User submits title with only spaces
    - **Expected**: Error "Title is required" (after trimming)
    - **Test**: Submit "   " as title

12. **Unicode & Emoji Input**:
    - **Scenario**: Title contains emoji 🎉 or non-ASCII characters
    - **Expected**: Saved and displayed correctly (UTF-8 encoding)
    - **Test**: Create task "生日派对 🎂"

13. **Very Long Session (>7 days)**:
    - **Scenario**: User remains logged in for >7 days without activity
    - **Expected**: Session expires, redirect to login on next action
    - **Test**: Mock system time, advance >7 days

14. **Deleted User's Tasks**:
    - **Scenario**: User account deleted (out of scope for Phase 2, but plan for Phase 3)
    - **Expected**: Cascade delete tasks (ON DELETE CASCADE foreign key)
    - **Test**: N/A for Phase 2

---

## Functional Requirements (FR)

### Authentication (FR-001 to FR-011)

- **FR-001**: System MUST provide user registration endpoint `POST /api/auth/signup` accepting email + password
- **FR-002**: System MUST validate email format (RFC 5322) before account creation
- **FR-003**: System MUST reject passwords <8 characters
- **FR-004**: System MUST hash passwords using bcrypt with cost factor ≥12
- **FR-005**: System MUST prevent duplicate email registration (case-insensitive check)
- **FR-006**: System MUST provide login endpoint `POST /api/auth/signin` accepting email + password
- **FR-007**: System MUST issue Better Auth session token on successful login
- **FR-008**: System MUST store session token in httpOnly cookie with 7-day expiry (30 days with "remember me")
- **FR-009**: System MUST validate session token on all protected routes
- **FR-010**: System MUST redirect unauthenticated users to `/auth/signin`
- **FR-011**: System MUST provide logout endpoint `POST /api/auth/signout` to clear session

### Task Management (FR-012 to FR-035)

#### Read Operations
- **FR-012**: System MUST provide endpoint `GET /api/tasks` returning all tasks for authenticated user
- **FR-013**: System MUST filter tasks by `user_id = authenticated_user.id` (mandatory)
- **FR-014**: System MUST sort tasks by `created_at DESC` by default
- **FR-015**: System MUST return task fields: id, title, description, completed, created_at, updated_at, priority, tags, category
- **FR-016**: System MUST provide endpoint `GET /api/tasks/{id}` for single task retrieval
- **FR-017**: System MUST return 404 if task.id not found OR task.user_id ≠ authenticated_user.id

#### Create Operations
- **FR-018**: System MUST provide endpoint `POST /api/tasks` accepting title, description (optional), priority, tags, category
- **FR-019**: System MUST auto-generate UUID for task.id
- **FR-020**: System MUST set task.user_id to authenticated user's id
- **FR-021**: System MUST set created_at and updated_at to current UTC timestamp
- **FR-022**: System MUST default completed to false
- **FR-023**: System MUST validate title: required, 1-200 chars
- **FR-024**: System MUST validate description: optional, max 1000 chars
- **FR-025**: System MUST return 201 Created with task object on success

#### Update Operations
- **FR-026**: System MUST provide endpoint `PATCH /api/tasks/{id}` accepting partial updates (title, description, completed, priority, tags, category)
- **FR-027**: System MUST update only provided fields (partial update)
- **FR-028**: System MUST update updated_at timestamp on every change
- **FR-029**: System MUST return 404 if task not owned by user
- **FR-030**: System MUST validate updated fields against same rules as create

#### Delete Operations
- **FR-031**: System MUST provide endpoint `DELETE /api/tasks/{id}`
- **FR-032**: System MUST perform hard delete (remove from database)
- **FR-033**: System MUST return 204 No Content on success
- **FR-034**: System MUST return 404 if task not owned by user
- **FR-035**: System MUST not allow recovery after deletion

### Security & Authorization (FR-036 to FR-040)

- **FR-036**: System MUST filter ALL task queries by authenticated user_id (no exceptions)
- **FR-037**: System MUST return 404 (not 403) when user attempts to access task they don't own
- **FR-038**: System MUST use parameterized queries for all database operations (prevent SQL injection)
- **FR-039**: System MUST sanitize user input to prevent XSS attacks
- **FR-040**: System MUST enforce rate limiting: 5 login attempts per IP per minute

### Error Handling (FR-041 to FR-043)

- **FR-041**: System MUST return user-friendly error messages (no stack traces in production)
- **FR-042**: System MUST use proper HTTP status codes (200, 201, 400, 401, 404, 429, 500)
- **FR-043**: System MUST log errors server-side without exposing sensitive data

---

## Non-Functional Requirements (NFR)

### Performance (NFR-001 to NFR-005)

- **NFR-001**: API response time MUST be <200ms for 95% of requests under normal load (10 concurrent users)
- **NFR-002**: Database queries MUST use indexes on: user_id, completed, created_at
- **NFR-003**: Frontend initial page load MUST be <2 seconds on 3G network
- **NFR-004**: Task list rendering MUST handle up to 1000 tasks without pagination (Phase 2 limit)
- **NFR-005**: API MUST support 100 requests/minute per user without degradation

### Security (NFR-006 to NFR-012)

- **NFR-006**: Passwords MUST be hashed using bcrypt with cost factor 12
- **NFR-007**: Session tokens MUST be stored in httpOnly cookies (not localStorage)
- **NFR-008**: All production API calls MUST use HTTPS (enforce with HSTS headers)
- **NFR-009**: User input MUST be sanitized to prevent XSS (use DOMPurify or equivalent)
- **NFR-010**: Database credentials MUST be stored in environment variables (never in code)
- **NFR-011**: No plaintext passwords MUST ever be logged or exposed in API responses
- **NFR-012**: CORS MUST be configured to allow only frontend domain

### Usability (NFR-013 to NFR-018)

- **NFR-013**: Empty states MUST provide clear guidance ("Create your first task")
- **NFR-014**: Success/error messages MUST be visible for 3-5 seconds
- **NFR-015**: Destructive actions (delete) MUST require confirmation
- **NFR-016**: Forms MUST show inline validation errors
- **NFR-017**: Loading states MUST use skeleton UI or spinners (not blank screens)
- **NFR-018**: All interactive elements MUST have hover/focus states

### Maintainability (NFR-019 to NFR-024)

- **NFR-019**: Backend code MUST use Python type hints (enforced by Pyright strict mode)
- **NFR-020**: Frontend code MUST use TypeScript strict mode
- **NFR-021**: Test coverage MUST be ≥80% for both frontend and backend
- **NFR-022**: API MUST have auto-generated OpenAPI/Swagger documentation
- **NFR-023**: Code MUST follow linting rules (Ruff for Python, ESLint for TypeScript)
- **NFR-024**: All async operations MUST have proper error handling

### Development Environment (NFR-025 to NFR-028)

- **NFR-025**: `docker-compose up` MUST start all services (backend, frontend, database)
- **NFR-026**: Hot reload MUST work within 3 seconds of code changes
- **NFR-027**: Environment variables MUST support `.env` files for local development
- **NFR-028**: Single environment variable (DATABASE_URL) MUST switch between local PostgreSQL and Neon

### Deployment (NFR-029 to NFR-033)

- **NFR-029**: Backend MUST deploy to Hugging Face Spaces via Docker SDK
- **NFR-030**: Backend MUST listen on port 7860 (Hugging Face Spaces requirement)
- **NFR-031**: Frontend MUST deploy to Vercel with zero-config (optimal Next.js support)
- **NFR-032**: Database MUST use Neon PostgreSQL serverless with branching for dev/staging/prod
- **NFR-033**: CORS MUST be configured to allow Vercel frontend domain to access HF Space backend

---

## Success Criteria (Measurable)

- **SC-001**: New user can register and log in within 1 minute
- **SC-002**: Authenticated user can create a task in <2 seconds (from click to visible)
- **SC-003**: Task list loads in <1 second for up to 1000 tasks
- **SC-004**: 100% data isolation verified: User A cannot see User B's tasks under any URL manipulation
- **SC-005**: All 7 user stories have passing E2E tests (Playwright)
- **SC-006**: Backend test coverage ≥80% (pytest-cov)
- **SC-007**: Frontend test coverage ≥80% (Vitest + React Testing Library)
- **SC-008**: Zero SQL injection vulnerabilities (verified by security scan)
- **SC-009**: Zero XSS vulnerabilities (verified by security scan)
- **SC-010**: `docker-compose up` starts all services in <30 seconds
- **SC-011**: Frontend Lighthouse score ≥90 (Performance, Accessibility, Best Practices, SEO)
- **SC-012**: API documentation auto-generated and accessible at `/api/docs`
- **SC-013**: Successful deployment to Vercel (frontend) + HuggingFace (backend) + Neon (database)
- **SC-014**: Phase 1 CLI remains 100% functional (all 81 tests still passing)

---

## Assumptions

1. **Browser Support**: Modern browsers only (Chrome, Firefox, Safari, Edge – last 2 years)
2. **Task Volume**: Average user has 0–1000 tasks (no pagination needed in Phase 2)
3. **Authentication Method**: Session-based with Better Auth (not OAuth in Phase 2)
4. **Email Verification**: Email format validation only (no verification email in Phase 2)
5. **Language**: English only (no i18n in Phase 2)
6. **Timezone**: Timestamps stored in UTC, displayed in user's local timezone (browser auto-detect)
7. **Single-User Editing**: No collaborative editing (no conflict resolution needed)
8. **Mobile Experience**: Responsive design, but not native mobile apps
9. **Search**: No full-text search in Phase 2 (simple list view only)
10. **Undo/Redo**: Not supported in Phase 2

---

## Out of Scope for Phase 2

### Features Deferred to Phase 3+

- Task filtering/sorting UI (beyond default newest-first)
- Search and full-text search
- Real-time updates (WebSocket/SSE)
- Push notifications
- Email notifications
- File attachments
- Rich text description editor
- Collaborative features (sharing tasks, teams)
- Subtasks and hierarchical tasks
- Task templates
- Recurring tasks
- Reminders and due date alerts

### UI/UX Deferred

- Dark mode toggle
- Customizable themes
- Drag-and-drop task reordering
- Bulk operations (select multiple, delete all completed)
- Export/import (CSV, JSON)
- Print view

### Advanced Auth Deferred

- OAuth providers (Google, GitHub)
- Two-factor authentication (2FA)
- Password reset via email
- Email verification
- Account deletion
- Profile management (avatar, bio)

### Technical Features Deferred

- Offline support (PWA)
- Mobile apps (iOS, Android)
- API versioning (v2)
- GraphQL API
- Webhooks
- Rate limiting per user (only per IP in Phase 2)
- Audit logs
- Data export compliance (GDPR)
- Internationalization (i18n)

---

## Technology Stack (from Constitution)

### Backend
- **Framework**: FastAPI 0.100+
- **Language**: Python 3.13+
- **Package Manager**: UV
- **ORM**: SQLModel (built on Pydantic + SQLAlchemy)
- **Database**: Neon PostgreSQL (serverless)
- **Migration Tool**: Alembic
- **Authentication**: Better Auth (with Python adapter)
- **Validation**: Pydantic models
- **Testing**: pytest, pytest-cov, pytest-asyncio
- **Type Checking**: Pyright (strict mode)
- **Linting**: Ruff
- **Deployment**: Hugging Face Spaces (Docker SDK, port 7860)

### Frontend
- **Framework**: Next.js 15 (App Router)
- **Language**: TypeScript 5 (strict mode)
- **Styling**: Tailwind CSS 4
- **Components**: shadcn/ui (Radix UI + Tailwind)
- **Authentication**: Better Auth client
- **HTTP Client**: fetch (native) with error handling
- **Form Validation**: Zod
- **Testing**: Vitest, React Testing Library, Playwright (E2E)
- **Linting**: ESLint
- **Deployment**: Vercel

### Database
- **Provider**: Neon PostgreSQL 16
- **Features**: Serverless, auto-scaling, branching (dev/staging/prod)
- **Connection Pooling**: Neon built-in pooler
- **SSL**: Required (sslmode=require)

### Development
- **Containerization**: Docker + Docker Compose
- **Local Database**: PostgreSQL 16 (Docker) OR Neon dev branch
- **Hot Reload**: FastAPI auto-reload, Next.js Fast Refresh
- **API Documentation**: OpenAPI (auto-generated by FastAPI)

---

## Migration from Phase 1

### Data Migration Strategy

**Goal**: Migrate existing Phase 1 JSON tasks to Phase 2 PostgreSQL database.

**Approach**:
1. Create "Phase 1 Migration" default user account
2. Read `cli/tasks.json`
3. Transform each task:
   - Generate new UUID for id (replace sequential int)
   - Add user_id (default migration user)
   - Add created_at/updated_at (use current timestamp)
   - Preserve title, description, completed
4. Insert into tasks table
5. Verify count matches (no data loss)

**Migration Script**: `backend/scripts/migrate_phase1_to_phase2.py`

**Rollback**: Restore from Neon snapshot (branching feature)

### Backward Compatibility

**Phase 1 CLI Independence**:
- Phase 1 CLI continues to use `cli/tasks.json` (local file)
- Phase 2 uses Neon PostgreSQL (cloud database)
- **No shared data** between Phase 1 and Phase 2 in production
- Migration script is **one-time, manual, optional**
- Users can run Phase 1 CLI standalone without any Phase 2 dependencies

**Semantic Compatibility**:
- CRUD operations have identical behavior (create, read, update, delete, complete)
- Validation rules unchanged (title 1-200, description max 1000)
- Completed is boolean only (true/false)

---

## Acceptance Testing Plan

### Test Levels

1. **Unit Tests** (Backend: pytest, Frontend: Vitest)
   - Model validation
   - Repository functions
   - API route handlers
   - React components

2. **Integration Tests** (Backend: pytest with TestClient)
   - API endpoints with database
   - Authentication flow
   - CRUD operations end-to-end

3. **E2E Tests** (Playwright)
   - Full user journeys (registration → login → CRUD → logout)
   - Cross-browser testing (Chrome, Firefox, Safari)
   - Mobile viewport testing

4. **Security Tests**
   - SQL injection attempts
   - XSS payload attempts
   - Session hijacking prevention
   - Rate limiting validation

### Test Coverage Targets

- Backend: ≥80% line coverage
- Frontend: ≥80% line coverage
- E2E: All 7 user stories covered

### Acceptance Criteria Validation

Each acceptance criterion (AC-X.Y) must have:
- At least 1 automated test
- Manual QA verification
- Documented in test report

---

## Related ADRs

- **ADR-001**: ID Migration Strategy (int → UUID) - Justifies UUID primary keys
- **ADR-002**: Monorepo Structure - Explains Phase 1 independence and Phase 2 coexistence
- **ADR-003**: Database Choice (Neon PostgreSQL) - Database selection rationale
- **ADR-004**: Authentication Strategy (Better Auth) - Auth approach justification
- **ADR-005**: Deployment Strategy (Hugging Face Spaces) - Backend hosting on HF Spaces (port 7860), frontend on Vercel

---

## Open Questions & Risks

### Open Questions
1. **Q1**: Should we implement password reset in Phase 2 or defer to Phase 3?
   - **Decision**: Defer to Phase 3 (out of scope)

2. **Q2**: Should tasks have soft delete (deleted_at) or hard delete?
   - **Decision**: Hard delete in Phase 2 (simpler), soft delete in Phase 3 if needed

3. **Q3**: Should we implement task filtering/sorting UI in Phase 2?
   - **Decision**: Basic default sort only (newest first), advanced filtering in Phase 3

### Risks

| Risk | Impact | Mitigation |
|------|--------|------------|
| Better Auth Python adapter doesn't exist | High | Create minimal adapter OR use custom JWT implementation |
| Neon cold start latency (>500ms) | Medium | Use connection pooler, warm-up queries, or Neon reserved compute |
| Phase 1 CLI tests break after restructure | High | Validate Phase 1 tests still pass (already verified: 81/81 passing) |
| Learning curve for Better Auth | Medium | Allocate extra time for authentication implementation |
| Deployment complexity (3 platforms) | Medium | Document deployment steps, automate with CI/CD scripts |

---

## Next Steps

1. ✅ **Specification Complete** → Architect reviews and approves
2. ⏳ **Invoke /sp.plan** → AI Engineer creates implementation plan
3. ⏳ **Invoke /sp.tasks** → Generate actionable, ordered tasks
4. ⏳ **Invoke /sp.implement** → Execute tasks with test-driven development
5. ⏳ **Review & Deploy** → Verify all success criteria, deploy to production

---

**Status**: Ready for Planning (`/sp.plan`)
**Approved By**: Architect (shery123pk)
**Date**: 2025-12-26
