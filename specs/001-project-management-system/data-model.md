# Data Model: Multi-Tenant Project Management System

**Feature**: 001-project-management-system
**Date**: 2025-12-27
**Status**: Complete

## Overview

This document defines the complete database schema for the multi-tenant project management system. All entities use UUID primary keys and enforce multi-tenant isolation via organization_id filtering.

---

## Entity Relationship Diagram

```
User (authentication)
├── Session (1:N)
├── Notification (1:N)
├── OrganizationMember (1:N)
│   └── Organization (N:1)
│       ├── Invitation (1:N)
│       ├── Project (1:N)
│       │   ├── ProjectMember (1:N)
│       │   ├── Board (1:N)
│       │   │   ├── Column (1:N)
│       │   │   │   └── Task (1:N)
│       │   │   │       ├── Comment (1:N)
│       │   │   │       ├── Attachment (1:N)
│       │   │   │       └── ActivityLog (1:N)
│       │   │   └── Task (1:N)
│       │   └── Task (1:N, project-level)
│       └── OrganizationMember (1:N)
└── Task.assignee (N:1, optional)
```

---

## Entities

### 1. User

**Purpose**: Represents a person using the system

**Fields**:
| Field | Type | Constraints | Description |
|-------|------|-------------|-------------|
| id | UUID | PK | Unique identifier |
| email | String | UNIQUE, NOT NULL, lowercase | User's email address |
| hashed_password | String | NOT NULL | Bcrypt-hashed password |
| full_name | String | NOT NULL | Display name |
| avatar_url | String | NULLABLE | Profile picture URL |
| email_verified | Boolean | NOT NULL, default=False | Email verification status |
| timezone | String | NOT NULL, default="UTC" | User's timezone |
| language | String | NOT NULL, default="en" | Preferred language |
| created_at | DateTime | NOT NULL, auto | Account creation timestamp |
| updated_at | DateTime | NOT NULL, auto | Last update timestamp |

**Indexes**:
- PRIMARY KEY (id)
- UNIQUE INDEX (email)

**Validation Rules**:
- email: Valid email format, lowercase
- password: Min 8 chars, at least 1 number or special character
- full_name: 1-100 characters
- timezone: Valid IANA timezone string
- language: ISO 639-1 language code

**State Transitions**:
- email_verified: False → True (after email verification)
- Cannot transition back to False (requires new account)

---

### 2. Session

**Purpose**: Tracks active user sessions with JWT tokens

**Fields**:
| Field | Type | Constraints | Description |
|-------|------|-------------|-------------|
| id | UUID | PK | Unique identifier |
| user_id | UUID | FK(User.id) CASCADE, NOT NULL | Session owner |
| token | String | UNIQUE, NOT NULL | Hashed JWT access token |
| refresh_token | String | UNIQUE, NULLABLE | Refresh token for rotation |
| expires_at | DateTime | NOT NULL | Session expiration |
| ip_address | String | NULLABLE | Client IP address |
| user_agent | String | NULLABLE | Client user agent |
| created_at | DateTime | NOT NULL, auto | Session creation |

**Indexes**:
- PRIMARY KEY (id)
- INDEX (user_id)
- UNIQUE INDEX (token)
- INDEX (expires_at) - for cleanup queries

**Validation Rules**:
- expires_at: Must be in the future
- token: Must be a valid JWT hash

---

### 3. Organization

**Purpose**: Multi-tenant workspace/tenant

**Fields**:
| Field | Type | Constraints | Description |
|-------|------|-------------|-------------|
| id | UUID | PK | Unique identifier |
| slug | String | UNIQUE, NOT NULL, lowercase | URL-safe identifier (e.g., "acme-corp") |
| name | String | NOT NULL | Display name |
| description | Text | NULLABLE | Organization description |
| logo_url | String | NULLABLE | Organization logo URL |
| owner_id | UUID | FK(User.id) SET NULL, NULLABLE | Current owner |
| created_at | DateTime | NOT NULL, auto | Creation timestamp |
| updated_at | DateTime | NOT NULL, auto | Last update timestamp |
| archived | Boolean | NOT NULL, default=False | Soft delete flag |

**Indexes**:
- PRIMARY KEY (id)
- UNIQUE INDEX (slug)
- INDEX (owner_id)
- INDEX (archived) - for filtering active orgs

**Validation Rules**:
- slug: 3-50 chars, lowercase, alphanumeric + hyphens, no consecutive hyphens
- name: 1-100 characters
- description: Max 1000 characters

**State Transitions**:
- archived: False ⇄ True (soft delete/restore)

---

### 4. OrganizationMember

**Purpose**: User membership in an organization with role

**Fields**:
| Field | Type | Constraints | Description |
|-------|------|-------------|-------------|
| id | UUID | PK | Unique identifier |
| organization_id | UUID | FK(Organization.id) CASCADE, NOT NULL | Organization |
| user_id | UUID | FK(User.id) CASCADE, NOT NULL | Member |
| role | Enum | NOT NULL | "owner", "admin", "member" |
| joined_at | DateTime | NOT NULL, auto | Membership start |

**Indexes**:
- PRIMARY KEY (id)
- UNIQUE INDEX (organization_id, user_id) - no duplicate memberships
- INDEX (user_id) - for user's orgs lookup
- INDEX (organization_id, role) - for role-based queries

**Validation Rules**:
- role: Must be one of ["owner", "admin", "member"]
- Only one owner per organization (enforced at application level)

---

### 5. Invitation

**Purpose**: Pending organization invitations

**Fields**:
| Field | Type | Constraints | Description |
|-------|------|-------------|-------------|
| id | UUID | PK | Unique identifier |
| organization_id | UUID | FK(Organization.id) CASCADE, NOT NULL | Target organization |
| email | String | NOT NULL, lowercase | Invitee email |
| role | Enum | NOT NULL | "admin" or "member" (not "owner") |
| token | UUID | UNIQUE, NOT NULL | Invitation token (UUID) |
| invited_by | UUID | FK(User.id) SET NULL, NULLABLE | Inviter |
| expires_at | DateTime | NOT NULL | Expiration (7 days from creation) |
| accepted_at | DateTime | NULLABLE | Acceptance timestamp |
| created_at | DateTime | NOT NULL, auto | Invitation creation |

**Indexes**:
- PRIMARY KEY (id)
- UNIQUE INDEX (token)
- INDEX (organization_id, email) - for duplicate invitation check
- INDEX (expires_at) - for cleanup queries

**Validation Rules**:
- email: Valid email format, lowercase
- role: Must be "admin" or "member" (no "owner")
- expires_at: Exactly 7 days from created_at
- accepted_at: Null (pending) or <= expires_at

**State Transitions**:
- accepted_at: Null → DateTime (when accepted)
- Cannot un-accept (invitation becomes inactive)

---

### 6. Project

**Purpose**: Work initiative within an organization

**Fields**:
| Field | Type | Constraints | Description |
|-------|------|-------------|-------------|
| id | UUID | PK | Unique identifier |
| organization_id | UUID | FK(Organization.id) CASCADE, NOT NULL | Parent organization |
| key | String | NOT NULL, uppercase | Project key (e.g., "WEB") |
| name | String | NOT NULL | Display name |
| description | Text | NULLABLE | Project description |
| icon | String | NULLABLE | Emoji or icon name |
| visibility | Enum | NOT NULL, default="private" | "private" or "organization" |
| created_by | UUID | FK(User.id) SET NULL, NULLABLE | Creator |
| archived | Boolean | NOT NULL, default=False | Soft delete flag |
| next_task_number | Integer | NOT NULL, default=1 | Sequential task counter |
| created_at | DateTime | NOT NULL, auto | Creation timestamp |
| updated_at | DateTime | NOT NULL, auto | Last update timestamp |

**Indexes**:
- PRIMARY KEY (id)
- UNIQUE INDEX (organization_id, key) - unique keys per org
- INDEX (organization_id, archived) - for filtering active projects
- INDEX (created_by)

**Validation Rules**:
- key: 2-10 chars, uppercase, alphanumeric only
- name: 1-100 characters
- description: Max 2000 characters
- visibility: Must be "private" or "organization"
- next_task_number: Positive integer

**State Transitions**:
- archived: False ⇄ True (soft delete/restore)
- next_task_number: Increments atomically on task creation

---

### 7. ProjectMember

**Purpose**: User membership in a project with role

**Fields**:
| Field | Type | Constraints | Description |
|-------|------|-------------|-------------|
| id | UUID | PK | Unique identifier |
| project_id | UUID | FK(Project.id) CASCADE, NOT NULL | Project |
| user_id | UUID | FK(User.id) CASCADE, NOT NULL | Member |
| role | Enum | NOT NULL | "admin", "member", "viewer" |
| added_at | DateTime | NOT NULL, auto | Membership start |

**Indexes**:
- PRIMARY KEY (id)
- UNIQUE INDEX (project_id, user_id) - no duplicate memberships
- INDEX (user_id) - for user's projects lookup
- INDEX (project_id, role) - for role-based queries

**Validation Rules**:
- role: Must be one of ["admin", "member", "viewer"]
- User must be a member of the project's organization

---

### 8. Board

**Purpose**: Kanban board within a project

**Fields**:
| Field | Type | Constraints | Description |
|-------|------|-------------|-------------|
| id | UUID | PK | Unique identifier |
| project_id | UUID | FK(Project.id) CASCADE, NOT NULL | Parent project |
| name | String | NOT NULL, default="Main Board" | Board name |
| description | Text | NULLABLE | Board description |
| board_type | Enum | NOT NULL, default="kanban" | "kanban" (only type for MVP) |
| created_at | DateTime | NOT NULL, auto | Creation timestamp |
| updated_at | DateTime | NOT NULL, auto | Last update timestamp |

**Indexes**:
- PRIMARY KEY (id)
- INDEX (project_id) - for project's boards

**Validation Rules**:
- name: 1-100 characters
- description: Max 500 characters
- board_type: Must be "kanban"

**Note**: MVP supports one board per project (auto-created on project creation)

---

### 9. Column

**Purpose**: Workflow state column on a Kanban board

**Fields**:
| Field | Type | Constraints | Description |
|-------|------|-------------|-------------|
| id | UUID | PK | Unique identifier |
| board_id | UUID | FK(Board.id) CASCADE, NOT NULL | Parent board |
| name | String | NOT NULL | Column name (e.g., "Todo", "In Progress") |
| color | String | NOT NULL, default="#6366F1" | Hex color code |
| position | Float | NOT NULL | Ordering (0.0, 1000.0, 2000.0, ...) |
| wip_limit | Integer | NULLABLE | Work-in-progress limit |
| created_at | DateTime | NOT NULL, auto | Creation timestamp |
| updated_at | DateTime | NOT NULL, auto | Last update timestamp |

**Indexes**:
- PRIMARY KEY (id)
- INDEX (board_id, position) - for column ordering

**Validation Rules**:
- name: 1-50 characters
- color: Valid hex color code (#RRGGBB)
- position: Positive float
- wip_limit: Null or positive integer

---

### 10. Task

**Purpose**: Work item on a Kanban board

**Fields**:
| Field | Type | Constraints | Description |
|-------|------|-------------|-------------|
| id | UUID | PK | Unique identifier |
| project_id | UUID | FK(Project.id) CASCADE, NOT NULL | Parent project |
| board_id | UUID | FK(Board.id) CASCADE, NOT NULL | Parent board |
| column_id | UUID | FK(Column.id) CASCADE, NOT NULL | Current column |
| task_number | Integer | NOT NULL | Sequential number per project |
| title | String | NOT NULL | Task title (max 200 chars) |
| description | Text | NULLABLE | Markdown description |
| task_type | Enum | NOT NULL, default="task" | "story", "bug", "task", "epic" |
| priority | Enum | NOT NULL, default="medium" | "critical", "high", "medium", "low", "none" |
| assignee_id | UUID | FK(User.id) SET NULL, NULLABLE | Assigned user |
| reporter_id | UUID | FK(User.id) SET NULL, NOT NULL | Task creator |
| due_date | Date | NULLABLE | Deadline |
| story_points | Integer | NULLABLE | Effort estimate |
| position | Float | NOT NULL | Ordering within column |
| labels | JSON | NOT NULL, default=[] | Array of label strings |
| archived | Boolean | NOT NULL, default=False | Soft delete flag |
| completed | Boolean | NOT NULL, default=False | Completion status (Phase 2 compat) |
| created_at | DateTime | NOT NULL, auto | Creation timestamp |
| updated_at | DateTime | NOT NULL, auto | Last update timestamp |

**Indexes**:
- PRIMARY KEY (id)
- UNIQUE INDEX (project_id, task_number) - unique task numbers per project
- INDEX (column_id, position) - for board view
- INDEX (assignee_id) - for "my tasks" view
- INDEX (project_id, archived) - for filtering active tasks
- INDEX (due_date) - for deadline queries

**Validation Rules**:
- title: 1-200 characters
- description: Max 10000 characters (Markdown)
- task_type: Must be one of ["story", "bug", "task", "epic"]
- priority: Must be one of ["critical", "high", "medium", "low", "none"]
- story_points: Null or 1-100
- position: Positive float
- labels: Array of strings, each max 50 chars

**State Transitions**:
- completed: False ⇄ True (task completion toggle)
- archived: False → True (soft delete, no restore in MVP)
- column_id: Any column in same board (drag-and-drop)

---

### 11. Comment

**Purpose**: Discussion thread on a task

**Fields**:
| Field | Type | Constraints | Description |
|-------|------|-------------|-------------|
| id | UUID | PK | Unique identifier |
| task_id | UUID | FK(Task.id) CASCADE, NOT NULL | Parent task |
| user_id | UUID | FK(User.id) SET NULL, NOT NULL | Comment author |
| content | Text | NOT NULL | Markdown content |
| edited | Boolean | NOT NULL, default=False | Edit flag |
| created_at | DateTime | NOT NULL, auto | Creation timestamp |
| updated_at | DateTime | NOT NULL, auto | Last edit timestamp |

**Indexes**:
- PRIMARY KEY (id)
- INDEX (task_id, created_at) - for comment ordering

**Validation Rules**:
- content: 1-5000 characters (Markdown)
- Editable within 5 minutes of creation (enforced at application level)

**State Transitions**:
- edited: False → True (when updated within 5 min of creation)

---

### 12. Attachment

**Purpose**: File attached to a task

**Fields**:
| Field | Type | Constraints | Description |
|-------|------|-------------|-------------|
| id | UUID | PK | Unique identifier |
| task_id | UUID | FK(Task.id) CASCADE, NOT NULL | Parent task |
| user_id | UUID | FK(User.id) SET NULL, NOT NULL | Uploader |
| filename | String | NOT NULL | Original filename |
| file_size | Integer | NOT NULL | File size in bytes |
| mime_type | String | NOT NULL | MIME type |
| storage_path | String | NOT NULL | File system or S3 path |
| created_at | DateTime | NOT NULL, auto | Upload timestamp |

**Indexes**:
- PRIMARY KEY (id)
- INDEX (task_id, created_at) - for attachment listing

**Validation Rules**:
- filename: 1-255 chars, sanitized (no path traversal)
- file_size: Max 10MB (10,485,760 bytes)
- mime_type: Whitelist: image/*, application/pdf, application/msword, text/*, application/json, application/zip
- Max 20 attachments per task (enforced at application level)

---

### 13. ActivityLog

**Purpose**: Audit trail of task changes

**Fields**:
| Field | Type | Constraints | Description |
|-------|------|-------------|-------------|
| id | UUID | PK | Unique identifier |
| task_id | UUID | FK(Task.id) CASCADE, NOT NULL | Related task |
| user_id | UUID | FK(User.id) SET NULL, NOT NULL | Actor |
| action | String | NOT NULL | "created", "updated", "moved", "commented", etc. |
| field_name | String | NULLABLE | Changed field (e.g., "status", "priority") |
| old_value | Text | NULLABLE | Previous value |
| new_value | Text | NULLABLE | New value |
| created_at | DateTime | NOT NULL, auto | Event timestamp |

**Indexes**:
- PRIMARY KEY (id)
- INDEX (task_id, created_at DESC) - for activity timeline

**Validation Rules**:
- action: Must be one of predefined actions
- field_name: Required for "updated" action, null for others

---

### 14. Notification

**Purpose**: In-app notifications for users

**Fields**:
| Field | Type | Constraints | Description |
|-------|------|-------------|-------------|
| id | UUID | PK | Unique identifier |
| user_id | UUID | FK(User.id) CASCADE, NOT NULL | Recipient |
| type | Enum | NOT NULL | "task_assigned", "mentioned", "comment_added", "due_soon" |
| reference_id | UUID | NOT NULL | Task or comment ID |
| title | String | NOT NULL | Notification title |
| message | Text | NOT NULL | Notification message |
| read | Boolean | NOT NULL, default=False | Read status |
| created_at | DateTime | NOT NULL, auto | Creation timestamp |

**Indexes**:
- PRIMARY KEY (id)
- INDEX (user_id, read, created_at DESC) - for notification listing

**Validation Rules**:
- type: Must be one of ["task_assigned", "mentioned", "comment_added", "due_soon"]
- title: 1-200 characters
- message: 1-500 characters

**State Transitions**:
- read: False → True (mark as read)

---

## Database Constraints & Triggers

### Foreign Key Constraints

All foreign keys use **CASCADE DELETE** except:
- `Organization.owner_id` → `User.id` (SET NULL - org can exist without owner during transfer)
- `Project.created_by` → `User.id` (SET NULL - preserve project if user deleted)
- `Task.assignee_id` → `User.id` (SET NULL - unassign if user deleted)
- `Task.reporter_id` → `User.id` (SET NULL - preserve task if user deleted)
- `Comment.user_id` → `User.id` (SET NULL - preserve comment if user deleted)
- `Attachment.user_id` → `User.id` (SET NULL - preserve attachment if user deleted)
- `ActivityLog.user_id` → `User.id` (SET NULL - preserve audit trail if user deleted)
- `Invitation.invited_by` → `User.id` (SET NULL - preserve invitation if inviter deleted)

### Check Constraints

```sql
-- Organization slug format
ALTER TABLE organization ADD CONSTRAINT org_slug_format
  CHECK (slug ~ '^[a-z0-9-]+$' AND slug NOT LIKE '--%');

-- Project key format
ALTER TABLE project ADD CONSTRAINT project_key_format
  CHECK (key ~ '^[A-Z0-9]+$');

-- Color hex format
ALTER TABLE column ADD CONSTRAINT column_color_format
  CHECK (color ~ '^#[0-9A-Fa-f]{6}$');

-- Email format (basic check)
ALTER TABLE user ADD CONSTRAINT user_email_format
  CHECK (email ~ '^[^@]+@[^@]+\.[^@]+$');

-- Positive file size
ALTER TABLE attachment ADD CONSTRAINT attachment_file_size
  CHECK (file_size > 0 AND file_size <= 10485760);
```

### Application-Level Constraints

These constraints are enforced in application logic (not database):
- Only one owner per organization
- Max 20 attachments per task
- Comments editable within 5 minutes
- Password requirements (min 8 chars, complexity)
- Email verification required before email notifications

---

## Migration Strategy (Phase 2 → Project Management System)

### Step 1: Create Default Organization

```python
async def migrate_existing_users():
    # For each existing user, create a "Personal" organization
    users = await session.exec(select(User))
    for user in users:
        org = Organization(
            slug=f"personal-{user.id[:8]}",
            name=f"{user.full_name}'s Workspace",
            owner_id=user.id,
        )
        session.add(org)

        # Add user as owner
        member = OrganizationMember(
            organization_id=org.id,
            user_id=user.id,
            role="owner",
        )
        session.add(member)

    await session.commit()
```

### Step 2: Create Default Project & Board

```python
async def migrate_existing_tasks():
    orgs = await session.exec(select(Organization))
    for org in orgs:
        # Create default project
        project = Project(
            organization_id=org.id,
            key="TODO",
            name="My Tasks",
            visibility="private",
            created_by=org.owner_id,
        )
        session.add(project)
        await session.flush()  # Get project.id

        # Add owner as project admin
        member = ProjectMember(
            project_id=project.id,
            user_id=org.owner_id,
            role="admin",
        )
        session.add(member)

        # Create default board
        board = Board(
            project_id=project.id,
            name="Main Board",
        )
        session.add(board)
        await session.flush()  # Get board.id

        # Create default columns
        columns = [
            Column(board_id=board.id, name="Todo", position=0.0),
            Column(board_id=board.id, name="In Progress", position=1000.0),
            Column(board_id=board.id, name="Done", position=2000.0),
        ]
        for col in columns:
            session.add(col)

    await session.commit()
```

### Step 3: Migrate Existing Tasks

```python
async def migrate_task_data():
    # Assuming Phase 2 tasks are in a "tasks" table
    old_tasks = await session.exec(select(OldTask))

    for old_task in old_tasks:
        # Find user's default project
        user_org = await get_user_default_org(old_task.user_id)
        user_project = await get_org_default_project(user_org.id)
        board = await get_project_default_board(user_project.id)

        # Determine column based on completed status
        if old_task.completed:
            column = await get_column_by_name(board.id, "Done")
        else:
            column = await get_column_by_name(board.id, "Todo")

        # Create new task
        new_task = Task(
            project_id=user_project.id,
            board_id=board.id,
            column_id=column.id,
            task_number=user_project.next_task_number,
            title=old_task.title,
            description=old_task.description,
            priority=old_task.priority,  # Already exists in Phase 2
            completed=old_task.completed,  # Preserve for backward compat
            reporter_id=old_task.user_id,
            assignee_id=old_task.user_id,  # Assign to self
            labels=old_task.tags,  # Map tags to labels
            created_at=old_task.created_at,
            updated_at=old_task.updated_at,
            position=float(user_project.next_task_number) * 1000.0,
        )
        session.add(new_task)

        # Increment task counter
        user_project.next_task_number += 1

    await session.commit()
```

### Step 4: Preserve Phase 2 API Compatibility

```python
# Keep /api/tasks endpoint for backward compatibility
@router.get("/api/tasks")
async def get_tasks_legacy(current_user: User = Depends(get_current_user)):
    """Legacy endpoint: Get tasks from user's default project"""
    org = await get_user_default_org(current_user.id)
    project = await get_org_default_project(org.id)
    return await get_project_tasks(project.id)

@router.post("/api/tasks")
async def create_task_legacy(task_data: dict, current_user: User = Depends(get_current_user)):
    """Legacy endpoint: Create task in user's default project"""
    org = await get_user_default_org(current_user.id)
    project = await get_org_default_project(org.id)
    return await create_task(project.id, task_data, current_user)
```

---

## Performance Considerations

### Recommended Indexes (Summary)

1. **Multi-tenant queries**: `(organization_id, ...)`
2. **Task lookups**: `(project_id, task_number)`
3. **Board view**: `(column_id, position)`
4. **User's tasks**: `(assignee_id)`
5. **Timeline queries**: `(task_id, created_at DESC)`

### Query Optimization

- Use `select_related` / `joinedload` for related entities
- Pagination on all list endpoints (limit 100 default)
- Avoid N+1 queries with eager loading

### Estimated Table Sizes (5,000 users)

| Table | Rows (MVP) | Growth Rate |
|-------|-----------|-------------|
| User | 5,000 | Linear with users |
| Session | 10,000 | 2x users (multiple devices) |
| Organization | 100 | Low (most users share orgs) |
| OrganizationMember | 5,000 | Linear with users |
| Project | 500 | 5 per org average |
| Task | 50,000 | 100 per org average |
| Comment | 100,000 | 2x tasks average |
| ActivityLog | 200,000 | 4x tasks average |

Total estimated storage: <1GB (text-heavy data)

---

## Data Model Complete

This data model supports all functional requirements from spec.md:
- ✅ Multi-tenant architecture with organization isolation
- ✅ Role-based access control (org-level and project-level)
- ✅ Kanban boards with drag-and-drop task ordering
- ✅ Sequential task numbering per project
- ✅ File attachments with size limits
- ✅ Comments with @mentions
- ✅ Activity logging for audit trail
- ✅ Backward compatibility with Phase 2 todo app

Ready to proceed with API contract definition.
