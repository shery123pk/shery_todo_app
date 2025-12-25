---
id: 001
title: Evolution of Todo Constitution v1.0.0
stage: constitution
date: 2025-12-26
surface: agent
model: claude-sonnet-4-5
feature: none
branch: master
user: shery123pk
command: /sp.constitution
labels: ["constitution", "governance", "sdd", "serena-rules", "semantic-editing"]
links:
  spec: null
  ticket: null
  adr: null
  pr: null
files:
 - .specify/memory/constitution.md
tests:
 - N/A (constitution documentation)
---

## Prompt

Project Constitution
The Evolution of Todo
A 5-Phase Hackathon Project: From Simple CLI to Cloud-Native AI-Powered Distributed Todo System
Version: 1.1.0 (December 25, 2025)
Core Purpose: Demonstrate mastery of Spec-Driven Development (SDD) using Claude Code and Spec-Kit Plus, where the human acts as Architect and Claude (AI) acts as the exclusive Developer. Evolve a basic todo app across five phases in a single monorepo, ensuring additive evolution, full traceability, and integration of reusable intelligence via subagents and agent skills.
Supremacy Clause: This Constitution is the ultimate authority. Any conflicting spec, plan, task, code, or decision is invalid and must be regenerated to comply.

[Full constitution text provided by user, including all 7 core principles, domain model, technology stack, repository structure, quality standards, phase roadmap, 10 subagent roles, execution policies, ADR guidelines, and governance procedures]

Also include Serena's usage rules in your constitution:

# Constitution Rules

- All semantic code changes should go through Serena-assisted edits.
- An LSP semantic search must be used before manual code edits.
- Agents should avoid blind regex or text matching edits.

This ensures your agent always uses structured editing over guesswork.

## Response snapshot

Created comprehensive project constitution v1.0.0 for "The Evolution of Todo" hackathon project with the following key components:

**Core Principles (6 principles)**:
1. Spec-Driven Development Only - Strict SDD workflow enforcement
2. AI as Sole Developer - Clear human/AI role separation
3. Semantic Code Editing (Serena Rules) - LSP-based structured editing mandate
4. Full Traceability & Audit Trail - ADR→Spec→Plan→Tasks→Code→Tests linkage
5. Test-First & Evolutionary Safeguards - >80% coverage, regression protection
6. Reusable Intelligence Integration - Modular subagents with defined skills

**Unified Domain Model**: Progressive schema across 5 phases (Phase 1 core: id, title, description, completed; Phase 2+ adds priority, tags, timestamps; Phase 3+ adds due_date, recurrence, reminders, assigned_to, parent_id)

**Technology Stack**: Python 3.13+/UV, FastAPI, SQLModel, Next.js 16+, TypeScript, Better Auth, OpenAI Agents SDK/ChatKit, MCP SDK, Kafka/Redpanda, Dapr, Neon PostgreSQL, Docker/K8s/Helm, GitHub Actions

**10 Specialized Subagents**: AI Engineer, Backend Engineer, Data Migration, File & Persistence, Frontend Engineer, QA & Testing, UX Polisher, DevOps & Deployment, Security & Compliance, Documentation

**5-Phase Roadmap**: CLI→Full-Stack Web→AI Chatbot→Local K8s→Cloud Deployment

**Governance**: Semantic versioning, amendment procedures, compliance review, conflict resolution hierarchy

**Serena Integration**: Added as Principle III with mandatory LSP-based editing, semantic search before edits, prohibition of blind regex/text matching

## Outcome

- ✅ Impact: Established constitutional foundation for entire project; all future work must comply with these principles
- 🧪 Tests: N/A (governance document)
- 📁 Files: Created .specify/memory/constitution.md (508 lines), created history/prompts/constitution/ directory structure
- 🔁 Next prompts: /sp.specify to create feature specifications, /sp.plan for implementation planning
- 🧠 Reflection: Successfully integrated Serena semantic editing rules as a core constitutional principle, ensuring all code changes use LSP-aware tools rather than blind text manipulation. This elevates code quality and prevents breaking changes.

## Evaluation notes (flywheel)

- Failure modes observed: None
- Graders run and results (PASS/FAIL):
  - ✅ PASS - All placeholders filled
  - ✅ PASS - Serena rules integrated as Principle III
  - ✅ PASS - All 10 subagents documented with skills
  - ✅ PASS - Phase roadmap complete with transition requirements
  - ✅ PASS - Semantic versioning and governance procedures defined
- Prompt variant (if applicable): Initial constitution creation (no variants)
- Next experiment (smallest change to try): Create first feature specification using /sp.specify to test SDD workflow compliance
