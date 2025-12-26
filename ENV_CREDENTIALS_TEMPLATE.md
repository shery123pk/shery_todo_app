# Environment Variables - Credentials Template
**Author: Sharmeen Asif**

Fill in this template with your actual credentials, then copy to the respective `.env` files.

---

## 📝 Where to Get Credentials

| Service | Where to Get | Free Tier? |
|---------|-------------|-----------|
| **Neon PostgreSQL** | https://console.neon.tech | ✅ Yes (3GB) |
| **OpenAI API** | https://platform.openai.com/api-keys | ❌ No ($5 min) |
| **Qdrant Cloud** | https://cloud.qdrant.io | ✅ Yes (1GB) |

---

## 🔑 Backend Environment Variables

**File:** `backend/.env`

```bash
# ============================================
# 1. NEON POSTGRESQL DATABASE
# ============================================
# Get from: https://console.neon.tech → Your Project → Connection String
DATABASE_URL=postgresql://YOUR_USER:YOUR_PASSWORD@ep-XXX-XXX.us-east-2.aws.neon.tech/neondb?sslmode=require

# Example (REPLACE WITH YOUR ACTUAL CREDENTIALS):
# DATABASE_URL=postgresql://sharmeen:abc123pass@ep-cool-tree-123456.us-east-2.aws.neon.tech/neondb?sslmode=require


# ============================================
# 2. AUTHENTICATION SECRET
# ============================================
# Generate with: python -c "import secrets; print(secrets.token_urlsafe(32))"
BETTER_AUTH_SECRET=PASTE_GENERATED_SECRET_HERE

# Example (GENERATE YOUR OWN!):
# BETTER_AUTH_SECRET=Xy9Kp2Lm4Nq7Rt8Sw1Uv3Wx6Yz0Ab5Cd


# ============================================
# 3. URLs (for local development)
# ============================================
BETTER_AUTH_URL=http://localhost:8000
FRONTEND_URL=http://localhost:3000


# ============================================
# 4. APPLICATION SETTINGS
# ============================================
DEBUG=true
ENVIRONMENT=development


# ============================================
# 5. OPENAI API
# ============================================
# Get from: https://platform.openai.com/api-keys
OPENAI_API_KEY=sk-proj-YOUR_OPENAI_KEY_HERE

# Example (REPLACE WITH YOUR KEY):
# OPENAI_API_KEY=sk-proj-abc123def456ghi789jkl012mno345pqr678

# Choose model (gpt-4o recommended)
OPENAI_MODEL=gpt-4o


# ============================================
# 6. QDRANT VECTOR DATABASE
# ============================================
# Get from: https://cloud.qdrant.io → Your Cluster
QDRANT_URL=https://YOUR_CLUSTER_ID.aws.cloud.qdrant.io
QDRANT_API_KEY=YOUR_QDRANT_API_KEY_HERE
QDRANT_COLLECTION=todo_embeddings

# Example (REPLACE WITH YOUR CREDENTIALS):
# QDRANT_URL=https://abc123-xyz789.aws.cloud.qdrant.io
# QDRANT_API_KEY=qdr_abc123xyz789


# ============================================
# 7. OPTIONAL: Kafka (Phase V)
# ============================================
KAFKA_ENABLED=false
KAFKA_BROKERS=localhost:9092
```

---

## 🔑 Frontend Environment Variables

**File:** `frontend/.env.local`

```bash
# Backend API URL
NEXT_PUBLIC_API_URL=http://localhost:8000

# Authentication Secret (MUST MATCH BACKEND!)
BETTER_AUTH_SECRET=PASTE_SAME_SECRET_FROM_BACKEND_HERE

# Backend Auth URL
BETTER_AUTH_URL=http://localhost:8000
```

**⚠️ CRITICAL:** The `BETTER_AUTH_SECRET` must be **EXACTLY THE SAME** in both `backend/.env` and `frontend/.env.local`!

---

## 🔑 Chatbot Environment Variables (Optional)

**File:** `chatbot/.env`

Only needed if running standalone chatbot (not required for web interface).

```bash
# OpenAI API (same as backend)
OPENAI_API_KEY=sk-proj-YOUR_OPENAI_KEY_HERE
OPENAI_MODEL=gpt-4o

# Backend API
API_URL=http://localhost:8000

# Qdrant (same as backend)
QDRANT_URL=https://YOUR_CLUSTER_ID.aws.cloud.qdrant.io
QDRANT_API_KEY=YOUR_QDRANT_API_KEY_HERE
QDRANT_COLLECTION=todo_embeddings
```

---

## ✅ Setup Checklist

### Before You Start

- [ ] Have Python 3.13+ installed
- [ ] Have Node.js 18.17+ installed
- [ ] Have UV installed (`curl -LsSf https://astral.sh/uv/install.sh | sh`)

### Get Credentials

#### Neon PostgreSQL

- [ ] Created account at https://console.neon.tech
- [ ] Created new project
- [ ] Copied full connection string (with `?sslmode=require`)
- [ ] Pasted into `DATABASE_URL`

#### OpenAI

- [ ] Created account at https://platform.openai.com
- [ ] Added payment method (minimum $5)
- [ ] Generated API key
- [ ] Copied key (starts with `sk-proj-`)
- [ ] Pasted into `OPENAI_API_KEY`

#### Qdrant

- [ ] Created account at https://cloud.qdrant.io
- [ ] Created cluster
- [ ] Copied cluster URL
- [ ] Generated and copied API key
- [ ] Pasted both into `QDRANT_URL` and `QDRANT_API_KEY`

#### Authentication Secret

- [ ] Generated secret: `python -c "import secrets; print(secrets.token_urlsafe(32))"`
- [ ] Copied output
- [ ] Pasted into `BETTER_AUTH_SECRET` in **both** backend and frontend

### Create Files

- [ ] Created `backend/.env` from template above
- [ ] Created `frontend/.env.local` from template above
- [ ] Verified `BETTER_AUTH_SECRET` matches in both files

### Install & Run

- [ ] Installed backend: `cd backend && uv sync`
- [ ] Ran migrations: `uv run alembic upgrade head`
- [ ] Started backend: `uv run uvicorn app.main:app --reload`
- [ ] Installed frontend: `cd frontend && npm install`
- [ ] Started frontend: `npm run dev`
- [ ] Opened browser: http://localhost:3000

---

## 🎯 Quick Copy Template

For easy copying, here's a minimal template:

### Backend `.env`:
```bash
DATABASE_URL=postgresql://
BETTER_AUTH_SECRET=
BETTER_AUTH_URL=http://localhost:8000
FRONTEND_URL=http://localhost:3000
DEBUG=true
ENVIRONMENT=development
OPENAI_API_KEY=sk-proj-
OPENAI_MODEL=gpt-4o
QDRANT_URL=https://
QDRANT_API_KEY=
QDRANT_COLLECTION=todo_embeddings
KAFKA_ENABLED=false
```

### Frontend `.env.local`:
```bash
NEXT_PUBLIC_API_URL=http://localhost:8000
BETTER_AUTH_SECRET=
BETTER_AUTH_URL=http://localhost:8000
```

---

## 📚 Full Setup Guide

For detailed instructions, see: [SETUP_WITH_NEON_OPENAI_QDRANT.md](./SETUP_WITH_NEON_OPENAI_QDRANT.md)

---

## 🆘 Having Trouble?

Common issues:

1. **"Database connection failed"**
   - Check `DATABASE_URL` has `?sslmode=require` at the end
   - Verify credentials are correct
   - Test with: `psql "YOUR_DATABASE_URL"`

2. **"OpenAI API error"**
   - Verify API key starts with `sk-proj-`
   - Check payment method is added
   - View usage: https://platform.openai.com/usage

3. **"Qdrant connection failed"**
   - Verify cluster URL format: `https://xxx.cloud.qdrant.io`
   - Check API key is correct
   - Ensure cluster is running (not suspended)

4. **"Authentication failed"**
   - Verify `BETTER_AUTH_SECRET` matches in backend and frontend
   - Must be exactly the same, no extra spaces
   - Regenerate if needed

---

**Ready to start? Follow the full guide:** [SETUP_WITH_NEON_OPENAI_QDRANT.md](./SETUP_WITH_NEON_OPENAI_QDRANT.md)

**Author:** Sharmeen Asif
**Last Updated:** 2025-12-26
