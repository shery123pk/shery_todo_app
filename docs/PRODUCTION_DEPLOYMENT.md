# Production Deployment Guide
**Author: Sharmeen Asif**

This guide covers deploying the Todo Application (Phase II) to production using HuggingFace Spaces, Vercel, and Neon PostgreSQL.

## Architecture Overview

```
┌─────────────────┐      ┌──────────────────┐      ┌─────────────────┐
│  Vercel         │─────▶│  HF Spaces       │─────▶│  Neon PostgreSQL│
│  (Frontend)     │      │  (Backend API)   │      │  (Database)     │
│  Next.js 15     │      │  FastAPI         │      │  PostgreSQL 16  │
└─────────────────┘      └──────────────────┘      └─────────────────┘
```

## Prerequisites

- [x] GitHub account with repository access
- [x] HuggingFace account (https://huggingface.co/join)
- [x] Vercel account (https://vercel.com/signup)
- [x] Neon account (https://neon.tech)
- [x] Git installed locally
- [x] UV package manager installed

## Step 1: Deploy Database to Neon

### 1.1 Create Neon Project

1. Go to https://console.neon.tech
2. Click **New Project**
3. Configure:
   - **Project name**: `todo-app-production`
   - **PostgreSQL version**: 16
   - **Region**: Choose closest to your users (e.g., US East, EU West)
   - **Compute size**: 0.25 CU (free tier) or higher

### 1.2 Get Connection String

After project creation, copy the connection string:
```
postgresql://[user]:[password]@[host]/[database]?sslmode=require
```

Save this as `DATABASE_URL` - you'll need it for backend deployment.

### 1.3 Run Database Migrations

```bash
# From project root
cd backend

# Set environment variable (Windows PowerShell)
$env:DATABASE_URL="postgresql://[user]:[password]@[host]/[database]?sslmode=require"

# Set environment variable (Linux/Mac)
export DATABASE_URL="postgresql://[user]:[password]@[host]/[database]?sslmode=require"

# Run migrations
uv run alembic upgrade head
```

Verify success:
```bash
uv run alembic current
# Should show: (head)
```

## Step 2: Deploy Backend to HuggingFace Spaces

### 2.1 Create HuggingFace Space

1. Go to https://huggingface.co/new-space
2. Configure:
   - **Space name**: `todo-backend`
   - **License**: MIT
   - **SDK**: Docker
   - **Hardware**: CPU basic (free tier)
   - **Visibility**: Public or Private

### 2.2 Prepare Backend for Deployment

The backend is already configured for port 7860 (HF Spaces requirement).

Verify `backend/Dockerfile`:
```dockerfile
# Should expose port 7860
EXPOSE 7860

# Should start with --port 7860
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "7860"]
```

### 2.3 Configure Secrets in HuggingFace

Go to your Space → Settings → Repository secrets:

Add these secrets:
```
DATABASE_URL=postgresql://[user]:[password]@[host]/[database]?sslmode=require
BETTER_AUTH_SECRET=[generate-with-command-below]
BETTER_AUTH_URL=https://[your-username]-todo-backend.hf.space
FRONTEND_URL=https://[your-vercel-app].vercel.app
```

Generate secure secret:
```bash
# Python
python -c "import secrets; print(secrets.token_urlsafe(32))"

# Or OpenSSL
openssl rand -base64 32
```

### 2.4 Deploy to HuggingFace

**Option A: Direct Git Push**

```bash
# From project root
cd backend

# Add HF remote (replace USERNAME and SPACE_NAME)
git remote add hf https://huggingface.co/spaces/USERNAME/SPACE_NAME
git subtree push --prefix backend hf main
```

**Option B: Upload via Web UI**

1. Go to your Space → Files
2. Upload entire `backend/` directory
3. Ensure `Dockerfile` is at root of Space

### 2.5 Monitor Deployment

1. Go to Space → App tab
2. Watch build logs
3. Wait for "Application startup complete"
4. Test API: `https://[your-username]-todo-backend.hf.space/docs`

### 2.6 Verify Backend Health

```bash
# Test health endpoint
curl https://[your-username]-todo-backend.hf.space/

# Expected response:
# {"message": "Todo API is running"}

# Test API documentation
curl https://[your-username]-todo-backend.hf.space/docs
```

## Step 3: Deploy Frontend to Vercel

### 3.1 Import Repository to Vercel

1. Go to https://vercel.com/new
2. Select **Import Git Repository**
3. Choose your GitHub repository: `shery_todo_app`
4. Configure:
   - **Framework Preset**: Next.js
   - **Root Directory**: `frontend/`
   - **Build Command**: `npm run build`
   - **Output Directory**: `.next`

### 3.2 Configure Environment Variables

In Vercel project settings → Environment Variables:

```
NEXT_PUBLIC_API_URL=https://[your-username]-todo-backend.hf.space
BETTER_AUTH_SECRET=[same-as-backend]
BETTER_AUTH_URL=https://[your-username]-todo-backend.hf.space
```

**IMPORTANT**: Use the same `BETTER_AUTH_SECRET` as backend!

### 3.3 Deploy

Click **Deploy** - Vercel will automatically:
1. Install dependencies
2. Run build
3. Deploy to production
4. Assign URL: `https://[project-name].vercel.app`

### 3.4 Update Backend FRONTEND_URL

1. Go back to HuggingFace Space settings
2. Update secret: `FRONTEND_URL=https://[project-name].vercel.app`
3. Restart Space (Settings → Factory Reboot)

### 3.5 Configure Custom Domain (Optional)

In Vercel project → Settings → Domains:
1. Add your domain (e.g., `todo.example.com`)
2. Configure DNS records as instructed
3. Wait for SSL certificate provisioning

## Step 4: Production Verification

### 4.1 Create Test User

```bash
# Using curl
curl -X POST https://[your-username]-todo-backend.hf.space/api/auth/signup \
  -H "Content-Type: application/json" \
  -d '{
    "email": "test@example.com",
    "password": "TestPassword123!",
    "full_name": "Test User"
  }'
```

### 4.2 Test Authentication Flow

1. Go to `https://[project-name].vercel.app`
2. Click "Sign Up"
3. Create account with email and password
4. Verify redirect to dashboard
5. Test "Remember me" checkbox

### 4.3 Test Todo Operations

1. **Create Task**: Click "Add task" → Enter title → Submit
2. **View Tasks**: Verify task appears in list
3. **Update Task**: Click edit → Modify title → Save
4. **Complete Task**: Click checkbox → Verify strikethrough
5. **Filter Tasks**: Test "All", "Active", "Completed" filters
6. **Delete Task**: Click delete → Verify removal

### 4.4 Test Multi-User Isolation

1. Open incognito window
2. Create different user account
3. Create tasks for second user
4. Verify tasks don't appear for first user

### 4.5 Performance Testing

```bash
# Test API response time
curl -w "@curl-format.txt" -o /dev/null -s https://[your-username]-todo-backend.hf.space/api/tasks

# Create curl-format.txt:
time_namelookup:  %{time_namelookup}s\n
time_connect:     %{time_connect}s\n
time_total:       %{time_total}s\n
```

Expected response times:
- API calls: < 500ms
- Page load: < 2s
- Task operations: < 300ms

## Step 5: Monitoring and Maintenance

### 5.1 Set Up Monitoring

**HuggingFace Spaces:**
- Monitor Space logs for errors
- Check CPU/Memory usage in Space dashboard
- Set up uptime monitoring (e.g., UptimeRobot)

**Vercel:**
- Use Vercel Analytics (included)
- Monitor deployment logs
- Check function execution times

**Neon:**
- Monitor database connections
- Check query performance
- Set up storage alerts

### 5.2 Database Backups

Neon automatically backs up your database. To create manual backup:

1. Go to Neon Console → Branches
2. Create new branch from `main`
3. Name it with date: `backup-2024-01-15`

### 5.3 Rolling Back Deployments

**Vercel:**
```bash
# List deployments
vercel list

# Promote previous deployment
vercel promote [deployment-url]
```

**HuggingFace:**
```bash
# Revert to previous commit
cd backend
git revert HEAD
git push hf main
```

## Troubleshooting

### Issue: "Authentication failed"

**Symptoms**: Cannot sign in/sign up
**Causes**:
- Mismatched `BETTER_AUTH_SECRET` between frontend and backend
- Incorrect `BETTER_AUTH_URL`

**Solution**:
1. Verify secrets match exactly in both deployments
2. Check URL format (no trailing slash)
3. Restart both deployments

### Issue: "Database connection failed"

**Symptoms**: 500 errors, "could not connect to server"
**Causes**:
- Invalid `DATABASE_URL`
- Neon database suspended (free tier)
- SSL mode not configured

**Solution**:
1. Verify connection string includes `?sslmode=require`
2. Check Neon project is active (not suspended)
3. Test connection with `psql`:
   ```bash
   psql "postgresql://[user]:[password]@[host]/[database]?sslmode=require"
   ```

### Issue: "CORS errors in browser console"

**Symptoms**: Frontend cannot call backend API
**Causes**:
- Incorrect `FRONTEND_URL` in backend
- CORS middleware not configured

**Solution**:
1. Update backend `FRONTEND_URL` to exact Vercel URL
2. Verify `backend/app/main.py` has correct CORS origins:
   ```python
   app.add_middleware(
       CORSMiddleware,
       allow_origins=[frontend_url],
       allow_credentials=True,
   )
   ```
3. Restart backend

### Issue: "Migrations out of sync"

**Symptoms**: "Table already exists" or "Column not found"
**Solution**:
```bash
# Connect to Neon database
export DATABASE_URL="postgresql://..."

# Check current migration
uv run alembic current

# Stamp to latest (if migrations were manually applied)
uv run alembic stamp head

# Or run missing migrations
uv run alembic upgrade head
```

## Cost Estimation

### Free Tier Limits

**Neon (Free Tier)**:
- 1 project
- 10 branches
- 3 GB storage
- Suspends after 5 minutes of inactivity

**HuggingFace Spaces (Free Tier)**:
- CPU basic hardware
- No GPU access
- Public spaces only
- May have cold starts

**Vercel (Hobby Plan - Free)**:
- 100 GB bandwidth/month
- 100 deployments/day
- 6000 build minutes/month

### Estimated Monthly Costs (Paid Tiers)

- **Neon Pro**: $19/month (always-on, no suspend, 8 GB storage)
- **HuggingFace Spaces**: $0 (CPU basic) or $60/month (dedicated CPU)
- **Vercel Pro**: $20/month (custom domains, analytics)

**Total for production**: $39-99/month depending on traffic

## Security Checklist

- [x] Database uses SSL connections (`?sslmode=require`)
- [x] Secrets not committed to repository
- [x] `BETTER_AUTH_SECRET` is cryptographically secure (32+ characters)
- [x] Sessions expire after 7 days (or 30 with "remember me")
- [x] Passwords hashed with bcrypt (10 rounds)
- [x] API rate limiting enabled (if implemented)
- [x] CORS restricted to frontend domain only
- [x] HTTPS enforced on all services

## Next Steps

After successful deployment:

1. **Custom Domain**: Set up custom domain in Vercel
2. **Email Service**: Integrate email for password resets (e.g., SendGrid)
3. **Analytics**: Add Google Analytics or Plausible
4. **Error Tracking**: Integrate Sentry for error monitoring
5. **CI/CD**: Set up GitHub Actions for automated deployments
6. **Documentation**: Create user guide and API documentation
7. **Testing**: Run load tests to determine scaling needs

## Support

For issues or questions:
- **HuggingFace**: https://huggingface.co/docs/hub/spaces
- **Vercel**: https://vercel.com/docs
- **Neon**: https://neon.tech/docs
- **Project Issues**: [GitHub repository issues]

---

**Deployment Checklist**:
- [ ] Neon database created and migrations run
- [ ] HuggingFace Space created with secrets configured
- [ ] Backend deployed and health check passes
- [ ] Vercel project created with environment variables
- [ ] Frontend deployed and accessible
- [ ] Backend FRONTEND_URL updated with Vercel URL
- [ ] Test user account created successfully
- [ ] All CRUD operations tested
- [ ] Multi-user isolation verified
- [ ] Production monitoring set up
