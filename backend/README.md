# Project Management System - Backend API

Professional multi-tenant project management system backend built with FastAPI and PostgreSQL.

## Tech Stack

- **Framework**: FastAPI 0.110+
- **Language**: Python 3.13+
- **ORM**: SQLModel (SQLAlchemy 2.0 + Pydantic v2)
- **Database**: PostgreSQL 15+ (Neon serverless)
- **Authentication**: JWT tokens in HttpOnly cookies
- **Migrations**: Alembic
- **Testing**: pytest + httpx (async client)
- **Package Manager**: UV

## Prerequisites

- Python 3.13+
- UV package manager ([Install UV](https://astral.sh/uv/install.sh))
- PostgreSQL 15+ or Neon account

## Setup

### 1. Install Dependencies

```bash
# Create virtual environment and install dependencies
uv venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate

# Install dependencies
uv pip install -e ".[dev]"
```

### 2. Configure Environment

```bash
cp .env.example .env
```

Edit `.env` with your configuration:
- `DATABASE_URL`: Neon PostgreSQL connection string
- `JWT_SECRET`: Generate with `openssl rand -hex 32`
- `SMTP_*`: Email service credentials for verification/reset emails

### 3. Initialize Database

```bash
# Run migrations
alembic upgrade head

# Optional: Seed with sample data
uv run python scripts/seed_data.py
```

### 4. Run Development Server

```bash
uv run uvicorn app.main:app --reload --port 8000
```

Server runs at http://localhost:8000
- API docs: http://localhost:8000/docs (Swagger UI)
- Alternative docs: http://localhost:8000/redoc (ReDoc)

## Project Structure

```
backend/
├── app/
│   ├── __init__.py
│   ├── main.py                 # FastAPI app initialization
│   ├── config.py               # Pydantic settings
│   ├── database.py             # Database connection
│   ├── dependencies.py         # Dependency injection
│   ├── models/                 # SQLModel models
│   │   ├── base.py
│   │   ├── user.py
│   │   ├── organization.py
│   │   └── ...
│   ├── routers/                # API route handlers
│   │   ├── auth.py
│   │   ├── organizations.py
│   │   └── ...
│   ├── services/               # Business logic
│   │   ├── auth_service.py
│   │   ├── email_service.py
│   │   └── ...
│   └── utils/                  # Utilities
│       ├── auth.py             # JWT, password hashing
│       └── errors.py           # Error handling
├── alembic/                    # Database migrations
├── tests/                      # Pytest tests
├── pyproject.toml              # Dependencies
└── README.md
```

## Testing

```bash
# Run all tests
uv run pytest

# Run with coverage report
uv run pytest --cov=app --cov-report=html

# Run specific test file
uv run pytest tests/test_auth.py

# View coverage report
open htmlcov/index.html
```

## Code Quality

```bash
# Format code
uv run ruff format .

# Lint code
uv run ruff check .

# Fix auto-fixable issues
uv run ruff check --fix .

# Type checking
uv run pyright
```

## Database Migrations

```bash
# Create new migration
alembic revision --autogenerate -m "Add new column"

# Apply migrations
alembic upgrade head

# Rollback one migration
alembic downgrade -1
```

## API Documentation

Once the server is running, visit:
- Swagger UI: http://localhost:8000/docs
- ReDoc: http://localhost:8000/redoc

## Development

This is feature `001-project-management-system`. See:
- Specification: `../specs/001-project-management-system/spec.md`
- Architecture Plan: `../specs/001-project-management-system/plan.md`
- Tasks: `../specs/001-project-management-system/tasks.md`
