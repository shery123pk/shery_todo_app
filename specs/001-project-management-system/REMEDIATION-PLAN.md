# Remediation Plan: Critical Issues from Analysis

**Date**: 2025-12-27
**Feature**: 001-project-management-system
**Analysis Report**: history/prompts/001-project-management-system/001-specification-analysis-report.tasks.prompt.md

---

## Overview

This document provides detailed remediation for the **1 CRITICAL** and **3 HIGH** severity issues identified in the specification analysis:

1. **C1 (CRITICAL)**: Add test tasks to comply with Constitution Article V
2. **G1 (HIGH)**: Add transfer ownership task (FR-013)
3. **G2 (HIGH)**: Add export activity CSV task (FR-049)
4. **G3 (HIGH)**: Add audit logging task (FR-078)

---

## Issue C1: Add Test Tasks (CRITICAL)

### Problem
Constitution Article V mandates:
- "Generate tests with/before code"
- "Maintain >80% code coverage"

But tasks.md explicitly omits test tasks, violating this requirement.

### Solution Strategy

**Approach**: Insert test tasks **before** each implementation task following Test-Driven Development (TDD) principles.

**Test Task Naming Convention**: `T###-TEST [P?] [Story] Description`

**Coverage Targets**:
- Backend: pytest tests for all API endpoints, services, models
- Frontend: Vitest tests for all components, hooks, utilities
- E2E: Playwright tests for each user story acceptance scenario
- Regression: Phase 2 todo app compatibility tests

### Detailed Test Task Additions

I'll show the pattern for each phase. The full list would add ~250 test tasks.

#### Phase 1: Setup - Add 2 Test Tasks

Insert after T010:

```markdown
- [ ] T011-TEST Verify backend project structure and dependencies in backend/tests/test_setup.py (check all imports work, config loads, database connects)
- [ ] T012-TEST Verify frontend project structure and TypeScript compilation in frontend/tests/setup.test.ts (check tsconfig, imports, Tailwind loads)
```

**Renumber existing T011-T023 → T013-T025**

#### Phase 2: Foundational - Add 13 Test Tasks

Insert test tasks before each foundational task. Example:

```markdown
## Phase 2: Foundational (Blocking Prerequisites)

- [ ] T013-TEST [P] Write pytest tests for database connection in backend/tests/test_database.py (test async engine creation, session management, connection pooling)
- [ ] T013 Create database configuration module in backend/app/database.py (async engine, session management with Neon PostgreSQL connection)

- [ ] T014-TEST [P] Write pytest tests for config loading in backend/tests/test_config.py (test env var parsing, defaults, validation)
- [ ] T014 Create application configuration module in backend/app/config.py (Pydantic BaseSettings for environment variables)

- [ ] T015-TEST Write pytest tests for FastAPI app initialization in backend/tests/test_main.py (test CORS config, middleware, router registration)
- [ ] T015 Create FastAPI app initialization in backend/app/main.py (CORS, middleware, router registration, exception handlers)

- [ ] T016-TEST [P] Write pytest tests for base SQLModel mixins in backend/tests/models/test_base.py (test UUID generation, timestamp auto-update, org scoping)
- [ ] T016 [P] Create base SQLModel mixins in backend/app/models/base.py (UUID primary keys, timestamps, organization scoping)

... (continue pattern for T017-T025)
```

**Renumber existing T011-T023 → T013-T038 with interleaved tests**

#### Phase 3: User Story 7 (Auth) - Add 22 Test Tasks + 1 E2E

Pattern for auth endpoints:

```markdown
- [ ] T039-TEST [P] [US7] Write pytest tests for User model in backend/tests/models/test_user.py (test field validation, email lowercase, password hashing on create)
- [ ] T039 [P] [US7] Create User model in backend/app/models/user.py (...)

- [ ] T040-TEST [P] [US7] Write pytest tests for Session model in backend/tests/models/test_session.py (test token uniqueness, expiration validation, cascade delete)
- [ ] T040 [P] [US7] Create Session model in backend/app/models/user.py (...)

- [ ] T041-TEST [US7] Write pytest tests for User/Session migrations in backend/tests/migrations/test_001_users.py (test schema creation, indexes, constraints)
- [ ] T041 [US7] Create Alembic migration for User and Session tables (...)

- [ ] T042-TEST [US7] Write pytest tests for AuthService in backend/tests/services/test_auth_service.py (test signup with valid/invalid data, signin success/failure, verify_email token validation, password reset flow, profile updates, password change)
- [ ] T042 [US7] Implement AuthService in backend/app/services/auth_service.py (...)

- [ ] T043-TEST [US7] Write pytest tests for POST /api/auth/signup in backend/tests/routers/test_auth.py::test_signup (test 201 success, 400 invalid email, 409 duplicate email, 400 weak password)
- [ ] T043 [US7] Implement POST /api/auth/signup endpoint (...)

... (continue for all auth endpoints T044-T052)

- [ ] T053-TEST [P] [US7] Write Vitest tests for signup page in frontend/tests/components/auth/SignupPage.test.tsx (test form validation, submit success, error handling)
- [ ] T053 [P] [US7] Create signup page in frontend/app/auth/signup/page.tsx (...)

... (continue for all auth components T054-T060)

- [ ] T061-TEST [US7] Write E2E tests for complete auth flow in frontend/tests/e2e/auth.spec.ts (test signup → verify email → signin → update profile → change password → signout)
- [ ] T061 [US7] Create Zustand auth store (...)
```

**Add 22 unit test tasks + 1 E2E test = 23 test tasks for US7**

#### Phase 4: User Story 1 (Orgs) - Add 25 Test Tasks + 1 E2E + 1 Missing Task

Insert missing task T058a (transfer ownership):

```markdown
- [ ] T073-TEST [US1] Write pytest tests for DELETE /api/organizations/{slug}/members/{user_id} in backend/tests/routers/test_organizations.py::test_remove_member (test 204 success, 403 cannot remove owner, 403 non-admin, 404 org not found)
- [ ] T073 [US1] Implement DELETE /api/organizations/{slug}/members/{user_id} endpoint (...)

- [ ] T074-TEST [US1] Write pytest tests for PUT /api/organizations/{slug}/members/{user_id}/role in backend/tests/routers/test_organizations.py::test_change_member_role (test 200 success, 403 non-owner, 400 invalid role)
- [ ] T074 [US1] Implement PUT /api/organizations/{slug}/members/{user_id}/role endpoint (...)

**NEW TASK (FR-013 coverage gap):**
- [ ] T075-TEST [US1] Write pytest tests for PUT /api/organizations/{slug}/transfer-ownership in backend/tests/routers/test_organizations.py::test_transfer_ownership (test 200 success owner changes, 403 non-owner, 400 target not admin, 404 target user not found)
- [ ] T075 [US1] Implement PUT /api/organizations/{slug}/transfer-ownership endpoint in backend/app/routers/organizations.py (verify new owner is org admin, update owner_id, demote old owner to admin, notify both users)

- [ ] T076-TEST [US1] Write pytest tests for GET /api/invitations/{token} in backend/tests/routers/test_invitations.py::test_view_invitation (test 200 success, 404 invalid token, 410 expired token)
- [ ] T076 [US1] Implement GET /api/invitations/{token} endpoint (...)

... (continue for all org tasks)
```

**Add 26 unit test tasks (including T075-TEST for transfer ownership) + 1 E2E test**

#### Phase 7: User Story 4 (Comments) - Add 17 Test Tasks + 1 Missing Task

Insert missing task T132a (export activity CSV):

```markdown
- [ ] T146-TEST [US4] Write pytest tests for GET /api/tasks/{taskId}/activity in backend/tests/routers/test_tasks.py::test_get_activity (test 200 success sorted by date, 404 task not found, 403 not project member)
- [ ] T146 [US4] Implement GET /api/tasks/{taskId}/activity endpoint (...)

**NEW TASK (FR-049 coverage gap):**
- [ ] T147-TEST [US4] Write pytest tests for GET /api/tasks/{taskId}/activity/export in backend/tests/routers/test_tasks.py::test_export_activity_csv (test 200 CSV with headers, content-type header, streaming for large datasets, 403 non-admin)
- [ ] T147 [US4] Implement GET /api/tasks/{taskId}/activity/export endpoint in backend/app/routers/tasks.py (generate CSV with headers: timestamp, user, action, field, old_value, new_value; stream response for large datasets; admin only)

- [ ] T148-TEST [US4] Verify activity logging on task update in backend/tests/routers/test_tasks.py::test_task_update_creates_activity (test ActivityLog entries created for each changed field)
- [ ] T148 [US4] Add activity logging to task update handler (...)

... (continue for all comment/activity tasks)
```

**Add 18 unit test tasks (including T147-TEST for CSV export) + 1 E2E test**

#### Phase 13: Polish - Add Security Tests + Missing Audit Task

Insert missing task T187a (audit logging):

```markdown
- [ ] T187-TEST [P] Write pytest tests for rate limiting in backend/tests/test_rate_limiting.py (test 429 after exceeding limits, rate limit headers, IP vs user limits)
- [ ] T187 [P] Add rate limiting middleware to backend/app/main.py (...)

**NEW TASK (FR-078 coverage gap):**
- [ ] T188-TEST [P] Write pytest tests for AuditService in backend/tests/services/test_audit_service.py (test audit log creation for delete org, delete project, delete task; verify timestamp, user_id, resource_type, resource_id captured)
- [ ] T188 [P] Implement AuditService in backend/app/services/audit_service.py (log_admin_action method, create audit_logs table entry with user_id, action_type enum, resource_type, resource_id, timestamp, metadata JSON)

- [ ] T189-TEST [P] Write pytest tests for CSRF protection in backend/tests/test_csrf.py (test double-submit cookie validation, 403 on CSRF mismatch)
- [ ] T189 [P] Add CSRF protection to backend/app/main.py (...)

... (continue for all polish tasks)

**NEW: Security validation tests (after T204-T205):**
- [ ] T224-TEST [P] Security test: Path traversal prevention in backend/tests/security/test_file_upload_security.py (attempt upload with filename "../../etc/passwd", verify sanitization, file saved with safe name)
- [ ] T225-TEST [P] Security test: MIME type bypass in backend/tests/security/test_file_upload_security.py (rename malicious.exe to malicious.jpg, verify MIME validation rejects despite extension)
- [ ] T226-TEST [P] Security test: SQL injection on search in backend/tests/security/test_sql_injection.py (attempt search with "'; DROP TABLE tasks; --", verify parameterized query prevents injection)
- [ ] T227-TEST [P] Security test: XSS in comments in backend/tests/security/test_xss.py (submit comment with <script>alert('XSS')</script>, verify sanitization removes script tags)
```

**Add 4 security test tasks after file upload implementation**

### Summary of Test Task Additions

| Phase | Implementation Tasks | Test Tasks to Add | E2E Tests | Total New Tasks |
|-------|---------------------|-------------------|-----------|-----------------|
| Setup | 10 | 2 | 0 | 2 |
| Foundational | 13 | 13 | 0 | 13 |
| US7 (Auth) | 22 | 22 | 1 | 23 |
| US1 (Orgs) | 25 + 1 new | 26 | 1 | 27 |
| US2 (Projects) | 24 | 24 | 1 | 25 |
| US3 (Tasks) | 21 | 21 | 1 | 22 |
| US4 (Comments) | 17 + 1 new | 18 | 1 | 19 |
| US5 (Attachments) | 12 | 12 | 1 | 13 |
| US6 (Board Custom) | 9 | 9 | 1 | 10 |
| US8 (Dashboard) | 9 | 9 | 1 | 10 |
| US9 (Notifications) | 14 | 14 | 1 | 15 |
| US10 (Search) | 7 | 7 | 1 | 8 |
| Polish | 26 + 1 new | 26 + 4 security | 0 | 30 |
| **TOTAL** | **209 + 3 new = 212** | **203** | **10** | **217** |

**New Task Count**: 209 implementation + 3 missing requirements = 212 implementation tasks
**New Test Count**: 203 unit/integration + 10 E2E = 213 test tasks
**Grand Total**: **425 tasks** (was 209, adding 216 tasks)

---

## Issue G1: Add Transfer Ownership Task (HIGH)

**Location**: Phase 4 (User Story 1) after T074

**Task to Insert**:

```markdown
- [ ] T075-TEST [US1] Write pytest tests for PUT /api/organizations/{slug}/transfer-ownership in backend/tests/routers/test_organizations.py::test_transfer_ownership (test 200 success owner changes, 403 non-owner, 400 target not admin, 404 target user not found)
- [ ] T075 [US1] Implement PUT /api/organizations/{slug}/transfer-ownership endpoint in backend/app/routers/organizations.py (verify new owner is org admin, update owner_id, demote old owner to admin, notify both users)
```

**Requirement Coverage**: FR-013 "Organization owners MUST be able to transfer ownership to another member"

---

## Issue G2: Add Export Activity CSV Task (HIGH)

**Location**: Phase 7 (User Story 4) after T146

**Task to Insert**:

```markdown
- [ ] T147-TEST [US4] Write pytest tests for GET /api/tasks/{taskId}/activity/export in backend/tests/routers/test_tasks.py::test_export_activity_csv (test 200 CSV with headers, content-type header, streaming for large datasets, 403 non-admin)
- [ ] T147 [US4] Implement GET /api/tasks/{taskId}/activity/export endpoint in backend/app/routers/tasks.py (generate CSV with headers: timestamp, user, action, field, old_value, new_value; stream response for large datasets; admin only)
```

**Requirement Coverage**: FR-049 "System MUST allow project admins to export activity logs as CSV"

---

## Issue G3: Add Audit Logging Task (HIGH)

**Location**: Phase 13 (Polish) after T187

**Task to Insert**:

```markdown
- [ ] T188-TEST [P] Write pytest tests for AuditService in backend/tests/services/test_audit_service.py (test audit log creation for delete org, delete project, delete task; verify timestamp, user_id, resource_type, resource_id captured)
- [ ] T188 [P] Implement AuditService in backend/app/services/audit_service.py (log_admin_action method, create audit_logs table entry with user_id, action_type enum, resource_type, resource_id, timestamp, metadata JSON)
```

**Requirement Coverage**: FR-078 "System MUST log all admin actions (delete organization, delete project, delete task)"

**Additional Changes Required**:
- Add `audit_logs` table to Alembic migration (suggest adding to T096 migration or new migration)
- Update delete endpoints to call `AuditService.log_admin_action()` before deletion

---

## Implementation Steps

### Step 1: Backup Current tasks.md

```bash
cp specs/001-project-management-system/tasks.md specs/001-project-management-system/tasks.md.backup
```

### Step 2: Regenerate tasks.md with Tests

**Option A (Automated)**: Use a script to insert test tasks
**Option B (Manual)**: Edit tasks.md following the patterns above

### Step 3: Renumber All Tasks

With test tasks inserted before implementation tasks, renumber sequentially:
- Original T001 → stays T001
- Insert T001-TEST → no test needed for setup tasks
- Original T011 → becomes T013
- Insert T013-TEST → test for database config
- Continue through all 425 tasks

### Step 4: Update Task References

Search for task references in:
- Dependency graph section
- Implementation strategy section
- Comments/notes sections

Update all T### references to match new numbering.

### Step 5: Validate Changes

Run constitution compliance check:
- ✅ All implementation tasks have corresponding test tasks
- ✅ Test tasks follow TDD pattern (test before code)
- ✅ >80% coverage achievable with 213 test tasks for 212 implementation tasks
- ✅ E2E tests cover all user story acceptance scenarios

---

## Approval Required

**Before proceeding, please confirm**:

1. ✅ Approve adding ~216 test tasks to tasks.md (doubles task count 209 → 425)
2. ✅ Approve adding 3 missing requirement tasks (T075, T147, T188)
3. ✅ Approve renumbering all existing tasks to accommodate insertions
4. ✅ Approve test-first approach (test tasks before implementation tasks)

**Once approved, I will**:
1. Generate the complete updated tasks.md with all test tasks
2. Insert the 3 missing requirement tasks
3. Renumber all tasks sequentially
4. Update dependency graph and references
5. Validate constitution compliance

**Reply "APPROVED" to proceed with remediation.**
