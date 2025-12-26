# ADR-005: Deployment Strategy - Hugging Face Spaces for Backend

**Status:** Accepted
**Date:** 2025-12-26
**Deciders:** Architect (shery123pk), AI Developer (Claude)
**Related Phase:** Phase 2 - Full-Stack Web
**Supersedes:** N/A

---

## Context and Problem Statement

Phase 2 requires deploying a full-stack web application with:
- **Frontend**: Next.js 15 App Router
- **Backend**: FastAPI REST API
- **Database**: Neon PostgreSQL (serverless, external)

We need hosting platforms that:
- Support free tier for hackathon demos
- Provide easy deployment workflow
- Scale to production if needed
- Align with AI/developer community focus

**Key Questions:**
1. Where to host FastAPI backend?
2. Where to host Next.js frontend?
3. How to connect frontend ↔ backend ↔ database?
4. What are deployment requirements (ports, Docker, secrets)?

---

## Decision Drivers

### Must Have
- ✅ **Free Tier**: Sufficient for hackathon demo without ongoing costs
- ✅ **Docker Support**: Backend needs containerization
- ✅ **FastAPI Compatible**: Must run Python 3.13+ with uvicorn
- ✅ **External Database**: Must connect to Neon PostgreSQL via URL
- ✅ **Secrets Management**: Secure env var storage (DATABASE_URL, JWT secrets)
- ✅ **CORS Support**: Frontend and backend on different domains

### Should Have
- 🎯 **Easy Deployment**: Git push to deploy or one-click setup
- 🎯 **Auto-Scaling**: Handle traffic spikes (10-100 concurrent users)
- 🎯 **Community Visibility**: Public showcase potential
- 🎯 **API Documentation**: Access to /docs endpoint
- 🎯 **Global CDN**: Fast frontend delivery worldwide

### Nice to Have
- 💡 **CI/CD Integration**: GitHub Actions support
- 💡 **Custom Domains**: Brandable URLs
- 💡 **Analytics**: Built-in usage metrics
- 💡 **Uptime Monitoring**: Health checks and alerts

---

## Considered Options

### Option 1: Hugging Face Spaces (Docker) ✅ SELECTED

**Backend: Hugging Face Spaces (Docker SDK)**
**Frontend: Vercel**
**Database: Neon PostgreSQL**

#### Hugging Face Spaces - Backend

**Deployment URL**: `https://[username]-todo-backend.hf.space`

**Pros:**
- ✅ **Free Tier**: Generous CPU tier for demos (2 vCPU, 16GB RAM)
- ✅ **Docker Support**: Full Docker container support (any Python version, dependencies)
- ✅ **Port Requirement**: Standard port 7860 (well-documented)
- ✅ **Community Focus**: AI/ML community visibility (aligns with hackathon theme)
- ✅ **Git Integration**: Deploy from GitHub repository
- ✅ **Secrets Management**: Built-in secrets UI (DATABASE_URL, BETTER_AUTH_SECRET)
- ✅ **Persistent Storage**: Optional for logs/cache (not needed for stateless API)
- ✅ **Public API Access**: /docs endpoint publicly accessible
- ✅ **Zero Cold Start**: Always-on free tier (no sleep mode)

**Cons:**
- ⚠️ **Port 7860 Required**: Must configure uvicorn to listen on 7860 (not flexible)
- ⚠️ **CPU-Based Scaling**: No GPU needed (actually a pro for cost)
- ⚠️ **Custom Domain Limitations**: Subdomain only (no apex domain on free tier)
- ⚠️ **Newer Platform**: Less mature than Heroku/Vercel (but actively developed)

**Configuration:**

```dockerfile
# backend/Dockerfile (Hugging Face compatible)
FROM python:3.13-slim

WORKDIR /app

# Copy requirements
COPY pyproject.toml ./
RUN pip install --no-cache-dir -e .

# Copy application code
COPY app/ ./app/

# Expose HF required port
EXPOSE 7860

# Run uvicorn on port 7860
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "7860"]
```

**Secrets Configuration** (via HF Space UI):
```bash
DATABASE_URL=postgresql://user:pass@ep-xxx.neon.tech/neondb?sslmode=require
BETTER_AUTH_SECRET=your-secret-key-here
BETTER_AUTH_URL=https://[username]-todo-backend.hf.space
FRONTEND_URL=https://[your-app].vercel.app
```

#### Vercel - Frontend

**Deployment URL**: `https://[your-app].vercel.app`

**Pros:**
- ✅ **Next.js Optimized**: Built specifically for Next.js (creators of Next.js)
- ✅ **Free Tier**: Generous (100GB bandwidth/month)
- ✅ **Global CDN**: Edge network worldwide
- ✅ **Zero-Config Deploy**: Push to GitHub, auto-deploy
- ✅ **Env Vars**: Easy secrets management
- ✅ **Preview Deployments**: Auto-preview for PRs
- ✅ **Analytics**: Built-in Web Vitals tracking

**Cons:**
- ⚠️ **Vendor Lock-In**: Optimized for Vercel platform
- ⚠️ **Serverless Functions**: Limited to 10s execution (not relevant for frontend-only)

**Configuration:**

```bash
# frontend/.env.production
NEXT_PUBLIC_API_URL=https://[username]-todo-backend.hf.space
```

---

### Option 2: Railway (Backend) + Vercel (Frontend)

**Provider:** Railway.app (backend), Vercel (frontend)

**Pros:**
- ✅ **Simple Deployment**: Git push to deploy
- ✅ **Flexible Ports**: Any port (not fixed like HF)
- ✅ **Database Integration**: Built-in PostgreSQL option
- ✅ **Good DX**: Developer-friendly UI

**Cons:**
- ❌ **No Free Tier**: $5/month minimum after trial ends
- ❌ **Cost**: Not sustainable for demo/hackathon without payment
- ❌ **Trial Limits**: 500 hours/month (requires credit card)

**Decision**: Rejected due to lack of permanent free tier.

---

### Option 3: Render (Backend) + Vercel (Frontend)

**Provider:** Render.com (backend), Vercel (frontend)

**Pros:**
- ✅ **Free Tier**: 750 hours/month free for web services
- ✅ **Docker Support**: Native Docker deployment
- ✅ **Managed PostgreSQL**: Optional (but we use Neon)

**Cons:**
- ❌ **Cold Start**: Free tier spins down after 15 minutes inactivity (~1 minute resume)
- ❌ **Limited Resources**: 512MB RAM (tight for FastAPI + dependencies)
- ❌ **Monthly Limits**: 750 hours = ~31 days (barely covers full month)

**Decision**: Rejected due to cold start latency and resource limits.

---

### Option 4: Fly.io (Backend) + Vercel (Frontend)

**Provider:** Fly.io (backend), Vercel (frontend)

**Pros:**
- ✅ **Free Tier**: 3 shared-cpu VMs with 256MB RAM
- ✅ **Global Deploy**: Edge deployment worldwide
- ✅ **Docker Native**: First-class Docker support

**Cons:**
- ❌ **RAM Limits**: 256MB per VM (too small for FastAPI + SQLModel)
- ❌ **Complexity**: More complex setup than HF Spaces
- ❌ **Credit Card Required**: Must provide payment method

**Decision**: Rejected due to RAM limitations and complexity.

---

### Option 5: Hugging Face Spaces (Static) for Frontend

**Alternative**: Deploy both frontend and backend to Hugging Face Spaces

**Pros:**
- ✅ **Single Platform**: Everything on HF
- ✅ **Simplicity**: One deployment pipeline

**Cons:**
- ❌ **Not Optimized for Next.js**: Static Space lacks Next.js optimizations (SSR, ISR, API routes)
- ❌ **No Edge Network**: Slower than Vercel CDN
- ❌ **Build Complexity**: Must build Next.js to static export (loses dynamic features)

**Decision**: Use Vercel for frontend (superior Next.js support), HF for backend only.

---

## Decision Outcome

**Chosen Option:** **Hugging Face Spaces (Docker) for Backend + Vercel for Frontend** ✅

### Rationale

1. **Free & Sustainable**: Both platforms offer generous free tiers suitable for long-term demos
2. **Community Alignment**: HF Spaces visibility aligns with AI/ML hackathon theme
3. **Optimal Performance**: Vercel's Next.js optimization + HF's always-on backend
4. **Developer Experience**: Simple deployment (git push), good docs, active communities
5. **Scalability Path**: Both platforms offer paid tiers if demo needs scaling

**Trade-off Accepted**: Port 7860 requirement (HF Spaces) is minor constraint - easy to configure in Dockerfile.

---

## Implementation

### Architecture Diagram

```
┌─────────────────────────────────────────────────────────────────┐
│                      PRODUCTION DEPLOYMENT                       │
└─────────────────────────────────────────────────────────────────┘

┌──────────────────┐      HTTPS       ┌───────────────────┐
│   User Browser   │ ────────────────> │  Vercel (Frontend) │
│                  │                   │  Next.js 15       │
└──────────────────┘                   │  Global CDN       │
                                       └───────────────────┘
                                              │
                                              │ API Calls
                                              │ (CORS enabled)
                                              ▼
                                       ┌───────────────────┐
                                       │  HF Space (Backend)│
                                       │  FastAPI          │
                                       │  Port 7860        │
                                       │  Docker Container │
                                       └───────────────────┘
                                              │
                                              │ PostgreSQL
                                              │ (DATABASE_URL)
                                              ▼
                                       ┌───────────────────┐
                                       │  Neon PostgreSQL  │
                                       │  Serverless       │
                                       │  (Cloud)          │
                                       └───────────────────┘

┌─────────────────────────────────────────────────────────────────┐
│                    LOCAL DEVELOPMENT                             │
└─────────────────────────────────────────────────────────────────┘

$ docker-compose up

┌──────────────┐      ┌──────────────┐      ┌──────────────┐
│  Frontend    │      │  Backend     │      │  Neon Dev    │
│  localhost   │ ───> │  localhost   │ ───> │  Branch      │
│  :3000       │      │  :8000       │      │  (cloud)     │
└──────────────┘      └──────────────┘      └──────────────┘
```

---

### Backend Deployment (Hugging Face Spaces)

#### Step 1: Create Hugging Face Space

1. Go to https://huggingface.co/spaces
2. Click "Create new Space"
3. **Space name**: `todo-backend` (becomes `[username]-todo-backend`)
4. **Space SDK**: Docker
5. **Visibility**: Public (for demo) or Private
6. Click "Create Space"

#### Step 2: Configure Dockerfile

**File**: `backend/Dockerfile`

```dockerfile
FROM python:3.13-slim

# Set working directory
WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    gcc \
    postgresql-client \
    && rm -rf /var/lib/apt/lists/*

# Copy dependency files
COPY pyproject.toml README.md ./
COPY app/ ./app/

# Install Python dependencies
RUN pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir -e .

# Expose Hugging Face required port
EXPOSE 7860

# Health check
HEALTHCHECK --interval=30s --timeout=10s --start-period=40s --retries=3 \
  CMD python -c "import requests; requests.get('http://localhost:7860/health')"

# Run application
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "7860", "--workers", "1"]
```

**Key Requirements**:
- ✅ **Port 7860**: HF Spaces requirement (non-negotiable)
- ✅ **Host 0.0.0.0**: Listen on all interfaces
- ✅ **Single Worker**: Free tier has limited resources
- ✅ **Health Check**: Optional but recommended

#### Step 3: Configure FastAPI for HF Spaces

**File**: `backend/app/main.py`

```python
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import os

app = FastAPI(
    title="Todo API",
    description="Full-Stack Todo Application - Phase 2",
    version="1.0.0",
    docs_url="/docs",  # Swagger UI
    redoc_url="/redoc",  # ReDoc
)

# CORS Configuration
frontend_url = os.getenv("FRONTEND_URL", "http://localhost:3000")
app.add_middleware(
    CORSMiddleware,
    allow_origins=[frontend_url, "https://*.vercel.app"],  # Vercel preview deploys
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/health")
async def health_check():
    """Health check endpoint for HF Spaces."""
    return {"status": "healthy", "service": "todo-backend"}

@app.get("/")
async def root():
    """Root endpoint with API info."""
    return {
        "message": "Todo API - Phase 2",
        "docs": "/docs",
        "health": "/health"
    }

# Import routers
from app.routers import tasks, auth
app.include_router(auth.router, prefix="/api/auth", tags=["Authentication"])
app.include_router(tasks.router, prefix="/api/tasks", tags=["Tasks"])
```

#### Step 4: Set Secrets in HF Space

1. Go to your Space settings → "Variables and Secrets"
2. Add secrets:

```bash
DATABASE_URL = postgresql://user:pass@ep-xxx.neon.tech/neondb?sslmode=require
BETTER_AUTH_SECRET = your-secret-key-generate-with-openssl-rand-base64-32
BETTER_AUTH_URL = https://[username]-todo-backend.hf.space
FRONTEND_URL = https://[your-app].vercel.app
```

#### Step 5: Deploy to HF Space

**Option A: Git Push** (Recommended)
```bash
git remote add hf https://huggingface.co/spaces/[username]/todo-backend
git push hf main
```

**Option B: GitHub Sync**
- Link GitHub repo to HF Space in settings
- Auto-deploy on push to main

#### Step 6: Verify Deployment

- **API Root**: https://[username]-todo-backend.hf.space/
- **Swagger Docs**: https://[username]-todo-backend.hf.space/docs
- **Health Check**: https://[username]-todo-backend.hf.space/health

---

### Frontend Deployment (Vercel)

#### Step 1: Connect GitHub Repository

1. Go to https://vercel.com
2. Click "Add New" → "Project"
3. Import GitHub repository: `shery_todo_app`
4. Vercel auto-detects Next.js

#### Step 2: Configure Build Settings

**Root Directory**: `frontend/`

Vercel auto-configures:
- **Framework**: Next.js
- **Build Command**: `npm run build`
- **Output Directory**: `.next`
- **Install Command**: `npm install`

#### Step 3: Set Environment Variables

```bash
NEXT_PUBLIC_API_URL = https://[username]-todo-backend.hf.space
```

#### Step 4: Deploy

Click "Deploy" → Vercel builds and deploys automatically.

**Deployment URL**: https://[your-app].vercel.app

#### Step 5: Update Backend CORS

Update HF Space secret `FRONTEND_URL` with actual Vercel URL:
```bash
FRONTEND_URL = https://[your-app].vercel.app
```

---

### Local Development Environment

**File**: `docker-compose.yml` (unchanged)

```yaml
version: '3.8'

services:
  backend:
    build: ./backend
    ports:
      - "8000:8000"  # Local uses 8000, production uses 7860
    environment:
      - DATABASE_URL=${DATABASE_URL}  # Neon dev branch
      - BETTER_AUTH_SECRET=${BETTER_AUTH_SECRET}
      - FRONTEND_URL=http://localhost:3000
    volumes:
      - ./backend:/app
    command: uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload

  frontend:
    build: ./frontend
    ports:
      - "3000:3000"
    environment:
      - NEXT_PUBLIC_API_URL=http://localhost:8000
    volumes:
      - ./frontend:/app
      - /app/node_modules
    command: npm run dev

  # Optional: Local PostgreSQL (alternative to Neon dev branch)
  # db:
  #   image: postgres:16-alpine
  #   environment:
  #     POSTGRES_USER: todo_user
  #     POSTGRES_PASSWORD: todo_password
  #     POSTGRES_DB: todo_db
  #   ports:
  #     - "5432:5432"
```

**Start Local Dev**:
```bash
docker-compose up
```

- Frontend: http://localhost:3000
- Backend: http://localhost:8000
- API Docs: http://localhost:8000/docs

---

## Consequences

### Positive
- ✅ **Zero Cost**: Permanent free tier for both platforms
- ✅ **Simple Deployment**: Git push to deploy
- ✅ **Community Visibility**: HF Space public showcase
- ✅ **Production Ready**: Both platforms scale to paid tiers if needed
- ✅ **Best-in-Class Tools**: Vercel for Next.js, HF for ML/AI community
- ✅ **Separate Concerns**: Frontend and backend can scale independently

### Negative
- ⚠️ **Port 7860 Constraint**: Must configure uvicorn for HF
  - **Mitigation**: Simple one-line change in Dockerfile CMD
- ⚠️ **Cross-Domain CORS**: Frontend and backend on different domains
  - **Mitigation**: Properly configured CORS middleware (already planned)
- ⚠️ **Two Deployment Pipelines**: Must deploy frontend and backend separately
  - **Mitigation**: Can automate with GitHub Actions

### Neutral
- 🔄 **Learning Curve**: HF Spaces newer than Heroku/Railway
  - **Acceptable**: Good documentation, active community

---

## Deployment Checklist

### Pre-Deployment

- [ ] Backend Dockerfile uses port 7860
- [ ] FastAPI configured with CORS for Vercel domain
- [ ] Health check endpoint implemented (`/health`)
- [ ] Environment variables documented
- [ ] Secrets generated (BETTER_AUTH_SECRET)
- [ ] Neon database created and migrated

### Backend (HF Space)

- [ ] HF Space created (`[username]-todo-backend`)
- [ ] Docker SDK selected
- [ ] Secrets configured in HF Space settings
- [ ] Dockerfile tested locally with port 7860
- [ ] Pushed to HF Space (git or GitHub sync)
- [ ] Verified /docs endpoint accessible
- [ ] Verified /health endpoint returns 200

### Frontend (Vercel)

- [ ] GitHub repo connected to Vercel
- [ ] Root directory set to `frontend/`
- [ ] Environment variable `NEXT_PUBLIC_API_URL` set to HF Space URL
- [ ] Deployment successful
- [ ] Verified frontend loads and can reach backend API

### Post-Deployment

- [ ] Updated backend CORS with production Vercel URL
- [ ] Tested full user journey (signup → login → CRUD → logout)
- [ ] Verified HTTPS works (both platforms)
- [ ] Documented URLs in README.md
- [ ] Created demo user account for showcase

---

## Monitoring & Maintenance

### Hugging Face Space

- **Logs**: View in Space UI → "Logs" tab
- **Restart**: Space UI → "Factory Restart"
- **Metrics**: View in "Analytics" tab (if enabled)
- **Uptime**: HF free tier is always-on (no sleep)

### Vercel

- **Logs**: Vercel dashboard → Project → Deployments → View logs
- **Analytics**: Built-in Web Vitals
- **Redeploy**: Trigger from GitHub commit or manual trigger

### Neon Database

- **Metrics**: Neon console → Project → Metrics
- **Branching**: Create dev/staging branches for testing
- **Backups**: Point-in-time recovery available

---

## Cost Analysis

### Free Tier Comparison

| Platform | Free Tier | Limits | Sufficient for Demo? |
|----------|-----------|--------|---------------------|
| **HF Space** | 2 vCPU, 16GB RAM | Always-on, 50GB storage | ✅ Yes |
| **Vercel** | 100GB bandwidth | 100 deployments/day | ✅ Yes |
| **Neon** | 0.5GB storage | 3GB bandwidth/month | ✅ Yes (estimated 10K tasks) |

**Total Monthly Cost**: **$0** for demo/hackathon 🎉

### Upgrade Path (if needed)

| Platform | Paid Tier | Cost | When to Upgrade |
|----------|-----------|------|-----------------|
| **HF Space** | Pro | $9/month | >50 concurrent users |
| **Vercel** | Pro | $20/month | >100GB bandwidth |
| **Neon** | Pro | $19/month | >0.5GB data |

---

## Alternatives Rejected

### Why Not Railway?
- No permanent free tier ($5/month minimum)
- Cost not sustainable for demo

### Why Not Render?
- Cold start latency (15 min inactivity → 1 min resume)
- 512MB RAM too tight for FastAPI + SQLModel

### Why Not Fly.io?
- 256MB RAM insufficient
- Credit card required
- More complex than HF Spaces

### Why Not HF Static Space for Frontend?
- Not optimized for Next.js (no SSR, ISR)
- Slower than Vercel CDN
- Loses Next.js dynamic features

---

## References

- **Hugging Face Spaces Docs**: https://huggingface.co/docs/hub/spaces-overview
- **HF Docker Spaces**: https://huggingface.co/docs/hub/spaces-sdks-docker
- **Vercel Next.js Docs**: https://vercel.com/docs/frameworks/nextjs
- **Neon Vercel Integration**: https://neon.tech/docs/guides/vercel
- **FastAPI Deployment**: https://fastapi.tiangolo.com/deployment/docker

---

## Related ADRs

- **ADR-001:** ID Migration Strategy (UUID for distributed systems)
- **ADR-002:** Monorepo Structure (Phase 1 independence preserved)
- **ADR-003:** Database Choice (Neon PostgreSQL serverless)
- **ADR-004:** Authentication Strategy (Better Auth with JWT)

---

**Decision Made By:** Architect + AI Developer
**Date Approved:** 2025-12-26
**Implementation Status:** 📋 Planned for Phase 2
**Review Date:** After Phase 2 deployment (validate performance/costs)
