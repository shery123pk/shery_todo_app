# TaskFlow - AI-Powered Project Management System

**Author: Sharmeen Asif**

A modern, full-stack task management application with AI chatbot, voice commands, and multi-language support (English & Urdu).

[![Tech Stack](https://img.shields.io/badge/Stack-FastAPI%20|%20Next.js%2015%20|%20PostgreSQL-blue)](#tech-stack)
[![AI Powered](https://img.shields.io/badge/AI-OpenAI%20GPT--4-green)](#features)
[![Languages](https://img.shields.io/badge/Languages-English%20|%20اردو-orange)](#advanced-features)
[![Deploy](https://img.shields.io/badge/Deploy-Vercel%20|%20HuggingFace-purple)](#deployment)

**Live Demo:** [Coming Soon]

---

## ✨ Features

### 🎯 Core Features (10/10 Complete)

1. **Add Task** - Create tasks via API or natural language
2. **Delete Task** - Remove tasks by ID or description
3. **Update Task** - Modify title, description, priority, tags
4. **View Task List** - Display all tasks with filters
5. **Mark as Complete** - Toggle completion status
6. **Priorities & Tags** - Organize with low/medium/high priority and custom tags
7. **Search & Filter** - Keyword search across title/description, filter by status/priority/category
8. **Sort Tasks** - Order by created date, due date, priority, or title
9. **Recurring Tasks** - Auto-reschedule daily/weekly/monthly tasks
10. **Due Dates & Reminders** - Email notifications 30 minutes before deadline

### 🚀 Advanced Features (2/4 Complete)

11. **🌍 Multi-Language Support** - Automatic Urdu/English detection with RTL text rendering
12. **🎤 Voice Commands** - Speech-to-text and text-to-speech in both languages
13. **🧠 Reusable Intelligence** - *(Planned)* AI agents for task categorization and smart scheduling
14. **☁️ Cloud-Native Blueprints** - *(Planned)* Terraform templates and Kubernetes deployment

---

## 🎬 Demo Video

### Voice Commands Demo
```
🎤 "Show me all my tasks"
🎤 "Add buy groceries tomorrow at 3pm with high priority"
🎤 "Mark task 1 as complete"
🎤 "میرے سارے ٹاسک دکھائیں" (Show all my tasks in Urdu)
```

### Natural Language AI
```
💬 "Create a weekly team meeting every Monday at 10am"
💬 "Show all high priority incomplete tasks"
💬 "کل شام 3 بجے گروسری خریدنا شامل کریں" (Add task in Urdu)
```

---

## 🏗️ Tech Stack

### Frontend
- **Framework:** Next.js 15 (App Router)
- **Language:** TypeScript
- **Styling:** Tailwind CSS
- **UI Components:** shadcn/ui + Radix UI
- **State Management:** React Context API
- **Voice:** Web Speech API (Browser-based, FREE)

### Backend
- **Framework:** FastAPI (Python 3.11+)
- **Database:** PostgreSQL (Neon - Serverless)
- **ORM:** SQLModel + SQLAlchemy
- **Auth:** JWT + bcrypt password hashing
- **AI:** OpenAI GPT-4 with Function Calling
- **Vector DB:** Qdrant (Semantic search)
- **Email:** SMTP (Gmail/SendGrid)

### DevOps
- **Frontend Hosting:** Vercel (Free)
- **Backend Hosting:** Hugging Face Spaces (Free)
- **Database:** Neon PostgreSQL (Free tier)
- **Package Manager:** UV (Python), npm (Node.js)
- **Version Control:** Git + GitHub

---

## 📦 Project Structure

```
shery_todo_app/
├── backend/                      # FastAPI Backend
│   ├── app/
│   │   ├── routers/             # API endpoints (tasks, auth, chatbot)
│   │   ├── models/              # Database models (User, Task, Session)
│   │   ├── services/            # Business logic (email, auth, reminders)
│   │   ├── schemas/             # Pydantic schemas for validation
│   │   └── main.py              # FastAPI application
│   ├── alembic/                 # Database migrations
│   ├── tests/                   # Backend tests
│   └── Dockerfile               # Docker image for deployment
│
├── frontend/                     # Next.js Frontend
│   ├── app/                     # App Router pages
│   │   ├── auth/               # Authentication pages
│   │   ├── tasks/              # Task management
│   │   └── page.tsx            # Dashboard
│   ├── components/              # React components
│   │   ├── auth/               # Auth forms
│   │   ├── tasks/              # Task components
│   │   ├── dashboard/          # Dashboard widgets
│   │   └── chatbot/            # AI Chatbot UI
│   ├── contexts/                # React contexts
│   ├── hooks/                   # Custom React hooks
│   └── types/                   # TypeScript types
│
├── cli/                          # CLI Version (96% test coverage)
│   ├── app/                     # CLI application
│   └── tests/                   # 81 passing tests
│
├── docs/                         # Documentation
│   ├── DEPLOYMENT_GUIDE.md      # Vercel + HuggingFace deployment
│   ├── ADVANCED_FEATURES.md     # Voice & Multi-language guide
│   ├── FEATURES_COMPLETE.md     # All 10 core features
│   └── EMAIL_SETUP.md           # Email reminder setup
│
└── specs/                        # Feature specifications
    └── 001-project-management-system/
```

---

## 🚀 Quick Start

### Prerequisites
- Node.js 18+ and npm
- Python 3.11+ and UV
- PostgreSQL database (or use Neon)
- OpenAI API key (for AI chatbot)

### 1. Clone Repository

```bash
git clone https://github.com/shery123pk/shery_todo_app.git
cd shery_todo_app
```

### 2. Backend Setup

```bash
cd backend

# Create .env file (copy from .env.example)
cp .env.example .env

# Edit .env with your credentials:
# DATABASE_URL=postgresql+asyncpg://...
# OPENAI_API_KEY=sk-...
# JWT_SECRET=your-secret-key

# Install dependencies
uv sync

# Run database migrations
uv run alembic upgrade head

# Start backend server
uv run uvicorn app.main:app --reload --port 8001
```

**Backend will be running at:** http://localhost:8001

### 3. Frontend Setup

```bash
cd frontend

# Install dependencies
npm install

# Create .env.local file
echo "NEXT_PUBLIC_API_URL=http://localhost:8001" > .env.local

# Start development server
npm run dev
```

**Frontend will be running at:** http://localhost:3002

### 4. Access the Application

- **Web App:** http://localhost:3002
- **API Docs:** http://localhost:8001/docs
- **Health Check:** http://localhost:8001/health

---

## 🎯 Usage Examples

### Web Interface

1. **Sign Up:** Create account at `/auth/signup`
2. **Dashboard:** View task stats and quick actions
3. **Chatbot:** Click purple button to open AI assistant
4. **Voice Input:** Click microphone to speak commands
5. **Urdu Support:** Type in Urdu, AI responds in Urdu!

### CLI Version (Local)

```bash
cd cli
uv run todo add "My first task"
uv run todo list
uv run todo complete 1
uv run todo delete 1
```

### API Endpoints

**Authentication:**
```bash
# Sign up
curl -X POST http://localhost:8001/api/auth/signup \
  -H "Content-Type: application/json" \
  -d '{"email":"user@example.com","password":"pass123","full_name":"John Doe"}'

# Sign in (get access token)
curl -X POST http://localhost:8001/api/auth/login \
  -d "username=user@example.com&password=pass123"
```

**Tasks:**
```bash
# Create task
curl -X POST http://localhost:8001/api/tasks \
  -H "Authorization: Bearer YOUR_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"title":"Buy groceries","priority":"high"}'

# List tasks
curl http://localhost:8001/api/tasks?completed=false \
  -H "Authorization: Bearer YOUR_TOKEN"
```

**AI Chatbot:**
```bash
# Chat with AI
curl -X POST http://localhost:8001/api/chatbot/chat \
  -H "Authorization: Bearer YOUR_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"message":"Show me all my tasks"}'
```

---

## 🌍 Multi-Language Support

### Automatic Language Detection
- Detects Urdu text using Unicode range (U+0600 to U+06FF)
- Automatically switches AI prompts and UI direction (RTL/LTR)
- Supports mixing English and Urdu in conversation

### Example Commands

**English:**
```
"Show me all my tasks"
"Add buy milk tomorrow at 3pm"
"Delete task 1"
```

**Urdu:**
```
"میرے سارے ٹاسک دکھائیں"
"کل شام 3 بجے دودھ خریدنا شامل کریں"
"پہلا ٹاسک ڈیلیٹ کریں"
```

---

## 🎤 Voice Commands

### How to Use
1. Open chatbot (purple floating button)
2. Click microphone button
3. Speak your command in English or Urdu
4. AI responds with voice playback

### Supported Browsers
- ✅ Chrome/Chromium (Recommended)
- ✅ Edge
- ✅ Safari (14.1+)
- ⚠️ Firefox (Limited support)

### Voice Features
- Speech-to-text in English & Urdu
- Text-to-speech responses
- Realistic voice synthesis (Sara, Samantha, etc.)
- Visual recording indicator
- No token usage (browser-based)

---

## 📧 Email Reminders

Set up email notifications for task deadlines:

1. Create Gmail App Password: https://myaccount.google.com/apppasswords
2. Add to backend `.env`:
   ```env
   SMTP_HOST=smtp.gmail.com
   SMTP_PORT=587
   SMTP_USERNAME=your-email@gmail.com
   SMTP_PASSWORD=your-app-password
   FROM_EMAIL=your-email@gmail.com
   ```
3. Restart backend - reminders check every 10 minutes

**See:** [EMAIL_SETUP.md](./EMAIL_SETUP.md) for detailed guide

---

## 🚢 Deployment

### Frontend (Vercel)

1. Go to https://vercel.com
2. Import GitHub repo: `shery123pk/shery_todo_app`
3. Configure:
   - **Root Directory:** `frontend`
   - **Framework:** Next.js
   - **Environment Variable:** `NEXT_PUBLIC_API_URL=YOUR_BACKEND_URL`
4. Deploy!

### Backend (Hugging Face Spaces)

1. Go to https://huggingface.co/spaces
2. Create new Space with Docker SDK
3. Upload `backend/` files and `Dockerfile`
4. Add environment secrets:
   - `DATABASE_URL`
   - `OPENAI_API_KEY`
   - `QDRANT_URL`
   - `QDRANT_API_KEY`
   - `JWT_SECRET`
5. Space will be live at: `https://YOUR_USERNAME-taskflow-backend.hf.space`

**See:** [DEPLOYMENT_GUIDE.md](./DEPLOYMENT_GUIDE.md) for complete instructions

---

## 📊 Testing

### Backend Tests

```bash
cd backend
uv run pytest -v
uv run pytest --cov=app --cov-report=html
```

### Frontend Tests

```bash
cd frontend
npm run test
npm run test:coverage
```

### CLI Tests (96% Coverage)

```bash
cd cli
uv run pytest -v
# 81 tests passing
```

---

## 🎓 Built For

**Panaversity Hackathon Project**

Demonstrates:
- ✅ Full-stack development (FastAPI + Next.js)
- ✅ AI integration (OpenAI GPT-4)
- ✅ Modern UI/UX (Tailwind + shadcn/ui)
- ✅ Multi-language support
- ✅ Voice interface
- ✅ Production deployment
- ✅ Comprehensive documentation

---

## 💰 Cost Breakdown

| Service | Free Tier | Used For |
|---------|-----------|----------|
| **Vercel** | Unlimited personal projects | Frontend hosting |
| **Hugging Face** | Unlimited public spaces | Backend API |
| **Neon** | 0.5GB storage, 191h compute | PostgreSQL database |
| **Qdrant Cloud** | 1GB free | Vector search (optional) |
| **OpenAI API** | Pay-per-use (~$0.002/request) | AI chatbot |

**Monthly Cost:** ~$0-5 (depending on usage)

**Note:** Voice features are FREE (browser Web Speech API)

---

## 📚 Documentation

- **[DEPLOYMENT_GUIDE.md](./DEPLOYMENT_GUIDE.md)** - Deploy to Vercel + HuggingFace
- **[ADVANCED_FEATURES.md](./ADVANCED_FEATURES.md)** - Voice & Multi-language
- **[FEATURES_COMPLETE.md](./FEATURES_COMPLETE.md)** - All 10 core features
- **[EMAIL_SETUP.md](./EMAIL_SETUP.md)** - Email reminder configuration
- **[WAKE_UP_SUMMARY.md](./WAKE_UP_SUMMARY.md)** - Quick reference guide

---

## 🤝 Contributing

This project follows Spec-Driven Development (SDD) principles. See constitution and specs in `.specify/` and `specs/` directories.

---

## 📜 License

MIT License - See [LICENSE](./LICENSE) file

---

## 🔗 Links

- **GitHub:** https://github.com/shery123pk/shery_todo_app
- **Author:** Sharmeen Asif
- **Built with:** [Claude Code](https://claude.com/claude-code)

---

## 🎯 Quick Stats

- **Total Files:** 150+
- **Lines of Code:** 10,000+
- **Features:** 12 (10 core + 2 advanced)
- **CLI Test Coverage:** 96% (81 tests)
- **Languages:** English, اردو (Urdu)
- **Tech Stack:** 10+ technologies
- **Documentation:** 5 comprehensive guides

---

**Last Updated:** 2025-12-28
**Status:** Production Ready ✅
**Version:** 2.0.0

🤖 Built with AI • 🎓 Panaversity Project • 🚀 Ready to Deploy
