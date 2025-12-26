---
id: 001
title: Deployment Strategy HuggingFace Spaces
stage: spec
date: 2025-12-26
surface: agent
model: claude-sonnet-4-5
feature: fullstack-web
branch: 002-fullstack-web
user: shery123pk
command: continue phase 2 spec
labels: ["deployment", "architecture", "adr", "huggingface-spaces", "vercel", "neon"]
links:
  spec: specs/002-fullstack-web/spec.md
  ticket: null
  adr: history/adr/005-deployment-strategy-huggingface-spaces.md
  pr: null
files:
  - history/adr/005-deployment-strategy-huggingface-spaces.md
  - specs/002-fullstack-web/spec.md
tests:
  - null
---

## Prompt

This revised plan updates the deployment strategy to use Hugging Face Spaces instead of Railway for backend hosting. The frontend remains deployable to Vercel (optimized for Next.js) or as a static Space if needed.

Frontend: Next.js 16+ → Deploy to Vercel (primary) for optimal performance/CDN
Backend: FastAPI → Deploy as Docker Space on Hugging Face (listens on port 7860, exposes /docs)
Database: Neon Serverless PostgreSQL (external, connected via DATABASE_URL)
Authentication: Better Auth + JWT (httpOnly cookies)

Key Requirements:
- Backend must use port 7860 (HuggingFace Spaces requirement)
- CORS configuration for Vercel ↔ HF Space communication
- Create ADR documenting deployment decision
- Update Phase 2 spec with HF deployment details

## Response snapshot

Created comprehensive deployment strategy documentation:

1. **ADR-005 Created** (8,000+ words): `history/adr/005-deployment-strategy-huggingface-spaces.md`
   - Decision: HuggingFace Spaces (backend) + Vercel (frontend) + Neon (database)
   - Rationale: 100% free tier, Docker support, zero-config Next.js, serverless PostgreSQL
   - Critical Dockerfile configuration for port 7860
   - CORS setup for cross-origin communication
   - Secrets management strategy
   - Deployment checklists
   - Cost analysis: $0/month for demo
   - Alternatives rejected: Railway ($5/mo minimum), Render (cold start), Fly.io (insufficient RAM)

2. **Phase 2 Spec Updated**: `specs/002-fullstack-web/spec.md`
   - Updated NFR-029 to NFR-033 with HF-specific deployment requirements
   - Added port 7860 requirement (NFR-030) - non-negotiable HF constraint
   - Added CORS requirement for Vercel ↔ HF communication (NFR-033)
   - Added ADR-005 reference to Related ADRs section
   - Updated deployment technology stack

Key Technical Details Documented:
- **Port 7860**: Mandatory for HuggingFace Spaces Docker SDK apps
- **Dockerfile CMD**: `uvicorn app.main:app --host 0.0.0.0 --port 7860`
- **CORS Origins**: Must allow `https://[your-app].vercel.app`
- **Environment Variables**: DATABASE_URL, BETTER_AUTH_SECRET, BETTER_AUTH_URL, FRONTEND_URL
- **Deployment URLs**: Backend at `https://[username]-todo-backend.hf.space`, Frontend at `https://[your-app].vercel.app`

## Outcome

- ✅ Impact: Finalized Phase 2 deployment architecture with complete documentation, enabling zero-cost demo deployment
- 🧪 Tests: No tests (documentation work)
- 📁 Files: Created ADR-005, updated Phase 2 spec (NFR-029 to NFR-033)
- 🔁 Next prompts: Proceed with `/sp.plan` to create implementation plan for Phase 2
- 🧠 Reflection: Deployment strategy now fully documented with all critical constraints (port 7860, CORS, secrets). Ready for implementation planning phase.

## Evaluation notes (flywheel)

- Failure modes observed: None - deployment strategy clearly specified by user
- Graders run and results (PASS/FAIL): PASS - All ADR sections complete, spec updated with NFRs, port 7860 documented
- Prompt variant (if applicable): Standard deployment strategy documentation
- Next experiment (smallest change to try): Test Dockerfile locally before HF deployment to verify port 7860 configuration
