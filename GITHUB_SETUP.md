# GitHub Repository Setup Guide

## Step 1: Create Repository on GitHub

1. **Navigate to:** https://github.com/new
2. **Fill in details:**
   - **Owner:** shery123pk
   - **Repository name:** `shery_todo_app`
   - **Description:** `Evolution of Todo - 5-phase project demonstrating Spec-Driven Development from CLI to Full-Stack AI App`
   - **Visibility:** ✅ Public (required for Vercel/HuggingFace deployment)
   - **Initialize:** ❌ Do NOT check any boxes (no README, .gitignore, license)
3. **Click:** "Create repository"

## Step 2: Push Code to GitHub

After creating the repository, run these commands in your terminal:

```bash
# Navigate to project directory
cd Z:\hk-2do\shery_todo_app

# Add GitHub remote
git remote add origin https://github.com/shery123pk/shery_todo_app.git

# Verify remote
git remote -v

# Push master branch
git push -u origin master

# Push feature branch (preserves development history)
git push origin 001-cli-todo-app

# Verify everything is pushed
git branch -a
```

## Step 3: Verify on GitHub

Visit: https://github.com/shery123pk/shery_todo_app

You should see:
- ✅ README.md displayed on homepage
- ✅ All source code in `src/` directory
- ✅ Tests in `tests/` directory
- ✅ Documentation in `specs/` and `history/`
- ✅ 2 branches: `master` and `001-cli-todo-app`
- ✅ 2 commits on master (initial + merge)

## Step 4: Repository Settings (Optional but Recommended)

### Add Topics
Go to: https://github.com/shery123pk/shery_todo_app/settings

Add topics:
- `spec-driven-development`
- `claude-code`
- `python`
- `cli`
- `todo-app`
- `fastapi` (for Phase 2+)
- `nextjs` (for Phase 2+)
- `ai-powered`

### Enable Issues and Projects
- ✅ Issues (for tracking Phase 2+ work)
- ✅ Projects (optional, for roadmap visualization)

### Branch Protection (Recommended for Phase 2+)
Protect `master` branch:
- Go to Settings → Branches → Add branch protection rule
- Branch name pattern: `master`
- ✅ Require pull request reviews before merging
- ✅ Require status checks to pass before merging

## Step 5: Prepare for Deployment

### For Vercel (Phase 2 - Frontend)
1. Install Vercel CLI: `npm i -g vercel`
2. Link repo: `vercel link`
3. Deploy: `vercel --prod`

**Note:** Phase 1 (CLI only) cannot be deployed to Vercel yet. Wait for Phase 2 (Next.js frontend).

### For HuggingFace (Phase 2 - Backend API)
1. Create account: https://huggingface.co/join
2. Create Space: https://huggingface.co/new-space
3. Configure for Docker/FastAPI
4. Link GitHub repository

**Note:** Phase 1 (CLI only) cannot be deployed to HuggingFace yet. Wait for Phase 2 (FastAPI backend).

---

## 📋 Checklist

- [ ] Created repository on GitHub
- [ ] Pushed master branch
- [ ] Pushed 001-cli-todo-app branch
- [ ] Verified code is visible on GitHub
- [ ] Added repository topics
- [ ] Reviewed PHASE1_STATUS.md
- [ ] Ready to start Phase 2

---

## 🚀 Quick Command Reference

```bash
# Clone on another machine
git clone https://github.com/shery123pk/shery_todo_app.git
cd shery_todo_app

# Install and run
pip install uv
uv sync
uv run todo --help

# Run tests
uv run pytest

# Start development
git checkout -b feature/your-feature-name
# ... make changes ...
git commit -m "Your message"
git push origin feature/your-feature-name
```

---

**Repository URL:** https://github.com/shery123pk/shery_todo_app
**Created:** 2025-12-26
**Status:** Phase 1 Complete ✅
