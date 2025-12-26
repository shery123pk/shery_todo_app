# Multi-Agent System Documentation

**Project**: Evolution of Todo - Shery's Multi-Phase Todo Application
**Purpose**: Specialized AI agents for Phase 2+ development
**Created**: 2025-12-26

---

## Overview

This directory contains specialized agent definitions for the Evolution of Todo project. Each agent has specific expertise and can be invoked to handle different aspects of the development workflow.

## Available Agents

| Agent ID | Role | Primary Skills |
|----------|------|----------------|
| `ai-engineer` | AI logic & integration specialist | OpenAI Agents SDK, MCP tools, NLP, conversation state |
| `backend-engineer` | API & server expert | FastAPI, SQLModel, MCP server, Kafka/Dapr |
| `data-migration` | Schema evolution guardian | Neon migrations, data validation, compatibility |
| `file-persistence` | I/O & storage handler | File ops, JSON, Dapr state, security |
| `frontend-engineer` | Next.js UI specialist | Next.js 15, TypeScript, Tailwind, Better Auth |
| `qa-testing` | Quality enforcer | pytest, Vitest, Playwright, accessibility audits |
| `token-checker` | Token & cost monitoring specialist | Token counting, cost tracking, budget enforcement |
| `serena` | Code search & navigation specialist | Semantic search, precise edits, refactoring |

---

## Invocation Syntax

### General Pattern
```
Invoke [Agent Name]: [Specific Task] per @specs/[feature].md
```

### Examples

**Backend Development**:
```
Invoke Backend Engineer: Implement task CRUD endpoints per @specs/002-fullstack-web/spec.md
```

**Frontend Development**:
```
Invoke Frontend Engineer: Create tasks dashboard page per @specs/002-fullstack-web/spec.md
```

**Testing**:
```
Invoke QA Testing: Create E2E tests for task management flow per @specs/002-fullstack-web/spec.md
```

**Data Migration**:
```
Invoke Data Migration: Migrate Phase 1 JSON tasks to PostgreSQL per @specs/002-fullstack-web/spec.md and @history/adr/001-id-migration-strategy.md
```

**Token Monitoring**:
```
Invoke Token Checker: Analyze token usage for Phase 2 implementation per @specs/002-fullstack-web/spec.md
```

**Code Refactoring**:
```
Invoke Serena: Rename function get_tasks to list_user_tasks across entire codebase
```

---

## Multi-Agent Workflows

### Workflow 1: Implementing a New Feature

**Step 1: Specification & Planning**
- User describes feature
- Create spec with `/sp.specify`
- Create plan with `/sp.plan`
- Generate tasks with `/sp.tasks`

**Step 2: Backend Implementation**
```
Invoke Backend Engineer: Implement [feature] API endpoints per @specs/[number]-[feature]/spec.md

Context:
- [Describe API requirements]
- [Authentication needed?]
- [Database schema changes?]

Deliverables:
- FastAPI routes
- SQLModel schemas
- Pydantic models
- Integration tests (>80% coverage)
```

**Step 3: Frontend Implementation**
```
Invoke Frontend Engineer: Implement [feature] UI per @specs/[number]-[feature]/spec.md

Context:
- [Describe UI requirements]
- [User interactions]
- [API endpoints from backend]

Deliverables:
- Next.js pages/components
- API integration
- Responsive design
- Component tests
```

**Step 4: Testing & Validation**
```
Invoke QA Testing: Validate [feature] implementation per @specs/[number]-[feature]/spec.md

Context:
- Backend deployed: [URL]
- Frontend deployed: [URL]
- Test scenarios: [list]

Deliverables:
- E2E test suite
- Accessibility audit
- Performance report
- Coverage report
```

### Workflow 2: AI Agent Integration

**Step 1: Design MCP Tools**
```
Invoke AI Engineer: Design MCP tools for [feature] per @specs/[number]-[feature]/spec.md

Context:
- Backend API available at [endpoints]
- User interactions: [natural language examples]
- Expected tool parameters and responses

Deliverables:
- MCP tool schemas
- Intent parsing logic
- Tool registration code
```

**Step 2: Implement Backend Tools**
```
Invoke Backend Engineer: Implement MCP server for [feature] per @specs/[number]-[feature]/spec.md

Context:
- MCP tool schemas from AI Engineer
- Existing FastAPI endpoints
- Authentication requirements

Deliverables:
- MCP server implementation
- Tool endpoint wrappers
- Integration tests
```

**Step 3: Integrate Frontend**
```
Invoke Frontend Engineer: Integrate ChatKit UI per @specs/003-ai-chatbot/spec.md

Context:
- MCP tools available
- Conversation flows
- User experience requirements

Deliverables:
- ChatKit component integration
- Message streaming UI
- Conversation history
```

### Workflow 3: Database Migration

**Step 1: Plan Migration**
```
Invoke Data Migration: Plan migration from [source] to [target] per @specs/[number]-[feature]/spec.md

Context:
- Source schema: [describe]
- Target schema: [describe]
- Data volume: [estimate]
- Downtime constraints: [specify]

Deliverables:
- Migration strategy document
- Risk assessment
- Rollback plan
```

**Step 2: Implement Migration**
```
Invoke Data Migration: Implement migration script per migration plan

Deliverables:
- Alembic migration
- Data transformation logic
- Validation tests
- Migration runbook
```

**Step 3: Test Migration**
```
Invoke QA Testing: Validate migration on dev/staging branches per migration plan

Deliverables:
- Pre-migration data snapshot
- Post-migration validation report
- Performance metrics
- Rollback test results
```

---

## Agent Collaboration Patterns

### Pattern 1: Backend-Frontend Handoff

1. **Backend Engineer** implements API:
   ```
   Invoke Backend Engineer: Implement user profile API per @specs/004-user-profiles/spec.md
   ```

2. Backend Engineer delivers:
   - API endpoints: `GET /api/users/:id`, `PATCH /api/users/:id`
   - OpenAPI spec: `backend/openapi.json`
   - Sample responses

3. **Frontend Engineer** consumes API:
   ```
   Invoke Frontend Engineer: Implement user profile page per @specs/004-user-profiles/spec.md

   Context:
   - API spec: @backend/openapi.json
   - Endpoints: GET/PATCH /api/users/:id
   - Authentication: Better Auth session cookies
   ```

### Pattern 2: AI-Backend Integration

1. **AI Engineer** designs tools:
   ```
   Invoke AI Engineer: Design MCP tools for task management per @specs/002-fullstack-web/spec.md
   ```

2. AI Engineer delivers:
   - Tool schemas (JSON)
   - Parameter validation rules
   - Expected responses

3. **Backend Engineer** implements:
   ```
   Invoke Backend Engineer: Implement MCP tools per AI Engineer specifications

   Context:
   - Tool schemas: [link to JSON]
   - Existing FastAPI endpoints to wrap
   ```

### Pattern 3: Migration-Testing Validation

1. **Data Migration** creates migration:
   ```
   Invoke Data Migration: Create migration for Better Auth tables per @history/adr/004-authentication-strategy-better-auth.md
   ```

2. Data Migration delivers:
   - Alembic migration file
   - Expected schema changes
   - Data integrity tests

3. **QA Testing** validates:
   ```
   Invoke QA Testing: Validate Better Auth migration per migration script

   Context:
   - Migration file: [path]
   - Test on Neon dev branch
   - Verify users, sessions, accounts tables
   ```

---

## Context Requirements

When invoking agents, always provide:

### Required Context
- **Specification Reference**: `@specs/[number]-[feature]/spec.md`
- **Task Description**: Clear, specific task with deliverables
- **Success Criteria**: How to validate completion

### Recommended Context
- **ADR References**: `@history/adr/[number]-[title].md` for architectural decisions
- **Related Code**: File paths, class names, function signatures
- **Dependencies**: Other agents, APIs, services that interact
- **Environment**: Dev, staging, prod URLs and credentials
- **Constraints**: Time, performance, security requirements

### Example: Comprehensive Invocation
```
Invoke Backend Engineer: Implement task tags feature per @specs/005-task-tags/spec.md

Context:
- ADR Reference: @history/adr/003-database-choice-neon-postgresql.md
- Database: Neon PostgreSQL with ARRAY column type
- Existing Code: backend/app/models/task.py (Task model)
- API Contract: Tags should be array of strings, max 10 per task
- Authentication: Requires user session (Better Auth)
- Performance: Tag queries should use GIN index

Deliverables:
- Update Task model with tags column (ARRAY)
- Alembic migration for tags column + GIN index
- API endpoints: POST /api/tasks/:id/tags, DELETE /api/tasks/:id/tags/:tag
- Pydantic models for tag operations
- Integration tests (>80% coverage)
- OpenAPI spec update

Success Criteria:
- Migration runs without errors on Neon dev branch
- API endpoints return correct data and status codes
- Tags are searchable with acceptable performance (<200ms)
- Tests pass with >80% coverage
```

---

## Agent Expertise Matrix

### AI Engineer Agent
- **Strong**: OpenAI Agents SDK, MCP tool design, NLP, conversation state
- **Medium**: Python, FastAPI basics, database concepts
- **Weak**: Frontend, CSS, browser APIs

**Best For**:
- Designing conversational interfaces
- MCP tool schema design
- Intent parsing and ambiguity handling
- Agent orchestration

**Avoid For**:
- Implementing FastAPI routes (use Backend Engineer)
- UI component design (use Frontend Engineer)

### Backend Engineer Agent
- **Strong**: FastAPI, SQLModel, PostgreSQL, REST APIs, MCP server impl
- **Medium**: Docker, Dapr, Kafka, performance optimization
- **Weak**: Frontend, React, browser APIs

**Best For**:
- API endpoint implementation
- Database schema design
- MCP server setup
- Authentication/authorization

**Avoid For**:
- UI components (use Frontend Engineer)
- NLP/conversation design (use AI Engineer)

### Data Migration Agent
- **Strong**: Alembic, SQLModel, data validation, Neon PostgreSQL
- **Medium**: Python scripting, ETL patterns
- **Weak**: API design, frontend, real-time systems

**Best For**:
- Schema migrations
- Phase migrations (JSON → PostgreSQL)
- Data integrity validation
- Rollback strategies

**Avoid For**:
- API implementation (use Backend Engineer)
- UI work (use Frontend Engineer)

### File & Persistence Agent
- **Strong**: File I/O, JSON, atomic writes, Dapr state, security
- **Medium**: Python, cloud storage (S3), caching
- **Weak**: Database design, frontend, networking

**Best For**:
- Phase 1 file operations review
- Dapr state store integration
- File upload/download security
- Storage abstraction

**Avoid For**:
- Database migrations (use Data Migration)
- API design (use Backend Engineer)

### Frontend Engineer Agent
- **Strong**: Next.js, React, TypeScript, Tailwind, shadcn/ui, Better Auth client
- **Medium**: HTML/CSS, accessibility, browser APIs
- **Weak**: Backend, databases, server-side logic

**Best For**:
- UI component development
- Page implementation
- Better Auth client integration
- Responsive design

**Avoid For**:
- API implementation (use Backend Engineer)
- MCP tool design (use AI Engineer)

### QA & Testing Agent
- **Strong**: pytest, Vitest, Playwright, accessibility audits, coverage
- **Medium**: CI/CD, security scanning, performance testing
- **Weak**: Feature implementation (not a developer)

**Best For**:
- Writing tests (unit, integration, E2E)
- Accessibility audits
- Coverage enforcement
- Test automation in CI/CD

**Avoid For**:
- Implementing features (delegate to appropriate engineer)
- Designing architecture (use relevant engineer + planning)

---

## Quality Standards

All agents must adhere to:

### Code Quality
- **Type Safety**: 100% (Pyright strict, TypeScript strict)
- **Test Coverage**: >80% (backend and frontend)
- **Linting**: Zero errors (Ruff, ESLint)
- **Documentation**: Inline comments for complex logic

### Performance
- **API Response**: p95 <200ms, p99 <500ms
- **Page Load**: Lighthouse Performance >90
- **Database Queries**: Indexed, optimized, no N+1

### Security
- **Authentication**: Required for all protected routes/endpoints
- **Input Validation**: Pydantic models, Zod schemas
- **SQL Injection**: Prevented (ORM only, parameterized queries)
- **XSS**: Prevented (React auto-escaping, CSP headers)
- **CSRF**: Prevented (SameSite cookies, CSRF tokens)

### Accessibility
- **WCAG 2.1 AA**: Zero critical violations
- **Keyboard Navigation**: All interactive elements accessible
- **Screen Readers**: ARIA labels, semantic HTML
- **Color Contrast**: >4.5:1 for text

---

## Troubleshooting

### Agent Not Understanding Context
**Problem**: Agent produces incorrect or incomplete output

**Solution**:
1. Provide more specific context (ADR references, code examples)
2. Break task into smaller, focused sub-tasks
3. Reference exact file paths and line numbers
4. Include expected input/output examples

### Agent Collaboration Failure
**Problem**: Agents produce incompatible outputs

**Solution**:
1. Explicitly pass deliverables from one agent to another
2. Use specification as single source of truth
3. Create integration contract (e.g., OpenAPI spec)
4. Have QA Testing agent validate integration

### Quality Standards Not Met
**Problem**: Agent output doesn't meet coverage/performance targets

**Solution**:
1. Invoke QA Testing agent to identify gaps
2. Provide specific quality targets in invocation
3. Request iterative improvements until standards met
4. Document exceptions in ADR if targets cannot be met

---

## Next Steps

1. **Test Agent System**: Invoke each agent with a small task to verify understanding
2. **Create Workflows**: Document common multi-agent workflows for your team
3. **Integrate with SDD**: Use agents in conjunction with `/sp.specify`, `/sp.plan`, `/sp.tasks`
4. **Iterate**: Refine agent definitions based on real-world usage

---

## Related Documentation

- **Constitution**: `.specify/memory/constitution.md` - Project principles
- **ADRs**: `history/adr/` - Architectural decisions
- **Specs**: `specs/` - Feature specifications
- **Templates**: `.specify/templates/` - Document templates

---

**Maintained By**: Architect (shery123pk) + AI Developer (Claude)
**Last Updated**: 2025-12-26
**Version**: 1.0.0
