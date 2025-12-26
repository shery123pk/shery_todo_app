# Production Deployment Checklist
**Author: Sharmeen Asif**
**Project: Todo Application - Phase II**

Use this checklist to ensure a smooth production deployment. Check off each item as you complete it.

---

## Pre-Deployment Checklist

### 1. Code Quality

- [ ] All Phase I tests passing (81/81 tests)
  ```bash
  cd cli && uv run pytest -v
  ```

- [ ] All Phase II backend tests passing
  ```bash
  cd backend && uv run pytest -v
  ```

- [ ] No TypeScript errors in frontend
  ```bash
  cd frontend && npm run build
  ```

- [ ] Code committed to Git
  ```bash
  git status  # Should show "nothing to commit, working tree clean"
  ```

- [ ] Pushed to GitHub remote
  ```bash
  git push origin main
  ```

### 2. Security Review

- [ ] No hardcoded secrets in codebase
  ```bash
  # Search for potential secrets
  grep -r "password\|secret\|api_key" --exclude-dir=.git --exclude-dir=node_modules --exclude-dir=__pycache__
  ```

- [ ] `.env` files are in `.gitignore`
  ```bash
  grep -E "^\.env$|^\.env\." .gitignore
  ```

- [ ] Database passwords are strong (20+ characters, mixed case, numbers, symbols)

- [ ] `BETTER_AUTH_SECRET` generated securely
  ```bash
  # Generate new secret
  python -c "import secrets; print(secrets.token_urlsafe(32))"
  ```

### 3. Environment Configuration

- [ ] Production `.env.production` file created (DO NOT commit!)

- [ ] All required environment variables documented

- [ ] Environment variables validated
  ```bash
  # Backend
  python scripts/verify-env.py backend

  # Frontend
  python scripts/verify-env.py frontend
  ```

---

## Phase 1: Database Deployment (Neon)

### Step 1.1: Create Neon Project

- [ ] Signed up at https://neon.tech
- [ ] Created new project: `todo-app-production`
- [ ] Selected region: ________________ (e.g., US East)
- [ ] PostgreSQL version: 16
- [ ] Copied connection string

**Connection String Format:**
```
postgresql://[user]:[password]@[host]/[database]?sslmode=require
```

**Your connection string:**
```
postgresql://____________________
```

### Step 1.2: Run Database Migrations

- [ ] Set `DATABASE_URL` environment variable
  ```bash
  # Windows PowerShell
  $env:DATABASE_URL="postgresql://..."

  # Linux/Mac
  export DATABASE_URL="postgresql://..."
  ```

- [ ] Verify connection
  ```bash
  cd backend
  uv run alembic current
  ```

- [ ] Run migrations
  ```bash
  uv run alembic upgrade head
  ```

- [ ] Verify migrations applied
  ```bash
  uv run alembic current
  # Should show: (head)
  ```

### Step 1.3: Test Database

- [ ] Can connect with psql
  ```bash
  psql "$DATABASE_URL"
  ```

- [ ] Tables created correctly
  ```sql
  \dt  -- List all tables
  -- Should see: users, tasks, sessions
  ```

- [ ] Can query tables
  ```sql
  SELECT COUNT(*) FROM users;
  SELECT COUNT(*) FROM tasks;
  ```

**Database Deployment Complete!** ✓

---

## Phase 2: Backend Deployment (HuggingFace Spaces)

### Step 2.1: Create HuggingFace Account

- [ ] Signed up at https://huggingface.co/join
- [ ] Email verified
- [ ] Username: ________________

### Step 2.2: Create New Space

- [ ] Visited https://huggingface.co/new-space
- [ ] Space name: `todo-backend`
- [ ] License: MIT
- [ ] SDK: Docker
- [ ] Hardware: CPU basic (free)
- [ ] Visibility: Public / Private (circle one)

**Your Space URL:**
```
https://huggingface.co/spaces/[USERNAME]/todo-backend
```

### Step 2.3: Configure Secrets

Go to Space Settings → Repository secrets

- [ ] Added `DATABASE_URL`
  ```
  Value: postgresql://[user]:[password]@[host]/[database]?sslmode=require
  ```

- [ ] Added `BETTER_AUTH_SECRET`
  ```
  Value: [32+ character random string]
  ```

- [ ] Added `BETTER_AUTH_URL`
  ```
  Value: https://[USERNAME]-todo-backend.hf.space
  ```

- [ ] Added `FRONTEND_URL` (placeholder, will update after Vercel deployment)
  ```
  Value: https://todo-app.vercel.app  # Update later!
  ```

### Step 2.4: Deploy Backend

**Option A: Git Subtree Push (Recommended)**

- [ ] Added HuggingFace remote
  ```bash
  cd backend
  git remote add hf https://huggingface.co/spaces/[USERNAME]/todo-backend
  ```

- [ ] Pushed backend code
  ```bash
  git subtree push --prefix backend hf main
  ```

**Option B: Manual Upload**

- [ ] Uploaded all files from `backend/` to Space via web UI
- [ ] Ensured `Dockerfile` is at root of Space

### Step 2.5: Verify Deployment

- [ ] Space build completed (no errors in logs)
- [ ] App is running (green status indicator)
- [ ] Health endpoint responds
  ```bash
  curl https://[USERNAME]-todo-backend.hf.space/
  # Expected: {"message":"Todo API is running"}
  ```

- [ ] API docs accessible
  ```
  https://[USERNAME]-todo-backend.hf.space/docs
  ```

**Backend Deployment Complete!** ✓

---

## Phase 3: Frontend Deployment (Vercel)

### Step 3.1: Create Vercel Account

- [ ] Signed up at https://vercel.com/signup
- [ ] Connected GitHub account
- [ ] Authorized Vercel to access repository

### Step 3.2: Import Repository

- [ ] Clicked "Import Project" on Vercel dashboard
- [ ] Selected repository: `shery_todo_app`
- [ ] Configure project settings:
  - Framework: Next.js
  - Root Directory: `frontend/`
  - Build Command: `npm run build`
  - Output Directory: `.next`

### Step 3.3: Set Environment Variables

- [ ] Added `NEXT_PUBLIC_API_URL`
  ```
  Value: https://[USERNAME]-todo-backend.hf.space
  ```

- [ ] Added `BETTER_AUTH_SECRET`
  ```
  Value: [SAME as backend - copy exactly!]
  ```

- [ ] Added `BETTER_AUTH_URL`
  ```
  Value: https://[USERNAME]-todo-backend.hf.space
  ```

**CRITICAL:** `BETTER_AUTH_SECRET` must match backend exactly!

### Step 3.4: Deploy

- [ ] Clicked "Deploy"
- [ ] Deployment succeeded (no errors)
- [ ] Production URL assigned: ________________.vercel.app

**Your Frontend URL:**
```
https://______________________.vercel.app
```

### Step 3.5: Update Backend Configuration

- [ ] Go back to HuggingFace Space settings
- [ ] Update `FRONTEND_URL` secret with Vercel URL
  ```
  Value: https://[YOUR-APP].vercel.app
  ```

- [ ] Restart Space (Settings → Factory Reboot)

**Frontend Deployment Complete!** ✓

---

## Phase 4: Integration Testing

### Step 4.1: Run Automated Tests

- [ ] Run production test suite
  ```bash
  python scripts/test-production.py \
    https://[USERNAME]-todo-backend.hf.space \
    https://[YOUR-APP].vercel.app
  ```

- [ ] All tests passed (0 failures)

### Step 4.2: Manual Testing

**Authentication Flow:**

- [ ] Open frontend URL in browser
- [ ] Can see login/signup page
- [ ] Click "Sign Up"
- [ ] Fill form with test credentials:
  - Email: test@example.com
  - Password: TestPassword123!
  - Name: Test User
- [ ] Submit form
- [ ] Redirected to dashboard (tasks page)

**Task Management:**

- [ ] Click "Add Task" or "+"
- [ ] Enter task title: "Buy groceries"
- [ ] Task appears in list
- [ ] Click checkbox to mark complete
- [ ] Task shows strikethrough/completed style
- [ ] Click "Edit" icon
- [ ] Change title to "Buy groceries (updated)"
- [ ] Changes saved and reflected
- [ ] Click "Delete" icon
- [ ] Task removed from list

**Filtering:**

- [ ] Create 3 tasks
- [ ] Complete 1 task
- [ ] Click "All" filter - shows 3 tasks
- [ ] Click "Active" filter - shows 2 tasks
- [ ] Click "Completed" filter - shows 1 task

**Session Persistence:**

- [ ] Sign out
- [ ] Close browser
- [ ] Reopen and visit frontend URL
- [ ] Click "Sign In" with same credentials
- [ ] See same tasks from before (data persisted)

**Multi-User Isolation:**

- [ ] Open incognito/private window
- [ ] Create different user account
  - Email: user2@example.com
  - Password: AnotherPassword123!
- [ ] Create tasks for user 2
- [ ] Switch back to original window (user 1)
- [ ] Verify user 2's tasks are NOT visible
- [ ] Verify user 1's tasks are still there

**Mobile Responsiveness:**

- [ ] Open frontend on mobile device (or use browser DevTools)
- [ ] Layout adapts to screen size
- [ ] All buttons/links tappable
- [ ] Forms usable on mobile
- [ ] No horizontal scrolling

### Step 4.3: Performance Testing

- [ ] Page load time < 2 seconds
  ```
  # Open DevTools → Network tab
  # Hard reload (Ctrl+Shift+R)
  # Check "Finish" time
  ```

- [ ] API calls respond < 500ms
  ```
  # DevTools → Network → XHR
  # Watch timing for API calls
  ```

- [ ] No console errors (DevTools → Console)

- [ ] Lighthouse score:
  - Performance: _____ / 100 (target: >90)
  - Accessibility: _____ / 100 (target: >90)
  - Best Practices: _____ / 100 (target: >90)
  - SEO: _____ / 100 (target: >90)

**Integration Testing Complete!** ✓

---

## Phase 5: Monitoring Setup

### Step 5.1: HuggingFace Monitoring

- [ ] Bookmark Space dashboard: https://huggingface.co/spaces/[USERNAME]/todo-backend
- [ ] Set up uptime monitor (e.g., UptimeRobot, Better Uptime)
  - URL to monitor: https://[USERNAME]-todo-backend.hf.space/
  - Check interval: 5 minutes
  - Alert contact: ________________ (email)

### Step 5.2: Vercel Monitoring

- [ ] Enable Vercel Analytics (Project → Analytics)
- [ ] Review deployment settings
- [ ] Set up custom domain (optional)

### Step 5.3: Neon Monitoring

- [ ] Review Neon dashboard metrics
- [ ] Check storage usage: _____ MB / 3 GB (free tier)
- [ ] Set up backup branch (Neon → Branches → Create branch from main)
  - Branch name: `backup-[DATE]`

**Monitoring Setup Complete!** ✓

---

## Phase 6: Documentation

### Step 6.1: Update README

- [ ] Add production URLs to README:
  ```markdown
  ## Live Demo

  - **Frontend**: https://[YOUR-APP].vercel.app
  - **Backend API**: https://[USERNAME]-todo-backend.hf.space
  - **API Docs**: https://[USERNAME]-todo-backend.hf.space/docs
  ```

- [ ] Add deployment status badges (optional):
  ```markdown
  ![Vercel](https://vercelbadges.vercel.app/api/[VERCEL_PROJECT_ID])
  ```

### Step 6.2: Document Credentials

**SECURE LOCATION ONLY - DO NOT COMMIT!**

Create `CREDENTIALS.txt` (add to `.gitignore`):

```
=== Todo App Production Credentials ===

Neon Database:
- Connection String: postgresql://...
- Project URL: https://console.neon.tech/app/projects/[PROJECT_ID]

HuggingFace Spaces:
- Space URL: https://huggingface.co/spaces/[USERNAME]/todo-backend
- App URL: https://[USERNAME]-todo-backend.hf.space

Vercel:
- Project URL: https://vercel.com/[USERNAME]/[PROJECT_NAME]
- App URL: https://[YOUR-APP].vercel.app

Secrets:
- BETTER_AUTH_SECRET: [REDACTED - stored in env]
- Database Password: [REDACTED - in connection string]

Created: [DATE]
```

**Documentation Complete!** ✓

---

## Final Checklist

- [ ] All services deployed and running
- [ ] All integration tests passing
- [ ] Monitoring configured
- [ ] Documentation updated
- [ ] Credentials backed up securely
- [ ] Team notified of deployment
- [ ] Users can access application

---

## Rollback Plan (If Issues Occur)

### Vercel Rollback

```bash
# List deployments
vercel list

# Promote previous working deployment
vercel promote [DEPLOYMENT_URL]
```

### HuggingFace Rollback

```bash
# Revert to previous commit
cd backend
git revert HEAD
git push hf main
```

### Database Rollback

```bash
# Downgrade one migration
uv run alembic downgrade -1

# Or specific version
uv run alembic downgrade [revision_id]
```

---

## Success Criteria

✅ **Deployment is successful if:**

1. Frontend loads without errors
2. Users can sign up and sign in
3. Tasks can be created, read, updated, deleted
4. Data persists across sessions
5. Multi-user isolation works correctly
6. No security vulnerabilities
7. Performance meets targets (< 2s page load, < 500ms API)
8. All monitoring systems operational

---

**Deployment Status:** ________________ (Complete / In Progress / Blocked)

**Deployed By:** ________________

**Deployment Date:** ________________

**Production URLs:**
- Frontend: ________________
- Backend: ________________
- API Docs: ________________

---

**Notes:**

[Add any deployment notes, issues encountered, or special configurations here]
