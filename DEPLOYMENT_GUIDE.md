# 🚀 Deployment Guide - Vercel + Hugging Face

## Overview
Deploy your Todo App for Panaversity Faculty Demo:
- **Frontend:** Vercel (Free)
- **Backend:** Hugging Face Spaces (Free)
- **Database:** Neon PostgreSQL (Free)
- **CLI:** Works locally (already tested ✅)

---

## 📋 Prerequisites

Before deploying, make sure you have:
- ✅ GitHub account
- ✅ Vercel account (free at vercel.com)
- ✅ Hugging Face account (free at huggingface.co)
- ✅ Neon database already set up (you have this)
- ✅ OpenAI API key (you have this)

---

## 🎯 Deployment Steps

### Step 1: Push to GitHub

```bash
# Initialize git (if not already)
cd Z:\hk-2do\shery_todo_app
git init

# Add .gitignore
echo "node_modules/" >> .gitignore
echo ".env*" >> .gitignore
echo ".venv/" >> .gitignore
echo "__pycache__/" >> .gitignore
echo "*.pyc" >> .gitignore
echo ".next/" >> .gitignore
echo "uv.lock" >> .gitignore

# Add all files
git add .

# Commit
git commit -m "Initial commit - Full-stack todo app with CLI"

# Create GitHub repo (go to github.com/new)
# Then push
git remote add origin https://github.com/YOUR_USERNAME/shery-todo-app.git
git branch -M main
git push -u origin main
```

---

### Step 2: Deploy Backend to Hugging Face

**Option A: Using Hugging Face Web UI (Easier)**

1. Go to https://huggingface.co/spaces
2. Click "Create new Space"
3. Settings:
   - **Name:** `shery-todo-backend`
   - **SDK:** Docker
   - **Visibility:** Public
   - Click "Create Space"

4. Add files to your space:
   - Copy all files from `backend/` folder
   - Add `Dockerfile` (see below)
   - Add `.env` with your secrets

**Dockerfile for Hugging Face:**
```dockerfile
FROM python:3.11-slim

WORKDIR /app

# Install uv
RUN pip install uv

# Copy requirements
COPY pyproject.toml ./
COPY app ./app

# Install dependencies
RUN uv pip install --system -e .

# Expose port
EXPOSE 7860

# Run app on Hugging Face port
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "7860"]
```

5. Add secrets in Space Settings:
   - `DATABASE_URL` = your Neon connection string
   - `OPENAI_API_KEY` = your OpenAI key
   - `QDRANT_URL` = your Qdrant URL
   - `QDRANT_API_KEY` = your Qdrant key
   - `BETTER_AUTH_SECRET` = your auth secret

6. Your backend will be live at:
   `https://YOUR_USERNAME-shery-todo-backend.hf.space`

**Option B: Using Hugging Face CLI (Advanced)**

```bash
# Install Hugging Face CLI
pip install huggingface-hub

# Login
huggingface-cli login

# Create space
huggingface-cli repo create shery-todo-backend --type space --space_sdk docker

# Clone and add files
git clone https://huggingface.co/spaces/YOUR_USERNAME/shery-todo-backend
cd shery-todo-backend

# Copy backend files
cp -r ../backend/* .

# Create Dockerfile (use content above)

# Commit and push
git add .
git commit -m "Add backend code"
git push
```

---

### Step 3: Deploy Frontend to Vercel

**Option A: Using Vercel Web UI (Easiest)**

1. Go to https://vercel.com
2. Click "Add New Project"
3. Import your GitHub repository
4. Configure settings:
   - **Framework Preset:** Next.js
   - **Root Directory:** `frontend`
   - **Build Command:** `npm run build`
   - **Install Command:** `npm install`

5. Add Environment Variables:
   ```
   NEXT_PUBLIC_API_URL=https://YOUR_USERNAME-shery-todo-backend.hf.space
   BETTER_AUTH_URL=https://YOUR_USERNAME-shery-todo-backend.hf.space
   ```

6. Click "Deploy"
7. Your app will be live at: `https://shery-todo-app.vercel.app`

**Option B: Using Vercel CLI**

```bash
# Install Vercel CLI
npm i -g vercel

# Login
vercel login

# Deploy
cd frontend
vercel

# Follow prompts:
# - Link to existing project? No
# - Project name: shery-todo-app
# - Framework: Next.js
# - Deploy? Yes

# Add environment variables
vercel env add NEXT_PUBLIC_API_URL production
# Enter: https://YOUR_USERNAME-shery-todo-backend.hf.space

vercel env add BETTER_AUTH_URL production
# Enter: https://YOUR_USERNAME-shery-todo-backend.hf.space

# Deploy to production
vercel --prod
```

---

### Step 4: Update CORS Settings

After deployment, update your backend `.env` on Hugging Face:

```bash
# In Hugging Face Space Settings -> Environment Variables
FRONTEND_URL=https://shery-todo-app.vercel.app
ALLOWED_ORIGINS=https://shery-todo-app.vercel.app,http://localhost:3002
```

---

## 🧪 Testing Deployment

### Test Backend:
```bash
curl https://YOUR_USERNAME-shery-todo-backend.hf.space/health
# Should return: {"status":"healthy","service":"project-management-api"}
```

### Test Frontend:
1. Open: `https://shery-todo-app.vercel.app`
2. Sign up / Sign in
3. Try chatbot
4. Test voice commands
5. Try Urdu: "میرے سارے ٹاسک دکھائیں"

---

## 📱 Demo for Panaversity Faculty

### Live URLs:
- **Frontend:** https://shery-todo-app.vercel.app
- **Backend:** https://YOUR_USERNAME-shery-todo-backend.hf.space
- **Docs:** https://YOUR_USERNAME-shery-todo-backend.hf.space/docs

### Features to Demonstrate:

1. **Web App:**
   - Sign up / Sign in
   - Dashboard with task stats
   - Create, edit, delete tasks
   - Kanban board

2. **Voice Commands (NEW!):**
   - Click mic button
   - Speak: "Show me all my tasks"
   - Bot speaks back!

3. **Multi-Language (NEW!):**
   - Type in Urdu
   - Bot responds in Urdu
   - RTL text support

4. **CLI (Local):**
   ```bash
   cd cli
   uv run todo add "Demo task"
   uv run todo list
   uv run todo complete 1
   ```

5. **All 10 Core Features:**
   - Add/Delete/Update/View tasks
   - Mark as complete
   - Priorities & tags
   - Search & filter
   - Sort tasks
   - Recurring tasks
   - Due dates & email reminders

---

## 💰 Cost Breakdown

| Service | Free Tier | Used For |
|---------|-----------|----------|
| Vercel | Unlimited personal projects | Frontend hosting |
| Hugging Face | Unlimited public spaces | Backend API |
| Neon | 0.5GB storage, 191 hours compute | PostgreSQL database |
| OpenAI API | Pay-per-use ($5 credit for new users) | AI Chatbot |

**Monthly Cost:** ~$0-5 (depending on OpenAI usage)

---

## 🔧 Troubleshooting

### Backend won't start on Hugging Face:
- Check logs in Space page
- Verify environment variables are set
- Ensure Dockerfile is correct
- Check port is 7860 (Hugging Face requirement)

### Frontend can't connect to backend:
- Verify `NEXT_PUBLIC_API_URL` in Vercel
- Check CORS settings in backend
- Make sure backend is running

### Database connection errors:
- Verify `DATABASE_URL` is correct
- Check Neon database is active
- Test connection locally first

---

## 🎓 For Panaversity Faculty

### Presentation Points:

1. **Full-Stack Architecture:**
   - Next.js 15 (Frontend)
   - FastAPI (Backend)
   - PostgreSQL (Database)
   - OpenAI GPT-4 (AI)

2. **Advanced Features:**
   - ✅ Voice input/output (NEW!)
   - ✅ Multi-language support (Urdu/English)
   - ✅ Real-time updates
   - ✅ Email reminders
   - ✅ Recurring tasks

3. **CLI Version:**
   - Clean architecture
   - 96% test coverage
   - 81 passing tests
   - Professional command-line interface

4. **Code Quality:**
   - TypeScript for type safety
   - Python type hints
   - Comprehensive documentation
   - Modular architecture

5. **Deployment:**
   - Production-ready
   - Scalable infrastructure
   - Free hosting
   - CI/CD ready

---

## 📊 Quick Stats

- **Total Files:** ~150
- **Lines of Code:** ~10,000+
- **Features:** 12 (10 core + 2 advanced)
- **Test Coverage:** 96% (CLI)
- **Documentation:** 5 comprehensive guides
- **Deployment Time:** ~30 minutes

---

## 🎯 Next Steps After Deployment

1. **Custom Domain (Optional):**
   - Buy domain on Namecheap
   - Add to Vercel project
   - Point to Vercel nameservers

2. **Analytics:**
   - Add Vercel Analytics
   - Track usage
   - Monitor performance

3. **CI/CD:**
   - Every git push = auto deploy
   - Already set up with Vercel
   - No configuration needed!

---

## 📞 Support

If you encounter issues:
1. Check logs on Vercel/Hugging Face
2. Review environment variables
3. Test locally first
4. Check CORS settings

---

**Ready to deploy?** Follow the steps above and your app will be live in 30 minutes! 🚀

**Your 5% limit** is safe - only chatbot uses tokens, all other features are free!
