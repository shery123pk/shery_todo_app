# Evolution of Todo
**Author: Sharmeen Asif**

A 5-phase project demonstrating Spec-Driven Development (SDD) from CLI to Full-Stack AI-Powered Application with Cloud Deployment.

## 🎯 Project Vision

This monorepo showcases the evolution of a todo application across five progressive phases, demonstrating:
- **Spec-Driven Development** with Claude Code and Spec-Kit Plus
- **AI as Sole Developer** (Claude) with Human as Architect
- **Full Traceability** from specs to code with ADRs and PHRs
- **Additive Evolution** where each phase builds on previous ones
- **Production Deployments** on Vercel (frontend), HuggingFace (backend), Neon (database), and DigitalOcean DOKS (cloud)

## 📊 Project Status

| Phase | Name | Status | Deployment |
|-------|------|--------|------------|
| **1** | CLI + In-Memory | ✅ Complete | Local |
| **2** | Full-Stack Web | ✅ Complete | Vercel + HuggingFace + Neon |
| **3** | AI-Powered Chatbot | ✅ Complete | Local / Docker |
| **4** | Local K8s Deployment | ✅ Complete | Minikube + Helm |
| **5** | Cloud Deployment | ✅ Complete | DigitalOcean DOKS + Kafka + Dapr |

## 🏗️ Monorepo Structure

```
shery_todo_app/
├── cli/                          # Phase 1: CLI Todo App ✅
│   ├── app/                      # Source code (models, storage, CLI)
│   ├── tests/                    # 81 tests, 96% coverage
│   └── pyproject.toml
├── backend/                      # Phase 2: FastAPI Backend ✅
│   ├── app/                      # API routes, models, auth, events
│   ├── alembic/                  # Database migrations
│   ├── tests/                    # Backend test suite
│   └── Dockerfile                # HuggingFace Spaces deployment
├── frontend/                     # Phase 2: Next.js Frontend ✅
│   ├── app/                      # App Router (auth, dashboard)
│   ├── components/               # React components (shadcn/ui)
│   ├── lib/                      # Utilities and API client
│   └── Dockerfile                # Vercel deployment
├── chatbot/                      # Phase 3: AI Chatbot ✅
│   ├── app/                      # MCP server, Claude agent, CLI
│   ├── tests/                    # Chatbot tests
│   └── Dockerfile                # Container deployment
├── k8s/                          # Phase 4: Kubernetes Manifests ✅
│   ├── *.yaml                    # K8s resources (namespace, deployments, services)
│   ├── helm/todo-app/            # Helm chart for todo application
│   └── deploy.sh                 # Minikube deployment script
├── infra/                        # Phase 5: Cloud Infrastructure ✅
│   ├── kafka/                    # Kafka + Zookeeper for event streaming
│   ├── dapr/                     # Dapr configuration (pub/sub, state store)
│   └── doks/terraform/           # Terraform IaC for DigitalOcean
├── .github/workflows/            # CI/CD Pipeline ✅
│   └── deploy.yml                # Automated testing and deployment
├── docs/                         # Documentation ✅
│   ├── PRODUCTION_DEPLOYMENT.md  # Production deployment guide
│   └── README.md                 # Documentation index
├── scripts/                      # Deployment Scripts ✅
│   ├── verify-env.py             # Environment validation
│   ├── test-production.py        # Production testing
│   └── deployment-checklist.md   # Step-by-step deployment
├── specs/                        # All phase specifications
│   └── 001-cli-todo-app/         # Phase 1 specs ✅
├── history/                      # Traceability artifacts
│   ├── adr/                      # Architecture Decision Records
│   └── prompts/                  # Prompt History Records (PHRs)
├── .specify/                     # Spec-Kit Plus configuration
│   ├── memory/constitution.md    # Project constitution
│   └── templates/                # SDD templates
└── README.md                     # This file
```

## 🚀 Quick Start

### Phase 1: CLI

```bash
# Navigate to CLI directory
cd cli

# Install dependencies
uv sync

# Use the CLI
uv run todo --help
uv run todo add "My first task"
uv run todo list
uv run todo complete 1
uv run todo delete 1

# Run tests
uv run pytest -v
```

### Phase 2: Full-Stack Web (Local Development)

```bash
# Backend
cd backend
uv sync
uv run alembic upgrade head
uv run uvicorn app.main:app --reload --port 8000

# Frontend (in new terminal)
cd frontend
npm install
npm run dev

# Access:
# - Frontend: http://localhost:3000
# - Backend API: http://localhost:8000
# - API Docs: http://localhost:8000/docs
```

### Phase 3: AI Chatbot

```bash
cd chatbot
uv sync

# Set environment variables
# ANTHROPIC_API_KEY=your-api-key
# API_URL=http://localhost:8000 (or your backend URL)

# Run chatbot
uv run chatbot

# Follow prompts to authenticate and chat
```

### Phase 4: Kubernetes (Minikube)

```bash
cd k8s

# Start Minikube and deploy all services
./deploy.sh

# Check deployment status
kubectl get pods -n todo-app
kubectl get services -n todo-app

# Access frontend
minikube service frontend-service -n todo-app
```

### Phase 5: Cloud Deployment

See [Production Deployment Guide](./docs/PRODUCTION_DEPLOYMENT.md) for detailed instructions on:
- Deploying to DigitalOcean DOKS with Terraform
- Setting up Kafka event streaming
- Configuring Dapr microservices
- Running CI/CD pipeline with GitHub Actions

## 📋 Phase Roadmap

### Phase 1: CLI + In-Memory ✅ COMPLETE

**Deliverables:**
- ✅ Command-line todo application with Typer
- ✅ In-memory storage with JSON persistence
- ✅ CRUD operations (add, list, update, delete, complete)
- ✅ 96% test coverage (81 tests passing)
- ✅ Full SDD workflow (constitution → spec → plan → tasks → implement)

**Tech Stack:** Python 3.13+, Typer, pytest, UV

**[View Phase 1 Details](./cli/README.md)**

---

### Phase 2: Full-Stack Web Application ✅ COMPLETE

**Deliverables:**
- ✅ REST API with FastAPI
- ✅ Next.js 15 frontend with shadcn/ui components
- ✅ PostgreSQL database (Neon-compatible)
- ✅ Custom JWT authentication (bcrypt password hashing)
- ✅ OpenAPI/Swagger documentation
- ✅ UUID-based task IDs with user isolation
- ✅ Production-ready Dockerfiles

**Tech Stack:** FastAPI, SQLModel, Alembic, Next.js 15, TypeScript, Tailwind CSS, shadcn/ui

**Deployment Targets:**
- **Frontend:** Vercel
- **Backend:** HuggingFace Spaces (port 7860)
- **Database:** Neon PostgreSQL

**Documentation:** [Production Deployment Guide](./docs/PRODUCTION_DEPLOYMENT.md)

---

### Phase 3: AI-Powered Chatbot ✅ COMPLETE

**Deliverables:**
- ✅ Natural language interface for task management
- ✅ Claude Sonnet 4 AI agent with function calling
- ✅ MCP (Model Context Protocol) server with 5 tools
- ✅ Rich CLI interface with authentication
- ✅ Conversational task management

**MCP Tools:**
1. `list_tasks` - Get all tasks (with filtering)
2. `create_task` - Create new task
3. `update_task` - Update existing task
4. `delete_task` - Delete task
5. `search_tasks` - Search tasks by keywords

**Tech Stack:** Anthropic Claude API, MCP SDK, httpx, rich

**Example Commands:**
- "Show me all my tasks"
- "Add buy groceries to my todo list"
- "Mark task 3 as complete"
- "Delete the task about shopping"

---

### Phase 4: Local Kubernetes Deployment ✅ COMPLETE

**Deliverables:**
- ✅ Docker images for all services (backend, frontend, chatbot)
- ✅ Kubernetes manifests (Deployments, Services, ConfigMaps, Secrets)
- ✅ PostgreSQL with PersistentVolumeClaim
- ✅ Init containers for database migrations
- ✅ Helm charts for templated deployment
- ✅ Minikube deployment script

**Kubernetes Resources:**
- Namespace: `todo-app`
- Deployments: postgres, backend, frontend, chatbot
- Services: ClusterIP (internal), LoadBalancer (frontend)
- Storage: PVC for PostgreSQL data

**Tech Stack:** Docker, Kubernetes 1.28+, Helm 3, Minikube

**Quick Deploy:**
```bash
cd k8s && ./deploy.sh
```

---

### Phase 5: Advanced Cloud Deployment ✅ COMPLETE

**Deliverables:**
- ✅ Event streaming with Apache Kafka + Zookeeper
- ✅ Microservices communication with Dapr sidecar
- ✅ Redis state store for Dapr
- ✅ Infrastructure as Code with Terraform
- ✅ DigitalOcean DOKS cluster configuration
- ✅ CI/CD pipeline with GitHub Actions

**Infrastructure Components:**
- **Kafka:** Event streaming for task operations (create, update, delete, complete)
- **Dapr:** Service mesh for pub/sub and state management
- **Terraform:** DOKS cluster, managed PostgreSQL, load balancer
- **CI/CD:** Automated testing → Docker build → Kubernetes deployment

**Event Streaming:** Tasks publish events to Kafka topics for real-time updates and analytics

**Tech Stack:** Apache Kafka, Dapr, Terraform, DigitalOcean, GitHub Actions

**Production Deployment:** See [docs/PRODUCTION_DEPLOYMENT.md](./docs/PRODUCTION_DEPLOYMENT.md)

## 📖 Documentation

### Specifications
- [Constitution](`./.specify/memory/constitution.md`) - Project governance and principles
- [Phase 1 Spec](./specs/001-cli-todo-app/spec.md) - CLI requirements
- [Phase 1 Plan](./specs/001-cli-todo-app/plan.md) - Implementation architecture
- [Phase 1 Tasks](./specs/001-cli-todo-app/tasks.md) - Executable task breakdown

### Status & History
- [Phase 1 Status Report](./PHASE1_STATUS.md) - Completion metrics and next steps
- [GitHub Setup Guide](./GITHUB_SETUP.md) - Repository deployment instructions
- [Prompt History Records](./history/prompts/) - Full development audit trail
- [Architecture Decisions](./history/adr/) - ADRs (to be created for Phase 2+)

## 🧪 Testing

### Phase 1 Tests

```bash
cd cli

# Run all tests
uv run pytest

# Run with coverage
uv run pytest --cov=todo_cli --cov-report=html

# Run specific test suite
uv run pytest tests/unit/test_models.py
uv run pytest tests/unit/test_repository.py
uv run pytest tests/integration/test_cli_commands.py

# Type checking
uv run pyright

# Linting
uv run ruff check .
```

**Current Coverage:** 96% (81/81 tests passing)

## 🚀 Deployment

### Phase 1: CLI (Local Only)

```bash
cd cli
uv pip install -e .
todo --help
```

### Phase 2+: Vercel + HuggingFace

**Prerequisites:**
1. GitHub repository: https://github.com/shery123pk/shery_todo_app
2. Vercel account for frontend deployment
3. HuggingFace account for backend deployment

**Frontend (Vercel):**
```bash
cd frontend
vercel --prod
```

**Backend (HuggingFace):**
- Create Space at https://huggingface.co/new-space
- Link GitHub repository
- Configure Docker deployment from `backend/Dockerfile`

*Note: Phase 2 deployment instructions will be added when implemented.*

## 🎓 Methodology

This project follows **Spec-Driven Development (SDD)** principles:

1. **Constitution First:** Define project governance and non-negotiables
2. **Specify:** Write detailed specs with user stories and acceptance criteria
3. **Plan:** Create implementation architecture with ADRs
4. **Task Breakdown:** Generate executable tasks with dependencies
5. **Implement:** AI executes tasks following TDD approach
6. **Trace:** Full audit trail with PHRs and commit messages

**Human Role:** Architect (specs, reviews, decisions)
**AI Role:** Developer (code, tests, implementation)

## 📊 Success Metrics

### Phase 1 Achievements
- ✅ 100% spec coverage (6/6 user stories)
- ✅ 96% code coverage (81 tests passing)
- ✅ 100% test pass rate
- ✅ <10 cyclomatic complexity
- ✅ Full SDD workflow executed
- ✅ Complete traceability (PHRs)

### Phase 2 Achievements
- ✅ Complete authentication system (JWT + bcrypt)
- ✅ Full CRUD API with OpenAPI documentation
- ✅ User isolation and data security
- ✅ Production-ready Dockerfiles
- ✅ Database migrations with Alembic
- ✅ Modern frontend with Next.js 15 and shadcn/ui

### Phase 3 Achievements
- ✅ AI agent with natural language understanding
- ✅ 5 MCP tools for task management
- ✅ Claude Sonnet 4 integration
- ✅ Conversational interface
- ✅ Authenticated API access

### Phase 4 Achievements
- ✅ All services containerized
- ✅ Complete Kubernetes manifests
- ✅ Helm charts for deployment
- ✅ Database persistence with PVCs
- ✅ Init containers for migrations
- ✅ Automated Minikube deployment

### Phase 5 Achievements
- ✅ Kafka event streaming implemented
- ✅ Dapr microservices architecture
- ✅ Terraform IaC for cloud deployment
- ✅ CI/CD pipeline with GitHub Actions
- ✅ Production-ready infrastructure

### Overall Project Success
- ✅ All 5 phases completed
- ✅ Full evolution from CLI to cloud deployment demonstrated
- ✅ Production-ready code for all phases
- ✅ Comprehensive documentation and deployment guides
- ✅ Multiple deployment options (local, Minikube, cloud)
- ✅ Complete tooling (environment validation, testing, deployment)

## 🤝 Contributing

This is a demonstration project following strict SDD principles. All changes must:
1. Start with a spec in `specs/`
2. Follow the constitution in `.specify/memory/constitution.md`
3. Maintain full traceability with PHRs
4. Preserve backward compatibility

## 📜 License

MIT

## 🔗 Links

- **Repository:** https://github.com/shery123pk/shery_todo_app
- **Constitution:** [.specify/memory/constitution.md](./.specify/memory/constitution.md)
- **Phase 1 Spec:** [specs/001-cli-todo-app/spec.md](./specs/001-cli-todo-app/spec.md)
- **Claude Code:** https://claude.com/claude-code
- **Spec-Kit Plus:** (embedded in `.specify/`)

---

**Current Phase:** All 5 Phases Complete ✅
**Last Updated:** 2025-12-26
**Status:** Production Ready (All Phases)
**Author:** Sharmeen Asif

🤖 Built with [Claude Code](https://claude.com/claude-code) | 🎓 Panaversity Hackathon Project
