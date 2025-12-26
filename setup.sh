#!/bin/bash

# Todo Application - Quick Setup Script
# Author: Sharmeen Asif
# This script automates the initial setup process

set -e  # Exit on error

echo "🚀 Todo Application - Quick Setup"
echo "=================================="
echo ""

# Colors
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m' # No Color

# Check if Python is installed
echo "Checking prerequisites..."
if ! command -v python3 &> /dev/null; then
    echo -e "${RED}❌ Python 3 is not installed${NC}"
    echo "Please install Python 3.13+ from https://www.python.org/downloads/"
    exit 1
fi
echo -e "${GREEN}✓ Python found: $(python3 --version)${NC}"

# Check if Node.js is installed
if ! command -v node &> /dev/null; then
    echo -e "${RED}❌ Node.js is not installed${NC}"
    echo "Please install Node.js 18.17+ from https://nodejs.org/"
    exit 1
fi
echo -e "${GREEN}✓ Node.js found: $(node --version)${NC}"

# Check if UV is installed
if ! command -v uv &> /dev/null; then
    echo -e "${RED}❌ UV is not installed${NC}"
    echo "Installing UV..."
    curl -LsSf https://astral.sh/uv/install.sh | sh
    export PATH="$HOME/.cargo/bin:$PATH"
fi
echo -e "${GREEN}✓ UV found${NC}"

# Check PostgreSQL
echo ""
echo "Checking PostgreSQL..."
if ! command -v psql &> /dev/null && ! command -v docker &> /dev/null; then
    echo -e "${YELLOW}⚠ PostgreSQL not found${NC}"
    echo "You can either:"
    echo "  1. Install PostgreSQL: https://www.postgresql.org/download/"
    echo "  2. Use Docker: docker run -d --name todo-postgres -e POSTGRES_USER=todo_user -e POSTGRES_PASSWORD=todo_pass -e POSTGRES_DB=todo_db -p 5432:5432 postgres:16-alpine"
    read -p "Press Enter to continue..."
else
    echo -e "${GREEN}✓ PostgreSQL or Docker found${NC}"
fi

# Setup Backend
echo ""
echo "📦 Setting up Backend..."
cd backend

# Copy .env.example if .env doesn't exist
if [ ! -f .env ]; then
    echo "Creating backend/.env from template..."
    cp .env.example .env

    # Generate secure secret
    SECRET=$(python3 -c "import secrets; print(secrets.token_urlsafe(32))")

    # Update .env with generated secret (works on Linux/Mac)
    if [[ "$OSTYPE" == "darwin"* ]]; then
        sed -i '' "s/dev-secret-key-change-in-production-min-32-chars/$SECRET/g" .env
    else
        sed -i "s/dev-secret-key-change-in-production-min-32-chars/$SECRET/g" .env
    fi

    echo -e "${GREEN}✓ Generated secure BETTER_AUTH_SECRET${NC}"
    echo ""
    echo -e "${YELLOW}⚠ IMPORTANT: Review and update backend/.env if needed${NC}"
    echo "  DATABASE_URL: Update if not using default credentials"
else
    echo -e "${YELLOW}⚠ backend/.env already exists, skipping...${NC}"
fi

# Install dependencies
echo "Installing backend dependencies..."
uv sync
echo -e "${GREEN}✓ Backend dependencies installed${NC}"

# Run migrations
echo "Running database migrations..."
if uv run alembic upgrade head; then
    echo -e "${GREEN}✓ Database migrations complete${NC}"
else
    echo -e "${RED}❌ Migration failed. Check DATABASE_URL in backend/.env${NC}"
    echo "Make sure PostgreSQL is running and credentials are correct"
    exit 1
fi

cd ..

# Setup Frontend
echo ""
echo "📦 Setting up Frontend..."
cd frontend

# Copy .env.local.example if .env.local doesn't exist
if [ ! -f .env.local ]; then
    echo "Creating frontend/.env.local from template..."
    cp .env.local.example .env.local

    # Copy the same secret from backend
    BACKEND_SECRET=$(grep BETTER_AUTH_SECRET ../backend/.env | cut -d '=' -f2)

    # Update frontend .env.local
    if [[ "$OSTYPE" == "darwin"* ]]; then
        sed -i '' "s/dev-secret-key-change-in-production-min-32-chars/$BACKEND_SECRET/g" .env.local
    else
        sed -i "s/dev-secret-key-change-in-production-min-32-chars/$BACKEND_SECRET/g" .env.local
    fi

    echo -e "${GREEN}✓ Synced BETTER_AUTH_SECRET with backend${NC}"
else
    echo -e "${YELLOW}⚠ frontend/.env.local already exists, skipping...${NC}"
fi

# Install dependencies
echo "Installing frontend dependencies..."
npm install
echo -e "${GREEN}✓ Frontend dependencies installed${NC}"

cd ..

# Done
echo ""
echo "=================================="
echo -e "${GREEN}✅ Setup Complete!${NC}"
echo "=================================="
echo ""
echo "📝 Next Steps:"
echo ""
echo "1. Start Backend (in one terminal):"
echo "   cd backend"
echo "   uv run uvicorn app.main:app --reload --port 8000"
echo ""
echo "2. Start Frontend (in another terminal):"
echo "   cd frontend"
echo "   npm run dev"
echo ""
echo "3. Open your browser:"
echo "   http://localhost:3000"
echo ""
echo "📚 Documentation:"
echo "   - Getting Started: GETTING_STARTED.md"
echo "   - Production Deploy: docs/PRODUCTION_DEPLOYMENT.md"
echo "   - Phase Integration: PHASE_INTEGRATION.md"
echo ""
echo "🎉 Happy coding!"
