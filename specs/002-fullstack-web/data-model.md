# Data Model: Full-Stack Web Application

**Feature**: 002-fullstack-web
**Database**: Neon PostgreSQL 16 (serverless)
**ORM**: SQLModel
**Migration Tool**: Alembic
**Date**: 2025-12-26

---

## Entity Relationship Diagram (ERD)

```mermaid
erDiagram
    User ||--o{ Task : owns
    User ||--o{ Session : has
    User ||--o{ Account : has

    User {
        uuid id PK
        varchar email UK
        boolean email_verified
        varchar name
        varchar hashed_password
        timestamp created_at
        timestamp updated_at
    }

    Task {
        uuid id PK
        uuid user_id FK
        varchar title
        text description
        boolean completed
        varchar priority
        text_array tags
        varchar category
        timestamp created_at
        timestamp updated_at
    }

    Session {
        uuid id PK
        uuid user_id FK
        varchar token UK
        timestamp expires_at
        inet ip_address
        text user_agent
        timestamp created_at
    }

    Account {
        uuid id PK
        uuid user_id FK
        varchar provider
        varchar provider_account_id
        text access_token
        text refresh_token
        timestamp expires_at
        timestamp created_at
    }
```

---

## Entity: User

### Purpose
Represents a registered user account with authentication credentials.

### Table: `users`

### Fields

| Field | SQL Type | Constraints | Python Type | Description |
|-------|----------|-------------|-------------|-------------|
| `id` | UUID | PRIMARY KEY, NOT NULL | `uuid.UUID` | Unique user identifier |
| `email` | VARCHAR(255) | UNIQUE, NOT NULL, INDEX | `str` | Lowercase normalized email address |
| `email_verified` | BOOLEAN | NOT NULL, DEFAULT false | `bool` | Email verification status (Phase 3) |
| `name` | VARCHAR(255) | NULLABLE | `str \| None` | User display name (optional) |
| `hashed_password` | VARCHAR(255) | NOT NULL | `str` | Bcrypt hashed password (cost factor 12) |
| `created_at` | TIMESTAMP WITH TIME ZONE | NOT NULL, DEFAULT now() | `datetime` | Account creation timestamp (UTC) |
| `updated_at` | TIMESTAMP WITH TIME ZONE | NOT NULL, DEFAULT now() | `datetime` | Last update timestamp (UTC) |

### Indexes

```sql
CREATE TABLE users (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    email VARCHAR(255) UNIQUE NOT NULL,
    email_verified BOOLEAN NOT NULL DEFAULT false,
    name VARCHAR(255),
    hashed_password VARCHAR(255) NOT NULL,
    created_at TIMESTAMP WITH TIME ZONE NOT NULL DEFAULT now(),
    updated_at TIMESTAMP WITH TIME ZONE NOT NULL DEFAULT now()
);

CREATE INDEX idx_users_email ON users(email);
CREATE INDEX idx_users_created_at ON users(created_at);
```

### SQLModel Definition

```python
# backend/app/models/user.py
from sqlmodel import SQLModel, Field
from uuid import UUID, uuid4
from datetime import datetime

class User(SQLModel, table=True):
    __tablename__ = "users"

    id: UUID = Field(default_factory=uuid4, primary_key=True)
    email: str = Field(max_length=255, unique=True, index=True, sa_column_kwargs={"nullable": False})
    email_verified: bool = Field(default=False)
    name: str | None = Field(default=None, max_length=255)
    hashed_password: str = Field(max_length=255, sa_column_kwargs={"nullable": False})
    created_at: datetime = Field(default_factory=datetime.utcnow, sa_column_kwargs={"nullable": False})
    updated_at: datetime = Field(default_factory=datetime.utcnow, sa_column_kwargs={"nullable": False})
```

### Pydantic Schemas

```python
# backend/app/schemas/user.py
from pydantic import BaseModel, EmailStr, Field
from uuid import UUID
from datetime import datetime

class UserCreate(BaseModel):
    """Request schema for user registration"""
    email: EmailStr
    password: str = Field(..., min_length=8, max_length=100)
    name: str | None = Field(None, max_length=255)

class UserRead(BaseModel):
    """Response schema for user data (no password)"""
    id: UUID
    email: str
    email_verified: bool
    name: str | None
    created_at: datetime

    class Config:
        from_attributes = True
```

### Validation Rules

- **email**: Must be valid RFC 5322 email, max 255 chars, converted to lowercase before storage
- **password**: Min 8 chars, max 100 chars (before hashing)
- **hashed_password**: Must be bcrypt hash, never exposed in API responses
- **name**: Optional, max 255 chars

### Constraints

- **Unique Email**: Case-insensitive unique constraint (enforced via lowercase normalization)
- **No Plaintext Passwords**: Only hashed_password stored, never plaintext
- **Immutable ID**: UUID never changes after creation

---

## Entity: Task

### Purpose
Represents a todo task owned by a specific user with completion tracking.

### Table: `tasks`

### Fields

| Field | SQL Type | Constraints | Python Type | Description |
|-------|----------|-------------|-------------|-------------|
| `id` | UUID | PRIMARY KEY, NOT NULL | `uuid.UUID` | Unique task identifier |
| `user_id` | UUID | FOREIGN KEY (users.id), NOT NULL, INDEX | `uuid.UUID` | Owner of the task |
| `title` | VARCHAR(200) | NOT NULL | `str` | Task title (1-200 chars) |
| `description` | TEXT | NULLABLE | `str \| None` | Task description (max 1000 chars, enforced in app) |
| `completed` | BOOLEAN | NOT NULL, DEFAULT false, INDEX | `bool` | Completion status |
| `priority` | VARCHAR(10) | NULLABLE, CHECK IN ('low', 'medium', 'high', 'critical') | `str \| None` | Task priority |
| `tags` | TEXT[] | DEFAULT '{}' | `list[str]` | Array of string tags |
| `category` | VARCHAR(50) | NULLABLE | `str \| None` | Task category |
| `created_at` | TIMESTAMP WITH TIME ZONE | NOT NULL, DEFAULT now(), INDEX | `datetime` | Creation timestamp (UTC) |
| `updated_at` | TIMESTAMP WITH TIME ZONE | NOT NULL, DEFAULT now() | `datetime` | Last update timestamp (UTC) |

### Indexes

```sql
CREATE TABLE tasks (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    user_id UUID NOT NULL REFERENCES users(id) ON DELETE CASCADE,
    title VARCHAR(200) NOT NULL,
    description TEXT,
    completed BOOLEAN NOT NULL DEFAULT false,
    priority VARCHAR(10) CHECK (priority IN ('low', 'medium', 'high', 'critical')),
    tags TEXT[] DEFAULT '{}',
    category VARCHAR(50),
    created_at TIMESTAMP WITH TIME ZONE NOT NULL DEFAULT now(),
    updated_at TIMESTAMP WITH TIME ZONE NOT NULL DEFAULT now()
);

-- Performance indexes
CREATE INDEX idx_tasks_user_id ON tasks(user_id);
CREATE INDEX idx_tasks_completed ON tasks(completed);
CREATE INDEX idx_tasks_created_at ON tasks(created_at);

-- Composite index for common query: user's tasks sorted by date
CREATE INDEX idx_tasks_user_completed_created ON tasks(user_id, completed, created_at DESC);
```

### SQLModel Definition

```python
# backend/app/models/task.py
from sqlmodel import SQLModel, Field
from uuid import UUID, uuid4
from datetime import datetime
from typing import List

class Task(SQLModel, table=True):
    __tablename__ = "tasks"

    id: UUID = Field(default_factory=uuid4, primary_key=True)
    user_id: UUID = Field(foreign_key="users.id", index=True, sa_column_kwargs={"nullable": False})
    title: str = Field(max_length=200, sa_column_kwargs={"nullable": False})
    description: str | None = Field(default=None, sa_column=Column(Text))
    completed: bool = Field(default=False, index=True)
    priority: str | None = Field(default=None, max_length=10)
    tags: List[str] = Field(default_factory=list, sa_column=Column(ARRAY(String)))
    category: str | None = Field(default=None, max_length=50)
    created_at: datetime = Field(default_factory=datetime.utcnow, index=True, sa_column_kwargs={"nullable": False})
    updated_at: datetime = Field(default_factory=datetime.utcnow, sa_column_kwargs={"nullable": False})
```

### Pydantic Schemas

```python
# backend/app/schemas/task.py
from pydantic import BaseModel, Field, field_validator
from uuid import UUID
from datetime import datetime
from typing import List, Literal

PriorityType = Literal["low", "medium", "high", "critical"]

class TaskCreate(BaseModel):
    """Request schema for creating a task"""
    title: str = Field(..., min_length=1, max_length=200)
    description: str | None = Field(None, max_length=1000)
    priority: PriorityType | None = None
    tags: List[str] = Field(default_factory=list)
    category: str | None = Field(None, max_length=50)

    @field_validator('title')
    def title_not_empty(cls, v):
        if not v.strip():
            raise ValueError('Title cannot be empty or whitespace')
        return v.strip()

    @field_validator('tags')
    def tags_max_length(cls, v):
        if len(v) > 10:
            raise ValueError('Maximum 10 tags allowed')
        return v

class TaskUpdate(BaseModel):
    """Request schema for updating a task (all fields optional)"""
    title: str | None = Field(None, min_length=1, max_length=200)
    description: str | None = Field(None, max_length=1000)
    completed: bool | None = None
    priority: PriorityType | None = None
    tags: List[str] | None = None
    category: str | None = Field(None, max_length=50)

class TaskRead(BaseModel):
    """Response schema for task data"""
    id: UUID
    user_id: UUID
    title: str
    description: str | None
    completed: bool
    priority: str | None
    tags: List[str]
    category: str | None
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True
```

### Validation Rules

- **title**: Required, 1-200 chars, trimmed (no leading/trailing whitespace)
- **description**: Optional, max 1000 chars
- **priority**: Optional, one of ['low', 'medium', 'high', 'critical']
- **tags**: Optional, max 10 tags per task
- **category**: Optional, max 50 chars

### State Transitions

```
                completed: false
                      ↓
      ┌───────────────────────────────┐
      │                               │
      │   click checkbox              │
      ↓                               ↓
  completed: true  ←──────────  completed: false
  (strikethrough)               (normal display)
```

### Foreign Keys

- `user_id` → `users.id` (ON DELETE CASCADE)
  - When user deleted, all their tasks are automatically deleted

---

## Entity: Session

### Purpose
Stores active user sessions for Better Auth session-based authentication.

### Table: `sessions`

### Fields

| Field | SQL Type | Constraints | Python Type | Description |
|-------|----------|-------------|-------------|-------------|
| `id` | UUID | PRIMARY KEY, NOT NULL | `uuid.UUID` | Unique session identifier |
| `user_id` | UUID | FOREIGN KEY (users.id), NOT NULL, INDEX | `uuid.UUID` | Session owner |
| `token` | VARCHAR(255) | UNIQUE, NOT NULL, INDEX | `str` | Session token (JWT or random string) |
| `expires_at` | TIMESTAMP WITH TIME ZONE | NOT NULL, INDEX | `datetime` | Session expiry timestamp (UTC) |
| `ip_address` | INET | NULLABLE | `str \| None` | Client IP address (optional) |
| `user_agent` | TEXT | NULLABLE | `str \| None` | Client User-Agent (optional) |
| `created_at` | TIMESTAMP WITH TIME ZONE | NOT NULL, DEFAULT now() | `datetime` | Session creation timestamp (UTC) |

### Indexes

```sql
CREATE TABLE sessions (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    user_id UUID NOT NULL REFERENCES users(id) ON DELETE CASCADE,
    token VARCHAR(255) UNIQUE NOT NULL,
    expires_at TIMESTAMP WITH TIME ZONE NOT NULL,
    ip_address INET,
    user_agent TEXT,
    created_at TIMESTAMP WITH TIME ZONE NOT NULL DEFAULT now()
);

CREATE UNIQUE INDEX idx_sessions_token ON sessions(token);
CREATE INDEX idx_sessions_user_id ON sessions(user_id);
CREATE INDEX idx_sessions_expires_at ON sessions(expires_at);
```

### SQLModel Definition

```python
# backend/app/models/session.py
from sqlmodel import SQLModel, Field
from uuid import UUID, uuid4
from datetime import datetime, timedelta

class Session(SQLModel, table=True):
    __tablename__ = "sessions"

    id: UUID = Field(default_factory=uuid4, primary_key=True)
    user_id: UUID = Field(foreign_key="users.id", index=True, sa_column_kwargs={"nullable": False})
    token: str = Field(max_length=255, unique=True, index=True, sa_column_kwargs={"nullable": False})
    expires_at: datetime = Field(index=True, sa_column_kwargs={"nullable": False})
    ip_address: str | None = Field(default=None)
    user_agent: str | None = Field(default=None)
    created_at: datetime = Field(default_factory=datetime.utcnow, sa_column_kwargs={"nullable": False})

    @classmethod
    def create_session(cls, user_id: UUID, token: str, remember_me: bool = False) -> "Session":
        """Factory method to create session with proper expiry"""
        expiry_days = 30 if remember_me else 7
        return cls(
            user_id=user_id,
            token=token,
            expires_at=datetime.utcnow() + timedelta(days=expiry_days),
        )
```

### Validation Rules

- **token**: Unique, secure random string or JWT
- **expires_at**: Must be future timestamp (7 or 30 days from creation)
- **Session Cleanup**: Expired sessions should be periodically deleted (background job)

### Foreign Keys

- `user_id` → `users.id` (ON DELETE CASCADE)
  - When user deleted, all their sessions are automatically deleted

---

## Entity: Account

### Purpose
Stores OAuth provider accounts linked to users (email, Google, GitHub).

### Table: `accounts`

### Fields

| Field | SQL Type | Constraints | Python Type | Description |
|-------|----------|-------------|-------------|-------------|
| `id` | UUID | PRIMARY KEY, NOT NULL | `uuid.UUID` | Unique account identifier |
| `user_id` | UUID | FOREIGN KEY (users.id), NOT NULL, INDEX | `uuid.UUID` | Account owner |
| `provider` | VARCHAR(50) | NOT NULL | `str` | OAuth provider ('email', 'google', 'github') |
| `provider_account_id` | VARCHAR(255) | NOT NULL | `str` | Provider-specific user ID |
| `access_token` | TEXT | NULLABLE | `str \| None` | Encrypted OAuth access token |
| `refresh_token` | TEXT | NULLABLE | `str \| None` | Encrypted OAuth refresh token |
| `expires_at` | TIMESTAMP WITH TIME ZONE | NULLABLE | `datetime \| None` | Token expiry timestamp (UTC) |
| `created_at` | TIMESTAMP WITH TIME ZONE | NOT NULL, DEFAULT now() | `datetime` | Account creation timestamp (UTC) |

### Indexes

```sql
CREATE TABLE accounts (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    user_id UUID NOT NULL REFERENCES users(id) ON DELETE CASCADE,
    provider VARCHAR(50) NOT NULL,
    provider_account_id VARCHAR(255) NOT NULL,
    access_token TEXT,
    refresh_token TEXT,
    expires_at TIMESTAMP WITH TIME ZONE,
    created_at TIMESTAMP WITH TIME ZONE NOT NULL DEFAULT now()
);

CREATE INDEX idx_accounts_user_id ON accounts(user_id);
CREATE UNIQUE INDEX idx_accounts_provider_account ON accounts(provider, provider_account_id);
```

### SQLModel Definition

```python
# backend/app/models/account.py
from sqlmodel import SQLModel, Field
from uuid import UUID, uuid4
from datetime import datetime

class Account(SQLModel, table=True):
    __tablename__ = "accounts"

    id: UUID = Field(default_factory=uuid4, primary_key=True)
    user_id: UUID = Field(foreign_key="users.id", index=True, sa_column_kwargs={"nullable": False})
    provider: str = Field(max_length=50, sa_column_kwargs={"nullable": False})
    provider_account_id: str = Field(max_length=255, sa_column_kwargs={"nullable": False})
    access_token: str | None = Field(default=None, sa_column=Column(Text))
    refresh_token: str | None = Field(default=None, sa_column=Column(Text))
    expires_at: datetime | None = Field(default=None)
    created_at: datetime = Field(default_factory=datetime.utcnow, sa_column_kwargs={"nullable": False})
```

### Validation Rules

- **provider**: One of ['email', 'google', 'github']
- **provider_account_id**: Required, max 255 chars
- **Unique Provider Account**: (provider, provider_account_id) must be unique
- **Token Security**: access_token and refresh_token should be encrypted at rest (Phase 3)

### Foreign Keys

- `user_id` → `users.id` (ON DELETE CASCADE)
  - When user deleted, all their OAuth accounts are automatically deleted

---

## Relationships

### One-to-Many Relationships

1. **User → Task**
   - One user owns many tasks
   - Foreign key: `tasks.user_id` → `users.id`
   - Cascade: ON DELETE CASCADE (delete tasks when user deleted)

2. **User → Session**
   - One user can have many active sessions (multi-device login)
   - Foreign key: `sessions.user_id` → `users.id`
   - Cascade: ON DELETE CASCADE (delete sessions when user deleted)

3. **User → Account**
   - One user can have multiple OAuth accounts (email + Google + GitHub)
   - Foreign key: `accounts.user_id` → `users.id`
   - Cascade: ON DELETE CASCADE (delete accounts when user deleted)

### Relationship Diagram

```
User (1) ────< (Many) Task
  │
  ├────< (Many) Session
  │
  └────< (Many) Account
```

---

## Database Migrations

### Tool
Alembic (SQLAlchemy migration tool, compatible with SQLModel)

### Migration Strategy

**Initial Schema** (`001_initial_schema.py`):
```python
def upgrade():
    # Create users table
    op.create_table(
        'users',
        sa.Column('id', sa.UUID(), primary_key=True, server_default=sa.text('gen_random_uuid()')),
        sa.Column('email', sa.String(255), unique=True, nullable=False),
        sa.Column('email_verified', sa.Boolean(), default=False, nullable=False),
        sa.Column('name', sa.String(255), nullable=True),
        sa.Column('hashed_password', sa.String(255), nullable=False),
        sa.Column('created_at', sa.TIMESTAMP(timezone=True), server_default=sa.func.now(), nullable=False),
        sa.Column('updated_at', sa.TIMESTAMP(timezone=True), server_default=sa.func.now(), nullable=False),
    )
    op.create_index('idx_users_email', 'users', ['email'])
    op.create_index('idx_users_created_at', 'users', ['created_at'])

    # Create tasks table
    op.create_table(
        'tasks',
        sa.Column('id', sa.UUID(), primary_key=True, server_default=sa.text('gen_random_uuid()')),
        sa.Column('user_id', sa.UUID(), sa.ForeignKey('users.id', ondelete='CASCADE'), nullable=False),
        sa.Column('title', sa.String(200), nullable=False),
        sa.Column('description', sa.Text(), nullable=True),
        sa.Column('completed', sa.Boolean(), default=False, nullable=False),
        sa.Column('priority', sa.String(10), nullable=True),
        sa.Column('tags', sa.ARRAY(sa.String()), server_default='{}', nullable=False),
        sa.Column('category', sa.String(50), nullable=True),
        sa.Column('created_at', sa.TIMESTAMP(timezone=True), server_default=sa.func.now(), nullable=False),
        sa.Column('updated_at', sa.TIMESTAMP(timezone=True), server_default=sa.func.now(), nullable=False),
    )
    op.create_index('idx_tasks_user_id', 'tasks', ['user_id'])
    op.create_index('idx_tasks_completed', 'tasks', ['completed'])
    op.create_index('idx_tasks_created_at', 'tasks', ['created_at'])
    op.create_index('idx_tasks_user_completed_created', 'tasks', ['user_id', 'completed', 'created_at'])

    # Add CHECK constraint for priority
    op.create_check_constraint(
        'ck_tasks_priority',
        'tasks',
        "priority IN ('low', 'medium', 'high', 'critical') OR priority IS NULL"
    )

    # Create sessions table
    op.create_table(
        'sessions',
        sa.Column('id', sa.UUID(), primary_key=True, server_default=sa.text('gen_random_uuid()')),
        sa.Column('user_id', sa.UUID(), sa.ForeignKey('users.id', ondelete='CASCADE'), nullable=False),
        sa.Column('token', sa.String(255), unique=True, nullable=False),
        sa.Column('expires_at', sa.TIMESTAMP(timezone=True), nullable=False),
        sa.Column('ip_address', sa.String(), nullable=True),
        sa.Column('user_agent', sa.Text(), nullable=True),
        sa.Column('created_at', sa.TIMESTAMP(timezone=True), server_default=sa.func.now(), nullable=False),
    )
    op.create_index('idx_sessions_token', 'sessions', ['token'], unique=True)
    op.create_index('idx_sessions_user_id', 'sessions', ['user_id'])
    op.create_index('idx_sessions_expires_at', 'sessions', ['expires_at'])

    # Create accounts table
    op.create_table(
        'accounts',
        sa.Column('id', sa.UUID(), primary_key=True, server_default=sa.text('gen_random_uuid()')),
        sa.Column('user_id', sa.UUID(), sa.ForeignKey('users.id', ondelete='CASCADE'), nullable=False),
        sa.Column('provider', sa.String(50), nullable=False),
        sa.Column('provider_account_id', sa.String(255), nullable=False),
        sa.Column('access_token', sa.Text(), nullable=True),
        sa.Column('refresh_token', sa.Text(), nullable=True),
        sa.Column('expires_at', sa.TIMESTAMP(timezone=True), nullable=True),
        sa.Column('created_at', sa.TIMESTAMP(timezone=True), server_default=sa.func.now(), nullable=False),
    )
    op.create_index('idx_accounts_user_id', 'accounts', ['user_id'])
    op.create_index('idx_accounts_provider_account', 'accounts', ['provider', 'provider_account_id'], unique=True)
```

### Migration Commands

```bash
# Create new migration (auto-generate from models)
cd backend
uv run alembic revision --autogenerate -m "Migration description"

# Apply migrations
uv run alembic upgrade head

# Rollback one migration
uv run alembic downgrade -1

# Show current migration version
uv run alembic current

# Show migration history
uv run alembic history
```

### Neon Branching Workflow

```bash
# Create dev branch for testing migrations
neon branches create --name dev --parent main

# Test migration on dev branch
export DATABASE_URL=postgresql://user:pass@ep-xxx-dev.neon.tech/db
alembic upgrade head

# If successful, merge to main
neon branches merge dev --into main

# If failed, delete dev branch and fix migration
neon branches delete dev
```

---

## Data Integrity Rules

### User Isolation (CRITICAL)
- **ALL task queries MUST filter by user_id** (no exceptions)
- Violation detection: If user A sees user B's tasks, critical security failure
- Enforcement: SQLModel relationships, FastAPI dependencies

### Cascade Deletes
When a user is deleted:
- ✅ All tasks owned by user are deleted
- ✅ All sessions for user are deleted
- ✅ All OAuth accounts for user are deleted

### Email Uniqueness
- **Case-insensitive**: "User@Example.com" == "user@example.com"
- Enforcement: Lowercase normalization before INSERT/UPDATE
- Index: UNIQUE index on email column

### Password Security
- **NEVER store plaintext passwords**
- **NEVER log passwords** (use `SecretStr` in Pydantic)
- **NEVER expose hashed_password** in API responses
- Bcrypt cost factor: 12 (adjustable if needed)

### Session Expiry
- Default: 7 days
- "Remember me": 30 days
- Expired sessions: Auto-cleanup via background job (cron or Celery)

### Timestamp Consistency
- All timestamps stored in **UTC** (no timezone offsets)
- Client-side rendering converts to user's local timezone
- Format: ISO 8601 (e.g., "2025-12-26T10:00:00Z")

---

## Performance Optimizations

### Indexes

| Table | Index Name | Columns | Purpose |
|-------|------------|---------|---------|
| users | idx_users_email | email | Unique lookup during login |
| users | idx_users_created_at | created_at | Admin queries (user growth) |
| tasks | idx_tasks_user_id | user_id | Filter tasks by owner |
| tasks | idx_tasks_completed | completed | Filter by completion status |
| tasks | idx_tasks_created_at | created_at | Sort tasks by date |
| tasks | idx_tasks_user_completed_created | user_id, completed, created_at DESC | **Most common query** |
| sessions | idx_sessions_token | token | Fast session lookup |
| sessions | idx_sessions_user_id | user_id | List user's sessions |
| sessions | idx_sessions_expires_at | expires_at | Cleanup expired sessions |
| accounts | idx_accounts_user_id | user_id | List user's OAuth accounts |
| accounts | idx_accounts_provider_account | provider, provider_account_id | Unique OAuth account lookup |

### Composite Index Rationale

```sql
CREATE INDEX idx_tasks_user_completed_created
ON tasks(user_id, completed, created_at DESC);
```

This index optimizes the most common query:
```sql
SELECT * FROM tasks
WHERE user_id = $1
  AND completed = $2
ORDER BY created_at DESC;
```

PostgreSQL can use this index for:
- Filtering by user_id (user isolation)
- Filtering by completed (show incomplete only)
- Sorting by created_at (newest first)

### Query Performance Targets

- **User lookup by email**: <10ms (unique index)
- **User's tasks list**: <20ms (composite index)
- **Single task fetch**: <5ms (primary key lookup)
- **Session validation**: <10ms (unique index on token)

---

## Schema Evolution (Future Phases)

### Phase 3 Additions (AI Chatbot)
- `tasks.due_date`: TIMESTAMP WITH TIME ZONE (optional)
- `tasks.recurrence`: JSONB (recurrence pattern)
- `tasks.reminders`: JSONB[] (reminder configurations)

### Phase 4 Additions (Kubernetes)
- `users.settings`: JSONB (user preferences)
- `tasks.assigned_to`: UUID (for team features)

### Phase 5 Additions (Cloud Deployment)
- `tasks.parent_id`: UUID (subtasks)
- `tasks.attachments`: JSONB[] (file metadata)
- Event sourcing tables (task_events, user_events)

**Migration Strategy**: Additive only (never remove columns in production)

---

## Summary

### Entities
- ✅ **4 core entities**: User, Task, Session, Account
- ✅ **3 foreign key relationships**: All with CASCADE delete
- ✅ **12 indexes**: Optimized for common queries
- ✅ **UUIDs**: All primary keys use UUID (per ADR-001)

### Constraints
- ✅ User email uniqueness (case-insensitive)
- ✅ Session token uniqueness
- ✅ OAuth account uniqueness (provider + provider_account_id)
- ✅ Priority enum validation (CHECK constraint)
- ✅ Cascade deletes on user removal

### Performance
- ✅ Composite index for main query (user_id, completed, created_at)
- ✅ Indexes on all foreign keys
- ✅ Indexes on frequently filtered columns

### Security
- ✅ No plaintext passwords
- ✅ User isolation enforced at database level
- ✅ httpOnly session cookies (not stored in DB, only metadata)

---

**Next Steps**:
1. ✅ **Data Model Complete**
2. ⏳ **Generate API Contracts** (`contracts/`)
3. ⏳ **Create Quickstart Guide** (`quickstart.md`)
4. ⏳ **Update Agent Context** (add Phase 2 technologies to `CLAUDE.md`)
5. ⏳ **Generate Tasks** (`/sp.tasks`)

---

**Status**: ✅ Complete
**Ready for**: API contract generation
