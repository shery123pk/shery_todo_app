# Credentials Best Practices - Multi-Project Setup
**Author: Sharmeen Asif**

Guide for reusing Neon, Qdrant, and HuggingFace credentials across multiple projects efficiently and securely.

---

## 🎯 TL;DR - Best Approach

| Service | Strategy | Why |
|---------|----------|-----|
| **Neon PostgreSQL** | ✅ One account, multiple databases | Free tier allows multiple DBs |
| **Qdrant** | ✅ One cluster, multiple collections | Cost-effective, easier to manage |
| **OpenAI** | ✅ One API key, track by project in code | Unified billing, usage tracking |
| **HuggingFace** | ✅ One account, multiple Spaces | Unlimited free Spaces |

---

## 1️⃣ Neon PostgreSQL - Multiple Databases

### ✅ Recommended: One Account, Separate Databases Per Project

**Why This Approach:**
- Free tier supports multiple databases
- Easy to manage from one dashboard
- Separate data isolation per project
- Individual connection strings

**Setup:**

```bash
# Project 1: Todo App
DATABASE_URL_TODO=postgresql://user:pass@ep-xxx.neon.tech/todo_db?sslmode=require

# Project 2: Blog App
DATABASE_URL_BLOG=postgresql://user:pass@ep-xxx.neon.tech/blog_db?sslmode=require

# Project 3: Ecommerce
DATABASE_URL_SHOP=postgresql://user:pass@ep-xxx.neon.tech/shop_db?sslmode=require
```

**How to Create Multiple Databases:**

1. Go to https://console.neon.tech
2. Select your project
3. Click **Databases** tab
4. Click **New Database**
5. Name it: `todo_db`, `blog_db`, etc.
6. Each gets same credentials, different database name

**Cost:** FREE (up to 10 databases in free tier)

### ❌ Alternative (NOT Recommended): Multiple Accounts

**Why Not:**
- Harder to manage
- Need multiple emails
- More confusing
- No cost benefit

---

## 2️⃣ Qdrant - Multiple Collections

### ✅ Recommended: One Cluster, Separate Collections Per Project

**Why This Approach:**
- One free cluster supports unlimited collections
- Shared resources = cost effective
- Easier management
- Same API credentials

**Setup:**

```bash
# Same credentials, different collections
QDRANT_URL=https://abc123.cloud.qdrant.io
QDRANT_API_KEY=qdr_xyz789

# Project 1: Todo App
QDRANT_COLLECTION=todo_embeddings

# Project 2: Blog App
QDRANT_COLLECTION=blog_embeddings

# Project 3: Ecommerce
QDRANT_COLLECTION=product_embeddings
```

**How to Use Multiple Collections:**

Collections are created automatically by your code:

```python
# In each project, just use different collection name
collection_name = "todo_embeddings"  # Project 1
collection_name = "blog_embeddings"  # Project 2
```

**Cost:** FREE (1 cluster = unlimited collections)

### 💡 When to Use Multiple Clusters:

Only if:
- One project has huge data (> 1GB vectors)
- Different geographic regions needed
- Strict data isolation required

**Cost:** $25/month per additional cluster

---

## 3️⃣ OpenAI API - One Key, Track Usage

### ✅ Recommended: One API Key, Add Project Tags in Code

**Why This Approach:**
- Unified billing
- One place to monitor usage
- Easier to manage quotas
- Track by project using user metadata

**Setup:**

```bash
# Same key for all projects
OPENAI_API_KEY=sk-proj-abc123xyz789

# Track usage per project using user field:
```

```python
# Project 1: Todo App
response = client.chat.completions.create(
    model="gpt-4o",
    messages=[...],
    user="todo-app-prod"  # Track this project
)

# Project 2: Blog App
response = client.chat.completions.create(
    model="gpt-4o",
    messages=[...],
    user="blog-app-prod"  # Track different project
)
```

**Monitor Usage:**
1. Go to https://platform.openai.com/usage
2. Filter by user ID to see per-project costs

**Cost:** Pay-per-use (shared budget across projects)

### 💡 Alternative: Separate API Keys Per Project

**When to use:**
- Separate billing required (different clients)
- Strict budget limits per project
- Team access control

**How:**
1. OpenAI dashboard → Create new key
2. Name it: "todo-app", "blog-app"
3. Set usage limits per key

**Cost:** Same rate, just separate tracking

---

## 4️⃣ HuggingFace - Multiple Spaces

### ✅ Recommended: One Account, Separate Spaces Per Project

**Why This Approach:**
- Unlimited free Spaces
- Each Space = separate container
- Independent deployments
- Easy switching

**Setup:**

```bash
# Project 1: Todo App Backend
Space: username/todo-backend
URL: https://username-todo-backend.hf.space

# Project 2: Blog API
Space: username/blog-api
URL: https://username-blog-api.hf.space

# Project 3: Shop Backend
Space: username/shop-backend
URL: https://username-shop-backend.hf.space
```

**How to Create Multiple Spaces:**

1. Go to https://huggingface.co/new-space
2. Create new Space for each project
3. Each has own secrets and environment
4. Deploy different code to each

**Cost:** FREE (unlimited CPU Spaces)

---

## 📊 Cost Comparison: Shared vs Separate

| Service | Shared Approach | Separate Approach |
|---------|----------------|-------------------|
| **Neon** | $0 (free tier) | $0 (still free) |
| **Qdrant** | $0 (1 cluster) | $25/month per cluster |
| **OpenAI** | ~$10/month total | ~$10/month total |
| **HuggingFace** | $0 (free Spaces) | $0 (free Spaces) |
| **TOTAL** | **$10/month** | **$35+/month** |

**Winner:** 🏆 Shared approach saves $25+/month!

---

## 🔐 Security Best Practices

### 1. Environment Variables Organization

Create a **master credentials file** (NOT in Git):

**File:** `~/credentials/cloud-services.env` (outside Git)

```bash
# ============================================
# SHARED CREDENTIALS (USE ACROSS PROJECTS)
# ============================================

# Neon PostgreSQL (same credentials, different DBs)
NEON_USER=your_user
NEON_PASSWORD=your_password
NEON_HOST=ep-xxx-xxx.us-east-2.aws.neon.tech
NEON_DB_TODO=todo_db
NEON_DB_BLOG=blog_db

# Qdrant (same credentials, different collections)
QDRANT_URL=https://abc123.cloud.qdrant.io
QDRANT_API_KEY=qdr_xyz789

# OpenAI (same key, track by user field)
OPENAI_API_KEY=sk-proj-abc123xyz789

# HuggingFace (same token)
HF_TOKEN=hf_abc123xyz789
```

### 2. Per-Project .env Files

**Project 1:** `todo-app/backend/.env`

```bash
# Build connection from master credentials
DATABASE_URL=postgresql://${NEON_USER}:${NEON_PASSWORD}@${NEON_HOST}/${NEON_DB_TODO}?sslmode=require
OPENAI_API_KEY=${OPENAI_API_KEY}
QDRANT_URL=${QDRANT_URL}
QDRANT_API_KEY=${QDRANT_API_KEY}
QDRANT_COLLECTION=todo_embeddings
```

**Project 2:** `blog-app/backend/.env`

```bash
DATABASE_URL=postgresql://${NEON_USER}:${NEON_PASSWORD}@${NEON_HOST}/${NEON_DB_BLOG}?sslmode=require
OPENAI_API_KEY=${OPENAI_API_KEY}
QDRANT_URL=${QDRANT_URL}
QDRANT_API_KEY=${QDRANT_API_KEY}
QDRANT_COLLECTION=blog_embeddings
```

### 3. Use Environment Variable Substitution

**Script to generate .env from master:**

```bash
#!/bin/bash
# generate-env.sh

source ~/credentials/cloud-services.env

cat > .env << EOF
DATABASE_URL=postgresql://${NEON_USER}:${NEON_PASSWORD}@${NEON_HOST}/${NEON_DB_TODO}?sslmode=require
OPENAI_API_KEY=${OPENAI_API_KEY}
QDRANT_URL=${QDRANT_URL}
QDRANT_API_KEY=${QDRANT_API_KEY}
QDRANT_COLLECTION=todo_embeddings
EOF
```

---

## 🎯 Recommended Setup for Multiple Projects

### Step 1: Create Shared Infrastructure

```bash
# One-time setup
1. Neon: Create account → 1 project → Multiple databases
2. Qdrant: Create account → 1 cluster
3. OpenAI: Create account → 1 API key
4. HuggingFace: Create account
```

### Step 2: Master Credentials File

Create: `~/credentials/master.env`

```bash
# Neon
NEON_CONNECTION_STRING=postgresql://user:pass@ep-xxx.neon.tech

# Qdrant
QDRANT_URL=https://xxx.cloud.qdrant.io
QDRANT_API_KEY=qdr_xxx

# OpenAI
OPENAI_API_KEY=sk-proj-xxx

# HuggingFace
HF_TOKEN=hf_xxx
```

### Step 3: Per-Project Configuration

```bash
# Project 1: Todo App
cd todo-app/backend
echo "QDRANT_COLLECTION=todo_embeddings" >> .env
echo "DATABASE_URL=${NEON_CONNECTION_STRING}/todo_db?sslmode=require" >> .env

# Project 2: Blog App
cd blog-app/backend
echo "QDRANT_COLLECTION=blog_embeddings" >> .env
echo "DATABASE_URL=${NEON_CONNECTION_STRING}/blog_db?sslmode=require" >> .env
```

---

## 💡 Pro Tips

### 1. Database Naming Convention

```bash
# Use consistent prefixes
{project_name}_db
{project_name}_{environment}

Examples:
- todo_dev
- todo_staging
- todo_prod
- blog_dev
- blog_prod
```

### 2. Qdrant Collections Naming

```bash
# Use project prefix
{project}_{data_type}

Examples:
- todo_embeddings
- blog_article_embeddings
- shop_product_embeddings
```

### 3. OpenAI User Tracking

```bash
# Format: {project}-{environment}-{feature}
user="todo-prod-chatbot"
user="blog-dev-summarizer"
user="shop-prod-recommendations"
```

### 4. Monitor Usage Per Project

**Weekly Review:**
1. OpenAI usage dashboard → Group by user field
2. Neon → Check each database size
3. Qdrant → Monitor collection vector counts

---

## 🚨 When NOT to Share Credentials

### Use Separate Credentials If:

1. **Client Projects:**
   - Different billing required
   - Client owns the credentials
   - Handoff to client team

2. **Production vs Development:**
   - Use separate Neon projects for prod/dev
   - Different OpenAI keys for prod/dev
   - Prevents dev from affecting prod

3. **Team Access Control:**
   - Different teams need different access
   - Security compliance requirements
   - Audit trail needed per project

4. **Geographic Requirements:**
   - Data residency laws
   - Latency optimization
   - Regional restrictions

---

## ✅ Summary: Your Setup for Multiple Projects

For **Todo App** (your current project):

```bash
# Neon: Create database "todo_db"
# Qdrant: Use collection "todo_embeddings"
# OpenAI: Use with user="todo-app-prod"
# HuggingFace: Deploy to username/todo-backend
```

For **Future Projects:**

```bash
# Neon: Create new database "project_db"
# Qdrant: Use new collection "project_embeddings"
# OpenAI: Same key, different user field
# HuggingFace: Create new Space username/project-backend
```

**Result:**
- ✅ One Neon account (10 databases)
- ✅ One Qdrant cluster (unlimited collections)
- ✅ One OpenAI key (track by project)
- ✅ One HuggingFace account (unlimited Spaces)
- ✅ Total cost: ~$10/month for all projects!

---

**Questions?** See also:
- [SETUP_WITH_NEON_OPENAI_QDRANT.md](./SETUP_WITH_NEON_OPENAI_QDRANT.md) - Initial setup
- [DEPLOY_TO_HUGGINGFACE.md](./DEPLOY_TO_HUGGINGFACE.md) - Deployment guide

**Author:** Sharmeen Asif
**Last Updated:** 2025-12-26
