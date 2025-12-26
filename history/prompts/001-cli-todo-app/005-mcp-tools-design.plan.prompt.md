---
id: 005
title: MCP Tools Design for Phase 1 CLI
stage: plan
date: 2025-12-26
surface: agent
model: claude-sonnet-4-5-20250929
feature: 001-cli-todo-app
branch: master
user: AEHTRAM
command: Invoke AI Engineer
labels: ["mcp-tools", "design", "ai-integration", "phase1"]
links:
  spec: specs/001-cli-todo-app/spec.md
  ticket: null
  adr: null
  pr: null
files:
  - specs/001-cli-todo-app/contracts/mcp-tools.md
tests:
  - None (design phase)
---

## Prompt

Invoke AI Engineer: Design MCP tools for Phase 1 CLI task management per @specs/001-cli-todo-app/spec.md

Context:
- CLI Commands: add, list, complete, update, delete
- Current Implementation: Python CLI with Click framework
- Data Storage: JSON file (tasks.json)
- Need to expose CLI functionality as MCP tools for AI agents

Deliverables:
- MCP tool schema definitions for each CLI command
- Parameter mapping (CLI args → MCP parameters)
- Expected tool responses
- Error handling patterns

Reference the AI Engineer agent definition at: .specify/agents/ai-engineer.md

## Response snapshot

Designed comprehensive MCP tool schemas for all 5 Phase 1 CLI commands:

1. **todo_add** - Create new task with title and optional description
   - Input: title (string, 1-200 chars), description (string, 0-1000 chars, optional)
   - Output: Task object with auto-assigned ID, success message
   - Errors: ValidationError for empty/too-long title or description

2. **todo_list** - View tasks with filtering
   - Input: filter (enum: "all", "incomplete", "completed", default: "incomplete")
   - Output: Array of task objects, summary statistics (total/completed/incomplete counts)
   - Errors: None (returns empty array if no tasks)

3. **todo_complete** - Mark task as done
   - Input: task_id (integer, minimum: 1)
   - Output: Updated task object with completed=true
   - Errors: NotFoundError if task doesn't exist

4. **todo_update** - Modify task title/description
   - Input: task_id (integer), title (string, optional), description (string, optional)
   - Constraint: At least one of title or description must be provided
   - Output: Updated task object, indication of which fields changed
   - Errors: NotFoundError, ValidationError

5. **todo_delete** - Permanently remove task
   - Input: task_id (integer), confirm (boolean, default: true)
   - Output: Deleted task info, success message with warning
   - Errors: NotFoundError

Key design decisions:
- Direct 1:1 mapping between CLI commands and MCP tools
- Stateless tools - each call creates fresh repository instance that loads/saves tasks.json
- Standardized error response format with error_type classification
- Rich responses with structured data suitable for LLM consumption
- Response format consistency across all tools
- Integration guide for Backend Engineer with implementation patterns
- Testing strategy with unit and integration test examples

Document includes:
- Complete JSON schemas for all 5 tools
- Parameter mapping tables showing CLI → MCP equivalence
- Implementation flow pseudo-code for each tool
- Success and error response examples
- Error handling patterns and classification
- Repository state management strategy
- Performance considerations (<100ms for all operations)
- Security considerations (input validation, file safety)
- Migration path to future phases (REST API, database)
- Integration guide for Backend Engineer
- Testing strategy and coverage requirements

## Outcome

- ✅ Impact: Complete MCP tool design specification ready for implementation
- 🧪 Tests: Testing strategy documented (unit tests, integration tests, coverage requirements)
- 📁 Files: Created specs/001-cli-todo-app/contracts/mcp-tools.md (comprehensive design doc)
- 🔁 Next prompts:
  - "Invoke Backend Engineer: Implement MCP server per @specs/001-cli-todo-app/contracts/mcp-tools.md"
  - "Invoke QA & Testing: Create MCP tool test suite per @specs/001-cli-todo-app/contracts/mcp-tools.md"
- 🧠 Reflection: Design leverages existing CLI implementation perfectly - minimal code changes needed since repository layer is already clean and testable. MCP tools are thin wrappers around existing functionality.

## Evaluation notes (flywheel)

- Failure modes observed: None - existing CLI implementation is well-structured for MCP exposure
- Graders run and results (PASS/FAIL): N/A (design phase, no code grading)
- Prompt variant (if applicable): Standard AI Engineer invocation pattern
- Next experiment (smallest change to try): Implement one MCP tool (todo_add) as proof of concept before full implementation
