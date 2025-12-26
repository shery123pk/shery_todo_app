# ADR-002: Monorepo Structure for Multi-Phase Evolution

**Status:** Accepted
**Date:** 2025-12-26
**Deciders:** Architect (shery123pk), AI Developer (Claude)
**Related Phase:** All Phases (1-5)
**Implementation:** Completed (commit ea9b5b3)

---

## Context and Problem Statement

The Evolution of Todo project spans 5 phases with different deployment targets:
- **Phase 1:** CLI (local installation)
- **Phase 2+:** Backend API (HuggingFace) + Frontend (Vercel)
- **Phase 3+:** AI chatbot integration
- **Phase 4+:** Kubernetes deployment
- **Phase 5:** Cloud production

**Key Questions:**
1. Single monorepo or multiple repositories?
2. How to structure for independent deployments (Vercel/HuggingFace)?
3. How to maintain shared specs, constitution, and history?
4. How to preserve Phase 1 CLI while adding Phase 2+?

---

## Decision Drivers

### Must Have
- ✅ **Constitution Mandate:** Monorepo required per `.specify/memory/constitution.md`
- ✅ **Additive Evolution:** Each phase builds on previous without breaking them
- ✅ **Full Traceability:** Shared specs, ADRs, PHRs across all phases
- ✅ **Deployment Independence:** Vercel can deploy frontend, HuggingFace can deploy backend

### Should Have
- 🎯 **Clear Separation:** Each phase in its own directory
- 🎯 **Shared Resources:** Common types, utilities, constants
- 🎯 **Development Ergonomics:** Easy local development with docker-compose

### Nice to Have
- 💡 **Code Reuse:** Share validation logic, domain models
- 💡 **Unified Versioning:** Single source of truth for releases

---

## Considered Options

### Option 1: Monorepo with Phase Directories ✅ SELECTED

**Structure:**
```
shery_todo_app/
├── cli/              # Phase 1: Python CLI
├── backend/          # Phase 2+: FastAPI
├── frontend/         # Phase 2+: Next.js
├── shared/           # Shared code/types
├── specs/            # All phase specifications
├── history/          # All ADRs and PHRs
├── .specify/         # Constitution and templates
└── docker-compose.yml
```

**Deployment Mapping:**
- Vercel: Detects `/frontend` directory
- HuggingFace: Detects `/backend` directory
- CLI: Local `uv pip install -e ./cli`

**Pros:**
- ✅ Constitution compliant (mandated structure)
- ✅ Full traceability (shared history/)
- ✅ Independent deployments (separate root dirs)
- ✅ Code sharing possible (shared/)
- ✅ Single git history for entire evolution
- ✅ Docker-compose can orchestrate all services

**Cons:**
- ⚠️ Need deployment config (root dir specification)
- ⚠️ Larger repository size
- ⚠️ Need tooling for managing multiple package.json/pyproject.toml

### Option 2: Separate Repositories per Phase

**Structure:**
```
shery-todo-cli/       # Repo 1: Phase 1
shery-todo-backend/   # Repo 2: Phase 2+ backend
shery-todo-frontend/  # Repo 3: Phase 2+ frontend
```

**Pros:**
- ✅ Simple deployment (one repo = one deploy)
- ✅ Smaller repository sizes
- ✅ Clear ownership boundaries

**Cons:**
- ❌ **Violates Constitution:** Monorepo mandated
- ❌ No shared specs/history
- ❌ Hard to track evolution
- ❌ Duplicate configuration
- ❌ Version synchronization nightmare

### Option 3: Monorepo with Workspaces (npm/pnpm)

**Structure:**
```
shery_todo_app/
├── packages/
│   ├── cli/
│   ├── backend/
│   ├── frontend/
│   └── shared/
├── package.json (workspace root)
└── pnpm-workspace.yaml
```

**Pros:**
- ✅ Native workspace support
- ✅ Dependency deduplication
- ✅ Easy cross-package imports

**Cons:**
- ⚠️ Requires pnpm/npm workspaces
- ⚠️ Python CLI doesn't fit workspace model
- ⚠️ More complex than needed for Phase 2

### Option 4: Polyrepo with Git Submodules

**Structure:**
```
shery-todo-monorepo/
├── cli/           # Git submodule
├── backend/       # Git submodule
└── frontend/      # Git submodule
```

**Pros:**
- ✅ Independent repositories
- ✅ Flexible versioning

**Cons:**
- ❌ Complex submodule management
- ❌ Poor developer experience
- ❌ History fragmentation

---

## Decision Outcome

**Chosen Option:** **Monorepo with Phase Directories** (Option 1) ✅

### Rationale

1. **Constitution Compliance:** Explicitly mandated structure
2. **Deployment Flexibility:** Platform-specific root directories
3. **Traceability:** Single source for all specs, ADRs, PHRs
4. **Evolution Showcase:** Easy to see progression from Phase 1 → 5
5. **Practical:** Works with Vercel's `/frontend` and HuggingFace's `/backend` detection

**Trade-off Accepted:** Slightly larger repo and need for deployment configuration is acceptable for the benefits of unified history and shared resources.

---

## Implementation

### Directory Structure (Implemented)

```
shery_todo_app/
├── cli/                          # Phase 1: CLI Todo App
│   ├── todo_cli/                 # Python source
│   │   ├── __init__.py
│   │   ├── models.py
│   │   ├── repository.py
│   │   ├── commands.py
│   │   ├── main.py
│   │   └── utils.py
│   ├── tests/                    # 81 tests, 96% coverage
│   │   ├── unit/
│   │   └── integration/
│   ├── pyproject.toml            # UV configuration
│   └── README.md
│
├── backend/                      # Phase 2+: FastAPI API
│   ├── app/
│   │   ├── main.py
│   │   ├── models/
│   │   ├── routers/
│   │   └── services/
│   ├── tests/
│   ├── pyproject.toml
│   ├── Dockerfile                # HuggingFace deployment
│   └── README.md
│
├── frontend/                     # Phase 2+: Next.js UI
│   ├── app/
│   │   ├── layout.tsx
│   │   ├── page.tsx
│   │   └── tasks/
│   ├── components/
│   ├── lib/
│   ├── package.json
│   ├── next.config.js
│   └── README.md
│
├── shared/                       # Shared code
│   ├── schemas/                  # Pydantic/Zod schemas
│   └── types/                    # TypeScript types
│
├── specs/                        # All phase specifications
│   ├── 001-cli-todo-app/         # Phase 1 (complete)
│   └── 002-fullstack-web/        # Phase 2 (to be created)
│
├── history/                      # Traceability
│   ├── adr/                      # Architecture Decision Records
│   │   ├── 001-id-migration-strategy.md
│   │   ├── 002-monorepo-structure.md
│   │   └── ...
│   └── prompts/                  # Prompt History Records
│       ├── constitution/
│       ├── 001-cli-todo-app/
│       └── 002-fullstack-web/
│
├── .specify/                     # Spec-Kit Plus
│   ├── memory/constitution.md
│   └── templates/
│
├── docker-compose.yml            # Multi-phase local dev
├── .gitignore
├── README.md                     # Monorepo documentation
└── PHASE1_STATUS.md
```

### Deployment Configuration

**Vercel (Frontend):**
```json
// vercel.json
{
  "buildCommand": "cd frontend && npm run build",
  "outputDirectory": "frontend/.next",
  "installCommand": "cd frontend && npm install",
  "framework": "nextjs"
}
```

**HuggingFace (Backend):**
```dockerfile
# backend/Dockerfile
FROM python:3.13-slim
WORKDIR /app
COPY backend/ /app/
RUN pip install -e .
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "7860"]
```

**CLI (Local):**
```bash
cd cli && uv pip install -e .
```

### Docker Compose (Local Development)

```yaml
# Multi-phase orchestration
services:
  backend:
    build: ./backend
    ports: ["8000:8000"]
    profiles: [phase2, phase3, phase4, phase5]

  frontend:
    build: ./frontend
    ports: ["3000:3000"]
    profiles: [phase2, phase3, phase4, phase5]

  db:
    image: postgres:16-alpine
    profiles: [phase2, phase3, phase4, phase5]
```

---

## Consequences

### Positive
- ✅ **Single Source of Truth:** All phases, specs, ADRs in one place
- ✅ **Constitution Compliant:** Matches mandated structure exactly
- ✅ **Deployment Ready:** Vercel and HuggingFace can detect subdirectories
- ✅ **Evolution Visible:** Easy to see progression from simple CLI to full-stack
- ✅ **Shared Resources:** Specs, constitution, history accessible to all phases
- ✅ **Git History:** Complete audit trail of all changes across phases

### Negative
- ⚠️ **Repository Size:** Grows with each phase (acceptable for learning project)
- ⚠️ **Deployment Config:** Need to configure root directories for platforms
  - **Mitigation:** `vercel.json` and `Dockerfile` handle this
- ⚠️ **Multiple Package Managers:** UV (Python) + npm (JavaScript)
  - **Mitigation:** Each phase self-contained with its own dependencies

### Neutral
- 🔄 **Developer Setup:** Need to install dependencies for each phase separately
  - `cd cli && uv pip install -e .`
  - `cd backend && uv pip install -e .`
  - `cd frontend && npm install`
  - **Or:** `docker-compose --profile phase2 up` (all at once)

---

## Migration Impact

### Phase 1 → Monorepo Restructure

**Completed:** Commit ea9b5b3 (2025-12-26)

**Changes:**
- ✅ Moved `src/todo_cli/` → `cli/todo_cli/`
- ✅ Moved `tests/` → `cli/tests/`
- ✅ Moved `pyproject.toml` → `cli/pyproject.toml`
- ✅ Created `backend/`, `frontend/`, `shared/` placeholders
- ✅ Updated `README.md` for monorepo structure
- ✅ Updated `cli/pyproject.toml` paths
- ✅ Updated `cli/tests/conftest.py` sys.path

**Verification:**
- ✅ All 81 tests still passing (96% coverage)
- ✅ CLI still works: `todo --help` functional
- ✅ Git history preserved

---

## Governance

### Adding New Phases

When adding Phase 3, 4, or 5:

1. **Create Phase Directory:**
   ```bash
   mkdir -p phase3-chatbot/
   ```

2. **Update docker-compose.yml:**
   ```yaml
   phase3-service:
     profiles: [phase3, phase4, phase5]
   ```

3. **Add to README:**
   - Update Phase Status table
   - Add Phase N section to roadmap

4. **Create ADRs:**
   - Document significant architectural decisions

5. **Maintain Backward Compatibility:**
   - Previous phases must continue working

### Monorepo Maintenance

- **Keep Phases Self-Contained:** Each phase has its own dependencies
- **Share Only Essentials:** Use `shared/` sparingly to avoid coupling
- **Document Cross-Phase Dependencies:** In respective ADRs
- **Test Independently:** Each phase has its own test suite

---

## References

- **Constitution:** `.specify/memory/constitution.md` - Mandatory Repository Structure
- **Vercel Monorepo Docs:** https://vercel.com/docs/monorepos
- **HuggingFace Docker Spaces:** https://huggingface.co/docs/hub/spaces-sdks-docker
- **Implementation:** `RESTRUCTURE_SUMMARY.md`

---

## Related ADRs

- **ADR-001:** ID Migration Strategy (enabled by monorepo isolation)
- **ADR-003:** Database Choice (Neon PostgreSQL deployment config)
- **Future ADR:** Phase 3 - MCP Tools Integration (will use shared/ for schemas)

---

## Alternatives Considered But Rejected

### Turborepo
- **Pros:** Built-in caching, task orchestration
- **Cons:** Overkill for 5-phase learning project, adds complexity
- **Decision:** Plain monorepo sufficient for our needs

### Nx
- **Pros:** Powerful monorepo tooling, dependency graph
- **Cons:** Steep learning curve, not needed for demo project
- **Decision:** Keep it simple with standard directory structure

---

**Decision Made By:** Architect + AI Developer
**Date Approved:** 2025-12-26
**Implementation Status:** ✅ Complete (commit ea9b5b3)
**Review Date:** Phase 4 planning (if Kubernetes adds complexity)
