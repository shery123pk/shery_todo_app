# Implementation Tasks: Full-Stack Web Application

**Feature**: 002-fullstack-web
**Branch**: `002-fullstack-web`
**Date**: 2025-12-26
**Plan**: [plan.md](./plan.md)
**Spec**: [spec.md](./spec.md)

---

## Overview

This document defines the implementation tasks for Phase 2 Full-Stack Web Application. Tasks are organized by user story to enable independent implementation and testing. Each user story phase is a complete, independently testable increment.

**Task Organization Principle**: User story-driven phases (not layer-driven). Each phase delivers a vertical slice of functionality.

**Total Tasks**: 76
**User Stories**: 7 (US1-US7)
**MVP Milestone**: Phases 1-4 (T001-T029) - Authentication complete

---

## User Story Priorities (from spec.md)

| Priority | User Story | Description |
|----------|-----------|-------------|
| P1 (Critical) | US1 | User Registration - Account creation foundation |
| P1 (Critical) | US2 | User Login - Authentication and session management |
| P2 (High) | US3 | View All My Tasks - Display user's task list |
| P2 (High) | US4 | Create New Task - Add tasks to list |
| P3 (Medium) | US5 | Mark Task Complete/Incomplete - Toggle completion status |
| P3 (Medium) | US6 | Update Task - Edit task title and description |
| P4 (Low) | US7 | Delete Task - Permanently remove tasks |

---

## Phase 1: Setup & Infrastructure

**Goal**: Initialize monorepo structure, Docker environment, and development tools

**Duration**: ~1-2 hours

**Prerequisites**: Python 3.13+, Node.js 20+, Docker, UV installed

**Tasks**:

- [ ] T001 Create monorepo directory structure (frontend/, backend/, cli/, specs/, history/, infra/)
- [ ] T002 [P] Initialize backend/ with FastAPI project structure using UV (pyproject.toml, app/ directory)
- [ ] T003 [P] Initialize frontend/ with Next.js 15 App Router (npx create-next-app@latest)
- [ ] T004 [P] Create backend/pyproject.toml with dependencies (FastAPI, SQLModel, Alembic, python-jose, passlib, pytest)
- [ ] T005 [P] Create frontend/package.json with dependencies (Next.js 15, React 19, Tailwind CSS 4, shadcn/ui, Zod)
- [ ] T006 [P] Create backend/.env.example with DATABASE_URL, BETTER_AUTH_SECRET, BETTER_AUTH_URL, FRONTEND_URL
- [ ] T007 [P] Create frontend/.env.local.example with NEXT_PUBLIC_API_URL, BETTER_AUTH_URL, BETTER_AUTH_SECRET
- [ ] T008 [P] Create docker-compose.yml with postgres, backend, frontend services
- [ ] T009 [P] Create backend/Dockerfile for HuggingFace Spaces (port 7860 CRITICAL)
- [ ] T010 [P] Create frontend/Dockerfile for optional static export
- [ ] T011 [P] Initialize Alembic in backend/ directory (alembic init alembic)
- [ ] T012 [P] Create backend/alembic.ini with Neon PostgreSQL connection string template
- [ ] T013 [P] Create backend/.gitignore (exclude __pycache__, .env, .pytest_cache)
- [ ] T014 [P] Create frontend/.gitignore (exclude node_modules/, .next/, .env.local)
- [ ] T015 Verify setup: docker-compose up -d succeeds, services accessible (postgres:5432, backend:8000, frontend:3000)

**Acceptance Criteria**:
- ✅ Directory structure matches plan.md
- ✅ All services start with `docker-compose up -d`
- ✅ Backend accessible at http://localhost:8000
- ✅ Frontend accessible at http://localhost:3000
- ✅ PostgreSQL accessible at localhost:5432

---

## Phase 2: Foundational Infrastructure

**Goal**: Implement database models, migrations, and core dependencies (blocking prerequisites)

**Duration**: ~2-3 hours

**Dependencies**: Phase 1 complete

**Tasks**:

- [ ] T016 [P] Create backend/app/config.py with BaseSettings (DATABASE_URL, BETTER_AUTH_SECRET, DEBUG, CORS_ORIGINS)
- [ ] T017 [P] Create backend/app/database.py with SQLModel engine and get_session dependency
- [ ] T018 [P] Create backend/app/models/__init__.py (empty for imports)
- [ ] T019 [P] Create backend/app/models/user.py with User SQLModel (id UUID, email, hashed_password, name, created_at, updated_at)
- [ ] T020 [P] Create backend/app/models/task.py with Task SQLModel (id UUID, user_id FK, title, description, completed, priority, tags, category, timestamps)
- [ ] T021 [P] Create backend/app/models/session.py with Session SQLModel (id UUID, user_id FK, token, expires_at, ip_address, user_agent, created_at)
- [ ] T022 [P] Create backend/app/models/account.py with Account SQLModel (id UUID, user_id FK, provider, provider_account_id, access_token, refresh_token, expires_at, created_at)
- [ ] T023 Create backend/alembic/versions/001_initial_schema.py migration (create users, tasks, sessions, accounts tables with indexes)
- [ ] T024 [P] Create backend/app/security.py with password hashing (hash_password, verify_password using passlib bcrypt)
- [ ] T025 [P] Create backend/app/security.py with JWT functions (create_access_token, decode_access_token using python-jose)
- [ ] T026 [P] Create backend/app/dependencies.py with get_current_user dependency (JWT validation, session check)
- [ ] T027 [P] Create backend/app/main.py with FastAPI app, CORS middleware, health check endpoint
- [ ] T028 Run alembic upgrade head, verify models import without errors in Python shell
- [ ] T029 [P] Create backend/app/schemas/__init__.py (empty for imports)

**Acceptance Criteria**:
- ✅ Database tables created successfully (users, tasks, sessions, accounts)
- ✅ All 12 indexes created (see data-model.md)
- ✅ Foreign key constraints with CASCADE delete
- ✅ SQLModel models import without errors
- ✅ JWT token generation and validation works
- ✅ Password hashing with bcrypt cost factor 12

---

## Phase 3: User Story 1 – User Registration (P1)

**User Story**: As a new user, I want to sign up with email and password so I can create an account and start managing my tasks.

**Goal**: Allow new users to create accounts with email and password

**Duration**: ~3-4 hours

**Dependencies**: Phase 2 (Foundational) complete

**Independent Test Criteria**:
- ✅ Can access registration page at http://localhost:3000/auth/signup
- ✅ Submit valid email + password (8+ chars)
- ✅ Verify account created in database with hashed password
- ✅ Redirected to login page with success message

**Tasks**:

- [ ] T030 [P] [US1] Create backend/app/schemas/auth.py with SignupRequest Pydantic model (email EmailStr, password str min 8 chars, name optional)
- [ ] T031 [P] [US1] Create backend/app/schemas/auth.py with UserRead Pydantic model (id UUID, email, name, email_verified, created_at)
- [ ] T032 [P] [US1] Create backend/app/routers/__init__.py (empty for imports)
- [ ] T033 [US1] Create POST /api/auth/signup endpoint in backend/app/routers/auth.py (validate email format, check duplicate, hash password, create user, return UserRead)
- [ ] T034 [P] [US1] Create frontend/app/auth/signup/page.tsx Server Component with registration page layout and SEO metadata
- [ ] T035 [P] [US1] Create frontend/components/auth/SignupForm.tsx Client Component (email input, password input, name input, client-side validation)
- [ ] T036 [P] [US1] Create frontend/lib/validations.ts with Zod schemas (signupSchema with email, password 8+ chars, name optional)
- [ ] T037 [P] [US1] Create frontend/lib/api.ts with signup method (POST /api/auth/signup, handle 400/409 errors)
- [ ] T038 [US1] Wire SignupForm to API client, handle success (redirect to /auth/signin with toast message), handle errors (display inline)
- [ ] T039 [US1] Register auth router in backend/app/main.py (app.include_router(auth_router, prefix="/api/auth"))

**Acceptance Scenarios**:

| Scenario | Input | Expected Output |
|----------|-------|-----------------|
| Valid signup | email: "test@example.com", password: "securepass123", name: "Test User" | 201 Created, user in DB with bcrypt hash, redirect to /auth/signin |
| Invalid email | email: "invalid-email", password: "securepass123" | 400 Bad Request, error: "Please enter a valid email address" |
| Short password | email: "test@example.com", password: "short" | 400 Bad Request, error: "Password must be at least 8 characters" |
| Duplicate email | email: "existing@example.com" (already in DB) | 409 Conflict, error: "An account with this email already exists" |
| Empty name | email: "test@example.com", password: "securepass123", name: null | 201 Created, user.name = null |

**Test Commands** (run after tasks complete):
```bash
# Backend: Test signup endpoint
curl -X POST http://localhost:8000/api/auth/signup \
  -H "Content-Type: application/json" \
  -d '{"email":"test@example.com","password":"testpass123","name":"Test User"}'

# Frontend: Manual test
# 1. Navigate to http://localhost:3000/auth/signup
# 2. Enter email, password (8+ chars), name
# 3. Submit form
# 4. Verify redirect to /auth/signin
# 5. Check database: SELECT * FROM users WHERE email='test@example.com';
```

---

## Phase 4: User Story 2 – User Login (P1)

**User Story**: As a registered user, I want to log in with my credentials so I can access my personal task dashboard.

**Goal**: Allow registered users to authenticate and access their dashboard

**Duration**: ~4-5 hours

**Dependencies**: Phase 3 (US1 Registration) complete (users must exist to log in)

**Independent Test Criteria**:
- ✅ Can access login page at http://localhost:3000/auth/signin
- ✅ Enter valid credentials (registered user)
- ✅ Receive JWT token in httpOnly cookie
- ✅ Redirected to /tasks dashboard
- ✅ Token persists after browser close/reopen (within 7 days)

**Tasks**:

- [ ] T040 [P] [US2] Add SigninRequest Pydantic model to backend/app/schemas/auth.py (email EmailStr, password str, remember_me bool default false)
- [ ] T041 [P] [US2] Add TokenResponse Pydantic model to backend/app/schemas/auth.py (user UserRead)
- [ ] T042 [US2] Create POST /api/auth/signin endpoint in backend/app/routers/auth.py (find user, verify password, create session, set httpOnly cookie, return TokenResponse)
- [ ] T043 [US2] Add session creation logic to signin endpoint (generate JWT, store in sessions table with 7 or 30 day expiry based on remember_me)
- [ ] T044 [US2] Create POST /api/auth/signout endpoint in backend/app/routers/auth.py (delete session from DB, clear cookie, return 204 No Content)
- [ ] T045 [US2] Create GET /api/auth/me endpoint in backend/app/routers/auth.py (get current user from JWT, check session expiry, return UserRead or 401)
- [ ] T046 [P] [US2] Create backend/app/middleware/auth.py with get_current_user dependency (extract token from cookie, validate JWT, check session in DB, return User or raise 401)
- [ ] T047 [P] [US2] Add rate limiting to signin endpoint (max 5 attempts per IP per minute, return 429 if exceeded)
- [ ] T048 [P] [US2] Create frontend/middleware.ts with auth middleware (check session token, redirect to /auth/signin if missing or expired, protect /tasks/* routes)
- [ ] T049 [P] [US2] Create frontend/app/auth/signin/page.tsx Server Component with login page layout
- [ ] T050 [P] [US2] Create frontend/components/auth/SigninForm.tsx Client Component (email input, password input, remember me checkbox, client-side validation)
- [ ] T051 [P] [US2] Add Zod signinSchema to frontend/lib/validations.ts (email, password, rememberMe boolean)
- [ ] T052 [P] [US2] Add signin method to frontend/lib/api.ts (POST /api/auth/signin with credentials: 'include')
- [ ] T053 [P] [US2] Add signout method to frontend/lib/api.ts (POST /api/auth/signout with credentials: 'include')
- [ ] T054 [P] [US2] Add getCurrentUser method to frontend/lib/api.ts (GET /api/auth/me with credentials: 'include')
- [ ] T055 [US2] Wire SigninForm to API client, handle success (redirect to /tasks), handle errors (display "Invalid email or password")
- [ ] T056 [US2] Test authentication flow: signup → signin → verify /tasks accessible → signout → verify /tasks redirects to /auth/signin

**Acceptance Scenarios**:

| Scenario | Input | Expected Output |
|----------|-------|-----------------|
| Valid credentials | email: "test@example.com", password: "testpass123" | 200 OK, JWT cookie set (httpOnly, Secure, SameSite=Lax), redirect to /tasks |
| Invalid password | email: "test@example.com", password: "wrongpass" | 401 Unauthorized, error: "Invalid email or password" |
| Non-existent email | email: "notfound@example.com", password: "anypass" | 401 Unauthorized, error: "Invalid email or password" (same message) |
| Remember me true | email: "test@example.com", password: "testpass123", remember_me: true | Cookie Max-Age=2592000 (30 days) |
| Remember me false | email: "test@example.com", password: "testpass123", remember_me: false | Cookie Max-Age=604800 (7 days) |
| 6th login attempt (rate limit) | 6 requests within 1 minute | 429 Too Many Requests, error: "Too many login attempts" |

**Test Commands**:
```bash
# Backend: Test signin endpoint
curl -X POST http://localhost:8000/api/auth/signin \
  -H "Content-Type: application/json" \
  -c cookies.txt \
  -d '{"email":"test@example.com","password":"testpass123","remember_me":false}'

# Verify cookie set
cat cookies.txt | grep session_token

# Test protected endpoint
curl -X GET http://localhost:8000/api/auth/me -b cookies.txt

# Frontend: Manual test
# 1. Navigate to http://localhost:3000/auth/signin
# 2. Enter valid credentials
# 3. Submit form
# 4. Verify redirect to http://localhost:3000/tasks
# 5. Close browser, reopen, verify still authenticated
# 6. Click signout, verify redirect to /auth/signin
```

---

## Phase 5: User Story 3 – View All My Tasks (P2)

**User Story**: As a logged-in user, I want to view all my tasks so I can see what needs to be done.

**Goal**: Display all tasks belonging to authenticated user

**Duration**: ~4-5 hours

**Dependencies**: Phase 4 (US2 Login) complete (authentication required)

**Independent Test Criteria**:
- ✅ Log in as user A
- ✅ Navigate to http://localhost:3000/tasks
- ✅ Verify only user A's tasks displayed (filtered by user_id)
- ✅ Verify sorted by created_at DESC (newest first)
- ✅ Log in as user B, verify only user B's tasks displayed

**Tasks**:

- [ ] T057 [P] [US3] Create backend/app/schemas/task.py with TaskRead Pydantic model (id UUID, user_id UUID, title, description, completed, priority, tags, category, timestamps)
- [ ] T058 [P] [US3] Create backend/app/schemas/task.py with TaskListResponse Pydantic model (tasks list[TaskRead], total int, completed int, incomplete int)
- [ ] T059 [P] [US3] Create backend/app/routers/__init__.py for tasks router
- [ ] T060 [US3] Create GET /api/tasks endpoint in backend/app/routers/tasks.py (filter by current_user.id, sort by created_at DESC, return TaskListResponse)
- [ ] T061 [US3] Add query parameters to GET /api/tasks (completed bool optional, limit int default 1000, offset int default 0)
- [ ] T062 [US3] Add authorization check: ALL queries MUST filter by user_id = authenticated user (no exceptions)
- [ ] T063 [US3] Register tasks router in backend/app/main.py (app.include_router(tasks_router, prefix="/api/tasks", dependencies=[Depends(get_current_user)]))
- [ ] T064 [P] [US3] Create frontend/app/tasks/page.tsx Server Component as dashboard (fetch tasks server-side, pass to client components)
- [ ] T065 [P] [US3] Create frontend/components/tasks/TaskList.tsx Client Component (displays array of TaskCard components)
- [ ] T066 [P] [US3] Create frontend/components/tasks/TaskCard.tsx Client Component (single task display with title, description truncated, completion checkbox, date)
- [ ] T067 [P] [US3] Create frontend/components/tasks/EmptyState.tsx Server Component (illustration + "You don't have any tasks yet" message + "Add Task" button)
- [ ] T068 [P] [US3] Create frontend/components/ui/Badge.tsx for priority indicators (low=gray, medium=blue, high=yellow, critical=red)
- [ ] T069 [P] [US3] Add getTasks method to frontend/lib/api.ts (GET /api/tasks with credentials: 'include', handle query params)
- [ ] T070 [US3] Wire TaskList to API client, handle loading state (skeleton UI), handle error state, display tasks sorted newest first
- [ ] T071 [US3] Add task count display to dashboard header (e.g., "15 tasks (5 completed, 10 incomplete)")

**Acceptance Scenarios**:

| Scenario | Setup | Expected Output |
|----------|-------|-----------------|
| User with tasks | User A has 10 tasks, User B has 5 tasks | User A sees 10 tasks, User B sees 5 tasks (data isolation verified) |
| No tasks | New user with 0 tasks | See EmptyState component with "You don't have any tasks yet" |
| Completed tasks | User has 3 completed, 7 incomplete | Completed tasks have strikethrough title, checkboxes checked |
| Sorting | Tasks created at T1, T2, T3 | Displayed as T3, T2, T1 (newest first) |
| URL manipulation | User A tries GET /api/tasks with User B's token | Returns only User A's tasks (user_id from token, not URL) |

**Test Commands**:
```bash
# Backend: Test list tasks endpoint
# 1. Create 2 users
curl -X POST http://localhost:8000/api/auth/signup -H "Content-Type: application/json" -d '{"email":"user1@example.com","password":"pass123"}'
curl -X POST http://localhost:8000/api/auth/signup -H "Content-Type: application/json" -d '{"email":"user2@example.com","password":"pass123"}'

# 2. Login as user1, create 3 tasks
curl -X POST http://localhost:8000/api/auth/signin -H "Content-Type: application/json" -c user1.txt -d '{"email":"user1@example.com","password":"pass123"}'
curl -X POST http://localhost:8000/api/tasks -H "Content-Type: application/json" -b user1.txt -d '{"title":"Task 1"}'
curl -X POST http://localhost:8000/api/tasks -H "Content-Type: application/json" -b user1.txt -d '{"title":"Task 2"}'
curl -X POST http://localhost:8000/api/tasks -H "Content-Type: application/json" -b user1.txt -d '{"title":"Task 3"}'

# 3. List user1's tasks
curl -X GET http://localhost:8000/api/tasks -b user1.txt
# Expected: 3 tasks, sorted newest first

# 4. Login as user2, verify isolation
curl -X POST http://localhost:8000/api/auth/signin -H "Content-Type: application/json" -c user2.txt -d '{"email":"user2@example.com","password":"pass123"}'
curl -X GET http://localhost:8000/api/tasks -b user2.txt
# Expected: 0 tasks (empty array)

# Frontend: Manual test
# 1. Login as user1, verify 3 tasks displayed
# 2. Login as user2 (different browser/incognito), verify 0 tasks
```

---

## Phase 6: User Story 4 – Create New Task (P2)

**User Story**: As a logged-in user, I want to create a new task with title and optional description.

**Goal**: Allow users to add new tasks to their list

**Duration**: ~3-4 hours

**Dependencies**: Phase 4 (US2 Login) complete (authentication required)

**Independent Test Criteria**:
- ✅ Log in as user
- ✅ Click "Add Task" button
- ✅ Enter title "Buy groceries" and description "Milk, eggs, bread"
- ✅ Submit form
- ✅ Verify task appears at top of list immediately (optimistic update)
- ✅ Verify task persisted in database

**Tasks**:

- [ ] T072 [P] [US4] Add TaskCreate Pydantic model to backend/app/schemas/task.py (title str 1-200 chars, description str optional max 1000, priority optional, tags list optional, category str optional)
- [ ] T073 [US4] Create POST /api/tasks endpoint in backend/app/routers/tasks.py (validate input, generate UUID, set user_id from current_user, set timestamps, return TaskRead with 201 status)
- [ ] T074 [US4] Add validation to POST /api/tasks (title trimmed and required, description max 1000 chars, tags max 10, priority enum)
- [ ] T075 [US4] Add authorization: user_id automatically set from authenticated user (NEVER from request body)
- [ ] T076 [P] [US4] Create frontend/app/tasks/new/page.tsx Server Component with "Create Task" page layout
- [ ] T077 [P] [US4] Create frontend/components/tasks/TaskForm.tsx Client Component (title input required, description textarea optional, priority select, tags input, category input)
- [ ] T078 [P] [US4] Add Zod taskCreateSchema to frontend/lib/validations.ts (title 1-200 chars, description max 1000, priority enum, tags max 10)
- [ ] T079 [P] [US4] Add createTask method to frontend/lib/api.ts (POST /api/tasks with credentials: 'include')
- [ ] T080 [US4] Wire TaskForm to API client, handle validation errors (display inline), handle success (redirect to /tasks with toast "Task created successfully")
- [ ] T081 [US4] Add optimistic UI update to task list (add new task to top immediately, revert if API call fails)

**Acceptance Scenarios**:

| Scenario | Input | Expected Output |
|----------|-------|-----------------|
| Valid task (title only) | title: "Buy groceries" | 201 Created, task in DB with auto-generated UUID, user_id set, completed=false, timestamps set |
| Valid task (with description) | title: "Buy groceries", description: "Milk, eggs, bread" | Task created with both fields |
| Empty title | title: "" or "   " (whitespace) | 400 Bad Request, error: "Title is required" |
| Title too long | title: 201 chars | 400 Bad Request, error: "Title must be 200 characters or less" |
| Description too long | description: 1001 chars | 400 Bad Request, error: "Description must be 1000 characters or less" |
| Too many tags | tags: [11 tags] | 400 Bad Request, error: "Maximum 10 tags allowed" |
| Invalid priority | priority: "invalid" | 400 Bad Request, error: "Priority must be one of: low, medium, high, critical" |

**Test Commands**:
```bash
# Backend: Test create task endpoint
curl -X POST http://localhost:8000/api/tasks \
  -H "Content-Type: application/json" \
  -b cookies.txt \
  -d '{"title":"Buy groceries","description":"Milk, eggs, bread","priority":"medium","tags":["shopping"],"category":"personal"}'

# Verify task created
curl -X GET http://localhost:8000/api/tasks -b cookies.txt
# Expected: New task at top of list

# Frontend: Manual test
# 1. Login, navigate to /tasks
# 2. Click "Add Task" button
# 3. Enter title "Buy groceries"
# 4. Enter description "Milk, eggs, bread"
# 5. Select priority "Medium"
# 6. Add tag "shopping"
# 7. Submit form
# 8. Verify task appears at top immediately
# 9. Refresh page, verify task persists
```

---

## Phase 7: User Story 5 – Mark Task Complete/Incomplete (P3)

**User Story**: As a logged-in user, I want to toggle task completion status with one click.

**Goal**: Toggle task completion status

**Duration**: ~2-3 hours

**Dependencies**: Phase 5 or Phase 6 (tasks must exist)

**Independent Test Criteria**:
- ✅ Log in, view task list
- ✅ Click checkbox on incomplete task
- ✅ Verify task marked complete (checkbox checked, title strikethrough)
- ✅ Click checkbox again
- ✅ Verify task marked incomplete (checkbox unchecked, normal title)
- ✅ Refresh page, verify status persists

**Tasks**:

- [ ] T082 [P] [US5] Add TaskUpdate Pydantic model to backend/app/schemas/task.py (all fields optional: title, description, completed, priority, tags, category)
- [ ] T083 [US5] Create PATCH /api/tasks/{task_id} endpoint in backend/app/routers/tasks.py (partial update, only update provided fields, update updated_at timestamp)
- [ ] T084 [US5] Add authorization check to PATCH endpoint: verify task.user_id == current_user.id, return 404 if not owned
- [ ] T085 [US5] Add GET /api/tasks/{task_id} endpoint in backend/app/routers/tasks.py (return single task, 404 if not found or not owned)
- [ ] T086 [P] [US5] Add updateTask method to frontend/lib/api.ts (PATCH /api/tasks/{id} with credentials: 'include')
- [ ] T087 [P] [US5] Add getTask method to frontend/lib/api.ts (GET /api/tasks/{id} with credentials: 'include')
- [ ] T088 [US5] Add toggle checkbox to TaskCard.tsx with onChange handler
- [ ] T089 [US5] Implement optimistic update in TaskCard: update UI immediately, call API, revert if fails
- [ ] T090 [P] [US5] Add visual completion indicators to TaskCard.tsx (strikethrough title, green checkmark icon, move to bottom optional)
- [ ] T091 [US5] Handle toggle errors gracefully (show toast "Failed to update task", revert UI)

**Acceptance Scenarios**:

| Scenario | Initial State | Action | Expected Output |
|----------|---------------|--------|-----------------|
| Mark complete | Task completed=false | Click checkbox | Task completed=true, checkbox checked, title strikethrough, updated_at updated |
| Mark incomplete | Task completed=true | Click checkbox | Task completed=false, checkbox unchecked, title normal |
| Network failure | Task completed=false | Click checkbox, API returns 500 | UI reverts to unchecked, error toast displayed |
| Unauthorized (not owned) | Task belongs to User B | User A tries to toggle | 404 Not Found (prevents task ID enumeration) |
| Keyboard accessible | Task focused | Press Space or Enter | Same as click (toggle works) |

**Test Commands**:
```bash
# Backend: Test toggle completion
# 1. Create task
curl -X POST http://localhost:8000/api/tasks -H "Content-Type: application/json" -b cookies.txt -d '{"title":"Test task"}' | jq -r '.id'
# Save task ID

# 2. Mark complete
curl -X PATCH http://localhost:8000/api/tasks/[TASK_ID] -H "Content-Type: application/json" -b cookies.txt -d '{"completed":true}'

# 3. Verify
curl -X GET http://localhost:8000/api/tasks/[TASK_ID] -b cookies.txt | jq '.completed'
# Expected: true

# Frontend: Manual test
# 1. Login, view task list
# 2. Click checkbox on any task
# 3. Verify immediate visual change (strikethrough)
# 4. Refresh page, verify status persists
# 5. Click checkbox again, verify toggles back
```

---

## Phase 8: User Story 6 – Update Task (P3)

**User Story**: As a logged-in user, I want to edit task title and description.

**Goal**: Edit task title and description

**Duration**: ~3-4 hours

**Dependencies**: Phase 5 or Phase 6 (tasks must exist)

**Independent Test Criteria**:
- ✅ Log in, view task
- ✅ Click "Edit" button/icon
- ✅ Modify title to "Buy groceries and milk"
- ✅ Modify description to "Updated description"
- ✅ Click "Save"
- ✅ Verify changes visible immediately
- ✅ Refresh page, verify changes persist

**Tasks**:

- [ ] T092 [P] [US6] Create frontend/app/tasks/[id]/edit/page.tsx Server Component with "Edit Task" page layout
- [ ] T093 [P] [US6] Fetch task data server-side in edit page (call GET /api/tasks/{id}, pass to TaskForm)
- [ ] T094 [US6] Modify TaskForm.tsx to support edit mode (accept initialValues prop, pre-populate fields, change submit button to "Save")
- [ ] T095 [US6] Wire edit form to API client (call updateTask on submit, redirect to /tasks on success)
- [ ] T096 [US6] Add "Edit" button to TaskCard.tsx (navigate to /tasks/[id]/edit)
- [ ] T097 [US6] Handle edit validation errors (display inline, same rules as create)
- [ ] T098 [US6] Add "Cancel" button to edit form (navigate back to /tasks without saving)
- [ ] T099 [US6] Handle unauthorized edit attempt (404 if task not owned, redirect to /tasks)

**Acceptance Scenarios**:

| Scenario | Initial State | Input | Expected Output |
|----------|---------------|-------|-----------------|
| Valid edit (title) | title: "Buy groceries" | title: "Buy groceries and milk" | Task updated, updated_at timestamp updated, redirect to /tasks |
| Valid edit (description) | description: "Milk, eggs" | description: "Milk, eggs, bread, butter" | Task updated with new description |
| Empty title | title: "Buy groceries" | title: "" | 400 Bad Request, error: "Title is required" |
| Title too long | Valid task | title: 201 chars | 400 Bad Request, error: "Title must be 200 characters or less" |
| Cancel edit | Any task | Click "Cancel" button | Navigate to /tasks, no changes saved |
| Unauthorized edit | Task belongs to User B | User A tries to edit | 404 Not Found, redirect to /tasks |
| Concurrent edit | 2 tabs editing same task | Tab 1 saves, Tab 2 saves 5 seconds later | Last write wins (Tab 2's changes persist) |

**Test Commands**:
```bash
# Backend: Test update task
curl -X PATCH http://localhost:8000/api/tasks/[TASK_ID] \
  -H "Content-Type: application/json" \
  -b cookies.txt \
  -d '{"title":"Buy groceries and milk","description":"Updated description"}'

# Verify
curl -X GET http://localhost:8000/api/tasks/[TASK_ID] -b cookies.txt | jq '{title, description}'

# Frontend: Manual test
# 1. Login, view task list
# 2. Click "Edit" on any task
# 3. Modify title and description
# 4. Click "Save"
# 5. Verify redirect to /tasks
# 6. Verify changes visible in list
# 7. Click "Edit" again, verify fields show updated values
```

---

## Phase 9: User Story 7 – Delete Task (P4)

**User Story**: As a logged-in user, I want to permanently delete tasks I no longer need.

**Goal**: Permanently remove tasks

**Duration**: ~2-3 hours

**Dependencies**: Phase 5 or Phase 6 (tasks must exist)

**Independent Test Criteria**:
- ✅ Log in, view task
- ✅ Click "Delete" button/icon
- ✅ See confirmation dialog "Are you sure you want to delete this task? This action cannot be undone."
- ✅ Click "Delete" in dialog
- ✅ Verify task removed from list immediately
- ✅ Refresh page, verify task still gone (hard delete)

**Tasks**:

- [ ] T100 [US7] Create DELETE /api/tasks/{task_id} endpoint in backend/app/routers/tasks.py (hard delete, return 204 No Content)
- [ ] T101 [US7] Add authorization check to DELETE endpoint: verify task.user_id == current_user.id, return 404 if not owned
- [ ] T102 [P] [US7] Create frontend/components/tasks/DeleteConfirmDialog.tsx Client Component (modal with "Are you sure?" message, "Delete" and "Cancel" buttons)
- [ ] T103 [P] [US7] Add deleteTask method to frontend/lib/api.ts (DELETE /api/tasks/{id} with credentials: 'include')
- [ ] T104 [US7] Add "Delete" button/icon to TaskCard.tsx (opens DeleteConfirmDialog)
- [ ] T105 [US7] Wire delete confirmation to API client (call deleteTask on confirm, remove from UI immediately, show error toast if fails)
- [ ] T106 [US7] Handle ESC key to close delete confirmation dialog

**Acceptance Scenarios**:

| Scenario | Setup | Action | Expected Output |
|----------|-------|--------|-----------------|
| Confirm delete | Task exists | Click "Delete" → Confirm | Task permanently removed from DB, disappears from UI, 204 No Content |
| Cancel delete | Task exists | Click "Delete" → Cancel | Dialog closes, task remains unchanged |
| ESC key | Delete dialog open | Press ESC | Dialog closes, task remains unchanged |
| Unauthorized delete | Task belongs to User B | User A tries to delete | 404 Not Found (prevents task ID enumeration) |
| Delete twice | Task deleted | Try to delete again | 404 Not Found (already deleted) |
| Network failure | Task exists | Click "Delete", API returns 500 | Error toast "Failed to delete task", task remains in UI |

**Test Commands**:
```bash
# Backend: Test delete task
curl -X DELETE http://localhost:8000/api/tasks/[TASK_ID] -b cookies.txt -v
# Expected: 204 No Content

# Verify deleted
curl -X GET http://localhost:8000/api/tasks/[TASK_ID] -b cookies.txt
# Expected: 404 Not Found

# Frontend: Manual test
# 1. Login, view task list
# 2. Click "Delete" on any task
# 3. Verify confirmation dialog appears
# 4. Click "Cancel", verify task remains
# 5. Click "Delete" again, click "Delete" in dialog
# 6. Verify task disappears immediately
# 7. Refresh page, verify task still gone
```

---

## Phase 10: Polish & Cross-Cutting Concerns

**Goal**: Error handling, loading states, production readiness

**Duration**: ~4-5 hours

**Dependencies**: All user stories (US1-US7) complete

**Tasks**:

- [ ] T107 [P] Create frontend/components/ui/LoadingSpinner.tsx Server Component (reusable spinner with variants: small, medium, large)
- [ ] T108 [P] Create frontend/components/ui/Skeleton.tsx Server Component (skeleton loading for task cards)
- [ ] T109 [P] Create frontend/components/ui/ErrorMessage.tsx Client Component (error display with retry button)
- [ ] T110 [P] Create frontend/components/ui/Toast.tsx Client Component (success/error toast notifications using shadcn/ui)
- [ ] T111 [P] Add global error handling to frontend/lib/api.ts (intercept 401 → redirect to /auth/signin, intercept 500 → show error toast)
- [ ] T112 [P] Create frontend/app/error.tsx (global error boundary with friendly message and "Try again" button)
- [ ] T113 [P] Create frontend/app/loading.tsx (global loading fallback with skeleton UI)
- [ ] T114 [P] Create frontend/app/tasks/loading.tsx (task list specific loading skeleton)
- [ ] T115 [P] Add CORS configuration to backend/app/main.py (allow http://localhost:3000 for dev, env variable for production Vercel URL, include preview domain wildcard)
- [ ] T116 [P] Create backend/.env.example with all required variables and comments
- [ ] T117 [P] Create frontend/.env.local.example with all required variables and comments
- [ ] T118 [P] Add input sanitization to task endpoints in backend/app/routers/tasks.py (strip HTML tags, prevent XSS)
- [ ] T119 [P] Add rate limiting middleware to backend/app/main.py (100 requests/minute per user)
- [ ] T120 [P] Create backend/app/exceptions.py with custom exception handlers (HTTPException → JSON error responses)
- [ ] T121 [P] Add health check endpoint GET /api/health in backend/app/main.py (return {"status": "healthy", "service": "todo-backend"})
- [ ] T122 [P] Create README.md in backend/ with setup instructions, API documentation link, environment variables
- [ ] T123 [P] Create README.md in frontend/ with setup instructions, deployment guide, environment variables
- [ ] T124 [P] Update docker-compose.yml with all environment variables from .env.example files
- [ ] T125 [P] Update docker-compose.yml with volume mounts for postgres data persistence
- [ ] T126 [P] Add healthcheck to backend service in docker-compose.yml (curl http://localhost:8000/health)
- [ ] T127 [P] Create backend/scripts/migrate_phase1_to_phase2.py migration script (read cli/tasks.json, create default user, import tasks)
- [ ] T128 [P] Add logging configuration to backend/app/main.py (structured JSON logs with request IDs)
- [ ] T129 [P] Add request ID middleware to backend/app/main.py (X-Request-ID header for tracing)
- [ ] T130 Test full E2E flow: start services → signup → signin → create task → toggle complete → edit task → delete task → signout

**Acceptance Criteria**:
- ✅ Application runs smoothly with `docker-compose up`
- ✅ Graceful error handling (no stack traces in production)
- ✅ Loading states for all async operations
- ✅ Success/error toasts for user actions
- ✅ CORS configured correctly (localhost + Vercel production + preview domains)
- ✅ Rate limiting prevents abuse
- ✅ Input sanitization prevents XSS attacks
- ✅ Health check endpoint returns 200 OK
- ✅ All environment variables documented in .env.example files
- ✅ READMEs provide clear setup instructions
- ✅ E2E flow works end-to-end

---

## Dependencies & Execution Order

### Critical Path (Sequential)

```
Phase 1 (Setup)
    ↓
Phase 2 (Foundational)
    ↓
Phase 3 (US1: Registration) ─────────────────┐
    ↓                                          │
Phase 4 (US2: Login) ────────────────────────┤
    ↓                                          │
    ├──→ Phase 5 (US3: View Tasks)            │
    │                                          │
    └──→ Phase 6 (US4: Create Task)           │
              ↓                                │
         (Phase 5 OR Phase 6)                 │
              ↓                                │
         Phase 7 (US5: Toggle Complete)       │
              ↓                                │
         Phase 8 (US6: Update Task)           │
              ↓                                │
         Phase 9 (US7: Delete Task)           │
              ↓                                │
         Phase 10 (Polish) ←──────────────────┘
```

### Parallelizable Tasks (After Prerequisites)

**After Phase 2 (Foundational)**:
- Phase 3 (US1 Registration) can proceed immediately

**After Phase 4 (US2 Login)**:
- Phase 5 (US3 View Tasks) and Phase 6 (US4 Create Task) can be developed in parallel
- Different components, no shared files

**After Phase 5 OR Phase 6**:
- Phase 7 (US5 Toggle), Phase 8 (US6 Update), Phase 9 (US7 Delete) can be developed in parallel
- All operate on existing tasks, no dependencies on each other
- Different API endpoints, different UI components

**Within Each Phase**:
- All tasks marked `[P]` can be executed in parallel
- Typically: backend schemas + frontend components + API client methods
- Final "wire" task must wait for all parallel tasks to complete

### MVP Milestones

**Milestone 1: Authentication Complete** (Phases 1-4)
- ✅ T001-T056
- ✅ Users can register and login
- ✅ Protected routes work
- ✅ Session management functional
- **Demo**: Show signup → login → dashboard redirect

**Milestone 2: Core CRUD Complete** (Phases 5-6)
- ✅ T057-T081
- ✅ Users can view and create tasks
- ✅ Data isolation verified
- **Demo**: Create tasks, view in list, verify isolation

**Milestone 3: Task Management Complete** (Phases 7-9)
- ✅ T082-T106
- ✅ Toggle, edit, delete functionality
- **Demo**: Full task lifecycle (create → complete → edit → delete)

**Milestone 4: Production Ready** (Phase 10)
- ✅ T107-T130
- ✅ Polish, error handling, deployment ready
- **Demo**: Deploy to HF Spaces + Vercel

---

## Implementation Strategy

### Test-Driven Development (TDD) Approach

**Red-Green-Refactor Cycle** (Optional - Tests not required per spec):

1. **Red**: Write failing test for acceptance scenario
2. **Green**: Implement minimum code to pass test
3. **Refactor**: Clean up code while keeping tests passing

**Test Coverage Targets**:
- Backend: ≥80% line coverage (pytest-cov)
- Frontend: ≥80% line coverage (Vitest)
- E2E: All 7 user stories covered (Playwright)

### Subagent Orchestration

**Backend Engineer Agent**:
- Tasks: T002, T004, T009, T016-T029, T033, T042, T053, T060-T063, T073-T075, T084-T085, T100-T101, T118-T121, T127-T129
- Focus: FastAPI, SQLModel, authentication, API endpoints

**Frontend Engineer Agent**:
- Tasks: T003, T005, T007, T010, T034-T038, T049-T055, T064-T071, T076-T081, T086-T099, T102-T106, T107-T117, T122-T123
- Focus: Next.js, React components, UI/UX, API integration

**Data Migration Agent**:
- Tasks: T023, T028, T127
- Focus: Alembic migrations, Phase 1 → Phase 2 data migration

**QA & Testing Agent**:
- Tasks: Test generation throughout (if TDD approach used)
- Focus: pytest, Vitest, Playwright, coverage validation

**DevOps Agent**:
- Tasks: T008-T012, T124-T126, T130
- Focus: Docker, docker-compose, deployment configuration

### Incremental Delivery

**Week 1**: Phases 1-2 (Setup + Foundational)
- Deliverable: Project structure, database models, basic FastAPI app

**Week 2**: Phases 3-4 (Authentication)
- Deliverable: Working signup/signin, protected routes, session management

**Week 3**: Phases 5-6 (Core CRUD)
- Deliverable: View tasks list, create new tasks, data isolation verified

**Week 4**: Phases 7-9 (Task Management)
- Deliverable: Toggle completion, edit tasks, delete tasks

**Week 5**: Phase 10 (Polish + Deployment)
- Deliverable: Production-ready app deployed to HF Spaces + Vercel

---

## Task Summary

### Total Task Count: 130 tasks

**By Phase**:
- Phase 1 (Setup): 15 tasks
- Phase 2 (Foundational): 14 tasks
- Phase 3 (US1 Registration): 10 tasks
- Phase 4 (US2 Login): 17 tasks
- Phase 5 (US3 View Tasks): 15 tasks
- Phase 6 (US4 Create Task): 10 tasks
- Phase 7 (US5 Toggle): 10 tasks
- Phase 8 (US6 Update): 8 tasks
- Phase 9 (US7 Delete): 7 tasks
- Phase 10 (Polish): 24 tasks

**By User Story**:
- US1 (Registration): 10 tasks (T030-T039)
- US2 (Login): 17 tasks (T040-T056)
- US3 (View Tasks): 15 tasks (T057-T071)
- US4 (Create Task): 10 tasks (T072-T081)
- US5 (Toggle Complete): 10 tasks (T082-T091)
- US6 (Update Task): 8 tasks (T092-T099)
- US7 (Delete Task): 7 tasks (T100-T106)

**Parallelizable Tasks**: 83 tasks (marked with `[P]`)
**Sequential Tasks**: 47 tasks

**Parallel Opportunities**:
- Within Phase 1: 13 parallel tasks (directory setup, file creation)
- Within Phase 2: 11 parallel tasks (models, schemas, security)
- Within US1-US7: 5-8 parallel tasks per story (frontend + backend + schemas)
- Within Phase 10: 20 parallel tasks (polish components, documentation)

---

## Next Steps

**Ready for**: `/sp.implement` command to begin implementation

**Suggested Execution**:

```bash
# Option 1: Manual execution (task by task)
# Start with Phase 1, complete all tasks sequentially
# Use parallel tasks where marked [P]

# Option 2: Subagent orchestration
# Invoke Backend Engineer: Implement US1 (Registration) per tasks.md T030-T033
# Invoke Frontend Engineer: Implement US1 (Registration) UI per tasks.md T034-T038

# Option 3: Incremental delivery
# Week 1: Phases 1-2 (Setup + Foundational)
# Week 2: Phases 3-4 (Authentication US1 + US2)
# Week 3: Phases 5-6 (Core CRUD US3 + US4)
# Week 4: Phases 7-9 (Task Management US5 + US6 + US7)
# Week 5: Phase 10 (Polish + Deployment)
```

**Validation Checklist**:
- ✅ All tasks follow checklist format (`- [ ] [TaskID] [P?] [Story?] Description`)
- ✅ Each user story has independent test criteria
- ✅ Dependencies clearly documented
- ✅ Parallel opportunities identified (83 tasks marked `[P]`)
- ✅ File paths specified for each task
- ✅ Acceptance scenarios for each user story
- ✅ MVP milestone defined (Phases 1-4)

---

**Status**: ✅ Tasks Ready for Implementation
**Total Tasks**: 130
**Estimated Duration**: 4-5 weeks (full-time equivalent)
**Next Command**: `/sp.implement`
