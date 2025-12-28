# Quickstart Guide: Project Management System

**Feature**: 001-project-management-system
**Date**: 2025-12-27
**Prerequisites**: Python 3.13+, Node.js 18+, PostgreSQL 15+ (or Neon account)

---

## Overview

This guide helps you set up the development environment for the multi-tenant project management system. The system consists of:
- **Backend**: FastAPI (Python 3.13+) with SQLModel ORM
- **Frontend**: Next.js 15 (TypeScript) with Tailwind CSS
- **Database**: Neon PostgreSQL (serverless) or local PostgreSQL
- **Auth**: Better Auth with JWT tokens in HttpOnly cookies

---

## Prerequisites

### Required Software

1. **Python 3.13+** with **UV** package manager
   ```bash
   # Install UV (Python package manager)
   curl -LsSf https://astral.sh/uv/install.sh | sh

   # Verify installation
   uv --version
   ```

2. **Node.js 18+** with npm/pnpm
   ```bash
   # Verify installation
   node --version
   npm --version
   ```

3. **PostgreSQL 15+** (local) OR **Neon account** (recommended for MVP)
   - Neon: Sign up at https://neon.tech (free tier available)
   - Local PostgreSQL: Download from https://www.postgresql.org/download/

4. **Git**
   ```bash
   git --version
   ```

---

## Project Setup

### 1. Clone Repository

```bash
git clone https://github.com/your-org/project-management-system.git
cd project-management-system

# Checkout feature branch
git checkout 001-project-management-system
```

---

### 2. Backend Setup

#### Step 1: Navigate to Backend Directory

```bash
cd backend
```

#### Step 2: Install Dependencies

```bash
# Create virtual environment and install dependencies with UV
uv venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate

# Install dependencies
uv pip install -r requirements.txt
```

#### Step 3: Create Environment File

```bash
cp .env.example .env
```

Edit `.env` with your configuration:

```env
# Database (Neon PostgreSQL)
DATABASE_URL=postgresql+asyncpg://user:password@host.neon.tech/dbname?sslmode=require

# JWT Secret (generate with: openssl rand -hex 32)
JWT_SECRET=your-secret-key-here-change-in-production

# Frontend URL (for CORS)
FRONTEND_URL=http://localhost:3000
ALLOWED_ORIGINS=http://localhost:3000,http://localhost:3004

# Email Service (SendGrid or SMTP)
SMTP_HOST=smtp.sendgrid.net
SMTP_PORT=587
SMTP_USERNAME=apikey
SMTP_PASSWORD=your-sendgrid-api-key
FROM_EMAIL=noreply@example.com

# Environment
ENVIRONMENT=development

# File Upload
MAX_FILE_SIZE_MB=10
UPLOAD_DIR=./uploads
```

#### Step 4: Initialize Database

```bash
# Run migrations (creates all tables)
alembic upgrade head

# Optional: Seed with sample data
uv run python scripts/seed_data.py
```

#### Step 5: Start Backend Server

```bash
# Development mode with auto-reload
uv run uvicorn app.main:app --reload --port 8000

# Server runs at: http://localhost:8000
# API docs: http://localhost:8000/docs (Swagger UI)
# Alternative docs: http://localhost:8000/redoc (ReDoc)
```

---

### 3. Frontend Setup

#### Step 1: Navigate to Frontend Directory

```bash
cd ../frontend
```

#### Step 2: Install Dependencies

```bash
# Using npm
npm install

# OR using pnpm (faster)
pnpm install
```

#### Step 3: Create Environment File

```bash
cp .env.example .env.local
```

Edit `.env.local`:

```env
NEXT_PUBLIC_API_URL=http://localhost:8000
```

#### Step 4: Start Frontend Development Server

```bash
# Development mode with hot reload
npm run dev

# OR
pnpm dev

# Server runs at: http://localhost:3000
# Auto-opens in browser
```

---

## Development Workflow

### Running Both Servers Concurrently

Option 1: Use separate terminals

```bash
# Terminal 1: Backend
cd backend
uv run uvicorn app.main:app --reload --port 8000

# Terminal 2: Frontend
cd frontend
npm run dev
```

Option 2: Use `docker-compose` (if configured)

```bash
docker-compose up
```

---

## Database Migrations

### Create New Migration

After modifying SQLModel models:

```bash
cd backend

# Auto-generate migration from model changes
alembic revision --autogenerate -m "Add new column to tasks table"

# Review the generated migration in alembic/versions/

# Apply migration
alembic upgrade head
```

### Rollback Migration

```bash
# Rollback one migration
alembic downgrade -1

# Rollback to specific revision
alembic downgrade <revision_id>

# Rollback all migrations
alembic downgrade base
```

---

## Running Tests

### Backend Tests

```bash
cd backend

# Run all tests
uv run pytest

# Run with coverage report
uv run pytest --cov=app --cov-report=html

# Run specific test file
uv run pytest tests/test_auth.py

# Run tests matching pattern
uv run pytest -k "test_create_task"

# View coverage report
open htmlcov/index.html
```

### Frontend Tests

```bash
cd frontend

# Run unit/component tests (Vitest)
npm run test

# Run tests in watch mode
npm run test:watch

# Run E2E tests (Playwright)
npm run test:e2e

# View test coverage
npm run test:coverage
```

---

## API Testing

### Using Swagger UI

1. Open http://localhost:8000/docs
2. Click "Authorize" button
3. Signup and signin to get session cookie
4. Test endpoints interactively

### Using cURL

```bash
# Signup
curl -X POST http://localhost:8000/api/auth/signup \
  -H "Content-Type: application/json" \
  -d '{
    "email": "test@example.com",
    "password": "SecurePass123!",
    "full_name": "Test User"
  }'

# Signin (saves cookies to file)
curl -X POST http://localhost:8000/api/auth/signin \
  -H "Content-Type: application/json" \
  -c cookies.txt \
  -d '{
    "email": "test@example.com",
    "password": "SecurePass123!"
  }'

# Get current user (using saved cookies)
curl -X GET http://localhost:8000/api/auth/me \
  -b cookies.txt

# Create organization
curl -X POST http://localhost:8000/api/organizations \
  -H "Content-Type: application/json" \
  -b cookies.txt \
  -d '{
    "slug": "my-org",
    "name": "My Organization"
  }'
```

### Using Postman/Insomnia

1. Import API contracts from `specs/001-project-management-system/contracts/`
2. Create environment with `base_url=http://localhost:8000`
3. Use cookie-based authentication (enable "Send cookies" in settings)

---

## Code Quality Tools

### Backend Linting & Formatting

```bash
cd backend

# Format code with Ruff
uv run ruff format .

# Lint code
uv run ruff check .

# Fix auto-fixable linting issues
uv run ruff check --fix .

# Type checking with Pyright
uv run pyright
```

### Frontend Linting & Formatting

```bash
cd frontend

# Format code with Prettier
npm run format

# Lint code with ESLint
npm run lint

# Fix auto-fixable linting issues
npm run lint:fix

# Type checking
npm run type-check
```

---

## Debugging

### Backend Debugging

#### VS Code Configuration (`.vscode/launch.json`)

```json
{
  "version": "0.2.0",
  "configurations": [
    {
      "name": "FastAPI Backend",
      "type": "python",
      "request": "launch",
      "module": "uvicorn",
      "args": ["app.main:app", "--reload"],
      "cwd": "${workspaceFolder}/backend",
      "env": {
        "PYTHONPATH": "${workspaceFolder}/backend"
      }
    }
  ]
}
```

#### Python Debugger (pdb)

```python
# Add breakpoint in code
import pdb; pdb.set_trace()

# Or use built-in breakpoint()
breakpoint()
```

### Frontend Debugging

#### Browser DevTools

- Chrome/Edge: F12 → Sources → Set breakpoints
- Network tab: Inspect API calls
- React DevTools: Install extension for component inspection

#### VS Code Configuration

```json
{
  "version": "0.2.0",
  "configurations": [
    {
      "name": "Next.js Frontend",
      "type": "node",
      "request": "launch",
      "runtimeExecutable": "npm",
      "runtimeArgs": ["run", "dev"],
      "cwd": "${workspaceFolder}/frontend",
      "console": "integratedTerminal"
    }
  ]
}
```

---

## Common Issues & Solutions

### Issue: `alembic upgrade head` fails with "relation already exists"

**Solution**: Database has stale schema. Drop and recreate:

```bash
# WARNING: Destroys all data
psql -d your_database -c "DROP SCHEMA public CASCADE; CREATE SCHEMA public;"
alembic upgrade head
```

### Issue: CORS errors in browser console

**Solution**: Check `ALLOWED_ORIGINS` in backend `.env` matches frontend URL

```env
ALLOWED_ORIGINS=http://localhost:3000,http://localhost:3004
```

### Issue: Session cookies not being set

**Solution**: Ensure both frontend and backend use same domain (localhost) and:
- Backend sets `SameSite=Lax` and `Secure=False` for local development
- Frontend `NEXT_PUBLIC_API_URL` matches backend URL

### Issue: `uv: command not found`

**Solution**: Install UV package manager:

```bash
curl -LsSf https://astral.sh/uv/install.sh | sh
source ~/.bashrc  # Or restart terminal
```

### Issue: Next.js build fails with TypeScript errors

**Solution**: Run type check and fix errors:

```bash
npm run type-check
# Fix reported errors
npm run build
```

---

## Environment Variables Reference

### Backend (`.env`)

| Variable | Description | Example |
|----------|-------------|---------|
| DATABASE_URL | PostgreSQL connection string | `postgresql+asyncpg://user:pass@host/db` |
| JWT_SECRET | Secret key for JWT signing | `openssl rand -hex 32` |
| FRONTEND_URL | Frontend URL for CORS | `http://localhost:3000` |
| ALLOWED_ORIGINS | Comma-separated allowed origins | `http://localhost:3000,http://localhost:3004` |
| SMTP_HOST | Email server host | `smtp.sendgrid.net` |
| SMTP_PORT | Email server port | `587` |
| SMTP_USERNAME | Email server username | `apikey` |
| SMTP_PASSWORD | Email server password | `your-sendgrid-api-key` |
| FROM_EMAIL | From email address | `noreply@example.com` |
| ENVIRONMENT | Environment name | `development` |
| MAX_FILE_SIZE_MB | Max upload file size (MB) | `10` |
| UPLOAD_DIR | File upload directory | `./uploads` |

### Frontend (`.env.local`)

| Variable | Description | Example |
|----------|-------------|---------|
| NEXT_PUBLIC_API_URL | Backend API URL | `http://localhost:8000` |

---

## Next Steps

1. **Read the Spec**: Review `specs/001-project-management-system/spec.md`
2. **Explore Data Model**: Review `specs/001-project-management-system/data-model.md`
3. **API Contracts**: Read `specs/001-project-management-system/contracts/`
4. **Run Tasks**: Execute tasks from `specs/001-project-management-system/tasks.md` (when generated)
5. **Follow Constitution**: Adhere to `.specify/memory/constitution.md` principles

---

## Support & Documentation

- **API Documentation**: http://localhost:8000/docs
- **Constitution**: `.specify/memory/constitution.md`
- **Spec**: `specs/001-project-management-system/spec.md`
- **ADRs**: `history/adr/` (when created)
- **PHRs**: `history/prompts/001-project-management-system/`

---

**Happy Coding! 🚀**
