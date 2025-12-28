# Tasks: Professional Multi-Tenant Project Management System

**Input**: Design documents from `/specs/001-project-management-system/`
**Prerequisites**: plan.md, spec.md, research.md, data-model.md, contracts/
**Constitution**: Article V mandates test-first development with >80% coverage

**Organization**: Tasks are grouped by user story to enable independent implementation and testing of each story.

**Tests**: ✅ TEST TASKS INCLUDED per Constitution Article V requirement. Test tasks inserted BEFORE implementation tasks following TDD principles.

## Format: `[ID] [P?] [Story] Description`

- **[P]**: Can run in parallel (different files, no dependencies)
- **[Story]**: Which user story this task belongs to (US1-US10)
- Include exact file paths in descriptions

---

## Phase 1: Setup (Shared Infrastructure)

**Purpose**: Project initialization and basic structure per plan.md

- [ ] T001 Create monorepo directory structure (backend/, frontend/, shared/)
- [ ] T002 Initialize Python project in backend/ with UV and pyproject.toml dependencies (FastAPI 0.110+, SQLModel, Better Auth, python-jose, bcrypt, aiofiles, aiosmtplib, alembic, pytest, httpx, ruff, pyright)
- [ ] T003 [P] Initialize Next.js 15 project in frontend/ with TypeScript strict mode and dependencies (React 18+, Tailwind CSS v3, shadcn/ui, TanStack Query v5, Zustand, @dnd-kit/core, React Hook Form, Zod, Vitest, Playwright)
- [ ] T004 [P] Configure backend linting/formatting tools (ruff, pyright) in backend/pyproject.toml
- [ ] T005 [P] Configure frontend linting/formatting tools (ESLint, Prettier, TypeScript) in frontend/
- [ ] T006 Create .env.example files for backend and frontend with all required environment variables per quickstart.md
- [ ] T007 Create README.md files in backend/ and frontend/ with setup instructions from quickstart.md
- [ ] T008 Configure Alembic for database migrations in backend/alembic/
- [ ] T009 [P] Setup Vercel configuration in frontend/vercel.json
- [ ] T010 [P] Create Dockerfile for backend deployment
- [ ] T011 Write pytest tests for backend project structure in backend/tests/test_setup.py (verify all imports work, config loads, database module exists)
- [ ] T012 [P] Write Vitest tests for frontend project structure in frontend/tests/setup.test.ts (verify tsconfig, imports work, Tailwind loads)

---

## Phase 2: Foundational (Blocking Prerequisites)

**Purpose**: Core infrastructure that MUST be complete before ANY user story can be implemented

**⚠️ CRITICAL**: No user story work can begin until this phase is complete

- [ ] T013 Write pytest tests for database connection in backend/tests/test_database.py (test async engine creation, session management, connection pooling, Neon connection)
- [ ] T014 Create database configuration module in backend/app/database.py (async engine, session management with Neon PostgreSQL connection)
- [ ] T015 [P] Write pytest tests for config loading in backend/tests/test_config.py (test env var parsing, defaults, Pydantic validation, missing required vars)
- [ ] T016 [P] Create application configuration module in backend/app/config.py (Pydantic BaseSettings for environment variables)
- [ ] T017 Write pytest tests for FastAPI app initialization in backend/tests/test_main.py (test CORS config, middleware registration, router mounting, exception handlers)
- [ ] T018 Create FastAPI app initialization in backend/app/main.py (CORS, middleware, router registration, exception handlers)
- [ ] T019 [P] Write pytest tests for base SQLModel mixins in backend/tests/models/test_base.py (test UUID generation, timestamp auto-update, organization scoping mixin)
- [ ] T020 [P] Create base SQLModel mixins in backend/app/models/base.py (UUID primary keys, timestamps, organization scoping)
- [ ] T021 [P] Write pytest tests for dependency injection in backend/tests/test_dependencies.py (test get_session, get_current_user, get_current_organization, auth failures)
- [ ] T022 [P] Create dependency injection utilities in backend/app/dependencies.py (get_session, get_current_user, get_current_organization)
- [ ] T023 [P] Write pytest tests for auth utilities in backend/tests/utils/test_auth.py (test password hashing with bcrypt cost 12, password verification, JWT creation/verification, token expiration)
- [ ] T024 [P] Create authentication utilities in backend/app/utils/auth.py (password hashing with bcrypt cost 12, JWT creation/verification)
- [ ] T025 [P] Write pytest tests for FileStorage in backend/tests/services/test_file_service.py (test save file, get_url, delete, path sanitization, directory creation)
- [ ] T026 [P] Create file storage service abstraction in backend/app/services/file_service.py (LocalFileStorage class with save/get_url/delete methods)
- [ ] T027 [P] Write pytest tests for EmailService in backend/tests/services/test_email_service.py (test SMTP connection, send_verification_email, send_reset_email, template rendering)
- [ ] T028 [P] Create email service in backend/app/services/email_service.py (SMTP with aiosmtplib, template methods for verification/reset/notification emails)
- [ ] T029 [P] Write pytest tests for error handling in backend/tests/utils/test_errors.py (test custom exceptions, error response formatters, validation errors)
- [ ] T030 [P] Create error handling utilities in backend/app/utils/errors.py (custom exceptions, error response formatters)
- [ ] T031 [P] Write Vitest tests for API client in frontend/tests/lib/api.test.ts (test fetch wrappers, auth headers, error handling, base URL config)
- [ ] T032 [P] Create API client utilities in frontend/lib/api.ts (fetch wrappers with auth, error handling, base URL configuration)
- [ ] T033 [P] Write Vitest tests for auth context in frontend/tests/lib/auth.test.tsx (test session management, user state, login/logout actions)
- [ ] T034 [P] Create auth context provider in frontend/lib/auth.ts (session management, user state)
- [ ] T035 [P] Write Vitest tests for TanStack Query client in frontend/tests/lib/queryClient.test.ts (test default options, cache configuration, retry logic)
- [ ] T036 [P] Configure TanStack Query client in frontend/lib/queryClient.ts (default options, cache configuration)
- [ ] T037 [P] Create TypeScript type definitions in frontend/types/models.ts (User, Organization, Project, Board, Task, etc.)

**Checkpoint**: Foundation ready - user story implementation can now begin in parallel

---

## Phase 3: User Story 7 - User Authentication & Profile Management (Priority: P1) 🎯 MVP

**Goal**: Enable users to create accounts, verify email, securely login, and manage their profile

**Independent Test**: New user can sign up, receive verification email, verify, login, update profile (name, avatar), and change password

### Implementation for User Story 7

- [ ] T038 [P] [US7] Write pytest tests for User model in backend/tests/models/test_user.py (test field validation, email lowercase normalization, password hashing on create, email_verified default false)
- [ ] T039 [P] [US7] Create User model in backend/app/models/user.py (id, email, hashed_password, full_name, avatar_url, email_verified, timezone, language, created_at, updated_at)
- [ ] T040 [P] [US7] Write pytest tests for Session model in backend/tests/models/test_user.py (test token uniqueness, refresh_token, expiration validation, cascade delete on user delete)
- [ ] T041 [P] [US7] Create Session model in backend/app/models/user.py (id, user_id, token, refresh_token, expires_at, ip_address, user_agent, created_at)
- [ ] T042 [US7] Write pytest tests for User/Session migrations in backend/tests/migrations/test_001_users.py (test tables created, indexes exist, constraints enforced, rollback works)
- [ ] T043 [US7] Create Alembic migration for User and Session tables in backend/alembic/versions/001_create_users_sessions.py
- [ ] T044 [US7] Write pytest tests for AuthService in backend/tests/services/test_auth_service.py (test signup valid/invalid data, signin success/failure, verify_email token validation, forgot/reset password flow, update_profile, change_password)
- [ ] T045 [US7] Implement AuthService in backend/app/services/auth_service.py (signup, signin, signout, verify_email, forgot_password, reset_password, update_profile, change_password)
- [ ] T046 [US7] Write pytest tests for POST /api/auth/signup in backend/tests/routers/test_auth.py::test_signup (test 201 success, 400 invalid email, 409 duplicate email, 400 weak password, email sent)
- [ ] T047 [US7] Implement POST /api/auth/signup endpoint in backend/app/routers/auth.py (create user, send verification email, return user data)
- [ ] T048 [US7] Write pytest tests for POST /api/auth/signin in backend/tests/routers/test_auth.py::test_signin (test 200 success with cookie, 401 wrong password, 401 user not found, remember_me flag)
- [ ] T049 [US7] Implement POST /api/auth/signin endpoint in backend/app/routers/auth.py (verify credentials, create session, set HttpOnly cookie, return user + expiration)
- [ ] T050 [US7] Write pytest tests for POST /api/auth/signout in backend/tests/routers/test_auth.py::test_signout (test 200 success, session deleted, cookie cleared)
- [ ] T051 [US7] Implement POST /api/auth/signout endpoint in backend/app/routers/auth.py (invalidate session, clear cookie)
- [ ] T052 [US7] Write pytest tests for GET /api/auth/me in backend/tests/routers/test_auth.py::test_get_me (test 200 success with user, 401 no session, 401 expired session)
- [ ] T053 [US7] Implement GET /api/auth/me endpoint in backend/app/routers/auth.py (return current user from session)
- [ ] T054 [US7] Write pytest tests for POST /api/auth/verify-email in backend/tests/routers/test_auth.py::test_verify_email (test 200 success marks verified, 400 invalid token, 410 expired token)
- [ ] T055 [US7] Implement POST /api/auth/verify-email endpoint in backend/app/routers/auth.py (validate token, mark email as verified)
- [ ] T056 [US7] Write pytest tests for POST /api/auth/forgot-password in backend/tests/routers/test_auth.py::test_forgot_password (test 200 always returned, email sent if user exists, no email if user not found for security)
- [ ] T057 [US7] Implement POST /api/auth/forgot-password endpoint in backend/app/routers/auth.py (generate reset token, send email, always return 200)
- [ ] T058 [US7] Write pytest tests for POST /api/auth/reset-password in backend/tests/routers/test_auth.py::test_reset_password (test 200 success password updated, 400 invalid token, 410 expired token, password strength validation)
- [ ] T059 [US7] Implement POST /api/auth/reset-password endpoint in backend/app/routers/auth.py (validate token, update password)
- [ ] T060 [US7] Write pytest tests for PUT /api/auth/profile in backend/tests/routers/test_auth.py::test_update_profile (test 200 success, 401 not authenticated, partial updates work, avatar URL validation)
- [ ] T061 [US7] Implement PUT /api/auth/profile endpoint in backend/app/routers/auth.py (update full_name, avatar_url, timezone, language)
- [ ] T062 [US7] Write pytest tests for PUT /api/auth/password in backend/tests/routers/test_auth.py::test_change_password (test 200 success, 400 wrong current password, 400 weak new password, old sessions invalidated)
- [ ] T063 [US7] Implement PUT /api/auth/password endpoint in backend/app/routers/auth.py (verify current password, update to new password)
- [ ] T064 [US7] Write pytest tests for rate limiting on auth in backend/tests/routers/test_auth.py::test_rate_limits (test 429 after 5 signin in 15min, 3 signup per hour, 3 forgot-password per hour)
- [ ] T065 [US7] Add rate limiting to auth endpoints in backend/app/routers/auth.py (5 signin per 15 min, 3 signup per hour, 3 forgot-password per hour)
- [ ] T066 [P] [US7] Write Vitest tests for signup page in frontend/tests/pages/auth/SignupPage.test.tsx (test form validation, submit success, duplicate email error, weak password error)
- [ ] T067 [P] [US7] Create signup page in frontend/app/auth/signup/page.tsx (email, password, full_name form with validation)
- [ ] T068 [P] [US7] Write Vitest tests for signin page in frontend/tests/pages/auth/SigninPage.test.tsx (test form validation, submit success, wrong password error, remember_me checkbox)
- [ ] T069 [P] [US7] Create signin page in frontend/app/auth/signin/page.tsx (email, password, remember_me form)
- [ ] T070 [P] [US7] Write Vitest tests for email verification page in frontend/tests/pages/auth/VerifyPage.test.tsx (test token validation, success state, expired token error)
- [ ] T071 [P] [US7] Create email verification page in frontend/app/auth/verify/page.tsx (token validation, success/error states)
- [ ] T072 [P] [US7] Write Vitest tests for password reset pages in frontend/tests/pages/auth/ResetPage.test.tsx (test request page email form, reset page with token and new password, success/error states)
- [ ] T073 [P] [US7] Create password reset flow pages in frontend/app/auth/reset/ (request page with email, reset page with token + new password)
- [ ] T074 [P] [US7] Write Vitest tests for profile settings page in frontend/tests/pages/me/ProfilePage.test.tsx (test edit name, avatar upload, timezone select, language select, form validation)
- [ ] T075 [P] [US7] Create user profile settings page in frontend/app/me/profile/page.tsx (edit name, avatar, timezone, language)
- [ ] T076 [US7] Write Vitest tests for auth store in frontend/tests/stores/authStore.test.ts (test user state updates, login/logout actions, session persistence)
- [ ] T077 [US7] Create Zustand auth store in frontend/stores/authStore.ts (current user state, login/logout actions)
- [ ] T078 [US7] Write Vitest tests for useAuth hook in frontend/tests/lib/hooks/useAuth.test.ts (test signup/signin/signout/getMe mutations, loading states, error handling)
- [ ] T079 [US7] Implement useAuth hook in frontend/lib/hooks/useAuth.ts (TanStack Query hooks for signup, signin, signout, getMe)
- [ ] T080 [US7] Write Vitest tests for ProtectedRoute in frontend/tests/components/auth/ProtectedRoute.test.tsx (test authenticated user sees children, unauthenticated redirects to signin)
- [ ] T081 [US7] Create ProtectedRoute component in frontend/components/auth/ProtectedRoute.tsx (redirect to signin if not authenticated)
- [ ] T082 [US7] Write Playwright E2E test for complete auth flow in frontend/tests/e2e/auth.spec.ts (test signup → verify email → signin → update profile → change password → signout)

**Checkpoint**: User authentication fully functional and independently testable

---

## Phase 4: User Story 1 - Organization Setup & Team Onboarding (Priority: P1) 🎯 MVP

**Goal**: Team lead can create organization, invite members via email, and manage roles

**Independent Test**: User creates org "Acme Corp", invites 5 members via email, assigns roles, verifies only invited members can access

### Implementation for User Story 1

- [ ] T083 [P] [US1] Write pytest tests for Organization model in backend/tests/models/test_organization.py (test slug uniqueness per user, name validation, archived default false, owner_id foreign key)
- [ ] T084 [P] [US1] Create Organization model in backend/app/models/organization.py (id, slug, name, description, logo_url, owner_id, created_at, updated_at, archived)
- [ ] T085 [P] [US1] Write pytest tests for OrganizationMember model in backend/tests/models/test_organization.py (test unique (org_id, user_id), role enum validation, cascade delete)
- [ ] T086 [P] [US1] Create OrganizationMember model in backend/app/models/organization.py (id, organization_id, user_id, role enum[owner/admin/member], joined_at)
- [ ] T087 [P] [US1] Write pytest tests for Invitation model in backend/tests/models/test_organization.py (test token uniqueness, expiration default 7 days, accepted_at nullable)
- [ ] T088 [P] [US1] Create Invitation model in backend/app/models/organization.py (id, organization_id, email, role, token UUID, invited_by, expires_at, accepted_at, created_at)
- [ ] T089 [US1] Write pytest tests for org migrations in backend/tests/migrations/test_002_organizations.py (test tables created, indexes, constraints, cascade delete rules)
- [ ] T090 [US1] Create Alembic migration for Organization, OrganizationMember, Invitation tables in backend/alembic/versions/002_create_organizations.py
- [ ] T091 [US1] Write pytest tests for POST /api/organizations in backend/tests/routers/test_organizations.py::test_create_org (test 201 success creator is owner, 400 duplicate slug, 400 invalid slug format)
- [ ] T092 [US1] Implement POST /api/organizations endpoint in backend/app/routers/organizations.py (create org, auto-add creator as owner)
- [ ] T093 [US1] Write pytest tests for GET /api/organizations in backend/tests/routers/test_organizations.py::test_list_orgs (test 200 returns user's orgs with role and counts, empty list if no orgs)
- [ ] T094 [US1] Implement GET /api/organizations endpoint in backend/app/routers/organizations.py (list user's orgs with role and counts)
- [ ] T095 [US1] Write pytest tests for GET /api/organizations/{slug} in backend/tests/routers/test_organizations.py::test_get_org (test 200 success with details, 404 not found, 403 not member)
- [ ] T096 [US1] Implement GET /api/organizations/{slug} endpoint in backend/app/routers/organizations.py (get org details with member/project counts)
- [ ] T097 [US1] Write pytest tests for PUT /api/organizations/{slug} in backend/tests/routers/test_organizations.py::test_update_org (test 200 success, 403 non-admin, 404 not found, partial updates)
- [ ] T098 [US1] Implement PUT /api/organizations/{slug} endpoint in backend/app/routers/organizations.py (update name, description, logo_url - admin/owner only)
- [ ] T099 [US1] Write pytest tests for DELETE /api/organizations/{slug} in backend/tests/routers/test_organizations.py::test_delete_org (test 204 success cascade deletes all, 403 non-owner, 400 name confirmation required)
- [ ] T100 [US1] Implement DELETE /api/organizations/{slug} endpoint in backend/app/routers/organizations.py (cascade delete all data - owner only, require name confirmation)
- [ ] T101 [US1] Write pytest tests for GET /api/organizations/{slug}/members in backend/tests/routers/test_organizations.py::test_list_members (test 200 members with roles, 403 non-member)
- [ ] T102 [US1] Implement GET /api/organizations/{slug}/members endpoint in backend/app/routers/organizations.py (list members with roles)
- [ ] T103 [US1] Write pytest tests for POST /api/organizations/{slug}/members/invite in backend/tests/routers/test_organizations.py::test_invite_member (test 201 invitation created and email sent, 429 rate limit 10/hour, 403 non-admin, 400 already member)
- [ ] T104 [US1] Implement POST /api/organizations/{slug}/members/invite endpoint in backend/app/routers/organizations.py (create invitation, send email, rate limit 10/hour)
- [ ] T105 [US1] Write pytest tests for DELETE /api/organizations/{slug}/members/{user_id} in backend/tests/routers/test_organizations.py::test_remove_member (test 204 success, 403 cannot remove owner, 403 non-admin, 404 member not found)
- [ ] T106 [US1] Implement DELETE /api/organizations/{slug}/members/{user_id} endpoint in backend/app/routers/organizations.py (remove member - admin/owner, cannot remove owner)
- [ ] T107 [US1] Write pytest tests for PUT /api/organizations/{slug}/members/{user_id}/role in backend/tests/routers/test_organizations.py::test_change_member_role (test 200 success, 403 non-owner, 400 invalid role, cannot demote owner)
- [ ] T108 [US1] Implement PUT /api/organizations/{slug}/members/{user_id}/role endpoint in backend/app/routers/organizations.py (change role - owner only)
- [ ] T109 [US1] Write pytest tests for PUT /api/organizations/{slug}/transfer-ownership in backend/tests/routers/test_organizations.py::test_transfer_ownership (test 200 owner changes and old owner becomes admin, 403 non-owner, 400 target not admin, 404 target not found)
- [ ] T110 [US1] Implement PUT /api/organizations/{slug}/transfer-ownership endpoint in backend/app/routers/organizations.py (verify new owner is org admin, update owner_id, demote old owner to admin, notify both users)
- [ ] T111 [US1] Write pytest tests for GET /api/invitations/{token} in backend/tests/routers/test_invitations.py::test_view_invitation (test 200 success with org details, 404 invalid token, 410 expired token)
- [ ] T112 [US1] Implement GET /api/invitations/{token} endpoint in backend/app/routers/invitations.py (view invitation details)
- [ ] T113 [US1] Write pytest tests for POST /api/invitations/{token}/accept in backend/tests/routers/test_invitations.py::test_accept_invitation (test 200 creates membership, 410 expired, 409 already member, auto-creates account if needed)
- [ ] T114 [US1] Implement POST /api/invitations/{token}/accept endpoint in backend/app/routers/invitations.py (accept invitation, create membership)
- [ ] T115 [US1] Write pytest tests for POST /api/invitations/{token}/decline in backend/tests/routers/test_invitations.py::test_decline_invitation (test 200 marks declined, 404 invalid token)
- [ ] T116 [US1] Implement POST /api/invitations/{token}/decline endpoint in backend/app/routers/invitations.py (mark invitation declined)
- [ ] T117 [P] [US1] Write Vitest tests for org list page in frontend/tests/pages/OrgListPage.test.tsx (test displays orgs, create button, role badges, empty state)
- [ ] T118 [P] [US1] Create organization list page in frontend/app/page.tsx (show user's orgs, create new org button)
- [ ] T119 [P] [US1] Write Vitest tests for CreateOrgModal in frontend/tests/components/organization/CreateOrgModal.test.tsx (test form validation, slug auto-generation from name, submit success, duplicate slug error)
- [ ] T120 [P] [US1] Create organization creation modal in frontend/components/organization/CreateOrgModal.tsx (slug, name, description form)
- [ ] T121 [P] [US1] Write Vitest tests for org dashboard in frontend/tests/pages/org/OrgDashboard.test.tsx (test recent activity, stats display, project list)
- [ ] T122 [P] [US1] Create organization dashboard page in frontend/app/[orgSlug]/page.tsx (recent activity, stats, project list)
- [ ] T123 [P] [US1] Write Vitest tests for org settings in frontend/tests/pages/org/OrgSettings.test.tsx (test edit form, delete with confirmation, archive toggle)
- [ ] T124 [P] [US1] Create organization settings page in frontend/app/[orgSlug]/settings/page.tsx (edit name, description, logo, danger zone for delete)
- [ ] T125 [P] [US1] Write Vitest tests for org members page in frontend/tests/pages/org/OrgMembers.test.tsx (test member list, role badges, remove button, invite button)
- [ ] T126 [P] [US1] Create organization members page in frontend/app/[orgSlug]/members/page.tsx (list members, invite button, role management)
- [ ] T127 [P] [US1] Write Vitest tests for InviteMemberModal in frontend/tests/components/organization/InviteMemberModal.test.tsx (test email validation, role selection, submit success)
- [ ] T128 [P] [US1] Create member invitation modal in frontend/components/organization/InviteMemberModal.tsx (email, role selection form)
- [ ] T129 [P] [US1] Write Vitest tests for invitation page in frontend/tests/pages/invitations/InvitationPage.test.tsx (test org details display, accept/decline buttons, expired state, already member state)
- [ ] T130 [P] [US1] Create invitation acceptance page in frontend/app/invitations/[token]/page.tsx (show org details, accept/decline buttons)
- [ ] T131 [US1] Write Vitest tests for useOrganizations hook in frontend/tests/lib/hooks/useOrganizations.test.ts (test CRUD mutations, loading states, optimistic updates)
- [ ] T132 [US1] Create useOrganizations hook in frontend/lib/hooks/useOrganizations.ts (TanStack Query hooks for CRUD operations)
- [ ] T133 [US1] Write Vitest tests for OrganizationContext in frontend/tests/lib/contexts/OrganizationContext.test.tsx (test current org state, org switcher)
- [ ] T134 [US1] Create organization context provider in frontend/lib/contexts/OrganizationContext.tsx (current org state, org switcher)
- [ ] T135 [US1] Write Playwright E2E test for org workflow in frontend/tests/e2e/organizations.spec.ts (test create org → invite member → accept invitation → change role → transfer ownership)

**Checkpoint**: Organization management fully functional and independently testable

---

## Phase 5: User Story 2 - Project Creation & Member Assignment (Priority: P1) 🎯 MVP

**Goal**: Org admin creates projects, assigns members with roles, defines project scope

**Independent Test**: Org admin creates "Website Redesign" project with key "WEB", assigns members with roles, verifies permissions control edit vs view

### Implementation for User Story 2

- [ ] T136 [P] [US2] Write pytest tests for Project model in backend/tests/models/test_project.py (test unique (org_id, key), key format validation, visibility enum, archived default false, next_task_number starts at 1)
- [ ] T137 [P] [US2] Create Project model in backend/app/models/project.py (id, organization_id, key, name, description, icon, visibility enum[private/organization], created_by, archived, next_task_number, created_at, updated_at)
- [ ] T138 [P] [US2] Write pytest tests for ProjectMember model in backend/tests/models/test_project.py (test unique (project_id, user_id), role enum validation, cascade delete)
- [ ] T139 [P] [US2] Create ProjectMember model in backend/app/models/project.py (id, project_id, user_id, role enum[admin/member/viewer], added_at)
- [ ] T140 [P] [US2] Write pytest tests for Board model in backend/tests/models/test_board.py (test one board per project for MVP, board_type enum, name required)
- [ ] T141 [P] [US2] Create Board model in backend/app/models/board.py (id, project_id, name, description, board_type enum[kanban], created_at, updated_at)
- [ ] T142 [P] [US2] Write pytest tests for Column model in backend/tests/models/test_board.py (test color hex validation, position ordering, wip_limit nullable, cascade delete)
- [ ] T143 [P] [US2] Create Column model in backend/app/models/board.py (id, board_id, name, color hex, position float, wip_limit nullable int, created_at, updated_at)
- [ ] T144 [US2] Write pytest tests for project migrations in backend/tests/migrations/test_003_projects.py (test tables created, indexes, constraints, default board creation trigger)
- [ ] T145 [US2] Create Alembic migration for Project, ProjectMember, Board, Column tables in backend/alembic/versions/003_create_projects_boards.py
- [ ] T146 [US2] Write pytest tests for POST /api/organizations/{orgSlug}/projects in backend/tests/routers/test_projects.py::test_create_project (test 201 success with auto-created board and 3 default columns, 400 duplicate key, 403 non-admin, creator auto-added as admin)
- [ ] T147 [US2] Implement POST /api/organizations/{orgSlug}/projects endpoint in backend/app/routers/projects.py (create project, auto-create board with 3 default columns, add creator as admin)
- [ ] T148 [US2] Write pytest tests for GET /api/organizations/{orgSlug}/projects in backend/tests/routers/test_projects.py::test_list_projects (test 200 with member/task counts, archived filter works, 403 non-member)
- [ ] T149 [US2] Implement GET /api/organizations/{orgSlug}/projects endpoint in backend/app/routers/projects.py (list org projects with member/task counts, filter by archived)
- [ ] T150 [US2] Write pytest tests for GET /api/projects/{projectKey} in backend/tests/routers/test_projects.py::test_get_project (test 200 with members and stats, 404 not found for non-members for security, 403 viewer can view)
- [ ] T151 [US2] Implement GET /api/projects/{projectKey} endpoint in backend/app/routers/projects.py (get project details with members and stats)
- [ ] T152 [US2] Write pytest tests for PUT /api/projects/{projectKey} in backend/tests/routers/test_projects.py::test_update_project (test 200 success, 403 non-admin, partial updates, icon validation)
- [ ] T153 [US2] Implement PUT /api/projects/{projectKey} endpoint in backend/app/routers/projects.py (update name, description, icon - admin only)
- [ ] T154 [US2] Write pytest tests for POST /api/projects/{projectKey}/archive in backend/tests/routers/test_projects.py::test_archive_project (test 200 sets archived=true, 403 non-admin, archived projects hidden from list)
- [ ] T155 [US2] Implement POST /api/projects/{projectKey}/archive endpoint in backend/app/routers/projects.py (set archived=true - admin only)
- [ ] T156 [US2] Write pytest tests for DELETE /api/projects/{projectKey} in backend/tests/routers/test_projects.py::test_delete_project (test 204 cascade deletes boards/tasks/comments/attachments, 403 non-admin)
- [ ] T157 [US2] Implement DELETE /api/projects/{projectKey} endpoint in backend/app/routers/projects.py (cascade delete all boards/tasks/comments/attachments - admin only)
- [ ] T158 [US2] Write pytest tests for GET /api/projects/{projectKey}/members in backend/tests/routers/test_projects.py::test_list_project_members (test 200 members with roles, 403 non-member)
- [ ] T159 [US2] Implement GET /api/projects/{projectKey}/members endpoint in backend/app/routers/projects.py (list project members with roles)
- [ ] T160 [US2] Write pytest tests for POST /api/projects/{projectKey}/members in backend/tests/routers/test_projects.py::test_add_project_member (test 201 success, 403 non-admin, 400 user not org member, 409 already member)
- [ ] T161 [US2] Implement POST /api/projects/{projectKey}/members endpoint in backend/app/routers/projects.py (add org member to project with role - admin only)
- [ ] T162 [US2] Write pytest tests for DELETE /api/projects/{projectKey}/members/{user_id} in backend/tests/routers/test_projects.py::test_remove_project_member (test 204 success, 403 non-admin, 404 not member)
- [ ] T163 [US2] Implement DELETE /api/projects/{projectKey}/members/{user_id} endpoint in backend/app/routers/projects.py (remove member - admin only)
- [ ] T164 [US2] Write pytest tests for PUT /api/projects/{projectKey}/members/{user_id}/role in backend/tests/routers/test_projects.py::test_change_project_member_role (test 200 success, 403 non-admin, 400 invalid role)
- [ ] T165 [US2] Implement PUT /api/projects/{projectKey}/members/{user_id}/role endpoint in backend/app/routers/projects.py (change role - admin only)
- [ ] T166 [US2] Write pytest tests for GET /api/projects/{projectKey}/boards in backend/tests/routers/test_boards.py::test_list_boards (test 200 returns boards, empty if none, 403 non-member)
- [ ] T167 [US2] Implement GET /api/projects/{projectKey}/boards endpoint in backend/app/routers/boards.py (list project boards)
- [ ] T168 [US2] Write pytest tests for GET /api/boards/{boardId} in backend/tests/routers/test_boards.py::test_get_board (test 200 with columns and tasks if include_tasks=true, columns sorted by position, 403 non-member)
- [ ] T169 [US2] Implement GET /api/boards/{boardId} endpoint in backend/app/routers/boards.py (get board with columns and tasks, optional include_tasks query param)
- [ ] T170 [P] [US2] Write Vitest tests for project list in frontend/tests/pages/org/ProjectList.test.tsx (test project cards with stats, create button, archived filter)
- [ ] T171 [P] [US2] Create project list page in frontend/app/[orgSlug]/page.tsx (show org's projects with stats, create project button)
- [ ] T172 [P] [US2] Write Vitest tests for CreateProjectModal in frontend/tests/components/project/CreateProjectModal.test.tsx (test key auto-generation, visibility toggle, icon picker, form validation)
- [ ] T173 [P] [US2] Create project creation modal in frontend/components/project/CreateProjectModal.tsx (key, name, description, icon, visibility form)
- [ ] T174 [P] [US2] Write Vitest tests for project dashboard in frontend/tests/pages/project/ProjectDashboard.test.tsx (test overview, stats, recent activity, members list)
- [ ] T175 [P] [US2] Create project dashboard page in frontend/app/[orgSlug]/[projectKey]/page.tsx (project overview, stats, recent activity)
- [ ] T176 [P] [US2] Write Vitest tests for project settings in frontend/tests/pages/project/ProjectSettings.test.tsx (test edit form, archive button, delete with confirmation)
- [ ] T177 [P] [US2] Create project settings page in frontend/app/[orgSlug]/[projectKey]/settings/page.tsx (edit project details, archive, delete)
- [ ] T178 [P] [US2] Write Vitest tests for project members page in frontend/tests/pages/project/ProjectMembers.test.tsx (test member list, add member modal, role management, remove button)
- [ ] T179 [P] [US2] Create project members page in frontend/app/[orgSlug]/[projectKey]/members/page.tsx (list members, add member button, role management)
- [ ] T180 [US2] Write Vitest tests for useProjects hook in frontend/tests/lib/hooks/useProjects.test.ts (test project CRUD mutations, member management, optimistic updates)
- [ ] T181 [US2] Create useProjects hook in frontend/lib/hooks/useProjects.ts (TanStack Query hooks for project CRUD)
- [ ] T182 [US2] Write Vitest tests for ProjectContext in frontend/tests/lib/contexts/ProjectContext.test.tsx (test current project state, project switching)
- [ ] T183 [US2] Create project context provider in frontend/lib/contexts/ProjectContext.tsx (current project state)
- [ ] T184 [US2] Write Playwright E2E test for project workflow in frontend/tests/e2e/projects.spec.ts (test create project → add members → assign roles → archive → restore → delete)

**Checkpoint**: Project management fully functional and independently testable

---

## Phase 6: User Story 3 - Task Management on Kanban Board (Priority: P1) 🎯 MVP

**Goal**: Team members create tasks, organize on Kanban board, drag-drop to update status, assign work

**Independent Test**: Member creates "Redesign homepage" task, adds details (description, priority High, assignee Alice), drags from "Todo" to "In Progress", verifies status updates

### Implementation for User Story 3

- [ ] T185 [P] [US3] Write pytest tests for Task model in backend/tests/models/test_task.py (test unique (project_id, task_number), display_id generation, position ordering, labels JSON, completed default false, all field validations)
- [ ] T186 [P] [US3] Create Task model in backend/app/models/task.py (id, project_id, board_id, column_id, task_number int, title, description markdown, task_type enum[story/bug/task/epic], priority enum[critical/high/medium/low/none], assignee_id nullable, reporter_id, due_date nullable, story_points nullable, position float, labels JSON array, archived bool, completed bool, created_at, updated_at)
- [ ] T187 [US3] Write pytest tests for task migrations in backend/tests/migrations/test_004_tasks.py (test table created, unique index on (project_id, task_number), composite indexes per data-model.md, foreign key constraints)
- [ ] T188 [US3] Create Alembic migration for Task table in backend/alembic/versions/004_create_tasks.py (with unique index on project_id, task_number and other indexes per data-model.md)
- [ ] T189 [US3] Write pytest tests for TaskNumberingService in backend/tests/services/test_task_numbering_service.py (test get_next_task_number with SELECT FOR UPDATE, concurrent request handling, sequence correctness)
- [ ] T190 [US3] Implement TaskNumberingService in backend/app/services/task_numbering_service.py (get_next_task_number with SELECT FOR UPDATE row-level lock)
- [ ] T191 [US3] Write pytest tests for POST /api/projects/{projectKey}/tasks in backend/tests/routers/test_tasks.py::test_create_task (test 201 with auto-incremented task_number and display_id KEY-NUM, 403 non-member, 400 invalid fields, default position calculation)
- [ ] T192 [US3] Implement POST /api/projects/{projectKey}/tasks endpoint in backend/app/routers/tasks.py (create task with auto-incremented task_number, generate display_id as KEY-NUMBER, default position)
- [ ] T193 [US3] Write pytest tests for GET /api/projects/{projectKey}/tasks in backend/tests/routers/test_tasks.py::test_list_tasks (test 200 with filters working: assignee_id, priority, column, labels, due_before, search, archived; pagination limit 100 default)
- [ ] T194 [US3] Implement GET /api/projects/{projectKey}/tasks endpoint in backend/app/routers/tasks.py (list tasks with filters: assignee_id, priority, status/column, labels, due_before, search, archived; pagination with limit 100 default)
- [ ] T195 [US3] Write pytest tests for GET /api/tasks/{taskId} in backend/tests/routers/test_tasks.py::test_get_task (test 200 with all fields, project info, assignee/reporter details, 403 non-member, 404 not found)
- [ ] T196 [US3] Implement GET /api/tasks/{taskId} endpoint in backend/app/routers/tasks.py (get task details with all fields, project info, assignee/reporter details)
- [ ] T197 [US3] Write pytest tests for PUT /api/tasks/{taskId} in backend/tests/routers/test_tasks.py::test_update_task (test 200 success updates any field, ActivityLog entries created for changes, 403 viewer cannot edit, partial updates work)
- [ ] T198 [US3] Implement PUT /api/tasks/{taskId} endpoint in backend/app/routers/tasks.py (update any field, create ActivityLog entries for changes)
- [ ] T199 [US3] Write pytest tests for PUT /api/tasks/{taskId}/move in backend/tests/routers/test_tasks.py::test_move_task (test 200 changes column_id and position, "moved" ActivityLog created, position calculation between tasks, 403 viewer cannot move)
- [ ] T200 [US3] Implement PUT /api/tasks/{taskId}/move endpoint in backend/app/routers/tasks.py (change column_id and position, create "moved" ActivityLog entry)
- [ ] T201 [US3] Write pytest tests for POST /api/tasks/{taskId}/duplicate in backend/tests/routers/test_tasks.py::test_duplicate_task (test 201 copies all fields except comments, increments task_number, 403 non-member)
- [ ] T202 [US3] Implement POST /api/tasks/{taskId}/duplicate endpoint in backend/app/routers/tasks.py (copy all fields except comments, increment task_number)
- [ ] T203 [US3] Write pytest tests for POST /api/tasks/{taskId}/archive in backend/tests/routers/test_tasks.py::test_archive_task (test 200 sets archived=true, archived tasks excluded from board, still searchable)
- [ ] T204 [US3] Implement POST /api/tasks/{taskId}/archive endpoint in backend/app/routers/tasks.py (set archived=true)
- [ ] T205 [US3] Write pytest tests for DELETE /api/tasks/{taskId} in backend/tests/routers/test_tasks.py::test_delete_task (test 204 cascade deletes comments/attachments/activity, 403 non-admin)
- [ ] T206 [US3] Implement DELETE /api/tasks/{taskId} endpoint in backend/app/routers/tasks.py (cascade delete comments/attachments/activity - admin only)
- [ ] T207 [P] [US3] Write Vitest tests for Kanban board page in frontend/tests/pages/board/BoardPage.test.tsx (test columns render, task cards display, drag-drop enabled, filters work)
- [ ] T208 [P] [US3] Create Kanban board page in frontend/app/[orgSlug]/[projectKey]/board/page.tsx (display columns with task cards, drag-drop enabled)
- [ ] T209 [P] [US3] Write Vitest tests for Column component in frontend/tests/components/board/Column.test.tsx (test header with name/color, task list, WIP limit indicator, droppable area)
- [ ] T210 [P] [US3] Create Column component in frontend/components/board/Column.tsx (column header with name/color, task list, WIP limit indicator, droppable area)
- [ ] T211 [P] [US3] Write Vitest tests for TaskCard in frontend/tests/components/board/TaskCard.test.tsx (test compact view shows title, assignee avatar, priority badge, due date, draggable behavior)
- [ ] T212 [P] [US3] Create TaskCard component in frontend/components/board/TaskCard.tsx (compact view: title, assignee avatar, priority badge, due date, draggable)
- [ ] T213 [P] [US3] Write Vitest tests for TaskDetailModal in frontend/tests/components/task/TaskDetailModal.test.tsx (test full-screen modal, all fields display, inline editing, tabs for comments/attachments/activity, close on Esc)
- [ ] T214 [P] [US3] Create TaskDetailModal component in frontend/components/task/TaskDetailModal.tsx (full-screen modal with all task fields, inline editing, tabs for comments/attachments/activity)
- [ ] T215 [P] [US3] Write Vitest tests for TaskForm in frontend/tests/components/task/TaskForm.test.tsx (test create/edit modes, React Hook Form + Zod validation, all field types, error states)
- [ ] T216 [P] [US3] Create TaskForm component in frontend/components/task/TaskForm.tsx (create/edit task form with React Hook Form + Zod validation)
- [ ] T217 [P] [US3] Write Vitest tests for drag-drop logic in frontend/tests/lib/hooks/useBoardDragDrop.test.ts (test @dnd-kit integration, position calculation between tasks, optimistic updates, error rollback)
- [ ] T218 [P] [US3] Create drag-and-drop logic in frontend/lib/hooks/useBoardDragDrop.ts (using @dnd-kit/core, calculate new position between tasks, optimistic updates)
- [ ] T219 [P] [US3] Write Vitest tests for TaskFilters in frontend/tests/components/board/TaskFilters.test.tsx (test assignee select, priority select, labels filter, due date picker, search input)
- [ ] T220 [P] [US3] Create task filters component in frontend/components/board/TaskFilters.tsx (assignee, priority, labels, due date, search input)
- [ ] T221 [US3] Write Vitest tests for useTasks hook in frontend/tests/lib/hooks/useTasks.test.ts (test task CRUD mutations, optimistic updates, error handling, cache invalidation)
- [ ] T222 [US3] Create useTasks hook in frontend/lib/hooks/useTasks.ts (TanStack Query hooks for task CRUD with optimistic updates)
- [ ] T223 [US3] Write Vitest tests for useBoard hook in frontend/tests/lib/hooks/useBoard.test.ts (test fetch board with columns and tasks, real-time optimistic updates on drag, polling for updates)
- [ ] T224 [US3] Create useBoard hook in frontend/lib/hooks/useBoard.ts (fetch board with columns and tasks, real-time optimistic updates on drag)
- [ ] T225 [US3] Write Vitest tests for board store in frontend/tests/stores/boardStore.test.ts (test filters state, selected task, drag state, reset on board change)
- [ ] T226 [US3] Create board state store in frontend/stores/boardStore.ts (Zustand store for filters, selected task, drag state)
- [ ] T227 [US3] Write Playwright E2E test for task workflow in frontend/tests/e2e/tasks.spec.ts (test create task → edit details → drag to new column → duplicate → archive → verify activity log)

**Checkpoint**: Task management and Kanban board fully functional and independently testable

---

## Phase 7: User Story 4 - Task Collaboration via Comments & Activity (Priority: P2)

**Goal**: Team members discuss tasks with comments, @mention users, view activity history

**Independent Test**: Member opens task, adds comment "@Alice can you review this design?", Alice receives notification, all users see activity log with timestamps

### Implementation for User Story 4

- [ ] T228 [P] [US4] Write pytest tests for Comment model in backend/tests/models/test_comment.py (test content required, edited default false, cascade delete on task delete, user attribution)
- [ ] T229 [P] [US4] Create Comment model in backend/app/models/comment.py (id, task_id, user_id, content markdown, edited bool, created_at, updated_at)
- [ ] T230 [P] [US4] Write pytest tests for ActivityLog model in backend/tests/models/test_activity.py (test action enum, field_name/old_value/new_value nullable, cascade delete, timestamp ordering)
- [ ] T231 [P] [US4] Create ActivityLog model in backend/app/models/activity.py (id, task_id, user_id, action string, field_name nullable, old_value nullable text, new_value nullable text, created_at)
- [ ] T232 [US4] Write pytest tests for comment/activity migrations in backend/tests/migrations/test_005_comments_activity.py (test tables created, indexes, foreign keys, cascade rules)
- [ ] T233 [US4] Create Alembic migration for Comment and ActivityLog tables in backend/alembic/versions/005_create_comments_activity.py
- [ ] T234 [US4] Write pytest tests for POST /api/tasks/{taskId}/comments in backend/tests/routers/test_comments.py::test_create_comment (test 201 success, @mention parsing works, notifications triggered for mentions, 403 non-member, markdown support)
- [ ] T235 [US4] Implement POST /api/tasks/{taskId}/comments endpoint in backend/app/routers/comments.py (create comment, parse @mentions, trigger notifications)
- [ ] T236 [US4] Write pytest tests for GET /api/tasks/{taskId}/comments in backend/tests/routers/test_comments.py::test_list_comments (test 200 sorted asc/desc by created_at, 403 non-member, edited flag shown)
- [ ] T237 [US4] Implement GET /api/tasks/{taskId}/comments endpoint in backend/app/routers/comments.py (list comments sorted by created_at asc/desc)
- [ ] T238 [US4] Write pytest tests for PUT /api/comments/{commentId} in backend/tests/routers/test_comments.py::test_edit_comment (test 200 within 5min sets edited=true, 403 after 5min, 403 non-author, content validation)
- [ ] T239 [US4] Implement PUT /api/comments/{commentId} endpoint in backend/app/routers/comments.py (edit comment within 5 min of creation, set edited=true)
- [ ] T240 [US4] Write pytest tests for DELETE /api/comments/{commentId} in backend/tests/routers/test_comments.py::test_delete_comment (test 204 success for author or admin, 403 non-author non-admin)
- [ ] T241 [US4] Implement DELETE /api/comments/{commentId} endpoint in backend/app/routers/comments.py (author or admin only)
- [ ] T242 [US4] Write pytest tests for GET /api/tasks/{taskId}/activity in backend/tests/routers/test_tasks.py::test_get_activity (test 200 sorted desc by created_at, includes created/updated/moved/commented actions, 403 non-member)
- [ ] T243 [US4] Implement GET /api/tasks/{taskId}/activity endpoint in backend/app/routers/tasks.py (list activity logs sorted by created_at desc)
- [ ] T244 [US4] Write pytest tests for GET /api/tasks/{taskId}/activity/export in backend/tests/routers/test_tasks.py::test_export_activity_csv (test 200 CSV with headers timestamp/user/action/field/old_value/new_value, content-type header, streaming for large datasets, 403 non-admin)
- [ ] T245 [US4] Implement GET /api/tasks/{taskId}/activity/export endpoint in backend/app/routers/tasks.py (generate CSV with headers: timestamp, user, action, field, old_value, new_value; stream response for large datasets; admin only)
- [ ] T246 [US4] Write pytest tests for activity logging on task update in backend/tests/routers/test_tasks.py::test_task_update_creates_activity (test ActivityLog entries created for each changed field with old/new values)
- [ ] T247 [US4] Add activity logging to task update handler in backend/app/routers/tasks.py (create ActivityLog entries for each field change)
- [ ] T248 [US4] Write pytest tests for activity logging on task move in backend/tests/routers/test_tasks.py::test_task_move_creates_activity (test "moved" ActivityLog with from_column/to_column in old_value/new_value)
- [ ] T249 [US4] Add activity logging to task move handler in backend/app/routers/tasks.py (create "moved" ActivityLog entry)
- [ ] T250 [P] [US4] Write Vitest tests for CommentThread in frontend/tests/components/comment/CommentThread.test.tsx (test comments display with author info, edit/delete buttons shown for author, markdown rendering, sort order)
- [ ] T251 [P] [US4] Create CommentThread component in frontend/components/comment/CommentThread.tsx (list comments with author info, edit/delete buttons)
- [ ] T252 [P] [US4] Write Vitest tests for CommentForm in frontend/tests/components/comment/CommentForm.test.tsx (test markdown editor, @mention autocomplete, submit button, character count, validation)
- [ ] T253 [P] [US4] Create CommentForm component in frontend/components/comment/CommentForm.tsx (markdown editor, @mention autocomplete, submit button)
- [ ] T254 [P] [US4] Write Vitest tests for ActivityTimeline in frontend/tests/components/task/ActivityTimeline.test.tsx (test chronological display, icons per action type, user attribution, time formatting)
- [ ] T255 [P] [US4] Create ActivityTimeline component in frontend/components/task/ActivityTimeline.tsx (chronological activity log with icons, user attribution)
- [ ] T256 [US4] Write Vitest tests for comment/activity tabs in TaskDetailModal in frontend/tests/components/task/TaskDetailModal.test.tsx (test tab switching, comment count badge, activity count)
- [ ] T257 [US4] Integrate CommentThread and ActivityTimeline into TaskDetailModal in frontend/components/task/TaskDetailModal.tsx (tabs for comments and activity)
- [ ] T258 [US4] Write Vitest tests for useComments hook in frontend/tests/lib/hooks/useComments.test.ts (test comment CRUD mutations, optimistic updates, @mention parsing)
- [ ] T259 [US4] Create useComments hook in frontend/lib/hooks/useComments.ts (TanStack Query hooks for comment CRUD)
- [ ] T260 [US4] Write Vitest tests for useActivity hook in frontend/tests/lib/hooks/useActivity.test.ts (test activity log fetching, export CSV download, polling for updates)
- [ ] T261 [US4] Create useActivity hook in frontend/lib/hooks/useActivity.ts (TanStack Query hook for activity log fetching)
- [ ] T262 [US4] Write Vitest tests for mention utilities in frontend/tests/lib/utils/mentions.test.ts (test @username pattern detection, user autocomplete fetching, replacement in text)
- [ ] T263 [US4] Implement @mention parsing and user autocomplete in frontend/lib/utils/mentions.ts (detect @username pattern, fetch matching users)
- [ ] T264 [US4] Write Playwright E2E test for collaboration workflow in frontend/tests/e2e/collaboration.spec.ts (test add comment with @mention → edit comment → receive notification → view activity log → export CSV)

**Checkpoint**: Task collaboration features fully functional and independently testable

---

## Phase 8: User Story 5 - File Attachments for Task Documentation (Priority: P2)

**Goal**: Team members attach design mockups, documents, screenshots to tasks

**Independent Test**: Member uploads "mockup.png" (3MB) to task, sees thumbnail, other members can download, uploader can delete

### Implementation for User Story 5

- [ ] T265 [P] [US5] Write pytest tests for Attachment model in backend/tests/models/test_attachment.py (test filename required, file_size validation, mime_type validation, storage_path unique, cascade delete)
- [ ] T266 [P] [US5] Create Attachment model in backend/app/models/attachment.py (id, task_id, user_id, filename, file_size int, mime_type, storage_path, created_at)
- [ ] T267 [US5] Write pytest tests for attachment migrations in backend/tests/migrations/test_006_attachments.py (test table created, indexes, foreign keys, cascade delete)
- [ ] T268 [US5] Create Alembic migration for Attachment table in backend/alembic/versions/006_create_attachments.py
- [ ] T269 [US5] Write pytest tests for POST /api/tasks/{taskId}/attachments in backend/tests/routers/test_attachments.py::test_upload (test 201 multipart upload, MIME type validation, size limit 10MB enforced, filename sanitization, max 20 per task enforced, 403 non-member)
- [ ] T270 [US5] Implement POST /api/tasks/{taskId}/attachments endpoint in backend/app/routers/attachments.py (multipart upload, validate MIME type/size/extension, sanitize filename, save to filesystem, max 10MB, max 20 per task)
- [ ] T271 [US5] Write pytest tests for GET /api/tasks/{taskId}/attachments in backend/tests/routers/test_attachments.py::test_list_attachments (test 200 with metadata and uploader info, 403 non-member, sorted by created_at desc)
- [ ] T272 [US5] Implement GET /api/tasks/{taskId}/attachments endpoint in backend/app/routers/attachments.py (list attachments with metadata and uploader info)
- [ ] T273 [US5] Write pytest tests for GET /api/attachments/{attachmentId}/download in backend/tests/routers/test_attachments.py::test_download (test 200 with file content, Content-Disposition header with filename, 403 non-member, 404 not found)
- [ ] T274 [US5] Implement GET /api/attachments/{attachmentId}/download endpoint in backend/app/routers/attachments.py (authenticated download with Content-Disposition header)
- [ ] T275 [US5] Write pytest tests for DELETE /api/attachments/{attachmentId} in backend/tests/routers/test_attachments.py::test_delete_attachment (test 204 deletes from storage and DB, 403 non-uploader non-admin, file removed from filesystem)
- [ ] T276 [US5] Implement DELETE /api/attachments/{attachmentId} endpoint in backend/app/routers/attachments.py (delete from storage and database - uploader or admin only)
- [ ] T277 [US5] Write pytest tests for upload directory creation in backend/tests/services/test_file_service.py::test_upload_dir_structure (test organized by org_id/project_id/task_id per research.md)
- [ ] T278 [US5] Create upload directory structure in backend/uploads/ (organized by org_id/project_id/task_id per research.md)
- [ ] T279 [P] [US5] Write Vitest tests for AttachmentList in frontend/tests/components/task/AttachmentList.test.tsx (test thumbnail grid for images, file icons for documents, download/delete buttons, uploader attribution)
- [ ] T280 [P] [US5] Create AttachmentList component in frontend/components/task/AttachmentList.tsx (thumbnail grid for images, file icons for documents, download/delete buttons)
- [ ] T281 [P] [US5] Write Vitest tests for FileUpload in frontend/tests/components/task/FileUpload.test.tsx (test drag-drop area, file input, progress indicator, size/type validation before upload, error states)
- [ ] T282 [P] [US5] Create FileUpload component in frontend/components/task/FileUpload.tsx (drag-drop area, file input, progress indicator, size/type validation)
- [ ] T283 [P] [US5] Write Vitest tests for ImagePreviewModal in frontend/tests/components/task/ImagePreviewModal.test.tsx (test full-size view, zoom controls, close on Esc, navigation between images)
- [ ] T284 [P] [US5] Create image preview modal in frontend/components/task/ImagePreviewModal.tsx (full-size image view with zoom)
- [ ] T285 [US5] Write Vitest tests for attachments tab in TaskDetailModal in frontend/tests/components/task/TaskDetailModal.test.tsx (test attachments tab with count badge, upload area, attachment list)
- [ ] T286 [US5] Integrate AttachmentList and FileUpload into TaskDetailModal in frontend/components/task/TaskDetailModal.tsx (attachments tab)
- [ ] T287 [US5] Write Vitest tests for useAttachments hook in frontend/tests/lib/hooks/useAttachments.test.ts (test upload with progress tracking, list, download, delete mutations, error handling)
- [ ] T288 [US5] Create useAttachments hook in frontend/lib/hooks/useAttachments.ts (TanStack Query hooks for upload/list/download/delete with progress tracking)
- [ ] T289 [US5] Write Playwright E2E test for attachment workflow in frontend/tests/e2e/attachments.spec.ts (test upload image → view thumbnail → open preview → download → delete)

**Checkpoint**: File attachment features fully functional and independently testable

---

## Phase 9: User Story 6 - Board & Column Customization (Priority: P2)

**Goal**: Project admins customize Kanban board columns (rename, add new states, set WIP limits)

**Independent Test**: Admin adds "Code Review" column between "In Progress" and "Done", sets WIP limit 5, team sees updated board layout

### Implementation for User Story 6

- [ ] T290 [US6] Write pytest tests for POST /api/boards/{boardId}/columns in backend/tests/routers/test_columns.py::test_create_column (test 201 success with name/color/position/wip_limit, 403 non-admin, position ordering works)
- [ ] T291 [US6] Implement POST /api/boards/{boardId}/columns endpoint in backend/app/routers/columns.py (create column with name, color, position, wip_limit - admin only)
- [ ] T292 [US6] Write pytest tests for PUT /api/columns/{columnId} in backend/tests/routers/test_columns.py::test_update_column (test 200 success updates name/color/wip_limit, 403 non-admin, color hex validation)
- [ ] T293 [US6] Implement PUT /api/columns/{columnId} endpoint in backend/app/routers/columns.py (update name, color, wip_limit - admin only)
- [ ] T294 [US6] Write pytest tests for DELETE /api/columns/{columnId} in backend/tests/routers/test_columns.py::test_delete_column (test 204 moves all tasks to target column first, 403 non-admin, 400 if move_tasks_to missing and column has tasks)
- [ ] T295 [US6] Implement DELETE /api/columns/{columnId} endpoint in backend/app/routers/columns.py (move all tasks to target column first, then delete - admin only, require move_tasks_to query param)
- [ ] T296 [US6] Write pytest tests for WIP limit validation in backend/tests/routers/test_tasks.py::test_move_task_wip_limit (test warning returned if moving to column at/exceeding WIP limit, move still succeeds but warns)
- [ ] T297 [US6] Add WIP limit validation to task move handler in backend/app/routers/tasks.py (warn if moving to column at/exceeding WIP limit)
- [ ] T298 [P] [US6] Write Vitest tests for board settings page in frontend/tests/pages/board/BoardSettings.test.tsx (test column list, add/edit/delete buttons, reorder drag-drop, admin-only access)
- [ ] T299 [P] [US6] Create board settings page in frontend/app/[orgSlug]/[projectKey]/board/settings/page.tsx (manage columns, add/edit/delete, reorder)
- [ ] T300 [P] [US6] Write Vitest tests for ColumnEditor in frontend/tests/components/board/ColumnEditor.test.tsx (test form for name, color picker, position input, WIP limit input, validation)
- [ ] T301 [P] [US6] Create ColumnEditor component in frontend/components/board/ColumnEditor.tsx (form for name, color picker, position, WIP limit)
- [ ] T302 [P] [US6] Write Vitest tests for WIP limit indicator in frontend/tests/components/board/Column.test.tsx (test shows X/limit, highlights when at/over limit with red badge)
- [ ] T303 [P] [US6] Add WIP limit indicator to Column component in frontend/components/board/Column.tsx (show X/limit, highlight when at/over limit)
- [ ] T304 [US6] Write Vitest tests for column reorder in frontend/tests/components/board/BoardSettings.test.tsx (test drag-drop reordering updates positions, optimistic updates, error rollback)
- [ ] T305 [US6] Add column drag-and-drop reordering in frontend/components/board/BoardSettings.tsx (using @dnd-kit/core, update positions)
- [ ] T306 [US6] Write Vitest tests for useColumns hook in frontend/tests/lib/hooks/useColumns.test.ts (test column CRUD mutations, reorder mutation, optimistic updates)
- [ ] T307 [US6] Create useColumns hook in frontend/lib/hooks/useColumns.ts (TanStack Query hooks for column CRUD)
- [ ] T308 [US6] Write Playwright E2E test for board customization in frontend/tests/e2e/board-customization.spec.ts (test add column → rename → change color → set WIP limit → reorder → delete with move tasks → verify board updates)

**Checkpoint**: Board customization features fully functional and independently testable

---

## Phase 10: User Story 8 - Dashboard & Task Overview (Priority: P3)

**Goal**: Users see dashboard with all tasks assigned to them across projects, with filtering/sorting

**Independent Test**: User navigates to "My Tasks", sees tasks from 3 projects grouped by project, filters by priority "Critical", sorts by due date

### Implementation for User Story 8

- [ ] T309 [US8] Write pytest tests for GET /api/organizations/{orgSlug}/dashboard in backend/tests/routers/test_dashboard.py::test_org_dashboard (test 200 with stats: member/project counts, total tasks, completed this week, overdue; recent activity; project list; 403 non-member)
- [ ] T310 [US8] Implement GET /api/organizations/{orgSlug}/dashboard endpoint in backend/app/routers/dashboard.py (org stats: member/project counts, total tasks, completed this week, overdue, recent activity, project list)
- [ ] T311 [US8] Write pytest tests for GET /api/projects/{projectKey}/dashboard in backend/tests/routers/test_dashboard.py::test_project_dashboard (test 200 with stats: tasks by status, completed this week/month, overdue, assigned to me; recent activity; upcoming deadlines; 403 non-member)
- [ ] T312 [US8] Implement GET /api/projects/{projectKey}/dashboard endpoint in backend/app/routers/dashboard.py (project stats: tasks by status, completed this week/month, overdue, assigned to me, recent activity, upcoming deadlines)
- [ ] T313 [US8] Write pytest tests for GET /api/users/me/tasks in backend/tests/routers/test_dashboard.py::test_my_tasks (test 200 with all user's tasks across projects, filters work: status, priority, project_key, due_before; group_by works: project, priority, due_date; sort_by works: due_date, priority, project; pagination)
- [ ] T314 [US8] Implement GET /api/users/me/tasks endpoint in backend/app/routers/dashboard.py (all tasks assigned to current user across all projects, with filters: status, priority, project_key, due_before, group_by, sort_by, pagination)
- [ ] T315 [P] [US8] Write Vitest tests for org dashboard in frontend/tests/pages/org/OrgDashboard.test.tsx (test stats cards, recent activity feed, project list with quick access, loading states)
- [ ] T316 [P] [US8] Create organization dashboard page in frontend/app/[orgSlug]/page.tsx (display org stats, recent activity, project list with quick access)
- [ ] T317 [P] [US8] Write Vitest tests for project dashboard in frontend/tests/pages/project/ProjectDashboard.test.tsx (test task breakdown chart, completed stats, overdue badge, recent activity, upcoming deadlines list)
- [ ] T318 [P] [US8] Create project dashboard page in frontend/app/[orgSlug]/[projectKey]/page.tsx (display project stats, task breakdown, recent activity, upcoming deadlines)
- [ ] T319 [P] [US8] Write Vitest tests for My Tasks page in frontend/tests/pages/me/MyTasks.test.tsx (test grouped by project display, filters work, sort options, quick status update, empty state)
- [ ] T320 [P] [US8] Create "My Tasks" page in frontend/app/me/tasks/page.tsx (grouped by project, filterable, sortable, quick status update)
- [ ] T321 [P] [US8] Write Vitest tests for DashboardStats in frontend/tests/components/dashboard/DashboardStats.test.tsx (test stat cards with icons, counts display, trends indication, responsive layout)
- [ ] T322 [P] [US8] Create DashboardStats component in frontend/components/dashboard/DashboardStats.tsx (stat cards with icons, counts, trends)
- [ ] T323 [P] [US8] Write Vitest tests for RecentActivity in frontend/tests/components/dashboard/RecentActivity.test.tsx (test activity feed with avatars, timestamps, links to tasks, load more pagination)
- [ ] T324 [P] [US8] Create RecentActivity component in frontend/components/dashboard/RecentActivity.tsx (activity feed with avatars, timestamps, links)
- [ ] T325 [US8] Write Vitest tests for useDashboard hook in frontend/tests/lib/hooks/useDashboard.test.ts (test org/project/user dashboard data fetching, refresh on interval, cache invalidation)
- [ ] T326 [US8] Create useDashboard hook in frontend/lib/hooks/useDashboard.ts (TanStack Query hooks for org/project/user dashboard data)
- [ ] T327 [US8] Write Playwright E2E test for dashboard workflow in frontend/tests/e2e/dashboards.spec.ts (test view org dashboard → click project → view project dashboard → navigate to My Tasks → filter and sort)

**Checkpoint**: Dashboard and overview features fully functional and independently testable

---

## Phase 11: User Story 9 - Email Notifications for Task Updates (Priority: P3)

**Goal**: Users receive email notifications when assigned tasks, @mentioned, or watching task updates

**Independent Test**: User enables email notifications in settings, gets assigned a task, receives email "You've been assigned to WEB-123", can disable notifications

### Implementation for User Story 9

- [ ] T328 [P] [US9] Write pytest tests for Notification model in backend/tests/models/test_notification.py (test type enum validation, reference_id required, read default false, cascade delete on user delete)
- [ ] T329 [P] [US9] Create Notification model in backend/app/models/notification.py (id, user_id, type enum[task_assigned/mentioned/comment_added/due_soon], reference_id UUID, title, message, read bool, created_at)
- [ ] T330 [US9] Write pytest tests for notification migrations in backend/tests/migrations/test_007_notifications.py (test table created, indexes on (user_id, read), foreign keys, cascade delete)
- [ ] T331 [US9] Create Alembic migration for Notification table in backend/alembic/versions/007_create_notifications.py
- [ ] T332 [US9] Write pytest tests for NotificationService in backend/tests/services/test_notification_service.py (test create_notification, send_email_notification checks email_verified and preferences before sending, notification types handled correctly)
- [ ] T333 [US9] Implement NotificationService in backend/app/services/notification_service.py (create_notification, send_email_notification methods)
- [ ] T334 [US9] Write pytest tests for notification creation on task assignment in backend/tests/routers/test_tasks.py::test_task_assign_notification (test task_assigned notification created when assignee changes, email sent if enabled)
- [ ] T335 [US9] Add notification creation to task assignment in backend/app/routers/tasks.py (trigger task_assigned notification)
- [ ] T336 [US9] Write pytest tests for notification creation on @mentions in backend/tests/routers/test_comments.py::test_mention_notification (test mentioned notification created for each @username, duplicate mentions deduplicated, email sent if enabled)
- [ ] T337 [US9] Add notification creation to comment @mentions in backend/app/routers/comments.py (trigger mentioned notification)
- [ ] T338 [US9] Write pytest tests for GET /api/notifications in backend/tests/routers/test_notifications.py::test_list_notifications (test 200 with filters: read, type; pagination; sorted by created_at desc; unread_count included)
- [ ] T339 [US9] Implement GET /api/notifications endpoint in backend/app/routers/notifications.py (list user notifications with filters: read, type, pagination)
- [ ] T340 [US9] Write pytest tests for PUT /api/notifications/{notificationId}/read in backend/tests/routers/test_notifications.py::test_mark_read (test 200 marks as read, 403 not owner, idempotent)
- [ ] T341 [US9] Implement PUT /api/notifications/{notificationId}/read endpoint in backend/app/routers/notifications.py (mark as read)
- [ ] T342 [US9] Write pytest tests for PUT /api/notifications/read-all in backend/tests/routers/test_notifications.py::test_mark_all_read (test 200 marks all unread as read, returns count)
- [ ] T343 [US9] Implement PUT /api/notifications/read-all endpoint in backend/app/routers/notifications.py (mark all as read)
- [ ] T344 [US9] Write pytest tests for email preferences in User model in backend/tests/models/test_user.py::test_email_notification_preferences (test email_notifications_enabled bool field, default true)
- [ ] T345 [US9] Add email notification preferences to User model in backend/app/models/user.py (email_notifications_enabled bool field)
- [ ] T346 [US9] Write pytest tests for email sending in backend/tests/services/test_email_service.py::test_notification_email (test checks email_verified and email_notifications_enabled before sending, queues if not verified, skips if disabled)
- [ ] T347 [US9] Implement background task for sending email notifications in backend/app/services/email_service.py (check email_verified and preferences before sending)
- [ ] T348 [P] [US9] Write Vitest tests for notification center in frontend/tests/pages/me/Notifications.test.tsx (test notification list, mark as read, filter by type, empty state, load more)
- [ ] T349 [P] [US9] Create notification center page in frontend/app/me/notifications/page.tsx (list notifications, mark as read, filter by type)
- [ ] T350 [P] [US9] Write Vitest tests for NotificationBell in frontend/tests/components/layout/NotificationBell.test.tsx (test bell icon in navbar, unread count badge, dropdown preview of recent 5, mark all read button, link to notification center)
- [ ] T351 [P] [US9] Create NotificationBell component in frontend/components/layout/NotificationBell.tsx (bell icon in navbar, unread count badge, dropdown preview)
- [ ] T352 [P] [US9] Write Vitest tests for notification preferences in frontend/tests/pages/me/ProfilePage.test.tsx (test email notifications toggle, save button, success feedback)
- [ ] T353 [P] [US9] Add notification preferences to profile settings in frontend/app/me/profile/page.tsx (toggle email notifications)
- [ ] T354 [US9] Write Vitest tests for useNotifications hook in frontend/tests/lib/hooks/useNotifications.test.ts (test list query with auto-refetch every 30s, mark read mutation, mark all read mutation, unread count)
- [ ] T355 [US9] Create useNotifications hook in frontend/lib/hooks/useNotifications.ts (TanStack Query hooks for notifications, auto-refetch)
- [ ] T356 [US9] Write Playwright E2E test for notification workflow in frontend/tests/e2e/notifications.spec.ts (test assign task → check notification bell shows badge → open dropdown → click notification → navigate to task → mark as read → badge updates)

**Checkpoint**: Email notification features fully functional and independently testable

---

## Phase 12: User Story 10 - Global Search & Filters (Priority: P3)

**Goal**: Users search tasks by title/description across all projects, apply advanced filters

**Independent Test**: User types "homepage" in global search, sees results from multiple projects, filters by assignee "Alice", clicks result to open task

### Implementation for User Story 10

- [ ] T357 [US10] Write pytest tests for GET /api/organizations/{orgSlug}/search in backend/tests/routers/test_search.py::test_org_search (test 200 full-text search across tasks/projects, filters work: q, project_key, assignee_id, priority, labels, due_before, created_after; pagination; relevance scoring)
- [ ] T358 [US10] Implement GET /api/organizations/{orgSlug}/search endpoint in backend/app/routers/search.py (full-text search across tasks/projects, filters: q, project_key, assignee_id, priority, labels, due_before, created_after, pagination, relevance scoring)
- [ ] T359 [US10] Write pytest tests for GET /api/projects/{projectKey}/search in backend/tests/routers/test_search.py::test_project_search (test 200 same as org search but scoped to project only)
- [ ] T360 [US10] Implement GET /api/projects/{projectKey}/search endpoint in backend/app/routers/search.py (same as org search but scoped to project)
- [ ] T361 [US10] Write pytest tests for search indexes in backend/tests/migrations/test_008_search_indexes.py (test PostgreSQL GIN index created on title + description, performance improvement verified)
- [ ] T362 [US10] Add full-text search indexes to Task table in backend/alembic/versions/008_add_search_indexes.py (PostgreSQL GIN index on title + description)
- [ ] T363 [P] [US10] Write Vitest tests for SearchBar in frontend/tests/components/layout/SearchBar.test.tsx (test autocomplete with debounce, keyboard shortcuts (/ to focus), recent searches stored, loading state)
- [ ] T364 [P] [US10] Create global search bar in frontend/components/layout/SearchBar.tsx (autocomplete, keyboard shortcuts, recent searches)
- [ ] T365 [P] [US10] Write Vitest tests for search results page in frontend/tests/pages/org/SearchResults.test.tsx (test tasks and projects displayed, filters sidebar, sort options, empty state, load more pagination)
- [ ] T366 [P] [US10] Create search results page in frontend/app/[orgSlug]/search/page.tsx (display tasks and projects, filters sidebar, sort options)
- [ ] T367 [P] [US10] Write Vitest tests for AdvancedFilters in frontend/tests/components/search/AdvancedFilters.test.tsx (test assignee select, priority checkboxes, labels input, date range pickers, reset button)
- [ ] T368 [P] [US10] Create AdvancedFilters component in frontend/components/search/AdvancedFilters.tsx (assignee, priority, labels, date ranges)
- [ ] T369 [US10] Write Vitest tests for useSearch hook in frontend/tests/lib/hooks/useSearch.test.ts (test search query with 300ms debounce, filters state, optimistic loading, cache results)
- [ ] T370 [US10] Create useSearch hook in frontend/lib/hooks/useSearch.ts (TanStack Query hooks for search with debouncing)
- [ ] T371 [US10] Write Playwright E2E test for search workflow in frontend/tests/e2e/search.spec.ts (test type in search bar → press / to focus → autocomplete appears → select result → see full results page → apply filters → click task → modal opens)

**Checkpoint**: Global search features fully functional and independently testable

---

## Phase 13: Polish & Cross-Cutting Concerns

**Purpose**: Improvements that affect multiple user stories

- [ ] T372 [P] Write pytest tests for CORS in backend/tests/test_main.py::test_cors (test allowed origins from env, preflight requests, credentials allowed)
- [ ] T373 [P] Add CORS configuration to backend/app/main.py per quickstart.md (ALLOWED_ORIGINS environment variable)
- [ ] T374 [P] Write pytest tests for rate limiting in backend/tests/test_rate_limiting.py (test 429 after exceeding limits: 100 req/min per IP, 500 req/min per user; rate limit headers; stricter for auth)
- [ ] T375 [P] Add rate limiting middleware to backend/app/main.py (100 req/min per IP, 500 req/min per user, stricter for auth endpoints)
- [ ] T376 [P] Write pytest tests for CSRF protection in backend/tests/test_csrf.py (test double-submit cookie validation, 403 on CSRF mismatch, exempt GET/HEAD/OPTIONS)
- [ ] T377 [P] Add CSRF protection to backend/app/main.py (double-submit cookie pattern)
- [ ] T378 [P] Write pytest tests for request logging in backend/tests/test_logging.py (test structured JSON logs with request_id, timestamp, method, path, status, duration)
- [ ] T379 [P] Add request logging middleware to backend/app/main.py (structured JSON logs)
- [ ] T380 [P] Add error tracking integration in backend/app/main.py (placeholder for Sentry)
- [ ] T381 [P] Write pytest tests for AuditService in backend/tests/services/test_audit_service.py (test audit log creation for delete org, delete project, delete task; verify timestamp, user_id, resource_type, resource_id, metadata captured)
- [ ] T382 [P] Implement AuditService in backend/app/services/audit_service.py (log_admin_action method, create audit_logs table entry with user_id, action_type enum, resource_type, resource_id, timestamp, metadata JSON)
- [ ] T383 [P] Write Vitest tests for root layout in frontend/tests/app/layout.test.tsx (test navbar renders, providers wrap children, Tailwind globals load, theme provider)
- [ ] T384 [P] Create root layout in frontend/app/layout.tsx (navbar, TanStack Query provider, auth provider, Tailwind globals)
- [ ] T385 [P] Write Vitest tests for Navbar in frontend/tests/components/layout/Navbar.test.tsx (test org switcher, project nav, search bar, notifications bell, user menu, responsive collapse)
- [ ] T386 [P] Create Navbar component in frontend/components/layout/Navbar.tsx (org switcher, project nav, search, notifications, user menu)
- [ ] T387 [P] Write Vitest tests for Sidebar in frontend/tests/components/layout/Sidebar.test.tsx (test project nav links, collapsible behavior, responsive hide on mobile, active state highlighting)
- [ ] T388 [P] Create Sidebar component in frontend/components/layout/Sidebar.tsx (project nav, collapsible, responsive)
- [ ] T389 [P] Write Vitest tests for UserMenu in frontend/tests/components/layout/UserMenu.test.tsx (test profile link, settings link, signout button, dropdown positioning)
- [ ] T390 [P] Create UserMenu component in frontend/components/layout/UserMenu.tsx (profile, settings, signout dropdown)
- [ ] T391 [P] Write Vitest tests for LoadingSkeleton in frontend/tests/components/common/LoadingSkeleton.test.tsx (test skeleton variants: card, list, table; animation)
- [ ] T392 [P] Create loading states and skeleton components in frontend/components/common/LoadingSkeleton.tsx
- [ ] T393 [P] Write Vitest tests for ErrorBoundary in frontend/tests/components/common/ErrorBoundary.test.tsx (test catches React errors, displays fallback UI, error reporting, reset button)
- [ ] T394 [P] Create error boundary component in frontend/components/common/ErrorBoundary.tsx (catch React errors, display fallback)
- [ ] T395 [P] Write Vitest tests for Toast in frontend/tests/components/common/Toast.test.tsx (test success/error/info variants, auto-dismiss timing, close button, stacking)
- [ ] T396 [P] Add toast notification system in frontend/components/common/Toast.tsx (success, error, info toasts)
- [ ] T397 [P] Configure shadcn/ui theme in frontend/components/ui/ (Button, Input, Modal, Select, etc.)
- [ ] T398 [P] Write Vitest tests for ThemeToggle in frontend/tests/components/layout/ThemeToggle.test.tsx (test dark/light/system modes, localStorage persistence, icon changes)
- [ ] T399 [P] Create dark/light mode toggle in frontend/components/layout/ThemeToggle.tsx (persist preference in localStorage)
- [ ] T400 [P] Write Vitest tests for keyboard shortcuts in frontend/tests/lib/hooks/useKeyboardShortcuts.test.ts (test C for create task, / for search, Esc for close modal, focus management)
- [ ] T401 [P] Add keyboard shortcuts handler in frontend/lib/hooks/useKeyboardShortcuts.ts (C for create task, / for search, Esc for close modal)
- [ ] T402 [P] Create form validation schemas in frontend/lib/schemas/ (Zod schemas for all forms matching backend Pydantic models)
- [ ] T403 [P] Write Vitest tests for utility functions in frontend/tests/lib/utils.test.ts (test date formatting, file size formatting, color utilities, cn classname merger, string truncation)
- [ ] T404 [P] Create utility functions in frontend/lib/utils.ts (date formatting, file size formatting, color utilities, cn classname merger)
- [ ] T405 Documentation: Update backend/README.md with deployment instructions per quickstart.md
- [ ] T406 Documentation: Update frontend/README.md with build and environment variables per quickstart.md
- [ ] T407 Write pytest tests for migration guide validation in backend/tests/test_migration.py (test Phase 2 tasks table compatibility, default org creation, backward-compat API wrapper works)
- [ ] T408 Documentation: Create migration guide in specs/001-project-management-system/MIGRATION.md for Phase 2 → Project Management System transition per data-model.md
- [ ] T409 Write pytest tests for filename sanitization in backend/tests/security/test_file_upload_security.py::test_path_traversal (test upload with filename "../../etc/passwd", verify sanitization, file saved with safe name)
- [ ] T410 Security: Add filename sanitization to file upload handler in backend/app/services/file_service.py (prevent path traversal)
- [ ] T411 Write pytest tests for MIME validation in backend/tests/security/test_file_upload_security.py::test_mime_bypass (test rename malicious.exe to malicious.jpg, verify MIME validation rejects despite extension)
- [ ] T412 Security: Add MIME type validation whitelist in backend/app/services/file_service.py per contracts/03-projects-tasks-api.md
- [ ] T413 Write pytest tests for SQL injection prevention in backend/tests/security/test_sql_injection.py (test search with "'; DROP TABLE tasks; --", verify parameterized query prevents injection)
- [ ] T414 Security: Validate SQL injection prevention on search endpoints (verify ORM parameterization)
- [ ] T415 Write pytest tests for XSS prevention in backend/tests/security/test_xss.py (test submit comment with <script>alert('XSS')</script>, verify sanitization removes script tags)
- [ ] T416 Security: Validate XSS prevention in comments and task descriptions (verify markdown renderer sanitizes)
- [ ] T417 [P] Write pytest tests for database connection pooling in backend/tests/test_database.py::test_connection_pool (test pool size configuration, connection reuse, timeout handling)
- [ ] T418 [P] Performance: Add database connection pooling configuration in backend/app/database.py
- [ ] T419 [P] Write pytest tests for pagination defaults in backend/tests/test_pagination.py (test all list endpoints use limit 100 default, offset 0 default, max limit 500 enforced)
- [ ] T420 [P] Performance: Add pagination defaults to all list endpoints in backend/app/routers/ (limit 100, offset 0)
- [ ] T421 [P] Write pytest tests for performance indexes in backend/tests/migrations/test_009_performance.py (test composite indexes per data-model.md: (org_id, slug), (project_id, task_number), (column_id, position), etc.)
- [ ] T422 [P] Performance: Add composite indexes per data-model.md recommendations in backend/alembic/versions/009_add_performance_indexes.py
- [ ] T423 Write Playwright E2E tests for regression suite in frontend/tests/e2e/regression-phase2.spec.ts (test all Phase 2 todo app features still work: auth, tasks CRUD, chatbot if exists)
- [ ] T424 Validation: Run quickstart.md validation end-to-end (verify setup instructions work)
- [ ] T425 Write pytest tests for >80% backend coverage in backend/tests/test_coverage.py (verify pytest-cov reports >80% for all modules)

---

## Dependencies & Execution Order

### Phase Dependencies

- **Setup (Phase 1)**: No dependencies - can start immediately
- **Foundational (Phase 2)**: Depends on Setup completion - BLOCKS all user stories
- **User Story 7 (Phase 3)**: Depends on Foundational - Can start after Phase 2 complete
- **User Story 1 (Phase 4)**: Depends on Foundational + US7 (auth required for org creation)
- **User Story 2 (Phase 5)**: Depends on Foundational + US1 (projects belong to orgs)
- **User Story 3 (Phase 6)**: Depends on Foundational + US2 (tasks belong to projects)
- **User Story 4 (Phase 7)**: Depends on Foundational + US3 (comments belong to tasks)
- **User Story 5 (Phase 8)**: Depends on Foundational + US3 (attachments belong to tasks)
- **User Story 6 (Phase 9)**: Depends on Foundational + US2 + US3 (column customization affects tasks)
- **User Story 8 (Phase 10)**: Depends on Foundational + US1 + US2 + US3 (dashboard aggregates org/project/task data)
- **User Story 9 (Phase 11)**: Depends on Foundational + US3 + US4 (notifications for task assignment and mentions)
- **User Story 10 (Phase 12)**: Depends on Foundational + US1 + US2 + US3 (search across orgs/projects/tasks)
- **Polish (Phase 13)**: Depends on all desired user stories being complete

### User Story Dependencies (Critical Path for MVP)

**P1 - MVP Critical Path**:
1. US7 (Auth - Phase 3) - No story dependencies
2. US1 (Orgs - Phase 4) - Depends on US7
3. US2 (Projects - Phase 5) - Depends on US1
4. US3 (Tasks - Phase 6) - Depends on US2

**P2 Stories** (can parallelize after P1):
- US4 (Comments - Phase 7) - Depends on US3
- US5 (Attachments - Phase 8) - Depends on US3
- US6 (Board Customization - Phase 9) - Depends on US2, US3

**P3 Stories** (can parallelize after P1):
- US8 (Dashboard - Phase 10) - Depends on US1, US2, US3
- US9 (Notifications - Phase 11) - Depends on US3, US4
- US10 (Search - Phase 12) - Depends on US1, US2, US3

### Parallel Opportunities

- **Within Setup (Phase 1)**: T003-T005, T009-T010 can run in parallel
- **Within Foundational (Phase 2)**: All [P] marked tasks can run in parallel (T015-T037)
- **Within User Stories**: Tasks marked [P] can run in parallel (backend models, frontend components)
- **Across User Stories**: After Foundational complete, P2 stories (US4, US5, US6) can be worked in parallel
- **Backend vs Frontend**: Backend and frontend tasks for same story can run in parallel (API endpoints vs UI components)

---

## Implementation Strategy

### MVP First (P1 Stories + Tests)

1. Complete Phase 1: Setup (T001-T012)
2. Complete Phase 2: Foundational (T013-T037) - CRITICAL BLOCKER
3. Complete Phase 3: User Story 7 - Auth (T038-T082)
4. Complete Phase 4: User Story 1 - Organizations (T083-T135)
5. Complete Phase 5: User Story 2 - Projects (T136-T184)
6. Complete Phase 6: User Story 3 - Tasks (T185-T227)
7. **STOP and VALIDATE**: Test all P1 stories work independently, verify >80% coverage
8. Complete Phase 13: Essential polish (T372-T425)
9. Deploy/demo MVP

**MVP Scope**: ~255 tasks (was 115 implementation-only, now includes 140 test tasks for P1)

### Incremental Delivery

1. **Foundation** (Phases 1-2): ~49 tasks → Foundation ready with tests
2. **MVP v1** (Add P1): ~206 tasks → Auth + Orgs + Projects + Tasks working with >80% coverage → Deploy
3. **MVP v2** (Add P2): ~89 tasks → Comments + Attachments + Board customization with tests → Deploy
4. **MVP v3** (Add P3): ~81 tasks → Dashboard + Notifications + Search with tests → Deploy
5. **Polish** (Phase 13): ~54 tasks → Production-ready with security tests and performance optimization

**Total**: **425 tasks** for complete implementation with >80% test coverage

### Test-First Development (TDD)

All implementation follows TDD workflow:
1. **Red**: Write failing test task first (T###-TEST)
2. **Green**: Write minimal implementation to pass test (T###)
3. **Refactor**: Improve code while keeping tests green

**Coverage Targets**:
- Backend: >80% line coverage via pytest
- Frontend: >80% component coverage via Vitest
- E2E: All user story acceptance scenarios via Playwright

---

## Summary Metrics

| Category | Count | Notes |
|----------|-------|-------|
| Implementation Tasks | 212 | 209 original + 3 missing requirements (FR-013, FR-049, FR-078) |
| Unit/Integration Test Tasks | 203 | pytest (backend), Vitest (frontend) |
| E2E Test Tasks | 10 | Playwright tests for each user story |
| **Total Tasks** | **425** | **Doubles from original 209 to comply with constitution** |
| Requirements Covered | 80/80 | 100% coverage (was 77/80, added 3 tasks) |
| Test Coverage Target | >80% | Constitution Article V requirement |
| User Stories | 10 | All mapped to phases with tests |
| MVP Tasks | ~255 | Setup + Foundation + P1 stories + essential polish (with tests) |

---

## Notes

- ✅ **Constitution Compliant**: Test tasks included per Article V
- ✅ **Coverage Gaps Filled**: Added T110 (transfer ownership), T245 (CSV export), T382 (audit logging)
- ✅ **Security Tests Added**: T409-T416 validate path traversal, MIME bypass, SQL injection, XSS
- [P] tasks = different files, no dependencies within phase
- [Story] label maps task to specific user story for traceability
- Each user story is independently completable and testable
- Commit after each task or logical test + implementation pair
- Stop at any checkpoint to validate story independently
- Backend uses FastAPI + SQLModel + Neon PostgreSQL per plan.md
- Frontend uses Next.js 15 + TypeScript + Tailwind per plan.md
- All file paths follow monorepo structure in plan.md
- Backward compatibility with Phase 2 todo app handled via T407-T408 migration tasks
