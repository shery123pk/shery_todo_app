# Evolution of Todo

A 5-phase project demonstrating Spec-Driven Development (SDD) from CLI to Full-Stack AI-Powered Application.

## 🎯 Project Vision

This monorepo showcases the evolution of a todo application across five progressive phases, demonstrating:
- **Spec-Driven Development** with Claude Code and Spec-Kit Plus
- **AI as Sole Developer** (Claude) with Human as Architect
- **Full Traceability** from specs to code with ADRs and PHRs
- **Additive Evolution** where each phase builds on previous ones
- **Production Deployments** on Vercel (frontend) and HuggingFace (backend)

## 📊 Project Status

| Phase | Name | Status | Deployment |
|-------|------|--------|------------|
| **1** | CLI + In-Memory | ✅ Complete | Local |
| **2** | Full-Stack Web | 🚧 Planning | Vercel + HuggingFace |
| **3** | AI-Powered Chatbot | 📋 Planned | TBD |
| **4** | Local K8s Deployment | 📋 Planned | Minikube |
| **5** | Cloud Deployment | 📋 Planned | DOKS/GKE |

## 🏗️ Monorepo Structure

```
shery_todo_app/
├── cli/                          # Phase 1: CLI Todo App ✅
│   ├── todo_cli/                 # Source code
│   ├── tests/                    # 81 tests, 96% coverage
│   └── pyproject.toml
├── backend/                      # Phase 2+: FastAPI API 🚧
│   └── README.md                 # Coming soon
├── frontend/                     # Phase 2+: Next.js UI 🚧
│   └── README.md                 # Coming soon
├── shared/                       # Shared code/types 🚧
│   └── README.md                 # Coming soon
├── specs/                        # All phase specifications
│   ├── 001-cli-todo-app/         # Phase 1 specs ✅
│   └── ...                       # Future phases
├── history/                      # Traceability artifacts
│   ├── adr/                      # Architecture Decision Records
│   └── prompts/                  # Prompt History Records (PHRs)
├── .specify/                     # Spec-Kit Plus configuration
│   ├── memory/constitution.md    # Project constitution
│   └── templates/                # SDD templates
├── docker-compose.yml            # Multi-phase local dev
├── PHASE1_STATUS.md              # Phase 1 completion report
└── README.md                     # This file
```

## 🚀 Quick Start

### Phase 1: CLI (Current)

```bash
# Install CLI
cd cli
uv pip install -e .

# Use the CLI
todo add "My first task" -d "This is a description"
todo list
todo complete 1
todo delete 1

# Run tests
uv run pytest
```

### Phase 2+: Full Stack (Coming Soon)

```bash
# Start all services for Phase 2
docker-compose --profile phase2 up

# Frontend will be at: http://localhost:3000
# Backend API will be at: http://localhost:8000
# API docs will be at: http://localhost:8000/docs
```

## 📋 Phase Roadmap

### Phase 1: CLI + In-Memory ✅ COMPLETE

**Deliverables:**
- ✅ Command-line todo application
- ✅ In-memory storage with JSON persistence
- ✅ CRUD operations (add, list, update, delete, complete)
- ✅ 96% test coverage (81 tests)
- ✅ Full SDD workflow (constitution → spec → plan → tasks → implement)

**Tech Stack:** Python 3.13+, Click, pytest, UV

**[View Phase 1 Details](./cli/README.md)** | **[View Status Report](./PHASE1_STATUS.md)**

### Phase 2: Full-Stack Web 🚧 NEXT

**Planned Deliverables:**
- REST API with FastAPI
- Next.js 15 frontend with shadcn/ui
- Neon PostgreSQL database
- Better Auth authentication
- OpenAPI documentation
- UUID-based task IDs

**Tech Stack:** FastAPI, Next.js, SQLModel, Tailwind CSS, Better Auth

**Deployment Targets:**
- **Frontend:** Vercel
- **Backend:** HuggingFace Spaces

**Required ADRs:**
1. ADR-001: ID Migration Strategy (int → UUID)
2. ADR-002: Monorepo Structure
3. ADR-003: Database Choice (Neon PostgreSQL)
4. ADR-004: Auth Strategy (Better Auth)

### Phase 3: AI-Powered Chatbot 📋 PLANNED

**Planned Deliverables:**
- Natural language interface for task management
- Claude-powered chatbot with MCP tools
- ChatKit integration
- Conversational UI

**Tech Stack:** Claude API, Agents SDK, MCP Protocol, ChatKit

### Phase 4: Local K8s Deployment 📋 PLANNED

**Planned Deliverables:**
- Dockerized applications
- Helm charts for deployment
- Minikube local cluster
- AIOps tools (kubectl-ai, kagent)

**Tech Stack:** Docker, Kubernetes, Helm, Minikube

### Phase 5: Cloud Deployment 📋 PLANNED

**Planned Deliverables:**
- Production Kubernetes deployment
- Event streaming with Kafka
- Service mesh with Dapr
- CI/CD pipeline
- Advanced features (real-time, notifications, etc.)

**Tech Stack:** DOKS/GKE, Redpanda Kafka, Dapr, ArgoCD

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
- ✅ 96% code coverage (81 tests)
- ✅ 100% test pass rate
- ✅ <10 cyclomatic complexity
- ✅ Full SDD workflow executed
- ✅ Complete traceability (4 PHRs)

### Overall Project Goals
- Demonstrate complete 5-phase evolution
- Maintain >80% test coverage across all phases
- Full backward compatibility (Phase N preserves Phase N-1)
- Production deployments on public platforms
- Complete documentation and traceability

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

**Current Phase:** 1 (Complete) ✅
**Next Phase:** 2 (Planning) 🚧
**Last Updated:** 2025-12-26
**Status:** Production Ready (Phase 1)

🤖 Built with [Claude Code](https://claude.com/claude-code)
