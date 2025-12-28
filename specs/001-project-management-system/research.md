# Research: Multi-Tenant Project Management System

**Feature**: 001-project-management-system
**Date**: 2025-12-27
**Status**: Complete

## Overview

This document captures research findings and architectural pattern decisions for implementing a production-grade, multi-tenant project management system. All technology choices align with the project constitution (Phase 2+ requirements).

---

## 1. Multi-Tenancy Architecture

### Decision: Row-Level Security with Organization Scoping

**Rationale**:
- Complete data isolation between organizations (tenants)
- Simpler than separate databases or schemas per tenant
- Better resource utilization and cost efficiency
- Easier backup/restore and migrations

**Pattern**:
```python
# All queries filter by organization_id
class OrganizationMixin:
    organization_id: UUID = Field(foreign_key="organization.id")

# Dependency injection ensures current user's org is always used
async def get_current_organization(
    current_user: User = Depends(get_current_user)
) -> Organization:
    # Returns org based on request context (URL slug or user's active org)
    ...
```

**Alternatives Considered**:
1. **Separate Databases** - Too complex, expensive, hard to query across tenants
2. **Schema-Based** - Moderate complexity, PostgreSQL-specific, migration challenges
3. **Row-Level Security (Chosen)** - Best balance of simplicity, performance, and portability

**Implementation Notes**:
- Use SQLAlchemy ORM filters on all queries
- Add composite indexes on `(organization_id, ...)` for performance
- Validate organization ownership in every protected endpoint
- Use database constraints (foreign keys with CASCADE) for data integrity

---

## 2. Sequential Task Numbering

### Decision: Database Sequence with Project-Scoped Counters

**Rationale**:
- User-friendly task IDs (WEB-1, WEB-2) like Jira/Linear
- Easier to communicate and remember than UUIDs
- Supports concurrent task creation without conflicts

**Pattern**:
```python
# Table structure
class Project(SQLModel, table=True):
    id: UUID
    key: str  # e.g., "WEB"
    next_task_number: int = Field(default=1)

class Task(SQLModel, table=True):
    id: UUID
    project_id: UUID
    task_number: int  # Sequential per project

# Service for atomic increment
class TaskNumberingService:
    async def get_next_task_number(self, project_id: UUID) -> int:
        # Use SELECT FOR UPDATE to lock row during increment
        async with session.begin():
            project = await session.get(Project, project_id, with_for_update=True)
            task_number = project.next_task_number
            project.next_task_number += 1
            await session.commit()
            return task_number
```

**Alternatives Considered**:
1. **UUID-only** - Simpler implementation but poor UX (hard to remember/communicate)
2. **PostgreSQL Sequences** - Per-database, not per-project, would need complex naming
3. **Atomic Counter (Chosen)** - Row-level lock ensures no race conditions

**Implementation Notes**:
- Use `SELECT FOR UPDATE` to prevent concurrent increments
- Display as `{project.key}-{task.task_number}` in UI and URLs
- Index on `(project_id, task_number)` for fast lookups
- Handle edge case: deleted tasks don't reuse numbers (gaps are OK)

---

## 3. File Storage Strategy

### Decision: Local Filesystem (MVP) → S3-Compatible (Production)

**Rationale**:
- Start simple with local filesystem for MVP
- Migrate to S3 for production scalability and reliability
- Use abstraction layer to make migration seamless

**Pattern**:
```python
# Abstract file service
class FileStorageService(Protocol):
    async def save(self, file: UploadFile, path: str) -> str: ...
    async def get_url(self, path: str) -> str: ...
    async def delete(self, path: str) -> None: ...

# MVP implementation
class LocalFileStorage(FileStorageService):
    base_path = "./uploads"

    async def save(self, file: UploadFile, path: str) -> str:
        full_path = f"{self.base_path}/{path}"
        async with aiofiles.open(full_path, 'wb') as f:
            await f.write(await file.read())
        return path

# Production implementation (future)
class S3FileStorage(FileStorageService):
    async def save(self, file: UploadFile, path: str) -> str:
        # Upload to S3 with boto3 or aioboto3
        ...
```

**Alternatives Considered**:
1. **Database BLOBs** - Poor performance, backup challenges, hard to scale
2. **Local Filesystem (Chosen for MVP)** - Simple, no external dependencies
3. **S3 from Start** - Over-engineering for MVP, adds complexity/cost

**Implementation Notes**:
- Organize files: `/uploads/org_{org_id}/project_{project_id}/task_{task_id}/{filename}`
- Validate MIME type and extension whitelist
- Sanitize filenames (remove path traversal characters)
- Enforce 10MB per-file limit, 20 files per task limit
- Generate download URLs with auth check (no direct filesystem access)

---

## 4. Authentication & Session Management

### Decision: Better Auth with JWT + Database Sessions

**Rationale**:
- Better Auth provides JWT utilities and best practices
- Database sessions enable revocation (logout from all devices)
- HttpOnly cookies prevent XSS attacks

**Pattern**:
```python
# Session model
class Session(SQLModel, table=True):
    id: UUID
    user_id: UUID
    token: str  # Hashed JWT
    refresh_token: str  # For token rotation
    expires_at: datetime
    ip_address: str
    user_agent: str

# JWT creation
def create_access_token(user_id: UUID, remember_me: bool = False) -> str:
    expire_days = 30 if remember_me else 7
    expire = datetime.utcnow() + timedelta(days=expire_days)
    payload = {"sub": str(user_id), "exp": expire}
    return jwt.encode(payload, settings.JWT_SECRET, algorithm="HS256")
```

**Alternatives Considered**:
1. **Pure JWT** - No revocation capability, can't logout from all devices
2. **Server-side Sessions Only** - Requires sticky sessions, complicates scaling
3. **Better Auth JWT + DB Sessions (Chosen)** - Best of both worlds

**Implementation Notes**:
- Store session token hash (not plaintext) in database
- Verify JWT signature and expiration on every request
- Check database session exists and is not expired
- Support "Remember Me" (30-day vs 7-day expiration)
- Implement refresh token rotation for security

---

## 5. Drag-and-Drop Task Ordering

### Decision: Float-Based Position Field

**Rationale**:
- Enables efficient drag-and-drop reordering without updating many rows
- Avoids sequential integers which require cascading updates

**Pattern**:
```python
class Task(SQLModel, table=True):
    position: float  # e.g., 1.0, 2.0, 2.5 (inserted between 2 and 3)
    column_id: UUID

# Reordering logic
async def move_task(task_id: UUID, target_column_id: UUID, position_index: int):
    tasks_in_column = await get_tasks_in_column(target_column_id)

    if position_index == 0:
        new_position = tasks_in_column[0].position / 2
    elif position_index >= len(tasks_in_column):
        new_position = tasks_in_column[-1].position + 1000
    else:
        prev_pos = tasks_in_column[position_index - 1].position
        next_pos = tasks_in_column[position_index].position
        new_position = (prev_pos + next_pos) / 2

    task.position = new_position
    task.column_id = target_column_id
    await session.commit()
```

**Alternatives Considered**:
1. **Sequential Integers** - Requires updating many rows on every reorder
2. **Linked List** - Complex queries, no sorting, hard to maintain
3. **Float Position (Chosen)** - Constant-time reorder, simple queries

**Implementation Notes**:
- Periodically rebalance positions if they get too close (future optimization)
- Default query order: `ORDER BY position ASC`
- Client-side drag-and-drop: @dnd-kit for accessibility and performance

---

## 6. Activity Logging & Audit Trail

### Decision: Event Sourcing Pattern (Simplified)

**Rationale**:
- Complete audit trail of all task changes
- Enables "undo" functionality (future)
- Compliance and debugging benefits

**Pattern**:
```python
class ActivityLog(SQLModel, table=True):
    id: UUID
    task_id: UUID
    user_id: UUID
    action: str  # "created", "updated", "moved", "commented", etc.
    field_name: Optional[str]  # e.g., "status", "priority"
    old_value: Optional[str]
    new_value: Optional[str]
    created_at: datetime

# Automatic logging in task update
async def update_task(task_id: UUID, updates: dict, current_user: User):
    task = await get_task(task_id)

    for field, new_value in updates.items():
        old_value = getattr(task, field)
        if old_value != new_value:
            # Log the change
            activity = ActivityLog(
                task_id=task_id,
                user_id=current_user.id,
                action="updated",
                field_name=field,
                old_value=str(old_value),
                new_value=str(new_value)
            )
            session.add(activity)

    # Update task fields
    for field, value in updates.items():
        setattr(task, field, value)

    await session.commit()
```

**Implementation Notes**:
- Log all task state changes (status, assignee, priority, due date, etc.)
- Log special events (created, commented, moved between columns)
- Display in task detail modal sorted by `created_at DESC`
- Allow export as CSV for compliance/auditing

---

## 7. Frontend State Management

### Decision: Zustand + TanStack Query

**Rationale**:
- Zustand for simple client-side UI state (modals, sidebar, theme)
- TanStack Query for server state (API data, caching, optimistic updates)
- Separation of concerns and React Server Components compatibility

**Pattern**:
```typescript
// Zustand store for UI state
interface UIStore {
  taskDetailModalOpen: boolean
  selectedTaskId: string | null
  sidebarCollapsed: boolean
  openTaskDetail: (taskId: string) => void
  closeTaskDetail: () => void
}

const useUIStore = create<UIStore>((set) => ({
  taskDetailModalOpen: false,
  selectedTaskId: null,
  sidebarCollapsed: false,
  openTaskDetail: (taskId) => set({ taskDetailModalOpen: true, selectedTaskId: taskId }),
  closeTaskDetail: () => set({ taskDetailModalOpen: false, selectedTaskId: null }),
}))

// TanStack Query for server state
const useTasks = (projectKey: string) => {
  return useQuery({
    queryKey: ['tasks', projectKey],
    queryFn: () => api.getTasks(projectKey),
    staleTime: 30000, // 30 seconds
  })
}

const useUpdateTask = () => {
  const queryClient = useQueryClient()

  return useMutation({
    mutationFn: ({ taskId, updates }: { taskId: string; updates: Partial<Task> }) =>
      api.updateTask(taskId, updates),
    onMutate: async ({ taskId, updates }) => {
      // Optimistic update
      await queryClient.cancelQueries({ queryKey: ['tasks'] })
      const previousTasks = queryClient.getQueryData(['tasks'])
      queryClient.setQueryData(['tasks'], (old: Task[]) =>
        old.map((task) => (task.id === taskId ? { ...task, ...updates } : task))
      )
      return { previousTasks }
    },
    onError: (err, variables, context) => {
      // Rollback on error
      queryClient.setQueryData(['tasks'], context.previousTasks)
    },
  })
}
```

**Implementation Notes**:
- Zustand: modals, sidebar, theme, filters
- TanStack Query: tasks, projects, organizations, users
- Optimistic updates for drag-and-drop (instant feedback)
- Automatic refetching on window focus and network reconnect

---

## 8. Email Service Integration

### Decision: SMTP with aiosmtplib (SendGrid/AWS SES)

**Rationale**:
- SendGrid free tier: 100 emails/day (sufficient for MVP)
- Standard SMTP protocol (not vendor-locked)
- Async email sending with aiosmtplib

**Pattern**:
```python
class EmailService:
    def __init__(self, smtp_host: str, smtp_port: int, username: str, password: str):
        self.smtp_host = smtp_host
        self.smtp_port = smtp_port
        self.username = username
        self.password = password

    async def send_email(self, to: str, subject: str, html: str):
        message = EmailMessage()
        message["From"] = self.username
        message["To"] = to
        message["Subject"] = subject
        message.set_content(html, subtype="html")

        async with aiosmtplib.SMTP(hostname=self.smtp_host, port=self.smtp_port) as smtp:
            await smtp.login(self.username, self.password)
            await smtp.send_message(message)

    async def send_verification_email(self, user: User, token: str):
        verify_url = f"{settings.FRONTEND_URL}/auth/verify?token={token}"
        await self.send_email(
            to=user.email,
            subject="Verify your email",
            html=f"Click to verify: <a href='{verify_url}'>{verify_url}</a>"
        )
```

**Implementation Notes**:
- Use environment variables for SMTP credentials
- Template emails with HTML (future: use Jinja2 templates)
- Queue emails (future: use background tasks or Celery)
- Track email delivery status (future: webhook integration)

---

## 9. Testing Strategy

### Decision: Three-Layer Testing (Unit, Integration, E2E)

**Rationale**:
- Unit tests for business logic (services, utilities)
- Integration tests for API endpoints (with test database)
- E2E tests for critical user flows (Playwright)

**Pattern**:
```python
# pytest fixtures
@pytest.fixture
async def test_db():
    """Create and cleanup test database"""
    engine = create_async_engine("postgresql+asyncpg://test:test@localhost/test_db")
    async with engine.begin() as conn:
        await conn.run_sync(SQLModel.metadata.create_all)
    yield engine
    async with engine.begin() as conn:
        await conn.run_sync(SQLModel.metadata.drop_all)

@pytest.fixture
async def client(test_db):
    """FastAPI test client with test database"""
    async with AsyncClient(app=app, base_url="http://test") as ac:
        yield ac

@pytest.fixture
async def authenticated_client(client):
    """Client with authenticated user session"""
    response = await client.post("/api/auth/signup", json={
        "email": "test@example.com",
        "password": "SecurePass123!",
        "full_name": "Test User"
    })
    assert response.status_code == 201
    # Login and return client with cookies
    ...
```

**Implementation Notes**:
- Use pytest-asyncio for async test support
- Mock external services (email, file storage) in tests
- Regression tests for Phase 2 endpoints
- Playwright for E2E: auth flow, task creation, drag-and-drop

---

## 10. Performance Optimization

### Best Practices from Research

1. **Database Indexes**:
   - Composite indexes on `(organization_id, project_id, ...)` for multi-tenant queries
   - Index on `(task.project_id, task.task_number)` for task lookup
   - Index on `(task.column_id, task.position)` for board view

2. **Query Optimization**:
   - Use `select_related` / `joinedload` for related entities
   - Limit result sets with pagination
   - Avoid N+1 queries (eager load relationships)

3. **Caching Strategy** (future):
   - Redis for session caching
   - Query result caching with TanStack Query (frontend)
   - CDN for static assets (Vercel Edge Network)

4. **Frontend Performance**:
   - Code splitting by route (Next.js automatic)
   - Lazy load images with `next/image`
   - Virtual scrolling for large task lists (react-window)
   - Debounce search inputs (300ms)

---

## Research Summary

All architectural decisions documented above align with:
- ✅ Constitution technology stack requirements
- ✅ Spec functional requirements and success criteria
- ✅ Industry best practices for multi-tenant SaaS applications
- ✅ Scalability targets (5,000 users, 10,000 tasks per org)
- ✅ Performance goals (p95 <200ms API, 60fps drag-and-drop)

**No unresolved NEEDS CLARIFICATION items remain.** Ready to proceed with Phase 1 (data model and API contracts).
