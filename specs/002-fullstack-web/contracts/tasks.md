# Task CRUD API Contract

**Feature**: 002-fullstack-web
**Base URL**: `/api/tasks`
**Authentication**: Required (all endpoints)
**Date**: 2025-12-26

---

## Endpoints

### GET /api/tasks

**Description**: List all tasks belonging to the authenticated user.

**Authentication**: Required (session token)

**Request Headers**:
```http
Cookie: session_token=<TOKEN>
```

**Query Parameters**:
- `completed` (optional): Filter by completion status
  - Type: boolean
  - Values: `true`, `false`
  - Default: No filter (show all)
- `limit` (optional): Max number of tasks to return
  - Type: integer
  - Range: 1-1000
  - Default: 1000
- `offset` (optional): Pagination offset
  - Type: integer
  - Min: 0
  - Default: 0

**Success Response (200 OK)**:
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
    },
    {
      "id": "234e5678-e89b-12d3-a456-426614174001",
      "user_id": "550e8400-e29b-41d4-a716-446655440000",
      "title": "Finish project report",
      "description": null,
      "completed": true,
      "priority": "high",
      "tags": ["work"],
      "category": "work",
      "created_at": "2025-12-25T14:00:00Z",
      "updated_at": "2025-12-26T10:30:00Z"
    }
  ],
  "total": 15,
  "completed": 5,
  "incomplete": 10
}
```

**Response Schema**:
```typescript
interface TaskListResponse {
  tasks: TaskRead[];
  total: number;        // Total number of user's tasks
  completed: number;    // Number of completed tasks
  incomplete: number;   // Number of incomplete tasks
}

interface TaskRead {
  id: string;                           // UUID
  user_id: string;                      // UUID
  title: string;                        // 1-200 chars
  description: string | null;           // Max 1000 chars
  completed: boolean;
  priority: "low" | "medium" | "high" | "critical" | null;
  tags: string[];                       // Array of strings
  category: string | null;              // Max 50 chars
  created_at: string;                   // ISO 8601 UTC
  updated_at: string;                   // ISO 8601 UTC
}
```

**Error Responses**:

**401 Unauthorized** - No session or invalid/expired token:
```json
{
  "detail": "Not authenticated"
}
```

**400 Bad Request** - Invalid query parameters:
```json
{
  "detail": "Invalid value for 'completed' parameter. Expected true or false."
}
```

**Sorting**: Tasks sorted by `created_at DESC` (newest first) by default.

**User Isolation**: Response ONLY includes tasks where `user_id = authenticated_user.id`.

**Example Usage**:
```bash
# Get all tasks
curl -X GET http://localhost:8000/api/tasks \
  -b cookies.txt

# Get only incomplete tasks
curl -X GET "http://localhost:8000/api/tasks?completed=false" \
  -b cookies.txt

# Get first 10 tasks
curl -X GET "http://localhost:8000/api/tasks?limit=10&offset=0" \
  -b cookies.txt
```

---

### POST /api/tasks

**Description**: Create a new task for the authenticated user.

**Authentication**: Required (session token)

**Request Headers**:
```http
Cookie: session_token=<TOKEN>
Content-Type: application/json
```

**Request Body**:
```json
{
  "title": "Buy groceries",
  "description": "Milk, eggs, bread",  // optional
  "priority": "medium",                 // optional
  "tags": ["shopping", "urgent"],       // optional
  "category": "personal"                // optional
}
```

**Request Schema**:
```typescript
interface TaskCreate {
  title: string;                        // Required, 1-200 chars, trimmed
  description?: string;                 // Optional, max 1000 chars
  priority?: "low" | "medium" | "high" | "critical";
  tags?: string[];                      // Optional, max 10 tags
  category?: string;                    // Optional, max 50 chars
}
```

**Success Response (201 Created)**:
```json
{
  "id": "123e4567-e89b-12d3-a456-426614174000",
  "user_id": "550e8400-e29b-41d4-a716-446655440000",
  "title": "Buy groceries",
  "description": "Milk, eggs, bread",
  "completed": false,
  "priority": "medium",
  "tags": ["shopping", "urgent"],
  "category": "personal",
  "created_at": "2025-12-26T12:00:00Z",
  "updated_at": "2025-12-26T12:00:00Z"
}
```

**Response Schema**: `TaskRead` (see above)

**Error Responses**:

**400 Bad Request** - Missing or invalid title:
```json
{
  "detail": "Title is required"
}
```

```json
{
  "detail": "Title must be 200 characters or less"
}
```

**400 Bad Request** - Description too long:
```json
{
  "detail": "Description must be 1000 characters or less"
}
```

**400 Bad Request** - Too many tags:
```json
{
  "detail": "Maximum 10 tags allowed"
}
```

**400 Bad Request** - Invalid priority:
```json
{
  "detail": "Priority must be one of: low, medium, high, critical"
}
```

**401 Unauthorized** - Not authenticated:
```json
{
  "detail": "Not authenticated"
}
```

**Auto-Generated Fields**:
- `id`: UUID (generated by database)
- `user_id`: Set to authenticated user's ID
- `completed`: Defaults to `false`
- `created_at`: Current UTC timestamp
- `updated_at`: Current UTC timestamp

**Example Usage**:
```bash
curl -X POST http://localhost:8000/api/tasks \
  -H "Content-Type: application/json" \
  -b cookies.txt \
  -d '{
    "title": "Buy groceries",
    "description": "Milk, eggs, bread",
    "priority": "medium",
    "tags": ["shopping"],
    "category": "personal"
  }'
```

---

### GET /api/tasks/{id}

**Description**: Get a single task by ID (only if owned by authenticated user).

**Authentication**: Required (session token)

**Request Headers**:
```http
Cookie: session_token=<TOKEN>
```

**URL Parameters**:
- `id`: UUID of the task

**Success Response (200 OK)**:
```json
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
```

**Response Schema**: `TaskRead`

**Error Responses**:

**401 Unauthorized** - Not authenticated:
```json
{
  "detail": "Not authenticated"
}
```

**404 Not Found** - Task not found OR not owned by authenticated user:
```json
{
  "detail": "Task not found"
}
```

**Security Note**: Returns `404 Not Found` (not `403 Forbidden`) to prevent task ID enumeration.

**Example Usage**:
```bash
curl -X GET http://localhost:8000/api/tasks/123e4567-e89b-12d3-a456-426614174000 \
  -b cookies.txt
```

---

### PATCH /api/tasks/{id}

**Description**: Update a task (partial update - all fields optional).

**Authentication**: Required (session token)

**Request Headers**:
```http
Cookie: session_token=<TOKEN>
Content-Type: application/json
```

**URL Parameters**:
- `id`: UUID of the task

**Request Body** (all fields optional):
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

**Request Schema**:
```typescript
interface TaskUpdate {
  title?: string;                       // Optional, 1-200 chars if provided
  description?: string;                 // Optional, max 1000 chars if provided
  completed?: boolean;
  priority?: "low" | "medium" | "high" | "critical" | null;
  tags?: string[];                      // Optional, max 10 tags if provided
  category?: string | null;             // Optional, max 50 chars if provided
}
```

**Success Response (200 OK)**:
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
  "created_at": "2025-12-26T09:00:00Z",
  "updated_at": "2025-12-26T14:30:00Z"
}
```

**Response Schema**: `TaskRead`

**Error Responses**:

**400 Bad Request** - Validation error:
```json
{
  "detail": "Title must be 200 characters or less"
}
```

**401 Unauthorized** - Not authenticated:
```json
{
  "detail": "Not authenticated"
}
```

**404 Not Found** - Task not found OR not owned by authenticated user:
```json
{
  "detail": "Task not found"
}
```

**Auto-Updated Fields**:
- `updated_at`: Set to current UTC timestamp on every update

**Unchanged Fields**:
- `id`: Never changes
- `user_id`: Never changes
- `created_at`: Never changes

**Example Usage**:
```bash
# Toggle completion status
curl -X PATCH http://localhost:8000/api/tasks/123e4567-e89b-12d3-a456-426614174000 \
  -H "Content-Type: application/json" \
  -b cookies.txt \
  -d '{"completed": true}'

# Update title and priority
curl -X PATCH http://localhost:8000/api/tasks/123e4567-e89b-12d3-a456-426614174000 \
  -H "Content-Type: application/json" \
  -b cookies.txt \
  -d '{
    "title": "Buy groceries and milk",
    "priority": "high"
  }'
```

---

### DELETE /api/tasks/{id}

**Description**: Permanently delete a task (hard delete, not soft delete).

**Authentication**: Required (session token)

**Request Headers**:
```http
Cookie: session_token=<TOKEN>
```

**URL Parameters**:
- `id`: UUID of the task

**Success Response (204 No Content)**:
No response body.

**Error Responses**:

**401 Unauthorized** - Not authenticated:
```json
{
  "detail": "Not authenticated"
}
```

**404 Not Found** - Task not found OR not owned by authenticated user:
```json
{
  "detail": "Task not found"
}
```

**Security Note**: Returns `404 Not Found` (not `403 Forbidden`) to prevent task ID enumeration.

**Database Operation**: Task is permanently removed from database (no recovery).

**Example Usage**:
```bash
curl -X DELETE http://localhost:8000/api/tasks/123e4567-e89b-12d3-a456-426614174000 \
  -b cookies.txt
```

---

## Common Patterns

### Optimistic UI Updates (Frontend)

```typescript
// 1. Update UI immediately (optimistic)
setTasks(tasks.map(t => t.id === taskId ? { ...t, completed: !t.completed } : t));

// 2. Send API request
try {
  await fetch(`/api/tasks/${taskId}`, {
    method: 'PATCH',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ completed: !task.completed }),
    credentials: 'include',
  });
} catch (error) {
  // 3. Revert UI if request fails
  setTasks(originalTasks);
  alert('Failed to update task. Please try again.');
}
```

### User Isolation (Backend)

```python
# Always filter by user_id
@router.get("/tasks")
async def list_tasks(
    current_user: User = Depends(get_current_user),
    session: Session = Depends(get_session)
):
    statement = select(Task).where(Task.user_id == current_user.id)
    tasks = session.exec(statement).all()
    return {"tasks": tasks}

# For single task, return 404 if not owned
@router.get("/tasks/{task_id}")
async def get_task(
    task_id: UUID,
    current_user: User = Depends(get_current_user),
    session: Session = Depends(get_session)
):
    task = session.get(Task, task_id)

    # Return 404 if task not found OR not owned (prevent enumeration)
    if not task or task.user_id != current_user.id:
        raise HTTPException(status_code=404, detail="Task not found")

    return task
```

---

## Security Considerations

### User Data Isolation
- ✅ ALL queries filtered by `user_id = authenticated_user.id`
- ✅ Users cannot access other users' tasks
- ✅ Returns `404 Not Found` (not `403 Forbidden`) to prevent task ID enumeration

### Input Validation
- ✅ Title: Trimmed, 1-200 chars
- ✅ Description: Max 1000 chars
- ✅ Tags: Max 10 per task
- ✅ Priority: Enum validation (low, medium, high, critical)
- ✅ XSS prevention: Input sanitized before rendering

### SQL Injection Prevention
- ✅ All queries use parameterized statements (SQLModel ORM)
- ✅ No raw SQL with string concatenation
- ✅ User input never directly inserted into queries

### Rate Limiting
- ✅ 100 requests/minute per user (across all endpoints)
- ✅ Prevents abuse and DoS attacks

---

## Database Operations

### List Tasks
```sql
SELECT id, user_id, title, description, completed, priority, tags, category, created_at, updated_at
FROM tasks
WHERE user_id = $1
ORDER BY created_at DESC
LIMIT $2 OFFSET $3;
```

### Create Task
```sql
INSERT INTO tasks (id, user_id, title, description, completed, priority, tags, category, created_at, updated_at)
VALUES ($1, $2, $3, $4, false, $5, $6, $7, now(), now())
RETURNING id, user_id, title, description, completed, priority, tags, category, created_at, updated_at;
```

### Get Task
```sql
SELECT id, user_id, title, description, completed, priority, tags, category, created_at, updated_at
FROM tasks
WHERE id = $1 AND user_id = $2;
```

### Update Task
```sql
UPDATE tasks
SET title = COALESCE($3, title),
    description = COALESCE($4, description),
    completed = COALESCE($5, completed),
    priority = COALESCE($6, priority),
    tags = COALESCE($7, tags),
    category = COALESCE($8, category),
    updated_at = now()
WHERE id = $1 AND user_id = $2
RETURNING id, user_id, title, description, completed, priority, tags, category, created_at, updated_at;
```

### Delete Task
```sql
DELETE FROM tasks
WHERE id = $1 AND user_id = $2
RETURNING id;
```

---

## Frontend Integration

### React API Client Example

```typescript
// frontend/lib/api.ts
const API_URL = process.env.NEXT_PUBLIC_API_URL;

export async function getTasks(completed?: boolean) {
  const params = new URLSearchParams();
  if (completed !== undefined) params.append('completed', String(completed));

  const response = await fetch(`${API_URL}/api/tasks?${params}`, {
    credentials: 'include',
  });

  if (!response.ok) throw new Error('Failed to fetch tasks');
  return response.json();
}

export async function createTask(data: TaskCreate) {
  const response = await fetch(`${API_URL}/api/tasks`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify(data),
    credentials: 'include',
  });

  if (!response.ok) {
    const error = await response.json();
    throw new Error(error.detail);
  }

  return response.json();
}

export async function updateTask(id: string, data: TaskUpdate) {
  const response = await fetch(`${API_URL}/api/tasks/${id}`, {
    method: 'PATCH',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify(data),
    credentials: 'include',
  });

  if (!response.ok) {
    const error = await response.json();
    throw new Error(error.detail);
  }

  return response.json();
}

export async function deleteTask(id: string) {
  const response = await fetch(`${API_URL}/api/tasks/${id}`, {
    method: 'DELETE',
    credentials: 'include',
  });

  if (!response.ok) {
    const error = await response.json();
    throw new Error(error.detail);
  }
}
```

---

## Testing Checklist

### Unit Tests
- ✅ Task validation (title, description, tags)
- ✅ Priority enum validation
- ✅ User isolation logic

### Integration Tests
- ✅ List tasks → 200 OK with user's tasks only
- ✅ List tasks with completed filter → filtered results
- ✅ Create task with valid data → 201 Created
- ✅ Create task with empty title → 400 Bad Request
- ✅ Create task with title >200 chars → 400 Bad Request
- ✅ Create task with >10 tags → 400 Bad Request
- ✅ Get task by ID (owned) → 200 OK
- ✅ Get task by ID (not owned) → 404 Not Found
- ✅ Update task (owned) → 200 OK
- ✅ Update task (not owned) → 404 Not Found
- ✅ Delete task (owned) → 204 No Content
- ✅ Delete task (not owned) → 404 Not Found
- ✅ All operations without auth → 401 Unauthorized

### Security Tests
- ✅ User A cannot see User B's tasks
- ✅ User A cannot update User B's tasks
- ✅ User A cannot delete User B's tasks
- ✅ SQL injection attempts fail safely
- ✅ XSS payloads are sanitized

---

## Performance Targets

- **List tasks** (<1000): <50ms (composite index)
- **Create task**: <20ms (UUID generation + insert)
- **Get single task**: <5ms (primary key lookup)
- **Update task**: <15ms (indexed update)
- **Delete task**: <10ms (indexed delete)

**Indexes used**:
- `idx_tasks_user_completed_created` (user_id, completed, created_at DESC) → List tasks query
- PRIMARY KEY (id) → Get/Update/Delete single task

---

**Status**: ✅ Complete
**Related**: [auth.md](./auth.md) for authentication endpoints
