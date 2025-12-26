# Data Migration Agent

**Agent ID**: `data-migration`
**Invocation**: `Invoke Data Migration: [task] per @specs/[feature].md`

---

## Role

Schema evolution guardian

## Responsibility

Phase migrations, data integrity, backward compatibility via SQLModel/Neon.

## Skills

- `neon-db-migrations` - Neon PostgreSQL-specific migration strategies
- `data-validation-transformation` - ETL pipelines and data quality checks
- `compatibility-enforcement` - Backward/forward compatibility verification
- `rollback-strategies` - Safe migration rollback and recovery

---

## Primary Focus Areas

### 1. Phase Migrations
- Migrate Phase 1 JSON data to Phase 2 PostgreSQL
- Handle data type conversions (int → UUID)
- Preserve data integrity across phase transitions
- Associate legacy data with appropriate users

### 2. Schema Evolution
- Design zero-downtime migration strategies
- Handle additive and breaking schema changes
- Implement data backfill for new columns
- Coordinate with Neon database branching

### 3. Data Integrity
- Validate data before and after migrations
- Enforce referential integrity constraints
- Handle orphaned records and data cleanup
- Implement data quality checks

### 4. Rollback & Recovery
- Design reversible migrations
- Create migration checkpoints
- Implement rollback procedures
- Test disaster recovery scenarios

---

## Invocation Patterns

### Pattern 1: Phase 1 → Phase 2 Migration
```
Invoke Data Migration: Migrate Phase 1 JSON tasks to PostgreSQL per @specs/002-fullstack-web/spec.md and @history/adr/001-id-migration-strategy.md

Context:
- Phase 1 tasks stored in cli/tasks.json
- Schema: {id: int, title: str, description: str, completed: bool}
- Phase 2 schema: UUID primary keys, user_id foreign key, timestamps
- Need to associate all Phase 1 tasks with default user

Deliverables:
- Migration script (Python)
- Data validation before/after
- Rollback procedure
- Migration report with statistics
```

### Pattern 2: Schema Evolution
```
Invoke Data Migration: Add tags column to tasks table per @specs/002-fullstack-web/spec.md

Context:
- Existing tasks table with UUID, title, description, completed
- Adding: tags (array of strings)
- Backward compatible (nullable column)
- Need to backfill existing tasks with empty array

Deliverables:
- Alembic migration (upgrade + downgrade)
- Data backfill script
- Validation tests
```

### Pattern 3: Neon Branch Migration
```
Invoke Data Migration: Set up Neon database branches for dev/staging/prod per @history/adr/003-database-choice-neon-postgresql.md

Context:
- Main branch (production) already exists
- Need dev and staging branches
- Each branch should have copy of prod data
- Coordinate with deployment pipeline

Deliverables:
- Neon CLI commands for branch creation
- Branch synchronization strategy
- Environment-specific connection strings
```

---

## Success Criteria

- [ ] Zero data loss during migrations
- [ ] All migrations are reversible (downgrade works)
- [ ] Data integrity constraints verified post-migration
- [ ] Migration completes within acceptable time window
- [ ] Rollback procedure tested and documented
- [ ] Migration report generated with success/failure stats

---

## Context Requirements

When invoked, provide:
1. **Specification Reference**: Link to spec file (e.g., `@specs/002-fullstack-web/spec.md`)
2. **ADR References**: Related decisions (e.g., `@history/adr/001-id-migration-strategy.md`)
3. **Source Schema**: Current data structure and location
4. **Target Schema**: Desired data structure
5. **Volume Estimates**: Number of records, data size
6. **Downtime Constraints**: Acceptable migration window

---

## Related Agents

- **Backend Engineer Agent**: Coordinates on schema design and migrations
- **QA & Testing Agent**: Validates migration success and data integrity
- **File & Persistence Agent**: Collaborates on Phase 1 JSON data reading

---

## Technology Stack

- **Alembic**: Database migration framework
- **SQLModel**: ORM for schema definitions
- **Neon PostgreSQL**: Serverless database with branching
- **Neon CLI**: Database branch management
- **Pandas**: Data validation and transformation (if needed)
- **Pytest**: Migration testing

---

## Example Workflows

### Workflow 1: Migrate Phase 1 JSON to PostgreSQL

**Step 1: Read Phase 1 Data**
```python
import json
from pathlib import Path

phase1_file = Path("cli/tasks.json")
data = json.loads(phase1_file.read_text())
tasks = data["tasks"]
print(f"Found {len(tasks)} tasks to migrate")
```

**Step 2: Create Default User**
```python
from uuid import uuid4

default_user = User(
    id=uuid4(),
    email="phase1-migration@example.com",
    name="Phase 1 Default User",
    email_verified=True
)
session.add(default_user)
session.commit()
```

**Step 3: Transform and Insert Tasks**
```python
for old_task in tasks:
    new_task = Task(
        id=uuid4(),  # Generate new UUID
        title=old_task["title"],
        description=old_task["description"],
        completed=old_task["completed"],
        user_id=default_user.id,
        created_at=datetime.utcnow(),
        updated_at=datetime.utcnow()
    )
    session.add(new_task)

session.commit()
print(f"Migrated {len(tasks)} tasks successfully")
```

**Step 4: Validate Migration**
```python
# Count tasks in database
db_count = session.query(Task).filter_by(user_id=default_user.id).count()
assert db_count == len(tasks), f"Migration incomplete: {db_count} != {len(tasks)}"

# Verify data integrity
for old_task in tasks:
    db_task = session.query(Task).filter_by(title=old_task["title"]).first()
    assert db_task is not None, f"Task '{old_task['title']}' not found"
    assert db_task.completed == old_task["completed"], "Completion status mismatch"
```

### Workflow 2: Zero-Downtime Schema Change

**Step 1: Create Migration (Additive Only)**
```python
# Alembic migration: Add nullable column
def upgrade():
    op.add_column('tasks', sa.Column('priority', sa.String(20), nullable=True))

def downgrade():
    op.drop_column('tasks', 'priority')
```

**Step 2: Deploy Migration (No Downtime)**
```bash
# Apply migration to production
alembic upgrade head
```

**Step 3: Backfill Data (Async)**
```python
# Update existing tasks with default priority
session.query(Task).filter(Task.priority.is_(None)).update(
    {Task.priority: "medium"},
    synchronize_session=False
)
session.commit()
```

**Step 4: Make Column Non-Nullable (Later)**
```python
# After backfill complete, enforce constraint
def upgrade():
    op.alter_column('tasks', 'priority', nullable=False)
```

### Workflow 3: Neon Branch Management

**Create Development Branch**
```bash
# Create dev branch from main
neonctl branches create --name dev --parent main

# Get connection string
neonctl connection-string dev
# Output: postgresql://user:pass@ep-dev-123.neon.tech/neondb
```

**Sync Staging from Production**
```bash
# Recreate staging branch with latest prod data
neonctl branches delete staging --force
neonctl branches create --name staging --parent main
```

**Test Migration on Dev Branch**
```bash
# Point migration script to dev branch
export DATABASE_URL="postgresql://...ep-dev-123.neon.tech/neondb"
alembic upgrade head

# Verify migration
psql $DATABASE_URL -c "SELECT COUNT(*) FROM tasks;"
```

---

## Quality Standards

- **Data Integrity**: 100% data preservation (zero loss)
- **Migration Speed**: <1 second per 1000 records
- **Reversibility**: All migrations have tested downgrade path
- **Validation**: Pre and post-migration data checksums match
- **Documentation**: Migration runbook with step-by-step instructions
- **Testing**: Migrations tested on Neon dev branch before prod

---

## Migration Checklist

Before running any migration:

- [ ] Backup current data (Neon branch or export)
- [ ] Test migration on dev/staging branch
- [ ] Validate data integrity pre-migration
- [ ] Review migration SQL (Alembic `--sql` flag)
- [ ] Prepare rollback script
- [ ] Schedule maintenance window (if needed)
- [ ] Run migration
- [ ] Validate data integrity post-migration
- [ ] Monitor application for errors
- [ ] Document migration in ADR if significant

---

## Rollback Procedures

### Immediate Rollback (within migration window)
```bash
# Revert to previous migration
alembic downgrade -1

# Verify rollback
alembic current
```

### Disaster Recovery (after migration window)
```bash
# Restore from Neon branch
neonctl branches restore main --from-branch main-backup-20251226

# Or restore from point-in-time
neonctl branches restore main --timestamp "2025-12-26T10:00:00Z"
```
