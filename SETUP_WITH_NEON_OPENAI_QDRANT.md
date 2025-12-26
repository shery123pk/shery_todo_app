# Setup Guide: Neon + OpenAI + Qdrant
**Author: Sharmeen Asif**
**Updated for: Neon PostgreSQL, OpenAI GPT-4, Qdrant Vector Database**

This guide will help you set up the Todo Application with cloud services.

---

## 📋 What You'll Need

1. **Neon PostgreSQL** - Cloud Postgres database (Free tier available)
2. **OpenAI API** - For AI chatbot (Paid, $5 minimum)
3. **Qdrant Cloud** - Vector database for semantic search (Free tier available)

---

## 🚀 Step-by-Step Setup

### Step 1: Get Neon PostgreSQL Database

#### 1.1 Create Neon Account

1. Go to **https://console.neon.tech**
2. Click **"Sign Up"** (GitHub, Google, or Email)
3. Verify your email

#### 1.2 Create Database Project

1. Click **"Create a project"**
2. Configure:
   - **Project name**: `todo-app`
   - **PostgreSQL version**: 16 (latest)
   - **Region**: Choose closest to you (e.g., US East, EU West)
   - **Compute size**: Shared (Free tier)

3. Click **"Create project"**

#### 1.3 Get Connection String

After creation, you'll see the connection string:

```
postgresql://your-user:your-password@ep-xxx-xxx.us-east-2.aws.neon.tech/neondb?sslmode=require
```

**Copy this entire string!** You'll need it for `DATABASE_URL`.

**Important Notes:**
- Neon requires `?sslmode=require` at the end
- Free tier suspends after 5 minutes of inactivity (auto-wakes on connection)
- 3 GB storage limit on free tier

---

### Step 2: Get OpenAI API Key

#### 2.1 Create OpenAI Account

1. Go to **https://platform.openai.com**
2. Click **"Sign Up"**
3. Verify your email and phone number

#### 2.2 Add Payment Method

1. Go to **Settings → Billing**
2. Click **"Add payment method"**
3. Add credit card (minimum $5 deposit)

**Pricing:**
- GPT-4o: $2.50 / 1M input tokens, $10 / 1M output tokens
- GPT-3.5 Turbo: $0.50 / 1M input tokens, $1.50 / 1M output tokens
- Embeddings (ada-002): $0.10 / 1M tokens

**Estimated costs for moderate usage:** $1-5/month

#### 2.3 Generate API Key

1. Go to **API Keys** (https://platform.openai.com/api-keys)
2. Click **"Create new secret key"**
3. Name it: `todo-app-chatbot`
4. **Copy the key** (starts with `sk-proj-...`)

⚠️ **IMPORTANT**: Save this key immediately! You can't see it again.

---

### Step 3: Get Qdrant Vector Database

#### 3.1 Create Qdrant Cloud Account

1. Go to **https://cloud.qdrant.io**
2. Click **"Get Started"**
3. Sign up with GitHub or Google

#### 3.2 Create Cluster

1. Click **"Create Cluster"**
2. Configure:
   - **Cluster name**: `todo-embeddings`
   - **Cloud Provider**: AWS or GCP
   - **Region**: Choose closest to you
   - **Node size**: Free tier (1GB RAM)

3. Click **"Create"**

#### 3.3 Get API Credentials

After cluster creation:

1. Click on your cluster name
2. Copy:
   - **Cluster URL**: `https://xxx-xxx.aws.cloud.qdrant.io`
   - **API Key**: Click "Generate API Key" → Copy the key

---

## 🔧 Configure Environment Variables

### Backend Configuration

Create `backend/.env`:

```bash
# ============================================
# REQUIRED: Database (Neon PostgreSQL)
# ============================================
DATABASE_URL=postgresql://your-user:your-password@ep-xxx-xxx.us-east-2.aws.neon.tech/neondb?sslmode=require

# ============================================
# REQUIRED: Authentication
# ============================================
# Generate with: python -c "import secrets; print(secrets.token_urlsafe(32))"
BETTER_AUTH_SECRET=your-generated-secret-here-min-32-chars
BETTER_AUTH_URL=http://localhost:8000

# ============================================
# REQUIRED: CORS
# ============================================
FRONTEND_URL=http://localhost:3000

# ============================================
# REQUIRED: Application
# ============================================
DEBUG=true
ENVIRONMENT=development

# ============================================
# REQUIRED: OpenAI API (for AI Chatbot)
# ============================================
OPENAI_API_KEY=sk-proj-your-openai-key-here
OPENAI_MODEL=gpt-4o  # Options: gpt-4o, gpt-4-turbo, gpt-3.5-turbo

# ============================================
# REQUIRED: Qdrant Vector Database
# ============================================
QDRANT_URL=https://your-cluster-id.aws.cloud.qdrant.io
QDRANT_API_KEY=your-qdrant-api-key-here
QDRANT_COLLECTION=todo_embeddings

# ============================================
# Optional: Kafka (Phase V)
# ============================================
KAFKA_ENABLED=false
KAFKA_BROKERS=localhost:9092
```

### Frontend Configuration

Create `frontend/.env.local`:

```bash
# Backend API URL
NEXT_PUBLIC_API_URL=http://localhost:8000

# Authentication (MUST MATCH BACKEND!)
BETTER_AUTH_SECRET=your-generated-secret-here-min-32-chars
BETTER_AUTH_URL=http://localhost:8000
```

### Chatbot Configuration (Optional - for standalone chatbot)

Create `chatbot/.env`:

```bash
# OpenAI API
OPENAI_API_KEY=sk-proj-your-openai-key-here
OPENAI_MODEL=gpt-4o

# Backend API
API_URL=http://localhost:8000

# Qdrant Vector Database
QDRANT_URL=https://your-cluster-id.aws.cloud.qdrant.io
QDRANT_API_KEY=your-qdrant-api-key-here
QDRANT_COLLECTION=todo_embeddings
```

---

## 🎯 Quick Setup Checklist

### Prerequisites

- [ ] Python 3.13+ installed
- [ ] Node.js 18.17+ installed
- [ ] UV package manager installed
- [ ] Git installed

### Cloud Services

- [ ] Neon PostgreSQL account created
- [ ] Neon database project created
- [ ] Connection string copied
- [ ] OpenAI account created
- [ ] Payment method added to OpenAI
- [ ] OpenAI API key generated and copied
- [ ] Qdrant Cloud account created
- [ ] Qdrant cluster created
- [ ] Qdrant URL and API key copied

### Configuration Files

- [ ] `backend/.env` created with all credentials
- [ ] `BETTER_AUTH_SECRET` generated (32+ characters)
- [ ] `frontend/.env.local` created
- [ ] `BETTER_AUTH_SECRET` matches in both files

### Installation

- [ ] Backend dependencies installed (`uv sync`)
- [ ] Database migrations run (`alembic upgrade head`)
- [ ] Frontend dependencies installed (`npm install`)

---

## 🚀 Running the Application

### Terminal 1 - Backend

```bash
cd backend
uv sync
uv run alembic upgrade head
uv run uvicorn app.main:app --reload --port 8000
```

**Expected output:**
```
✅ OpenAI client initialized for chatbot
✅ Qdrant service initialized successfully
🚀 Todo Backend API v1.0.0 starting...
📝 Environment: development
🔒 CORS enabled for: http://localhost:3000
INFO:     Uvicorn running on http://127.0.0.1:8000
```

### Terminal 2 - Frontend

```bash
cd frontend
npm install
npm run dev
```

**Expected output:**
```
  ▲ Next.js 15.x.x
  - Local:        http://localhost:3000

 ✓ Ready in 2.3s
```

### Access the Application

Open **http://localhost:3000** in your browser!

---

## ✨ Testing AI Features

### 1. Test AI Chatbot

1. Sign in to the app
2. Click **🤖 AI Chat** button
3. Try these commands:
   - "Show me all my tasks"
   - "Add buy groceries to my list"
   - "Find tasks about shopping"
   - "Mark the first task as complete"

### 2. Test Semantic Search (Qdrant)

The chatbot uses semantic search to find tasks:

```
You: "Find tasks related to shopping"
Bot: *Searches Qdrant embeddings* → Returns relevant tasks
```

This works even if the word "shopping" isn't in the task title!

---

## 💰 Cost Estimation

### Free Tier Limits

**Neon PostgreSQL (Free):**
- 3 GB storage
- Unlimited compute hours
- Auto-suspend after 5 min inactivity
- 1 project

**Qdrant Cloud (Free):**
- 1 cluster
- 1 GB RAM
- 4 GB storage
- Perfect for testing

**OpenAI (Paid):**
- No free tier
- Minimum $5 deposit
- Pay per token used

### Monthly Cost Estimate

**Light usage (testing/personal):**
- Neon: **$0** (free tier)
- Qdrant: **$0** (free tier)
- OpenAI: **$1-5** (depending on usage)

**Total: $1-5/month**

**Medium usage (small team):**
- Neon: **$0-19** (upgrade if needed)
- Qdrant: **$0-25** (upgrade if needed)
- OpenAI: **$10-20**

**Total: $10-64/month**

---

## 🔒 Security Best Practices

### Never Commit Secrets

Add to `.gitignore`:
```
.env
.env.local
*.env
```

### Use Environment Variables

✅ **Good:**
```python
api_key = os.getenv("OPENAI_API_KEY")
```

❌ **Bad:**
```python
api_key = "sk-proj-abc123..."  # NEVER DO THIS!
```

### Rotate Keys Regularly

- Change `BETTER_AUTH_SECRET` every 3-6 months
- Rotate API keys if compromised
- Use different keys for dev/staging/prod

---

## 🐛 Troubleshooting

### Issue: "Neon database connection failed"

**Error:** `could not connect to server`

**Solutions:**
1. Check `DATABASE_URL` has `?sslmode=require` at the end
2. Verify Neon project is active (not suspended)
3. Test connection:
   ```bash
   psql "postgresql://user:pass@ep-xxx.neon.tech/neondb?sslmode=require"
   ```

### Issue: "OpenAI API key invalid"

**Error:** `401 Unauthorized` or `Invalid API key`

**Solutions:**
1. Verify key starts with `sk-proj-`
2. Check for extra spaces in `.env` file
3. Confirm payment method added to OpenAI account
4. Try regenerating the API key

### Issue: "Qdrant connection failed"

**Error:** `Failed to connect to Qdrant`

**Solutions:**
1. Verify cluster is running (not suspended)
2. Check `QDRANT_URL` format: `https://xxx.cloud.qdrant.io`
3. Confirm API key is correct
4. Check cluster region matches your location

### Issue: "Chatbot gives error responses"

**Possible causes:**
- OpenAI API quota exceeded
- Database connection lost
- Invalid session token

**Solutions:**
1. Check OpenAI usage: https://platform.openai.com/usage
2. Verify backend is running
3. Re-login to get fresh session token

---

## 📊 Monitoring Usage

### OpenAI Usage

1. Go to https://platform.openai.com/usage
2. View:
   - Daily/monthly costs
   - Tokens used per model
   - Request counts

### Neon Usage

1. Go to https://console.neon.tech
2. Select your project
3. View:
   - Storage used
   - Compute time
   - Connection count

### Qdrant Usage

1. Go to https://cloud.qdrant.io
2. Click on cluster
3. View:
   - Vector count
   - Storage used
   - API requests

---

## 🎉 Next Steps

After successful setup:

1. **Create your first task** using the web GUI
2. **Try the AI chatbot** with natural language
3. **Test semantic search** by asking for related tasks
4. **Deploy to production** (see PRODUCTION_DEPLOYMENT.md)

---

## 📚 Additional Resources

- **Neon Docs**: https://neon.tech/docs
- **OpenAI API Docs**: https://platform.openai.com/docs
- **Qdrant Docs**: https://qdrant.tech/documentation
- **Project Documentation**: [docs/README.md](./docs/README.md)

---

**Questions?** Create an issue on GitHub: https://github.com/shery123pk/shery_todo_app/issues

**Author:** Sharmeen Asif
**Project:** Todo Application - Panaversity Hackathon
**Last Updated:** 2025-12-26
