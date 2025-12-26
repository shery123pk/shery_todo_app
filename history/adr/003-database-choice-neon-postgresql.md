# ADR-003: Database Choice - Neon PostgreSQL

**Status:** Accepted
**Date:** 2025-12-26
**Deciders:** Architect (shery123pk), AI Developer (Claude)
**Related Phase:** Phase 2 - Full-Stack Web
**Supersedes:** Phase 1 JSON file persistence

---

## Context and Problem Statement

Phase 2 requires a production-ready database to replace Phase 1's JSON file storage. The database must support:
- **FastAPI Backend:** HuggingFace Spaces deployment
- **Next.js Frontend:** Vercel deployment
- **SQLModel ORM:** Type-safe database operations
- **UUID Primary Keys:** Per ADR-001
- **Free Tier:** For demo/learning project

**Key Questions:**
1. Which PostgreSQL provider (Neon, Supabase, AWS RDS, etc.)?
2. Self-hosted or managed service?
3. How to handle development vs production databases?
4. What's the migration strategy from Phase 1 JSON?

---

## Decision Drivers

### Must Have
- ✅ **PostgreSQL 14+:** Required for SQLModel, native UUID support
- ✅ **Free Tier:** Must support demo deployment without ongoing costs
- ✅ **Serverless Compatible:** Works with HuggingFace Spaces + Vercel
- ✅ **Connection Pooling:** Handle serverless function cold starts
- ✅ **Backup/Recovery:** Data safety for production

### Should Have
- 🎯 **Branching:** Git-like database branches for development
- 🎯 **Fast Cold Starts:** Minimal latency on inactive database
- 🎯 **Good DX:** Easy setup, clear documentation
- 🎯 **Migrations Support:** Alembic/SQL migration tooling

### Nice to Have
- 💡 **Scale to Zero:** Save resources when not in use
- 💡 **Auto-Scaling:** Handle traffic spikes
- 💡 **Built-in Observability:** Query analytics, slow query detection

---

## Considered Options

### Option 1: Neon PostgreSQL ✅ SELECTED

**Provider:** https://neon.tech
**Plan:** Free Tier (0.5 GB storage, 1 compute unit)

**Pros:**
- ✅ **Serverless PostgreSQL:** True pay-per-use, scales to zero
- ✅ **Database Branching:** Git-like branches for dev/staging/prod
- ✅ **Instant Provisioning:** Database ready in <10 seconds
- ✅ **Connection Pooling:** Built-in pooler for serverless
- ✅ **Autosuspend:** Pauses after inactivity, resume in <500ms
- ✅ **Free Tier:** 3 GB data transfer/month, enough for demo
- ✅ **PostgreSQL 16:** Latest features, native UUID, JSON support
- ✅ **Vercel Integration:** Official integration with Vercel deployments

**Cons:**
- ⚠️ **Cold Start:** ~500ms resume time (acceptable for demo)
- ⚠️ **Free Tier Limits:** 0.5 GB storage, 10 branches
- ⚠️ **Newer Service:** Founded 2021, less mature than AWS RDS

**Connection String:**
```
postgresql://user:password@ep-cool-name-123456.us-east-2.aws.neon.tech/neondb?sslmode=require
```

**Database Branching:**
```bash
# Create branch from main
neonctl branches create --name dev

# Result: Instant copy of production data for testing
postgresql://user:password@ep-dev-branch-789012.us-east-2.aws.neon.tech/neondb
```

### Option 2: Supabase PostgreSQL

**Provider:** https://supabase.com
**Plan:** Free Tier (500 MB database, 2 GB bandwidth)

**Pros:**
- ✅ **Full BaaS:** PostgreSQL + Auth + Storage + Realtime
- ✅ **Generous Free Tier:** More storage than Neon
- ✅ **Built-in Auth:** Could replace Better Auth
- ✅ **Realtime Subscriptions:** PostgreSQL changes as events
- ✅ **Dashboard:** Nice UI for database management

**Cons:**
- ❌ **No Auto-Suspend:** Database always running (even on free tier)
- ❌ **Constitution Conflict:** Says "Better Auth" for authentication
- ❌ **Vendor Lock-in:** Supabase-specific features (Realtime, Auth)
- ❌ **Overkill:** Don't need BaaS features for Phase 2

### Option 3: Railway PostgreSQL

**Provider:** https://railway.app
**Plan:** $5/month credit (no free tier after trial)

**Pros:**
- ✅ **Simple Deployment:** Great DX, easy to use
- ✅ **Managed Service:** Automatic backups, scaling
- ✅ **PostgreSQL 16:** Latest version

**Cons:**
- ❌ **No Free Tier:** Requires payment after trial ends
- ❌ **Always Running:** No scale-to-zero
- ❌ **Cost:** $5-20/month for demo project

### Option 4: AWS RDS PostgreSQL

**Provider:** https://aws.amazon.com/rds/
**Plan:** Free Tier (750 hours/month for 12 months)

**Pros:**
- ✅ **Industry Standard:** Mature, battle-tested
- ✅ **Free Tier:** 12 months free (750 hours)
- ✅ **Full Control:** All PostgreSQL features
- ✅ **Backup/Recovery:** Automated backups

**Cons:**
- ❌ **Complex Setup:** VPC, security groups, etc.
- ❌ **Always Running:** No scale-to-zero, wastes free tier hours
- ❌ **Overkill:** Too enterprise for demo project
- ❌ **Free Tier Limited:** Only 12 months, then expensive

### Option 5: Self-Hosted PostgreSQL (Docker)

**Provider:** Self-hosted on HuggingFace or DigitalOcean
**Plan:** Variable cost

**Pros:**
- ✅ **Full Control:** Complete ownership
- ✅ **No Vendor Lock-in:** Standard PostgreSQL
- ✅ **Cost Effective:** Can be cheap on shared hosting

**Cons:**
- ❌ **Maintenance Burden:** Backups, updates, security patches
- ❌ **No Auto-Scaling:** Manual capacity planning
- ❌ **Complexity:** Infrastructure management
- ❌ **Not Serverless:** Always running, resource waste

### Option 6: Local SQLite → Prod PostgreSQL

**Provider:** SQLite (dev) + PostgreSQL (prod)
**Plan:** Free (SQLite) + TBD (PostgreSQL)

**Pros:**
- ✅ **Simple Development:** No database server needed
- ✅ **Fast Tests:** In-memory SQLite
- ✅ **Cheap:** SQLite is free

**Cons:**
- ❌ **Different Databases:** dev/prod parity issues
- ❌ **SQLite Limitations:** No UUID type, limited concurrency
- ❌ **Migration Complexity:** Different SQL dialects
- ❌ **Not Best Practice:** Leads to production bugs

---

## Decision Outcome

**Chosen Option:** **Neon PostgreSQL** (Serverless) ✅

### Rationale

1. **Serverless Architecture:** Perfect fit for HuggingFace + Vercel serverless deployments
2. **Database Branching:** Revolutionary feature for safe development
3. **Scale to Zero:** Free tier lasts indefinitely (not just 12 months)
4. **Vercel Integration:** Official partnership, easy setup
5. **Modern DX:** Fast provisioning, great documentation

**Trade-off Accepted:** 500ms cold start is acceptable for demo project. Production apps can use reserved compute to avoid cold starts.

---

## Implementation

### Phase 2 Database Setup

**Step 1: Create Neon Project**
```bash
# Using Neon CLI
neonctl projects create --name shery-todo-app

# Or via Web UI: https://console.neon.tech
```

**Step 2: Get Connection String**
```bash
# Connection string format
DATABASE_URL="postgresql://user:password@ep-cool-name-123456.us-east-2.aws.neon.tech/neondb?sslmode=require"
```

**Step 3: Create Database Branches**
```bash
# Main branch (production)
# Automatically created with project

# Development branch
neonctl branches create --name dev --parent main

# Staging branch (optional)
neonctl branches create --name staging --parent main
```

### FastAPI Configuration

**backend/app/database.py:**
```python
from sqlmodel import create_engine, Session
import os

# Get from environment variable
DATABASE_URL = os.getenv("DATABASE_URL")

# Configure engine with pooling
engine = create_engine(
    DATABASE_URL,
    echo=True,  # SQL logging in development
    pool_pre_ping=True,  # Verify connections before use
    pool_size=5,  # Connection pool size
    max_overflow=10  # Additional connections
)

def get_session():
    with Session(engine) as session:
        yield session
```

### Environment Variables

**Production (HuggingFace Spaces):**
```bash
# Set in HuggingFace Space settings
DATABASE_URL=postgresql://user:password@ep-prod-123456.neon.tech/neondb?sslmode=require
```

**Development (.env):**
```bash
# Local .env file (git ignored)
DATABASE_URL=postgresql://user:password@ep-dev-789012.neon.tech/neondb?sslmode=require
```

### SQLModel Schema

**backend/app/models/task.py:**
```python
from sqlmodel import SQLModel, Field, Column
from sqlalchemy.dialects.postgresql import UUID, ARRAY
from uuid import UUID as UUIDType, uuid4
from datetime import datetime

class Task(SQLModel, table=True):
    """Phase 2 Task model with PostgreSQL types."""

    id: UUIDType = Field(
        default_factory=uuid4,
        sa_column=Column(UUID(as_uuid=True), primary_key=True)
    )
    title: str = Field(max_length=200, index=True)
    description: str = Field(default="", max_length=1000)
    completed: bool = Field(default=False, index=True)

    # Phase 2 additions
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)
    priority: str | None = Field(default=None, max_length=20)
    tags: list[str] = Field(default_factory=list, sa_column=Column(ARRAY(str)))
    category: str | None = Field(default=None, max_length=50)
```

### Migrations with Alembic

**Setup:**
```bash
cd backend
uv pip install alembic
alembic init migrations
```

**Create Migration:**
```bash
# Auto-generate from SQLModel
alembic revision --autogenerate -m "Create tasks table"

# Apply migration
alembic upgrade head
```

---

## Consequences

### Positive
- ✅ **Zero Infrastructure:** No database server management
- ✅ **Cost Effective:** Free tier for demo, scales with usage
- ✅ **Fast Development:** Database branching enables parallel work
- ✅ **Production Ready:** Used by companies like Vercel, Replit
- ✅ **Modern Stack:** PostgreSQL 16, native UUID, JSON, JSONB
- ✅ **Backup Safety:** Automatic daily backups, point-in-time recovery

### Negative
- ⚠️ **Cold Start Latency:** 500ms resume time after inactivity
  - **Mitigation:** Use Neon's connection pooler, set autosuspend to 5 min
- ⚠️ **Free Tier Limits:** 0.5 GB storage, 3 GB bandwidth
  - **Mitigation:** Sufficient for demo project, can upgrade if needed
- ⚠️ **Vendor Dependency:** Tied to Neon's service availability
  - **Mitigation:** Can export to standard PostgreSQL if needed

### Neutral
- 🔄 **Learning Curve:** Need to learn Neon CLI and branching workflow
  - **Acceptable:** Good investment for modern database practices

---

## Migration Strategy

### Phase 1 → Phase 2 Data Migration

**Option A: Automated Script (Recommended)**
```python
# backend/scripts/migrate_phase1_to_phase2.py
import json
from pathlib import Path
from uuid import uuid4
from sqlmodel import Session, select
from app.database import engine
from app.models.task import Task

def migrate():
    """Migrate Phase 1 JSON to Phase 2 PostgreSQL."""
    # Read Phase 1 data
    phase1_file = Path("../cli/tasks.json")
    if not phase1_file.exists():
        print("No Phase 1 data found, skipping migration")
        return

    data = json.loads(phase1_file.read_text())

    # Transform and insert
    with Session(engine) as session:
        for old_task in data["tasks"]:
            new_task = Task(
                id=uuid4(),  # Generate new UUID
                title=old_task["title"],
                description=old_task["description"],
                completed=old_task["completed"]
            )
            session.add(new_task)
        session.commit()
        print(f"Migrated {len(data['tasks'])} tasks from Phase 1")

if __name__ == "__main__":
    migrate()
```

**Option B: Manual CSV Import**
1. Export Phase 1 to CSV
2. Use `psql` COPY command to import
3. Less code, but more manual

---

## Deployment Configuration

### HuggingFace Spaces

**backend/Dockerfile:**
```dockerfile
FROM python:3.13-slim

WORKDIR /app
COPY backend/ /app/

# Install dependencies
RUN pip install -e .

# Run migrations on startup
CMD alembic upgrade head && uvicorn app.main:app --host 0.0.0.0 --port 7860
```

**Environment Variable:**
- Set `DATABASE_URL` in HuggingFace Space settings

### Vercel (Frontend)

**No direct database access from frontend.**
Frontend calls backend API which handles database operations.

### Local Development

**docker-compose.yml:**
```yaml
services:
  # Option 1: Use Neon dev branch (recommended)
  backend:
    environment:
      DATABASE_URL: postgresql://...@ep-dev-branch.neon.tech/neondb

  # Option 2: Local PostgreSQL (for offline dev)
  db:
    image: postgres:16-alpine
    environment:
      POSTGRES_USER: todo_user
      POSTGRES_PASSWORD: todo_password
      POSTGRES_DB: todo_db
    ports: ["5432:5432"]
```

---

## Monitoring & Observability

### Neon Console

- **Metrics:** Query performance, storage usage, connections
- **Logs:** SQL query logs, slow query detection
- **Branching:** Visualize branch relationships

### FastAPI Logging

```python
# Log all SQL queries in development
engine = create_engine(
    DATABASE_URL,
    echo=True,  # SQL query logging
    echo_pool=True  # Connection pool logging
)
```

---

## Security

### Connection Security

- **SSL Required:** `?sslmode=require` in connection string
- **IAM Roles:** Can use Neon's role-based access control
- **IP Allowlist:** Can restrict connections to specific IPs

### Secrets Management

**Never commit credentials!**
```bash
# .env (git ignored)
DATABASE_URL=postgresql://...

# HuggingFace Space settings (encrypted)
DATABASE_URL=postgresql://...

# Vercel environment variables (encrypted)
# Not needed - frontend doesn't access DB directly
```

---

## Cost Analysis

### Neon Free Tier

- **Storage:** 0.5 GB (plenty for demo with ~10K tasks)
- **Compute:** 0.25 Compute Unit (shared, auto-suspend)
- **Bandwidth:** 3 GB/month (HTTP API traffic)
- **Branches:** 10 branches max

**Estimated Usage for Demo:**
- Storage: ~50 MB (1000 tasks)
- Bandwidth: <500 MB/month (API calls)
- **Cost: $0/month** ✅

### Upgrade Path (if needed)

- **Pro Plan:** $19/month
  - 10 GB storage
  - 100 GB bandwidth
  - Unlimited branches
  - Dedicated compute

---

## Alternatives Rejected

### Why Not Supabase?

- Violates constitution (Better Auth mandate)
- Vendor lock-in with Supabase-specific features
- Always-on database (not serverless)

### Why Not AWS RDS?

- Complex setup (VPC, security groups)
- Overkill for demo project
- Free tier limited to 12 months

### Why Not Self-Hosted?

- Maintenance burden
- Not serverless architecture
- Complexity outweighs benefits

---

## References

- **Neon Docs:** https://neon.tech/docs
- **Neon + Vercel:** https://neon.tech/docs/guides/vercel
- **SQLModel Docs:** https://sqlmodel.tiangolo.com/
- **Alembic Docs:** https://alembic.sqlalchemy.org/
- **PostgreSQL UUID:** https://www.postgresql.org/docs/current/datatype-uuid.html

---

## Related ADRs

- **ADR-001:** ID Migration Strategy (requires UUID support)
- **ADR-002:** Monorepo Structure (database in /backend directory)
- **ADR-004:** Auth Strategy (Better Auth will use this database)
- **Future ADR:** Phase 3 - Caching strategy (may add Redis)

---

**Decision Made By:** Architect + AI Developer
**Date Approved:** 2025-12-26
**Implementation Status:** 📋 Planned for Phase 2
**Review Date:** After Phase 2 deployment (validate performance/costs)
