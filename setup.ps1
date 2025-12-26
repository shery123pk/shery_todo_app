# Todo Application - Quick Setup Script (Windows PowerShell)
# Author: Sharmeen Asif
# This script automates the initial setup process

$ErrorActionPreference = "Stop"

Write-Host "🚀 Todo Application - Quick Setup" -ForegroundColor Cyan
Write-Host "==================================" -ForegroundColor Cyan
Write-Host ""

# Check Python
Write-Host "Checking prerequisites..." -ForegroundColor Yellow
try {
    $pythonVersion = python --version
    Write-Host "✓ Python found: $pythonVersion" -ForegroundColor Green
} catch {
    Write-Host "❌ Python 3 is not installed" -ForegroundColor Red
    Write-Host "Please install Python 3.13+ from https://www.python.org/downloads/"
    exit 1
}

# Check Node.js
try {
    $nodeVersion = node --version
    Write-Host "✓ Node.js found: $nodeVersion" -ForegroundColor Green
} catch {
    Write-Host "❌ Node.js is not installed" -ForegroundColor Red
    Write-Host "Please install Node.js 18.17+ from https://nodejs.org/"
    exit 1
}

# Check UV
try {
    $uvVersion = uv --version
    Write-Host "✓ UV found: $uvVersion" -ForegroundColor Green
} catch {
    Write-Host "❌ UV is not installed" -ForegroundColor Red
    Write-Host "Installing UV..."
    irm https://astral.sh/uv/install.ps1 | iex
}

# Check PostgreSQL or Docker
Write-Host ""
Write-Host "Checking PostgreSQL..." -ForegroundColor Yellow
$hasPostgres = Get-Command psql -ErrorAction SilentlyContinue
$hasDocker = Get-Command docker -ErrorAction SilentlyContinue

if (-not $hasPostgres -and -not $hasDocker) {
    Write-Host "⚠ PostgreSQL not found" -ForegroundColor Yellow
    Write-Host "You can either:"
    Write-Host "  1. Install PostgreSQL: https://www.postgresql.org/download/"
    Write-Host "  2. Use Docker: docker run -d --name todo-postgres -e POSTGRES_USER=todo_user -e POSTGRES_PASSWORD=todo_pass -e POSTGRES_DB=todo_db -p 5432:5432 postgres:16-alpine"
    Read-Host "Press Enter to continue..."
} else {
    Write-Host "✓ PostgreSQL or Docker found" -ForegroundColor Green
}

# Setup Backend
Write-Host ""
Write-Host "📦 Setting up Backend..." -ForegroundColor Cyan
Set-Location backend

# Copy .env.example if .env doesn't exist
if (-not (Test-Path .env)) {
    Write-Host "Creating backend/.env from template..."
    Copy-Item .env.example .env

    # Generate secure secret
    $SECRET = python -c "import secrets; print(secrets.token_urlsafe(32))"

    # Update .env with generated secret
    $envContent = Get-Content .env -Raw
    $envContent = $envContent -replace "dev-secret-key-change-in-production-min-32-chars", $SECRET
    Set-Content .env $envContent

    Write-Host "✓ Generated secure BETTER_AUTH_SECRET" -ForegroundColor Green
    Write-Host ""
    Write-Host "⚠ IMPORTANT: Review and update backend/.env if needed" -ForegroundColor Yellow
    Write-Host "  DATABASE_URL: Update if not using default credentials"
} else {
    Write-Host "⚠ backend/.env already exists, skipping..." -ForegroundColor Yellow
}

# Install dependencies
Write-Host "Installing backend dependencies..."
uv sync
Write-Host "✓ Backend dependencies installed" -ForegroundColor Green

# Run migrations
Write-Host "Running database migrations..."
try {
    uv run alembic upgrade head
    Write-Host "✓ Database migrations complete" -ForegroundColor Green
} catch {
    Write-Host "❌ Migration failed. Check DATABASE_URL in backend/.env" -ForegroundColor Red
    Write-Host "Make sure PostgreSQL is running and credentials are correct"
    exit 1
}

Set-Location ..

# Setup Frontend
Write-Host ""
Write-Host "📦 Setting up Frontend..." -ForegroundColor Cyan
Set-Location frontend

# Copy .env.local.example if .env.local doesn't exist
if (-not (Test-Path .env.local)) {
    Write-Host "Creating frontend/.env.local from template..."
    Copy-Item .env.local.example .env.local

    # Copy the same secret from backend
    $backendEnv = Get-Content ..\backend\.env -Raw
    $BACKEND_SECRET = [regex]::Match($backendEnv, "BETTER_AUTH_SECRET=(.+)").Groups[1].Value

    # Update frontend .env.local
    $frontendEnv = Get-Content .env.local -Raw
    $frontendEnv = $frontendEnv -replace "dev-secret-key-change-in-production-min-32-chars", $BACKEND_SECRET
    Set-Content .env.local $frontendEnv

    Write-Host "✓ Synced BETTER_AUTH_SECRET with backend" -ForegroundColor Green
} else {
    Write-Host "⚠ frontend/.env.local already exists, skipping..." -ForegroundColor Yellow
}

# Install dependencies
Write-Host "Installing frontend dependencies..."
npm install
Write-Host "✓ Frontend dependencies installed" -ForegroundColor Green

Set-Location ..

# Done
Write-Host ""
Write-Host "==================================" -ForegroundColor Green
Write-Host "✅ Setup Complete!" -ForegroundColor Green
Write-Host "==================================" -ForegroundColor Green
Write-Host ""
Write-Host "📝 Next Steps:"
Write-Host ""
Write-Host "1. Start Backend (in one terminal):"
Write-Host "   cd backend"
Write-Host "   uv run uvicorn app.main:app --reload --port 8000"
Write-Host ""
Write-Host "2. Start Frontend (in another terminal):"
Write-Host "   cd frontend"
Write-Host "   npm run dev"
Write-Host ""
Write-Host "3. Open your browser:"
Write-Host "   http://localhost:3000"
Write-Host ""
Write-Host "📚 Documentation:"
Write-Host "   - Getting Started: GETTING_STARTED.md"
Write-Host "   - Production Deploy: docs\PRODUCTION_DEPLOYMENT.md"
Write-Host "   - Phase Integration: PHASE_INTEGRATION.md"
Write-Host ""
Write-Host "🎉 Happy coding!" -ForegroundColor Cyan
