# Agent Quick Reference Card

**Project**: Evolution of Todo
**Purpose**: Fast agent invocation patterns
**Usage**: Copy, paste, modify for your task

---

## 🎯 Quick Invocation Templates

### AI Engineer Agent
```
Invoke AI Engineer: [Design MCP tools | Implement intent parser | Create agent orchestration] per @specs/[feature].md

Context:
- [Backend endpoints available]
- [User natural language examples]
- [Expected tool behavior]

Deliverables:
- [MCP tool schemas | Intent extraction logic | Agent routing]
- [Parameter validation]
- [Integration tests]
```

### Backend Engineer Agent
```
Invoke Backend Engineer: [Implement API endpoints | Create database schema | Set up MCP server] per @specs/[feature].md

Context:
- [Database: Neon PostgreSQL]
- [Authentication: Better Auth session]
- [Performance requirements]

Deliverables:
- [FastAPI routes | SQLModel schemas | MCP server config]
- [Pydantic models]
- [Integration tests (>80% coverage)]
```

### Data Migration Agent
```
Invoke Data Migration: [Migrate Phase X data | Create schema migration | Set up Neon branches] per @specs/[feature].md

Context:
- Source: [describe current state]
- Target: [describe desired state]
- Volume: [number of records]
- Downtime: [constraints]

Deliverables:
- [Migration script | Alembic migration | Neon CLI commands]
- [Validation tests]
- [Rollback procedure]
```

### File & Persistence Agent
```
Invoke File & Persistence: [Review file operations | Implement Dapr state | Secure file uploads] per @specs/[feature].md

Context:
- [Storage type: local | S3 | Dapr state]
- [Security requirements]
- [File types and size limits]

Deliverables:
- [File operation code | Dapr config | Security validation]
- [Atomic write pattern]
- [Security tests]
```

### Frontend Engineer Agent
```
Invoke Frontend Engineer: [Implement page | Create component | Integrate Better Auth] per @specs/[feature].md

Context:
- [API endpoints available]
- [UI requirements: responsive, accessible]
- [User flows]

Deliverables:
- [Next.js pages/components]
- [Tailwind styling]
- [Component tests]
- [Accessibility compliance]
```

### QA & Testing Agent
```
Invoke QA Testing: [Create integration tests | Run E2E tests | Audit accessibility] per @specs/[feature].md

Context:
- [Feature under test]
- [Test scenarios]
- [Coverage target: >80%]

Deliverables:
- [Test suite (pytest | Vitest | Playwright)]
- [Coverage report]
- [Accessibility audit results]
```

### Token Checker Agent
```
Invoke Token Checker: [Analyze usage | Set up tracking | Enforce budget] per @specs/[feature].md

Context:
- LLM Provider: [OpenAI | Anthropic | Multi]
- Budget: [Daily/Weekly/Monthly limits]
- Expected Usage: [Volume estimates]
- Alert Preferences: [Email | Slack | Webhooks]

Deliverables:
- [Usage analysis | Tracking middleware | Budget enforcement]
- [Cost projections]
- [Optimization recommendations]
- [Alert configuration]
```

### Serena Agent
```
Invoke Serena: [Find code | Map dependencies | Rename symbol | Extract function] per @specs/[feature].md

Context:
- Target: [File path, function name, line numbers]
- Scope: [File | Module | All]
- Language: [Python | TypeScript | Both]
- Safety: [Run tests | Preview only]

Deliverables:
- [Search results | Dependency graph | Refactored code]
- [List of modified files]
- [Impact analysis]
- [Test verification]
```

---

## 📋 Common Workflows

### New Feature Implementation
```
1. Invoke Backend Engineer: Implement [feature] API per @specs/XXX-[feature]/spec.md
2. Invoke Frontend Engineer: Implement [feature] UI per @specs/XXX-[feature]/spec.md
3. Invoke QA Testing: Validate [feature] per @specs/XXX-[feature]/spec.md
```

### Database Migration
```
1. Invoke Data Migration: Plan migration for [change] per @specs/XXX-[feature]/spec.md
2. Invoke Data Migration: Implement migration script per migration plan
3. Invoke QA Testing: Validate migration on Neon dev branch per migration plan
```

### AI Integration
```
1. Invoke AI Engineer: Design MCP tools for [feature] per @specs/XXX-[feature]/spec.md
2. Invoke Backend Engineer: Implement MCP server per AI Engineer specifications
3. Invoke Frontend Engineer: Integrate ChatKit UI per @specs/XXX-[feature]/spec.md
```

---

## 🔗 Essential References

| What | Where |
|------|-------|
| Agent Details | `.specify/agents/[agent-name].md` |
| Full Documentation | `.specify/agents/README.md` |
| Specifications | `specs/[number]-[feature]/spec.md` |
| ADRs | `history/adr/[number]-[title].md` |
| Constitution | `.specify/memory/constitution.md` |

---

## ✅ Invocation Checklist

Before invoking any agent:

- [ ] Specification exists: `@specs/[number]-[feature]/spec.md`
- [ ] Task is specific and focused
- [ ] Context is comprehensive (ADRs, code refs, constraints)
- [ ] Deliverables are clearly listed
- [ ] Success criteria are measurable

---

## 💡 Pro Tips

1. **Always reference specs**: Use `@specs/[feature].md` syntax
2. **Link ADRs**: Reference `@history/adr/[number]-[title].md` for context
3. **Be specific**: "Implement task CRUD API" better than "build backend"
4. **Provide examples**: Show expected input/output when possible
5. **Set quality bars**: Specify coverage, performance, accessibility targets
6. **Chain agents**: Pass deliverables from one agent to another
7. **Test early**: Invoke QA Testing agent frequently, not just at the end

---

## 🚀 Phase 2 Example Invocations

### Backend: Task CRUD API
```
Invoke Backend Engineer: Implement task CRUD endpoints per @specs/002-fullstack-web/spec.md

Context:
- Database: Neon PostgreSQL with UUID primary keys
- Authentication: Better Auth session cookies (user_id from session)
- ADR References: @history/adr/001-id-migration-strategy.md, @history/adr/003-database-choice-neon-postgresql.md
- API Contract: RESTful endpoints with JSON responses
- Rate Limiting: 100 requests/minute per user

Deliverables:
- FastAPI router: backend/app/routers/tasks.py
- SQLModel schema: backend/app/models/task.py
- Pydantic models: backend/app/schemas/task.py
- Dependency injection for auth: backend/app/dependencies.py
- Integration tests: backend/tests/integration/test_tasks.py (>80% coverage)
- OpenAPI spec update

Success Criteria:
- All CRUD operations work (Create, Read, Update, Delete)
- User isolation enforced (users only see their own tasks)
- API response times <200ms (p95)
- Tests pass with >80% coverage
```

### Frontend: Tasks Dashboard
```
Invoke Frontend Engineer: Implement tasks dashboard page per @specs/002-fullstack-web/spec.md

Context:
- API Endpoints: GET /api/tasks, POST /api/tasks, PATCH /api/tasks/:id, DELETE /api/tasks/:id
- Authentication: Better Auth session (middleware protects /tasks route)
- UI Requirements: Responsive (mobile-first), accessible (WCAG 2.1 AA)
- Component Library: shadcn/ui (Card, Button, Input)
- Styling: Tailwind CSS with dark mode support

Deliverables:
- Page: frontend/app/tasks/page.tsx (Server Component)
- Components: frontend/components/TaskList.tsx, frontend/components/TaskCard.tsx
- API Client: frontend/lib/api.ts (getTasks, createTask, completeTask, deleteTask)
- Optimistic UI updates for task completion
- Component tests: frontend/components/__tests__/TaskCard.test.tsx
- Accessibility: keyboard navigation, ARIA labels

Success Criteria:
- Page loads in <2 seconds
- Responsive on mobile (375px) to desktop (1920px)
- Lighthouse Performance >90, Accessibility >90
- All interactive elements keyboard accessible
- Component tests pass with >80% coverage
```

### Migration: Phase 1 to Phase 2
```
Invoke Data Migration: Migrate Phase 1 JSON tasks to PostgreSQL per @specs/002-fullstack-web/spec.md and @history/adr/001-id-migration-strategy.md

Context:
- Source: cli/tasks.json (Phase 1 JSON file)
- Source Schema: {id: int, title: str, description: str, completed: bool}
- Target: Neon PostgreSQL (Phase 2 database)
- Target Schema: {id: UUID, title: str, description: str, completed: bool, user_id: UUID, created_at: datetime, updated_at: datetime}
- Volume: ~10-100 tasks (demo data)
- Strategy: Create default user, associate all Phase 1 tasks with that user

Deliverables:
- Migration script: backend/scripts/migrate_phase1_to_phase2.py
- Default user creation logic
- Data validation (pre and post-migration)
- Migration report (tasks migrated, errors, warnings)
- Rollback procedure (if needed)

Success Criteria:
- 100% data preservation (no task data lost)
- All Phase 1 tasks accessible in Phase 2 UI
- Migration completes in <10 seconds
- Validation tests pass (task counts match, data integrity verified)
```

---

**Quick Start**: Copy any template above, fill in the bracketed placeholders, and run the invocation!
