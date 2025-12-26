# Getting Started Guide
**Author: Sharmeen Asif**

This guide will help you set up and run the Todo Application locally in under 10 minutes!

---

## 📋 Prerequisites

Before starting, make sure you have installed:

- ✅ **Python 3.13+** - [Download](https://www.python.org/downloads/)
- ✅ **Node.js 18.17+** - [Download](https://nodejs.org/)
- ✅ **UV** (Python package manager) - [Install](https://docs.astral.sh/uv/getting-started/installation/)
- ✅ **PostgreSQL** - [Download](https://www.postgresql.org/download/) OR use Docker
- ✅ **Git** - [Download](https://git-scm.com/downloads)

---

## 🚀 Quick Start (Local Development)

### Step 1: Clone the Repository

```bash
git clone https://github.com/shery123pk/shery_todo_app.git
cd shery_todo_app
```

---

### Step 2: Set Up PostgreSQL Database

**Option A: Using Docker (Recommended)**

```bash
# Start PostgreSQL in Docker
docker run -d \
  --name todo-postgres \
  -e POSTGRES_USER=todo_user \
  -e POSTGRES_PASSWORD=todo_pass \
  -e POSTGRES_DB=todo_db \
  -p 5432:5432 \
  postgres:16-alpine

# Verify it's running
docker ps | grep todo-postgres
```

**Option B: Using Local PostgreSQL**

```bash
# Connect to PostgreSQL
psql -U postgres

# Create database and user
CREATE DATABASE todo_db;
CREATE USER todo_user WITH PASSWORD 'todo_pass';
GRANT ALL PRIVILEGES ON DATABASE todo_db TO todo_user;

# Exit
\q
```

---

### Step 3: Configure Backend Environment Variables

**Create the `.env` file:**

```bash
cd backend
cp .env.example .env
```

**Edit `backend/.env` with your credentials:**

```bash
# Database Configuration
DATABASE_URL=postgresql://todo_user:todo_pass@localhost:5432/todo_db

# Authentication Secret (IMPORTANT: Generate a secure secret!)
BETTER_AUTH_SECRET=your-super-secret-key-min-32-characters-long-change-this

# Backend URL
BETTER_AUTH_URL=http://localhost:8000

# Frontend URL (for CORS)
FRONTEND_URL=http://localhost:3000

# Application Settings
DEBUG=true
ENVIRONMENT=development

# Optional: Kafka (for Phase V - Event Streaming)
KAFKA_ENABLED=false
KAFKA_BROKERS=localhost:9092
```

**⚠️ IMPORTANT: Generate a Secure Secret**

```bash
# Generate a secure BETTER_AUTH_SECRET:
python -c "import secrets; print(secrets.token_urlsafe(32))"

# Copy the output and paste it in BETTER_AUTH_SECRET
```

---

### Step 4: Set Up Backend

```bash
# Make sure you're in backend directory
cd backend

# Install dependencies
uv sync

# Run database migrations
uv run alembic upgrade head

# Verify setup
uv run alembic current
# Should show: (head)

# Start the backend server
uv run uvicorn app.main:app --reload --port 8000
```

**Expected Output:**
```
🚀 Todo Backend API v1.0.0 starting...
📝 Environment: development
🔒 CORS enabled for: http://localhost:3000
INFO:     Uvicorn running on http://127.0.0.1:8000 (Press CTRL+C to quit)
```

**Test Backend:**
Open http://localhost:8000/docs in your browser. You should see the API documentation.

---

### Step 5: Configure Frontend Environment Variables

**Open a new terminal and create `.env.local`:**

```bash
cd frontend
cp .env.local.example .env.local
```

**Edit `frontend/.env.local`:**

```bash
# Backend API URL
NEXT_PUBLIC_API_URL=http://localhost:8000

# Authentication Secret (MUST MATCH BACKEND!)
BETTER_AUTH_SECRET=your-super-secret-key-min-32-characters-long-change-this

# Backend Auth URL
BETTER_AUTH_URL=http://localhost:8000
```

**⚠️ CRITICAL:** `BETTER_AUTH_SECRET` must be **exactly the same** in both backend and frontend!

---

### Step 6: Set Up Frontend

```bash
# Make sure you're in frontend directory
cd frontend

# Install dependencies
npm install

# Start the development server
npm run dev
```

**Expected Output:**
```
  ▲ Next.js 15.x.x
  - Local:        http://localhost:3000
  - Environments: .env.local

 ✓ Ready in 2.3s
```

---

### Step 7: Access the Application

Open your browser and go to:

**🎉 http://localhost:3000**

You should see the **Todo Application** home page!

---

## 🎯 First Time Setup - Create an Account

1. Click **"Sign Up"** button
2. Fill in the form:
   - **Email:** your-email@example.com
   - **Password:** YourPassword123! (min 8 characters)
   - **Full Name:** Your Name
3. Click **"Create Account"**
4. You'll be redirected to the **Tasks Dashboard**

---

## 🧪 Test All Features

### 1. Test Web GUI (Phase II)

- ✅ Create a task: Click "+" or "Add Task" button
- ✅ Mark as complete: Click checkbox
- ✅ Edit task: Click edit icon
- ✅ Delete task: Click delete icon
- ✅ Filter tasks: Click "All", "Active", or "Completed"

### 2. Test CLI Interface (Phase I)

- Click the **$ CLI** button in the header
- Try commands:
  ```bash
  $ help
  $ list
  $ add Buy groceries
  $ complete 1
  $ delete 2
  $ exit
  ```

### 3. Test AI Chatbot (Phase III)

- Click the **🤖 AI Chat** button in the header
- Try natural language:
  - "Show me all my tasks"
  - "Add buy milk to my list"
  - "What can you help me with?"

**Note:** Full AI requires `ANTHROPIC_API_KEY` (see optional setup below)

---

## 🔧 Optional: Enable Full AI Chatbot (Phase III)

To enable the full Claude AI chatbot with natural language processing:

### 1. Get Anthropic API Key

1. Sign up at https://console.anthropic.com/
2. Get your API key from the dashboard
3. Copy the key (starts with `sk-ant-...`)

### 2. Configure Chatbot

```bash
cd chatbot
cp .env.example .env
```

**Edit `chatbot/.env`:**

```bash
# Anthropic API Key (REQUIRED for full chatbot)
ANTHROPIC_API_KEY=sk-ant-your-key-here

# Backend API URL
API_URL=http://localhost:8000

# Session token (will be provided by user at runtime)
```

### 3. Run Standalone Chatbot

```bash
cd chatbot
uv sync
uv run chatbot
```

Or integrate with web interface by setting `CHATBOT_API_URL` in backend `.env`.

---

## 🐳 Alternative: Run with Docker Compose

**Start everything with one command:**

```bash
# From project root
docker-compose up -d

# Check services
docker-compose ps

# View logs
docker-compose logs -f

# Stop all services
docker-compose down
```

**Services will be available at:**
- Frontend: http://localhost:3000
- Backend: http://localhost:8000
- PostgreSQL: localhost:5432

---

## 🔍 Troubleshooting

### Issue 1: Database Connection Failed

**Error:** `could not connect to server: Connection refused`

**Solution:**
```bash
# Check if PostgreSQL is running
docker ps | grep postgres
# OR
sudo systemctl status postgresql

# If using Docker, start it:
docker start todo-postgres

# Verify DATABASE_URL in backend/.env matches your setup
```

---

### Issue 2: Authentication Failed / Invalid Token

**Error:** `Invalid session token` or redirects to sign in

**Solution:**
```bash
# Ensure BETTER_AUTH_SECRET matches in both:
# - backend/.env
# - frontend/.env.local

# Regenerate secret:
python -c "import secrets; print(secrets.token_urlsafe(32))"

# Copy the SAME secret to both files
# Restart both backend and frontend
```

---

### Issue 3: CORS Errors in Browser Console

**Error:** `Access-Control-Allow-Origin` errors

**Solution:**
```bash
# Check FRONTEND_URL in backend/.env
# Should be: http://localhost:3000

# Check NEXT_PUBLIC_API_URL in frontend/.env.local
# Should be: http://localhost:8000

# Restart backend after changing .env
```

---

### Issue 4: Migration Error

**Error:** `Target database is not up to date`

**Solution:**
```bash
cd backend

# Check current migration
uv run alembic current

# Upgrade to latest
uv run alembic upgrade head

# If still failing, check DATABASE_URL
```

---

### Issue 5: Port Already in Use

**Error:** `Address already in use: 8000` or `3000`

**Solution:**
```bash
# Find process using the port
# On Windows:
netstat -ano | findstr :8000
netstat -ano | findstr :3000

# On Linux/Mac:
lsof -i :8000
lsof -i :3000

# Kill the process or use different port
# Backend:
uv run uvicorn app.main:app --reload --port 8001

# Frontend:
npm run dev -- -p 3001
```

---

### Issue 6: Module Not Found

**Error:** `ModuleNotFoundError` or `Cannot find module`

**Solution:**
```bash
# Backend:
cd backend
uv sync

# Frontend:
cd frontend
rm -rf node_modules package-lock.json
npm install

# Restart servers
```

---

## 📊 Verify Setup Checklist

Before running the application, verify:

- [ ] PostgreSQL is running and accessible
- [ ] `backend/.env` file exists with valid credentials
- [ ] `BETTER_AUTH_SECRET` is 32+ characters (not the default)
- [ ] `frontend/.env.local` file exists
- [ ] `BETTER_AUTH_SECRET` matches in backend and frontend
- [ ] `DATABASE_URL` points to your PostgreSQL instance
- [ ] Backend dependencies installed (`uv sync`)
- [ ] Frontend dependencies installed (`npm install`)
- [ ] Database migrations run (`alembic upgrade head`)

---

## 🎯 Next Steps

After successful setup:

1. **Explore All Phases:**
   - Web GUI: http://localhost:3000/tasks
   - CLI Interface: http://localhost:3000/cli
   - AI Chatbot: http://localhost:3000/chatbot

2. **Try Phase I Original CLI:**
   ```bash
   cd cli
   uv sync
   uv run todo --help
   ```

3. **Deploy to Production:**
   - See [docs/PRODUCTION_DEPLOYMENT.md](./docs/PRODUCTION_DEPLOYMENT.md)

4. **Run Tests:**
   ```bash
   # Backend tests
   cd backend
   uv run pytest -v

   # CLI tests
   cd cli
   uv run pytest -v
   ```

5. **Try Kubernetes (Phase IV):**
   ```bash
   cd k8s
   ./deploy.sh
   ```

---

## 📚 Additional Resources

- **Production Deployment:** [docs/PRODUCTION_DEPLOYMENT.md](./docs/PRODUCTION_DEPLOYMENT.md)
- **Phase Integration:** [PHASE_INTEGRATION.md](./PHASE_INTEGRATION.md)
- **Project Documentation:** [docs/README.md](./docs/README.md)
- **API Documentation:** http://localhost:8000/docs (after starting backend)

---

## 🆘 Still Having Issues?

1. **Check the logs:**
   - Backend: Look at terminal where `uvicorn` is running
   - Frontend: Look at terminal where `npm run dev` is running
   - Browser: Open DevTools → Console

2. **Verify environment variables:**
   ```bash
   # Backend
   cat backend/.env

   # Frontend
   cat frontend/.env.local
   ```

3. **Run verification script:**
   ```bash
   python scripts/verify-env.py backend
   python scripts/verify-env.py frontend
   ```

4. **Create GitHub Issue:**
   - Repository: https://github.com/shery123pk/shery_todo_app/issues
   - Include: Error message, OS, Python/Node versions

---

## ✅ Success Indicators

You'll know everything is working when:

1. ✅ Backend shows: `Uvicorn running on http://127.0.0.1:8000`
2. ✅ Frontend shows: `Ready in 2.3s`
3. ✅ Browser opens http://localhost:3000 without errors
4. ✅ You can sign up and create tasks
5. ✅ All three interfaces work (GUI, CLI, Chatbot)

---

## 🎉 You're Ready!

Congratulations! Your Todo Application is now running locally with all 5 phases integrated!

**Happy task managing!** 📝✨

---

**Author:** Sharmeen Asif
**Project:** Todo Application - Panaversity Hackathon
**Last Updated:** 2025-12-26
