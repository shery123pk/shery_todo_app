# Quickstart: Phase 2 Full-Stack Web Application

**Feature**: 002-fullstack-web
**Time to Setup**: ~5 minutes
**Prerequisites**: Python 3.13+, Node.js 20+, Docker, UV
**Date**: 2025-12-26

---

## Quick Start (3 Commands)

```bash
# 1. Start services
docker-compose up -d

# 2. Run migrations
cd backend && uv run alembic upgrade head

# 3. Open browser
# Frontend: http://localhost:3000
# Backend API Docs: http://localhost:8000/docs
```

---

## Prerequisites

Install these before starting:

- **Python 3.13+**: [Download](https://www.python.org/downloads/)
- **Node.js 20+**: [Download](https://nodejs.org/)
- **Docker & Docker Compose**: [Download](https://www.docker.com/get-started)
- **UV** (Python package manager): `pip install uv`
- **Git**: [Download](https://git-scm.com/)

Verify installations:
```bash
python --version   # Should be 3.13+
node --version     # Should be 20+
docker --version   # Should be 20+
uv --version      # Should be latest
```

---

## Local Development Setup

### 1. Clone Repository

```bash
git clone <repo-url>
cd shery_todo_app
git checkout 002-fullstack-web  # Or main if already merged
```

### 2. Environment Variables

**Backend** - Create `backend/.env`:
```bash
DATABASE_URL=postgresql://todo_user:todo_pass@localhost:5432/todo_db
BETTER_AUTH_SECRET=dev-secret-key-change-in-production-min-32-chars
BETTER_AUTH_URL=http://localhost:8000
FRONTEND_URL=http://localhost:3000
DEBUG=true
```

**Frontend** - Create `frontend/.env.local`:
```bash
NEXT_PUBLIC_API_URL=http://localhost:8000
BETTER_AUTH_URL=http://localhost:8000
BETTER_AUTH_SECRET=dev-secret-key-change-in-production-min-32-chars
```

**Copy from examples**:
```bash
cp backend/.env.example backend/.env
cp frontend/.env.local.example frontend/.env.local
```

### 3. Start Services with Docker Compose

```bash
# Start all services (backend, frontend, postgres)
docker-compose up -d

# Check services are running
docker-compose ps

# Expected output:
# NAME                COMMAND                  SERVICE    STATUS
# postgres            "docker-entrypoint.s…"   postgres   Up (healthy)
# backend             "uvicorn app.main:ap…"   backend    Up
# frontend            "npm run dev"            frontend   Up
```

**Services**:
- **PostgreSQL**: `localhost:5432` (database)
- **Backend**: `localhost:8000` (FastAPI)
- **Frontend**: `localhost:3000` (Next.js)

### 4. Run Database Migrations

```bash
cd backend
uv run alembic upgrade head
```

Expected output:
```
INFO  [alembic.runtime.migration] Running upgrade  -> 001_initial_schema, Initial schema
INFO  [alembic.runtime.migration] Running stamp_revision  -> 001_initial_schema
```

### 5. Verify Setup

**Backend Health Check**:
```bash
curl http://localhost:8000/health
# Expected: {"status":"healthy","service":"todo-backend"}
```

**Backend API Docs**:
- Open: http://localhost:8000/docs
- Should see Swagger UI with all endpoints

**Frontend**:
- Open: http://localhost:3000
- Should see landing page with "Sign Up" button

### 6. Create First User

**Option A: Via Frontend UI**
1. Navigate to http://localhost:3000/auth/signup
2. Enter email: `test@example.com`
3. Enter password: `testpass123`
4. Click "Sign Up"
5. Login at http://localhost:3000/auth/signin
6. Create your first task!

**Option B: Via API (curl)**
```bash
# 1. Sign up
curl -X POST http://localhost:8000/api/auth/signup \
  -H "Content-Type: application/json" \
  -d '{
    "email": "test@example.com",
    "password": "testpass123",
    "name": "Test User"
  }'

# 2. Sign in
curl -X POST http://localhost:8000/api/auth/signin \
  -H "Content-Type: application/json" \
  -c cookies.txt \
  -d '{
    "email": "test@example.com",
    "password": "testpass123"
  }'

# 3. Create task
curl -X POST http://localhost:8000/api/tasks \
  -H "Content-Type: application/json" \
  -b cookies.txt \
  -d '{
    "title": "My first task",
    "description": "Hello from Phase 2!"
  }'

# 4. List tasks
curl -X GET http://localhost:8000/api/tasks \
  -b cookies.txt
```

---

## Running Tests

### Backend Tests (pytest)

```bash
cd backend

# Run all tests
uv run pytest -v

# Run with coverage
uv run pytest --cov --cov-report=term-missing

# Run specific test file
uv run pytest tests/integration/test_auth.py -v

# Run specific test
uv run pytest tests/integration/test_auth.py::test_signup_success -v
```

**Expected**:
- All tests passing
- Coverage ≥80%

### Frontend Tests (Vitest)

```bash
cd frontend

# Run all tests
npm test

# Run with coverage
npm test -- --coverage

# Run in watch mode
npm test -- --watch

# Run specific test file
npm test -- src/components/__tests__/TaskCard.test.tsx
```

### E2E Tests (Playwright)

```bash
cd frontend

# Install Playwright browsers (first time only)
npx playwright install

# Run E2E tests (requires services running)
npx playwright test

# Run E2E tests with UI
npx playwright test --ui

# Run specific test
npx playwright test e2e/auth.spec.ts

# View test report
npx playwright show-report
```

**Prerequisites for E2E**:
- Backend must be running on `localhost:8000`
- Frontend must be running on `localhost:3000`

---

## Development Workflow

### Backend Development

**File Structure**:
```
backend/
├── app/
│   ├── main.py           # FastAPI app
│   ├── routers/          # API endpoints
│   ├── models/           # SQLModel entities
│   ├── schemas/          # Pydantic models
│   └── dependencies.py   # Dependency injection
├── alembic/              # Database migrations
└── tests/                # Test suite
```

**Common Commands**:
```bash
cd backend

# Start dev server (with hot reload)
uv run uvicorn app.main:app --reload --port 8000

# Create new migration
uv run alembic revision --autogenerate -m "Add new field"

# Apply migrations
uv run alembic upgrade head

# Rollback migration
uv run alembic downgrade -1

# Type check
uv run pyright

# Lint
uv run ruff check .

# Format
uv run ruff format .
```

### Frontend Development

**File Structure**:
```
frontend/
├── app/                  # Next.js App Router
│   ├── tasks/            # Tasks page (protected)
│   └── auth/             # Auth pages (public)
├── components/           # React components
├── lib/                  # Utilities (API client, auth)
└── __tests__/            # Test suite
```

**Common Commands**:
```bash
cd frontend

# Start dev server (with hot reload)
npm run dev

# Build for production
npm run build

# Start production server
npm start

# Type check
npm run type-check

# Lint
npm run lint

# Format
npm run format
```

---

## Production Deployment

### Backend (Hugging Face Spaces)

**Prerequisites**:
- Hugging Face account
- Neon PostgreSQL database (production branch)

**Steps**:
1. Create new Space:
   - Go to https://huggingface.co/spaces
   - Click "Create new Space"
   - Select "Docker" SDK
   - Name: `todo-backend`

2. Upload files:
   - Upload `backend/Dockerfile`
   - Upload `backend/` directory
   - Click "Commit to main"

3. Set Secrets (Settings → Repository secrets):
   ```
   DATABASE_URL=postgresql://user:pass@ep-xxx.pooler.neon.tech/db?sslmode=require
   BETTER_AUTH_SECRET=<random-32-char-string>
   BETTER_AUTH_URL=https://[username]-todo-backend.hf.space
   FRONTEND_URL=https://[your-app].vercel.app
   ```

4. Verify deployment:
   - URL: `https://[username]-todo-backend.hf.space`
   - API Docs: `https://[username]-todo-backend.hf.space/docs`

**CRITICAL**: Backend MUST listen on port 7860 (HF Spaces requirement).

Verify Dockerfile has:
```dockerfile
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "7860"]
```

### Frontend (Vercel)

**Prerequisites**:
- Vercel account
- GitHub repository

**Steps**:
1. Import project:
   - Go to https://vercel.com/new
   - Select your GitHub repository
   - Framework: Next.js (auto-detected)

2. Configure build:
   - Root Directory: `frontend`
   - Build Command: `npm run build`
   - Output Directory: `.next`

3. Set Environment Variables:
   ```
   NEXT_PUBLIC_API_URL=https://[username]-todo-backend.hf.space
   BETTER_AUTH_URL=https://[username]-todo-backend.hf.space
   BETTER_AUTH_SECRET=<same-as-backend>
   ```

4. Deploy:
   - Click "Deploy"
   - Vercel auto-deploys on every push to main

5. Verify deployment:
   - URL: `https://[your-app].vercel.app`

### Database (Neon)

**Prerequisites**:
- Neon account

**Steps**:
1. Create project:
   - Go to https://neon.tech
   - Click "Create Project"
   - Name: `todo-app`
   - Region: Select closest to your users

2. Create branches:
   ```bash
   # Install Neon CLI
   npm install -g neonctl

   # Create branches
   neon branches create --name dev
   neon branches create --name staging
   neon branches create --name main
   ```

3. Get connection strings:
   ```bash
   # Production (main branch)
   neon connection-string main

   # Staging
   neon connection-string staging

   # Dev
   neon connection-string dev
   ```

4. Update environment variables in HF Spaces and Vercel with production connection string.

---

## Troubleshooting

### Issue: Backend fails to connect to database

**Symptoms**:
```
sqlalchemy.exc.OperationalError: could not connect to server
```

**Solutions**:
1. Verify PostgreSQL is running:
   ```bash
   docker-compose ps postgres
   ```

2. Check DATABASE_URL in `backend/.env`:
   ```bash
   cat backend/.env | grep DATABASE_URL
   ```

3. Test connection:
   ```bash
   psql postgresql://todo_user:todo_pass@localhost:5432/todo_db
   ```

### Issue: Frontend shows CORS error

**Symptoms**:
```
Access to fetch at 'http://localhost:8000/api/tasks' from origin 'http://localhost:3000' has been blocked by CORS policy
```

**Solutions**:
1. Verify FRONTEND_URL in `backend/.env`:
   ```bash
   cat backend/.env | grep FRONTEND_URL
   # Should be: FRONTEND_URL=http://localhost:3000
   ```

2. Check FastAPI CORS middleware in `backend/app/main.py`:
   ```python
   app.add_middleware(
       CORSMiddleware,
       allow_origins=[frontend_url],
       allow_credentials=True,
       # ...
   )
   ```

3. Restart backend:
   ```bash
   docker-compose restart backend
   ```

### Issue: HF Spaces backend stuck on port 8000

**Symptoms**:
- HF Space shows "Application Error"
- Logs show: `Uvicorn running on http://0.0.0.0:8000`

**Solution**:
Update Dockerfile CMD to use port 7860:
```dockerfile
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "7860"]
```

### Issue: Neon connection timeout

**Symptoms**:
```
psycopg2.OperationalError: timeout expired
```

**Solutions**:
1. Use Neon Pooler (not direct connection):
   ```
   # Bad: postgresql://user:pass@ep-xxx.neon.tech/db
   # Good: postgresql://user:pass@ep-xxx.pooler.neon.tech/db
   ```

2. Add connection timeout:
   ```
   DATABASE_URL=postgresql://...?connect_timeout=10
   ```

3. Verify SSL is required:
   ```
   DATABASE_URL=postgresql://...?sslmode=require
   ```

### Issue: Phase 1 CLI tests failing

**Symptoms**:
```bash
cd cli && uv run pytest
# Some tests fail
```

**Solution**:
Phase 1 should remain independent. Verify:
1. CLI uses `cli/tasks.json` (not PostgreSQL)
2. No imports from `backend/` or `frontend/`
3. Run tests:
   ```bash
   cd cli
   uv run pytest -v
   # All 81 tests should pass
   ```

### Issue: Migration fails with "relation already exists"

**Symptoms**:
```
alembic.util.exc.CommandError: Can't locate revision identified by '...'
```

**Solution**:
1. Check current migration version:
   ```bash
   uv run alembic current
   ```

2. If database is ahead of migrations:
   ```bash
   # Option A: Stamp current version
   uv run alembic stamp head

   # Option B: Drop database and recreate
   docker-compose down -v
   docker-compose up -d
   uv run alembic upgrade head
   ```

---

## Common Commands Reference

### Docker Compose

```bash
# Start all services
docker-compose up -d

# Stop all services
docker-compose down

# Stop and remove volumes (clean slate)
docker-compose down -v

# View logs
docker-compose logs -f

# View logs for specific service
docker-compose logs -f backend

# Restart specific service
docker-compose restart backend

# Rebuild service
docker-compose up -d --build backend
```

### Database

```bash
# Connect to PostgreSQL (local)
psql postgresql://todo_user:todo_pass@localhost:5432/todo_db

# Connect to Neon (production)
psql postgresql://user:pass@ep-xxx.pooler.neon.tech/db?sslmode=require

# List tables
\dt

# Describe table
\d users
\d tasks

# Query
SELECT * FROM users;
SELECT * FROM tasks WHERE user_id = '...';

# Exit
\q
```

### Git

```bash
# Create feature branch
git checkout -b 002-fullstack-web

# Stage changes
git add .

# Commit
git commit -m "feat: implement task CRUD API"

# Push
git push origin 002-fullstack-web

# Create pull request (via GitHub CLI)
gh pr create --title "Phase 2: Full-Stack Web" --body "Implements task CRUD, auth, and web UI"
```

---

## Next Steps

After completing local setup:

1. ✅ **Run all tests** → Ensure 100% pass rate
2. ✅ **Deploy to staging** → Test on HF Spaces + Vercel preview
3. ✅ **Run E2E tests on staging** → Validate deployment
4. ✅ **Deploy to production** → Merge to main, auto-deploy
5. ✅ **Verify Phase 1 CLI** → Run `cd cli && uv run pytest`

**Related Documentation**:
- [Plan](./plan.md) - Implementation plan
- [Data Model](./data-model.md) - Database schema
- [Auth API](./contracts/auth.md) - Authentication endpoints
- [Tasks API](./contracts/tasks.md) - Task CRUD endpoints

---

**Status**: ✅ Complete
**Questions?**: Check [troubleshooting](#troubleshooting) or ask in project docs
