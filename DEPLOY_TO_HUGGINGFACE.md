# Deploy Backend to HuggingFace Spaces
**Author: Sharmeen Asif**

Complete guide to deploy your FastAPI backend to HuggingFace Spaces with Neon PostgreSQL, OpenAI, and Qdrant.

---

## 🎯 What You'll Deploy

- **Backend API:** FastAPI with all routes (auth, tasks, chatbot)
- **Database:** Neon PostgreSQL (cloud)
- **AI Chatbot:** OpenAI GPT-4
- **Vector Search:** Qdrant Cloud
- **Port:** 7860 (HuggingFace requirement)

---

## 📋 Prerequisites

Before deploying, ensure you have:

✅ HuggingFace account (https://huggingface.co/join)
✅ Neon PostgreSQL database created and migrations run
✅ OpenAI API key
✅ Qdrant cluster created
✅ Backend working locally

---

## 🚀 Step-by-Step Deployment

### Step 1: Create HuggingFace Space

1. Go to https://huggingface.co/new-space

2. Configure your Space:
   - **Owner:** Your username
   - **Space name:** `todo-backend`
   - **License:** MIT
   - **Select the SDK:** Docker
   - **Space hardware:** CPU basic - Free
   - **Repo type:** Public (or Private if you have Pro)

3. Click **Create Space**

You'll get: `https://huggingface.co/spaces/YOUR_USERNAME/todo-backend`

---

### Step 2: Configure Space Secrets

Secrets are environment variables that are hidden from public view.

1. Go to your Space → **Settings** tab
2. Scroll to **Repository secrets**
3. Click **New secret** for each:

#### Required Secrets:

| Secret Name | Value | How to Get |
|------------|-------|------------|
| `DATABASE_URL` | `postgresql://user:pass@ep-xxx.neon.tech/todo_db?sslmode=require` | From Neon console |
| `BETTER_AUTH_SECRET` | Generate: `python -c "import secrets; print(secrets.token_urlsafe(32))"` | Run command |
| `BETTER_AUTH_URL` | `https://YOUR_USERNAME-todo-backend.hf.space` | Your Space URL |
| `FRONTEND_URL` | `https://YOUR_APP.vercel.app` or temp: `http://localhost:3000` | Vercel URL |
| `OPENAI_API_KEY` | `sk-proj-xxx...` | From OpenAI dashboard |
| `OPENAI_MODEL` | `gpt-4o` | Or `gpt-4-turbo`, `gpt-3.5-turbo` |
| `QDRANT_URL` | `https://xxx.cloud.qdrant.io` | From Qdrant console |
| `QDRANT_API_KEY` | `qdr_xxx...` | From Qdrant console |
| `QDRANT_COLLECTION` | `todo_embeddings` | Your collection name |

#### Optional Secrets:

| Secret Name | Value | Purpose |
|------------|-------|---------|
| `DEBUG` | `false` | Disable debug in production |
| `ENVIRONMENT` | `production` | Set environment |
| `KAFKA_ENABLED` | `false` | Disable Kafka for now |

**Example adding a secret:**

```
Name: DATABASE_URL
Value: postgresql://sharmeen:abc123@ep-cool-tree-123.us-east-2.aws.neon.tech/todo_db?sslmode=require
```

Click **Add secret** after each one.

---

### Step 3: Prepare Backend Code for Deployment

The backend is already configured for port 7860, but let's verify:

#### 3.1 Check Dockerfile

Your `backend/Dockerfile` should expose port 7860:

```dockerfile
EXPOSE 7860

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "7860"]
```

✅ Already configured!

#### 3.2 Verify Dependencies

Check `backend/pyproject.toml` has:

```toml
dependencies = [
    "fastapi>=0.100.0",
    "sqlmodel>=0.0.14",
    "alembic>=1.13.0",
    "python-jose[cryptography]>=3.3.0",
    "passlib[bcrypt]>=1.7.4",
    "uvicorn[standard]>=0.25.0",
    "psycopg2-binary>=2.9.9",
    "pydantic>=2.5.0",
    "openai>=1.12.0",
    "qdrant-client>=1.7.0",
    "httpx>=0.27.0",
]
```

✅ Already configured!

---

### Step 4: Run Migrations on Neon Database

**IMPORTANT:** Run migrations BEFORE deploying!

```bash
# Set your Neon DATABASE_URL
export DATABASE_URL="postgresql://user:pass@ep-xxx.neon.tech/todo_db?sslmode=require"

# Or Windows PowerShell:
$env:DATABASE_URL="postgresql://user:pass@ep-xxx.neon.tech/todo_db?sslmode=require"

# Navigate to backend
cd backend

# Run migrations
uv run alembic upgrade head

# Verify
uv run alembic current
# Should show: (head)
```

**Why?** HuggingFace Spaces are stateless - migrations must be run separately.

---

### Step 5: Deploy to HuggingFace

#### Option A: Using Git (Recommended)

```bash
# From your project root
cd backend

# Add HuggingFace as remote
git remote add hf https://huggingface.co/spaces/YOUR_USERNAME/todo-backend

# Push only backend folder
git subtree push --prefix backend hf main
```

**If you get errors:**

```bash
# Force push (first time only)
git push hf `git subtree split --prefix backend main`:main --force
```

#### Option B: Manual Upload via Web UI

1. Go to your Space → **Files** tab
2. Click **Add file** → **Upload files**
3. Upload entire `backend/` directory:
   - `app/` folder
   - `alembic/` folder
   - `Dockerfile`
   - `pyproject.toml`
   - `alembic.ini`
   - `README.md`

⚠️ **Do NOT upload** `.env` file (use Secrets instead)

---

### Step 6: Monitor Deployment

1. Go to your Space → **App** tab

2. Watch the build logs:

```
Building Docker image...
Installing dependencies...
Starting application...
✅ OpenAI client initialized for chatbot
✅ Qdrant service initialized successfully
🚀 Todo Backend API v1.0.0 starting...
Application startup complete
```

3. Wait for "Running" status (2-5 minutes)

---

### Step 7: Verify Deployment

#### 7.1 Check Health Endpoint

Open in browser:
```
https://YOUR_USERNAME-todo-backend.hf.space/
```

Expected response:
```json
{
  "message": "Todo Backend API",
  "version": "1.0.0",
  "docs": "/docs",
  "health": "/health"
}
```

#### 7.2 Check API Documentation

Open:
```
https://YOUR_USERNAME-todo-backend.hf.space/docs
```

You should see Swagger UI with all endpoints!

#### 7.3 Test Chatbot Status

Open:
```
https://YOUR_USERNAME-todo-backend.hf.space/api/chatbot/status
```

Expected response:
```json
{
  "available": true,
  "message": "Chatbot service is online"
}
```

---

### Step 8: Update Frontend Configuration

Now update your frontend to use the deployed backend:

**File:** `frontend/.env.local`

```bash
# Update this line:
NEXT_PUBLIC_API_URL=https://YOUR_USERNAME-todo-backend.hf.space

# Keep these (generate matching secret):
BETTER_AUTH_SECRET=same-as-backend-secret
BETTER_AUTH_URL=https://YOUR_USERNAME-todo-backend.hf.space
```

**Then restart frontend:**

```bash
cd frontend
npm run dev
```

---

### Step 9: Test End-to-End

1. **Open frontend:** http://localhost:3000

2. **Sign Up:** Create a new account
   - Should call HuggingFace backend
   - Should create user in Neon database

3. **Create Task:** Add a new task
   - Should store in Neon
   - Should index in Qdrant (if configured)

4. **Test AI Chatbot:** Click 🤖 AI Chat
   - Try: "Show me all my tasks"
   - Should use OpenAI to respond

5. **Verify Data Persistence:**
   - Close browser
   - Reopen and sign in
   - Tasks should still be there!

---

## 🎉 Success! Your Backend is Deployed

**Your URLs:**

- **Backend API:** https://YOUR_USERNAME-todo-backend.hf.space
- **API Docs:** https://YOUR_USERNAME-todo-backend.hf.space/docs
- **Health Check:** https://YOUR_USERNAME-todo-backend.hf.space/health

---

## 🔄 Updating Your Deployment

### When You Make Code Changes:

```bash
cd backend

# Commit changes
git add .
git commit -m "Update backend feature"

# Push to HuggingFace
git subtree push --prefix backend hf main
```

HuggingFace will automatically rebuild and redeploy!

---

## 📊 Monitoring & Logs

### View Application Logs

1. Go to your Space → **App** tab
2. Scroll down to see logs
3. Watch for errors or warnings

### Common Log Messages:

```
✅ Good:
- "Application startup complete"
- "OpenAI client initialized"
- "Qdrant service initialized"

⚠️ Warnings (OK):
- "QDRANT_URL not configured" (if you skipped Qdrant)
- "Neon database auto-woke" (after 5 min suspend)

❌ Errors (Fix these):
- "Invalid OPENAI_API_KEY"
- "Database connection failed"
- "Qdrant connection failed"
```

---

## 💰 Cost & Performance

### HuggingFace Free Tier:

- ✅ **CPU basic:** FREE
- ✅ **Public Spaces:** Unlimited
- ⚠️ **Cold starts:** ~30 seconds (if idle)
- ⚠️ **Sleep mode:** After 48 hours inactivity

### Performance Tips:

1. **Upgrade to CPU persistent** ($60/month):
   - No cold starts
   - Always running
   - Better performance

2. **Use Neon Auto-suspend:**
   - Wakes in <1 second
   - No additional cost
   - Transparent to users

3. **Cache OpenAI responses:**
   - Save costs
   - Faster responses
   - Add Redis if needed

---

## 🐛 Troubleshooting

### Issue: "Application failed to start"

**Check logs for:**

```bash
# Missing secret
ERROR: OPENAI_API_KEY environment variable is required
→ Solution: Add OPENAI_API_KEY in Space secrets

# Database connection failed
ERROR: could not connect to server
→ Solution: Check DATABASE_URL has ?sslmode=require

# Invalid API key
ERROR: 401 Unauthorized
→ Solution: Regenerate OpenAI API key
```

### Issue: "Chatbot not working"

**Verify:**

1. OPENAI_API_KEY is set in Space secrets
2. OpenAI account has credits
3. Check logs for OpenAI errors

**Test directly:**

```bash
curl -X POST https://YOUR_USERNAME-todo-backend.hf.space/api/chatbot/chat \
  -H "Content-Type: application/json" \
  -d '{"message": "hello"}'
```

### Issue: "CORS errors in frontend"

**Fix:**

1. Update Space secret `FRONTEND_URL` to exact frontend URL
2. Restart Space (Settings → Factory reboot)
3. Clear browser cache

### Issue: "Database migrations not applied"

**Symptoms:** "Table does not exist" errors

**Solution:**

```bash
# Run migrations manually on Neon
export DATABASE_URL="your-neon-url"
cd backend
uv run alembic upgrade head
```

### Issue: "Space is sleeping"

**Symptoms:** First request takes 30+ seconds

**Solutions:**

1. **Free option:** Just wait (auto-wakes)
2. **Paid option:** Upgrade to persistent ($60/month)
3. **Workaround:** Ping endpoint every 10 minutes:
   ```bash
   # Cron job or GitHub Actions
   */10 * * * * curl https://YOUR_USERNAME-todo-backend.hf.space/health
   ```

---

## 🔒 Security Checklist

Before going live:

- [ ] All secrets in HuggingFace Secrets (not in code)
- [ ] `DEBUG=false` in production
- [ ] `ENVIRONMENT=production`
- [ ] Database has strong password
- [ ] OpenAI API key has usage limits set
- [ ] Qdrant has API key enabled
- [ ] CORS allows only your frontend domain
- [ ] Backend URL uses HTTPS
- [ ] Database connection uses SSL (`?sslmode=require`)

---

## 🚀 Next Steps

After successful backend deployment:

1. **Deploy Frontend to Vercel:**
   - See [docs/PRODUCTION_DEPLOYMENT.md](./docs/PRODUCTION_DEPLOYMENT.md)
   - Update `NEXT_PUBLIC_API_URL` to HuggingFace URL

2. **Set Up Custom Domain** (Optional):
   - HuggingFace Pro required
   - Settings → Custom domain

3. **Enable Monitoring:**
   - Set up UptimeRobot: https://uptimerobot.com
   - Monitor your Space URL

4. **Add Rate Limiting:**
   - Protect against abuse
   - Use slowapi or custom middleware

5. **Set Up Alerts:**
   - Email on Space downtime
   - OpenAI usage threshold alerts

---

## 📚 Additional Resources

- **HuggingFace Docs:** https://huggingface.co/docs/hub/spaces
- **Docker Spaces Guide:** https://huggingface.co/docs/hub/spaces-sdks-docker
- **Neon + HuggingFace:** https://neon.tech/docs/guides/huggingface
- **Project Docs:** [docs/README.md](./docs/README.md)

---

## ✅ Deployment Checklist

### Pre-Deployment

- [ ] Backend works locally
- [ ] All tests passing
- [ ] Migrations run on Neon database
- [ ] All credentials ready

### HuggingFace Setup

- [ ] Space created
- [ ] All secrets configured
- [ ] Dockerfile verified

### Deployment

- [ ] Code pushed to HuggingFace
- [ ] Build successful
- [ ] Application running

### Verification

- [ ] Health endpoint responds
- [ ] API docs accessible
- [ ] Chatbot status shows available
- [ ] Frontend can connect
- [ ] Sign up/sign in works
- [ ] Tasks CRUD works
- [ ] AI chatbot works

### Post-Deployment

- [ ] Frontend updated with backend URL
- [ ] End-to-end testing complete
- [ ] Monitoring set up
- [ ] Documentation updated

---

**Congratulations! Your backend is live on HuggingFace Spaces!** 🎉

**Need help?** Create an issue: https://github.com/shery123pk/shery_todo_app/issues

**Author:** Sharmeen Asif
**Last Updated:** 2025-12-26
