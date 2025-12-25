<!--
SYNC IMPACT REPORT
==================
Version Change: Initial Template → 1.0.0
Modified Principles: N/A (initial creation)
Added Sections: All sections added from template + Serena semantic editing rules
Removed Sections: None
Templates Status:
  ✅ .specify/templates/plan-template.md - Constitution Check section aligns
  ✅ .specify/templates/spec-template.md - User stories and requirements align
  ✅ .specify/templates/tasks-template.md - Phase-based organization aligns
  ⚠ CLAUDE.md - May need updates to reference new constitution principles
Follow-up TODOs: None
==================
-->

# The Evolution of Todo - Project Constitution

**Version**: 1.0.0 | **Ratified**: 2025-12-25 | **Last Amended**: 2025-12-26

## Preamble

**Core Purpose**: Demonstrate mastery of Spec-Driven Development (SDD) using Claude Code and Spec-Kit Plus, where the human acts as Architect and Claude (AI) acts as the exclusive Developer. Evolve a basic todo app across five phases in a single monorepo, ensuring additive evolution, full traceability, and integration of reusable intelligence via subagents and agent skills.

**Supremacy Clause**: This Constitution is the ultimate authority. Any conflicting spec, plan, task, code, or decision is invalid and must be regenerated to comply.

## Core Principles

### I. Spec-Driven Development Only

All features MUST follow the strict SDD workflow:

```
/sp.constitution → /sp.specify → /sp.plan → /sp.tasks → /sp.implement
```

**Rules**:
- No implementation without an approved, versioned spec in `specs/`
- Humans NEVER manually write or edit code—refine specs to fix issues
- Use Spec-Kit Plus conventions for organized specs (e.g., features, api, database, ui)
- Every spec MUST include user stories, acceptance criteria, edge cases, and test scenarios

**Rationale**: Spec-first ensures all work is traceable, reviewed, and aligned with architectural intent before execution.

### II. AI as Sole Developer

**Human (Architect) Responsibilities**:
- Author/refine specs using Spec-Kit Plus
- Review plans, ADRs, and outputs
- Validate tests and approve merges
- Decide trade-offs and invoke subagents

**AI (Claude) Responsibilities**:
- Generate plans, tasks, code, tests, docs from specs
- Invoke subagents for specialized tasks
- Suggest ADRs for significant decisions
- Ensure compliance with constitution invariants

**Rationale**: Clear role separation ensures architectural oversight while leveraging AI execution speed and consistency.

### III. Semantic Code Editing (Serena Rules)

All semantic code changes MUST follow structured editing practices:

**Mandatory Rules**:
- All semantic code changes MUST go through Serena-assisted edits or LSP-aware tools
- LSP semantic search MUST be used before manual code edits
- Agents MUST avoid blind regex or text matching edits
- Use Language Server Protocol (LSP) for:
  - Symbol lookup and navigation
  - Type-aware refactoring
  - Dependency analysis
  - Code structure understanding

**Rationale**: Structured editing over guesswork prevents breaking changes, maintains code integrity, and ensures type-safe modifications across the codebase.

### IV. Full Traceability & Audit Trail

Every feature MUST maintain complete linkage:

```
ADR → Spec → Plan → Tasks → Code → Tests
```

**Requirements**:
- Store in structured folders (e.g., `specs/features/`)
- Prompt History Records (PHRs) in `history/prompts/`
- Reference specs via `@specs/features/task-crud.md` in Claude prompts
- All architectural decisions documented in ADRs

**Rationale**: Full traceability enables verification, debugging, and learning across the project lifecycle.

### V. Test-First & Evolutionary Safeguards

**Mandatory Practices**:
- Generate tests with/before code
- Maintain >80% code coverage
- Full regression suites ensure later phases never break earlier ones
- Include chaos testing in distributed phases

**Rationale**: Test-first prevents regressions and ensures each phase adds value without breaking existing functionality.

### VI. Reusable Intelligence Integration

**Requirements**:
- Use Claude subagents with defined skills for modularity
- All agents/skills MUST be spec-driven and traceable
- Implement reusable agent skills for blueprints in deployment phases

**Rationale**: Modular, reusable agents enable consistent execution patterns and knowledge transfer across features.

## Unified Domain Model (Progressive & Additive)

### Phase 1 (Immutable Core)

- `id`: UUID (immutable)
- `title`: string (required, 1-200 chars)
- `description`: string (optional, max 1000 chars)
- `completed`: boolean (default false)

### Phase 2 Additions

- `priority`: enum["low", "medium", "high", "critical"]
- `tags`: list[string]
- `category`: string
- `created_at`, `updated_at`: ISO 8601 timestamps

### Phase 3+ Additions

- `due_date`: optional ISO 8601
- `recurrence`: optional pattern (e.g., weekly)
- `reminders`: list[reminder_config]
- `assigned_to`: optional user/agent ref
- `parent_id`: optional (subtasks)

### Invariants (NON-NEGOTIABLE)

1. `id` never mutates
2. `completed` is binary only (true/false)
3. Operations (e.g., create, complete) MUST be semantically consistent across CLI, Web, API, AI, MCP tools
4. All extensions MUST be backward-compatible with migration plans if needed

## Technology Stack & Standards

### Backend (All Phases)

- **Language**: Python 3.13+ (with UV for dependency management)
- **API Framework**: FastAPI (Phase 2+)
- **ORM**: SQLModel
- **Validation**: Pydantic models
- **Architecture**: Dependency injection; no global state

### Frontend (Phase 2+)

- **Framework**: Next.js 16+ (App Router)
- **Language**: TypeScript (strict mode)
- **Styling**: Tailwind CSS
- **Components**: Server Components default; client only for interactivity

### Authentication (Phase 2+)

- Better Auth (with JWT tokens for stateless verification)

### AI & Chat (Phase 3+)

- **UI**: OpenAI ChatKit (frontend UI)
- **Logic**: OpenAI Agents SDK (AI logic)
- **Tools**: Official MCP SDK (tool exposure, stateless)

### Event-Driven Architecture (Phase 5)

- **Messaging**: Kafka (via Redpanda Cloud or local Docker)
- **Abstractions**: Dapr for Pub/Sub, State, Bindings, Secrets, Invocation

### Database

- **Provider**: Neon Serverless PostgreSQL

### Deployment (Phase 4+)

- **Containerization**: Docker (with Gordon AI for assistance)
- **Orchestration**: Kubernetes (Minikube local, DOKS/GKE cloud)
- **Package Management**: Helm Charts
- **AIOps**: kubectl-ai, kagent
- **CI/CD**: GitHub Actions

### Code Editing Tools

- **Semantic Editing**: Serena or LSP-aware tools for all code modifications
- **LSP Servers**: Configured for Python (Pyright/Pylance), TypeScript (tsserver)
- **Refactoring**: Type-aware, symbol-based refactoring only

### Forbidden Practices

The following practices are STRICTLY PROHIBITED:

1. Manual code writing/editing by humans
2. Hard-coded secrets/URLs
3. Direct database access from frontend
4. Unparameterized queries
5. Vendor lock-in (use Dapr abstractions)
6. Blind regex or text-based code edits without LSP verification
7. Code modifications without semantic understanding

## Mandatory Repository Structure

```
hackathon-todo/
├── .spec-kit/                    # Spec-Kit Plus config
│   └── config.yaml
├── specs/                        # Organized specs
│   ├── overview.md               # Project overview
│   ├── architecture.md           # System architecture
│   ├── features/                 # User stories, acceptance criteria
│   │   ├── task-crud.md
│   │   ├── authentication.md
│   │   └── chatbot.md
│   ├── api/                      # REST/MCP endpoints
│   │   ├── rest-endpoints.md
│   │   └── mcp-tools.md
│   ├── database/                 # Schemas, migrations
│   │   └── schema.md
│   ├── ui/                       # Components, pages
│   │   ├── components.md
│   │   └── pages.md
├── history/
│   ├── adr/                      # Architecture Decisions
│   └── prompts/                  # PHRs
├── src/                          # Shared source (if needed)
├── frontend/                     # Next.js app
│   ├── CLAUDE.md
│   └── ... (Next.js files)
├── backend/                      # FastAPI app
│   ├── CLAUDE.md
│   └── ... (FastAPI files)
├── tests/                        # Unit/integration/e2e
├── infra/                        # Deployment
│   ├── docker/
│   ├── kubernetes/
│   ├── helm/
│   └── terraform/                # Optional IaC
├── docker-compose.yml            # Local dev
├── README.md                     # Setup, run instructions
└── CLAUDE.md                     # Root AI guidelines
```

## Quality, Security & Compliance Standards

### Specifications

- Clear user stories with acceptance criteria
- Comprehensive edge cases
- Test scenarios for all features
- No implementation details in specs

### Code Quality

- Readable, DRY (Don't Repeat Yourself)
- Cyclomatic complexity <10
- Full error handling and logging
- Structured logging for observability
- All edits must be semantically verified via LSP

### Security

- JWT verification for all protected endpoints
- Input validation on all user inputs
- HTTPS enforced for all communications
- Secrets managed via Dapr/Kubernetes secrets (never hard-coded)

### Privacy

- Minimal data collection
- GDPR-like retention and deletion policies
- User data anonymization where possible

### Documentation

- Versioned READMEs for setup and usage
- Inline comments only for complex logic
- OpenAPI documentation for all APIs

## Phase Evolution Roadmap

| Phase | Name | Key Deliverables | Tech Focus | Must Preserve |
|-------|------|------------------|------------|---------------|
| 1 | CLI + In-Memory | Basic CRUD CLI, file persistence optional | Python, UV | — |
| 2 | Full-Stack Web | REST API, Next.js UI, Neon DB, Better Auth | FastAPI, SQLModel | Phase 1 |
| 3 | AI-Powered Chatbot | Natural lang interface, MCP tools, ChatKit | Agents SDK, MCP | Phases 1–2 |
| 4 | Local K8s Deployment | Dockerized, Minikube, Helm, AIOps (kubectl-ai/kagent) | Docker/Gordon, Helm | Phases 1–3 |
| 5 | Cloud Deployment | Intermediate/Advanced features, Dapr, Kafka, DOKS/GKE | Redpanda Kafka, Dapr, CI/CD | Phases 1–4 |

### Phase Transition Requirements

All phase transitions MUST include:
1. Architecture Decision Record (ADR)
2. Migration plan with rollback strategy
3. Passing regression tests for all previous phases
4. Updated documentation

### Bonus Features (+600 points)

- Multi-language support (Urdu)
- Voice input/output
- Reusable agent skills library

## Subagents (Reusable Intelligence Roles)

Invoke via Claude CLI prompts, e.g., "Invoke [Agent]: [Task] per @specs/features/task-crud.md".

### 1. AI Engineer Agent

**Role**: AI logic & integration specialist

**Responsibility**: Handle NLP, agent orchestration, MCP tool mapping, conversation state via Dapr/DB.

**Skills**: openai-agents-sdk, mcp-tool-exposure, nlp-intent-parsing, ambiguity-handling, chatkit-ui-integration, stateless-conversation-management

### 2. Backend Engineer Agent

**Role**: API & server expert

**Responsibility**: FastAPI routes, SQLModel schemas/migrations, MCP server, Kafka/Dapr pubs/subs.

**Skills**: fastapi-routing, sqlmodel-orm-migrations, mcp-sdk-implementation, kafka-redpanda-integration, dapr-pubsub-state, pydantic-models

### 3. Data Migration Agent

**Role**: Schema evolution guardian

**Responsibility**: Phase migrations, data integrity, backward compat via SQLModel/Neon.

**Skills**: neon-db-migrations, data-validation-transformation, compatibility-enforcement, rollback-strategies

### 4. File & Persistence Agent

**Role**: I/O & storage handler

**Responsibility**: Phase 1 file ops, cloud storage abstraction, secure handling.

**Skills**: file-persistence, json-handling, dapr-state-management, input-sanitization

### 5. Frontend Engineer Agent

**Role**: Next.js UI specialist

**Responsibility**: Responsive components, ChatKit integration, Better Auth JWT client, Tailwind styling.

**Skills**: nextjs-app-router, typescript-strict, tailwind-css, better-auth-jwt, chatkit-frontend, accessibility-wcag

### 6. QA & Testing Agent

**Role**: Quality enforcer

**Responsibility**: Test suites, coverage, regressions across phases/MCP tools.

**Skills**: pytest-suites, e2e-testing, regression-validation, mcp-tool-testing, coverage-metrics

### 7. UX Polisher Agent

**Role**: Experience optimizer

**Responsibility**: UI flows, natural lang confirmations, multi-lang (Urdu bonus), voice input.

**Skills**: ux-flow-optimization, confirmation-dialogs, multi-language-i18n, voice-input-output, accessibility-compliance

### 8. DevOps & Deployment Agent

**Role**: Infrastructure & deployment expert

**Responsibility**: Docker, K8s, Helm, Dapr, CI/CD, AIOps tooling (kubectl-ai/kagent).

**Skills**: docker-containerization, kubernetes-orchestration, helm-charts, dapr-integration, github-actions-cicd, kubectl-ai-kagent

### 9. Security & Compliance Agent

**Role**: Security guardian

**Responsibility**: JWT auth, input validation, secrets management, HTTPS, audit logs.

**Skills**: better-auth-jwt-validation, input-sanitization, secrets-management-dapr, https-enforcement, security-auditing

### 10. Documentation Agent

**Role**: Documentation specialist

**Responsibility**: READMEs, API docs (OpenAPI), inline comments, ADRs, PHRs.

**Skills**: readme-authoring, openapi-documentation, adr-creation, phr-generation, inline-commenting

## Default Execution Policies

### Planning First

- Clarify and plan first
- Keep business understanding separate from technical plan
- Carefully architect before implementing

### API & Contract Integrity

- Do not invent APIs, data, or contracts
- Ask targeted clarifiers if missing information
- Document all assumptions in specs

### Security First

- Never hardcode secrets or tokens
- Use `.env` files and document secret requirements
- All secrets managed via Dapr/Kubernetes

### Minimal Change Principle

- Prefer the smallest viable diff
- Do not refactor unrelated code
- Each change must be justified by spec

### Code References

- Cite existing code with precise references (start:end:path)
- Propose new code in fenced blocks with file paths
- Keep reasoning private; output only decisions, artifacts, and justifications

### Semantic Code Editing Workflow

When modifying code:
1. Use LSP to locate exact symbols/definitions
2. Verify type information and dependencies
3. Use Serena or LSP-aware tools for edits
4. Validate changes semantically before committing
5. Never use blind text search/replace on code

## Execution Contract (Every Request)

For every development request, the following steps MUST be completed:

1. **Confirm surface and success criteria** (one sentence)
2. **List constraints, invariants, non-goals**
3. **Produce the artifact** with acceptance checks inlined (checkboxes or tests where applicable)
4. **Add follow-ups and risks** (max 3 bullets)
5. **Create PHR** in appropriate subdirectory under `history/prompts/` (constitution, feature-name, or general)
6. **Suggest ADR** if plan/tasks identified decisions meeting significance criteria

## Minimum Acceptance Criteria

Every deliverable MUST include:

- Clear, testable acceptance criteria
- Explicit error paths and constraints stated
- Smallest viable change; no unrelated edits
- Code references to modified/inspected files where relevant
- LSP-verified semantic correctness for all code changes

## Architectural Decision Records (ADRs)

### ADR Significance Test

After design/architecture work, test for ADR significance using ALL three criteria:

1. **Impact**: Does it have long-term consequences? (e.g., framework, data model, API, security, platform)
2. **Alternatives**: Were multiple viable options considered?
3. **Scope**: Is it cross-cutting and influences system design?

### ADR Suggestion Format

If ALL three criteria are true, suggest:

```
📋 Architectural decision detected: [brief-description]
   Document reasoning and tradeoffs? Run `/sp.adr [decision-title]`
```

**Rules**:
- Wait for user consent; NEVER auto-create ADRs
- Group related decisions (stacks, authentication, deployment) into one ADR when appropriate
- Each ADR must document: context, decision, consequences, alternatives considered

## Governance

### Amendment Procedure

1. Propose amendment with rationale
2. Document impact on existing specs, plans, tasks
3. Update all dependent templates and artifacts
4. Increment version according to semantic versioning
5. Create ADR for significant governance changes
6. Update Sync Impact Report

### Versioning Policy

- **MAJOR** (X.0.0): Backward incompatible governance/principle removals or redefinitions
- **MINOR** (x.Y.0): New principle/section added or materially expanded guidance
- **PATCH** (x.y.Z): Clarifications, wording, typo fixes, non-semantic refinements

### Compliance Review

- All PRs/reviews MUST verify compliance with this constitution
- Complexity MUST be justified against constitution principles
- Constitution supersedes all other practices, guides, and documentation
- Use `CLAUDE.md` for runtime development guidance (must align with constitution)

### Conflict Resolution

- In case of conflict: Constitution > ADR > Spec > Plan > Tasks > Code
- Conflicts must be resolved by updating lower-level artifacts to comply
- Document resolution in ADR if architecturally significant

**Version**: 1.0.0 | **Ratified**: 2025-12-25 | **Last Amended**: 2025-12-26
