# Implementation Plan: In-Memory Python Console Todo App

**Branch**: `001-cli-todo-app` | **Date**: 2025-12-26 | **Spec**: [spec.md](spec.md)
**Input**: Feature specification from `specs/001-cli-todo-app/spec.md`

## Summary

Build a Python 3.13+ command-line todo application with interactive CRUD operations and JSON file persistence. This establishes the immutable core domain model (Task: id, title, description, completed) that all future phases must preserve semantically. The implementation uses UV for dependency management, provides immediate feedback for all operations, and ensures data durability through automatic JSON persistence.

**Technical Approach**: Single-file Python CLI using standard library for core logic, minimal external dependencies (only for CLI framework), in-memory data structure with JSON serialization for persistence, comprehensive error handling with user-friendly messages.

## Technical Context

**Language/Version**: Python 3.13+
**Primary Dependencies**:
- Core: Python standard library (json, pathlib, signal, sys)
- CLI Framework: Click 8.1+ (command parsing, argument validation, help generation)
- Testing: pytest 8.0+ (unit/integration tests), pytest-cov (coverage reporting)
- Development: UV (fast Python package manager), ruff (linting/formatting)

**Storage**: JSON file (tasks.json) in current working directory
**Testing**: pytest with >80% coverage requirement, unit tests for domain logic, integration tests for CLI commands
**Target Platform**: Cross-platform (Windows, macOS, Linux) - any OS with Python 3.13+
**Project Type**: Single Python CLI application
**Performance Goals**:
- Startup: <1 second for 100 tasks
- Command execution: <100ms for all operations
- List display: <2 seconds for any number of tasks
**Constraints**:
- Title: 1-200 characters (required)
- Description: 0-1000 characters (optional)
- In-memory operations only (JSON is persistence layer, not database)
- Single-user, single-process (no concurrency)
**Scale/Scope**:
- Expected: 10-100 tasks typical usage
- Support: Up to 1000 tasks without performance degradation
- Single Python file CLI entry point, modular domain/repository separation

## Constitution Check

*GATE: Must pass before Phase 0 research. Re-check after Phase 1 design.*

### Principle I: Spec-Driven Development Only
- ✅ PASS: Specification approved and validated (16/16 quality checks)
- ✅ PASS: This plan generated from spec via `/sp.plan` command
- ✅ PASS: No code written before spec/plan approval

### Principle II: AI as Sole Developer
- ✅ PASS: AI (Claude) generating this plan from human-authored spec
- ✅ PASS: Human (Architect) will review and approve plan before `/sp.tasks`

### Principle III: Semantic Code Editing (Serena Rules)
- ✅ PASS: Plan includes LSP setup (Pyright for Python)
- ✅ PASS: All future code edits will use LSP-aware tools
- ✅ PASS: No blind regex/text edits planned

### Principle IV: Full Traceability & Audit Trail
- ✅ PASS: Clear lineage: Constitution → Spec → Plan → Tasks → Code → Tests
- ✅ PASS: PHR tracking enabled for all phases
- ✅ PASS: Git branch `001-cli-todo-app` isolates this feature

### Principle V: Test-First & Evolutionary Safeguards
- ✅ PASS: >80% coverage requirement documented
- ✅ PASS: Unit tests planned before implementation
- ✅ PASS: Integration tests planned for CLI commands
- ✅ PASS: Phase 1 immutable core protects future phase compatibility

### Principle VI: Reusable Intelligence Integration
- ✅ PASS: Backend Engineer Agent will handle implementation
- ✅ PASS: QA & Testing Agent will handle test suite
- ✅ PASS: File & Persistence Agent will handle JSON operations

### Technology Stack Compliance
- ✅ PASS: Python 3.13+ (constitution-mandated backend language)
- ✅ PASS: UV for dependency management (constitution-mandated)
- ✅ PASS: No forbidden practices (no hardcoded secrets, proper error handling)

### Quality Standards Compliance
- ✅ PASS: Code quality: Modular, DRY, complexity <10, type hints
- ✅ PASS: Testing: pytest, >80% coverage, unit + integration
- ✅ PASS: Documentation: README.md, inline comments for complexity only

**Overall Gate Status**: ✅ **ALL GATES PASSED** - Proceed to Phase 0 Research

## Project Structure

### Documentation (this feature)

```text
specs/001-cli-todo-app/
├── spec.md              # Feature specification (completed)
├── plan.md              # This file (in progress)
├── research.md          # Phase 0 output (to be generated)
├── data-model.md        # Phase 1 output (to be generated)
├── quickstart.md        # Phase 1 output (to be generated)
├── contracts/           # Phase 1 output (to be generated)
│   └── cli-commands.md  # CLI command specifications
├── checklists/
│   └── requirements.md  # Spec validation (completed)
└── tasks.md             # Phase 2 output (NOT created by /sp.plan)
```

### Source Code (repository root)

```text
src/
├── todo_cli/
│   ├── __init__.py
│   ├── main.py          # CLI entry point, interactive loop
│   ├── models.py        # Task model with validation
│   ├── repository.py    # InMemoryRepository with JSON persistence
│   ├── commands.py      # Click command implementations
│   └── utils.py         # Helper functions (formatting, validation)

tests/
├── unit/
│   ├── test_models.py       # Task model validation tests
│   ├── test_repository.py   # Repository CRUD operations tests
│   └── test_utils.py        # Utility function tests
├── integration/
│   ├── test_cli_commands.py # End-to-end CLI command tests
│   └── test_persistence.py  # JSON save/load integration tests
└── conftest.py              # pytest fixtures and test configuration

pyproject.toml           # UV project configuration, dependencies
README.md                # Setup and usage instructions
.python-version          # Python version pinning (3.13)
.gitignore               # Exclude __pycache__, .venv, tasks.json
```

**Structure Decision**: Single Python project structure selected because this is a standalone CLI application with no web/mobile components. All code lives under `src/todo_cli/` for clear module organization. Tests mirror the source structure for easy navigation. Using modern Python packaging with `pyproject.toml` and UV for fast dependency management.

## Complexity Tracking

> **No violations detected. All constitution gates passed.**

This section intentionally left empty as no complexity violations require justification.

## Phase 0: Research & Technology Decisions

### Research Topics

All technology decisions are straightforward for this CLI application. No research required as all choices align with constitution-mandated stack and standard Python practices.

### Technology Decisions

| Decision | Choice | Rationale | Alternatives Considered |
|----------|--------|-----------|-------------------------|
| Python Version | 3.13+ | Constitution-mandated; latest features (better error messages, performance) | 3.11, 3.12 (older, less performant) |
| Package Manager | UV | Constitution-mandated; 10-100x faster than pip | pip (slow), poetry (complex) |
| CLI Framework | Click 8.1+ | Industry standard, excellent docs, automatic help generation, type-safe | argparse (verbose), typer (heavier), fire (magic) |
| Persistence Format | JSON | Human-readable, stdlib support, future-phase compatible | pickle (opaque), sqlite (over-engineered for Phase 1) |
| Testing Framework | pytest | Constitution-standard, fixture support, parametrization | unittest (verbose), nose (unmaintained) |
| Linter/Formatter | ruff | Fast (Rust-based), replaces 10+ tools, auto-fix | black+flake8+isort (slow, multiple tools) |
| Type Checking | Pyright | LSP-compatible (Serena compliance), fast, VS Code native | mypy (slower), none (unsafe) |

### Dependency Justification

**Production Dependencies**:
- `click>=8.1.0`: CLI framework for command parsing, validation, help generation

**Development Dependencies**:
- `pytest>=8.0.0`: Testing framework (unit + integration)
- `pytest-cov>=4.1.0`: Coverage reporting (>80% requirement)
- `ruff>=0.2.0`: Linting and formatting
- `pyright>=1.1.0`: Type checking and LSP support (Serena compliance)

**No external dependencies** for core logic - uses stdlib for JSON, file I/O, signal handling to minimize attack surface and dependency bloat.

## Phase 1: Design & Contracts

### Architecture Overview

**Pattern**: Layered architecture with clear separation of concerns
- **Domain Layer** (`models.py`): Task entity with validation logic
- **Repository Layer** (`repository.py`): In-memory storage + JSON persistence
- **CLI Layer** (`commands.py`, `main.py`): User interaction and command dispatch
- **Utilities** (`utils.py`): Formatting, validation helpers

**Data Flow**:
1. User enters command → Click parses and validates arguments
2. Command handler → Repository method call
3. Repository → In-memory data structure modification
4. Repository → Auto-save to JSON (if write operation)
5. Command handler → Format and display result to user

**Error Handling Strategy**:
- Domain errors (validation): Raise `ValueError` with clear message
- Repository errors (not found): Raise `KeyError` with ID
- File I/O errors: Catch, display user-friendly message, continue with in-memory data
- All CLI commands: Catch exceptions, display formatted error, don't crash

### Key Components

#### 1. Task Model (`models.py`)

**Responsibility**: Represent todo item with validation

**Attributes**:
- `id: int` - Unique identifier (immutable, auto-assigned by repository)
- `title: str` - Task description (required, 1-200 chars)
- `description: str` - Optional details (0-1000 chars)
- `completed: bool` - Completion status (default False)

**Methods**:
- `__init__(id, title, description="", completed=False)`: Initialize with validation
- `validate_title(title) -> str`: Ensure 1-200 chars, raise ValueError if invalid
- `validate_description(desc) -> str`: Ensure 0-1000 chars, raise ValueError if invalid
- `to_dict() -> dict`: Serialize for JSON
- `from_dict(data: dict) -> Task`: Deserialize from JSON (class method)

**Validation Rules**:
- Title: Required, 1-200 characters, no leading/trailing whitespace
- Description: Optional, 0-1000 characters
- Completed: Boolean only (strict type checking)

#### 2. Repository (`repository.py`)

**Responsibility**: Manage in-memory task collection with JSON persistence

**State**:
- `tasks: dict[int, Task]` - In-memory storage (ID → Task mapping)
- `next_id: int` - Auto-increment counter for new task IDs
- `file_path: Path` - Path to tasks.json

**Methods**:
- `__init__(file_path="tasks.json")`: Initialize, load from file if exists
- `add(title: str, description: str = "") -> Task`: Create task, assign ID, save, return task
- `get(task_id: int) -> Task`: Retrieve task by ID, raise KeyError if not found
- `list_all() -> list[Task]`: Return all tasks sorted by ID
- `update(task_id: int, title: str = None, description: str = None) -> Task`: Update fields, save
- `complete(task_id: int) -> Task`: Mark task complete, save
- `delete(task_id: int) -> None`: Remove task, save
- `_load() -> None`: Load tasks from JSON, handle errors gracefully
- `_save() -> None`: Write tasks to JSON, handle I/O errors with user message

**Persistence Behavior**:
- Load on init: If file exists and valid JSON, restore tasks and next_id
- Load on error: Display warning, start with empty state
- Save on modification: Auto-save after add, update, complete, delete
- Save on exit: Explicit save called by exit command

#### 3. CLI Commands (`commands.py`)

**Responsibility**: Implement Click command handlers

**Command Group**: `cli` (main entry point)

**Commands**:
- `add <title> [--desc <description>]`: Create new task
- `list`: Display all tasks with formatting
- `complete <id>`: Mark task as complete
- `update <id> [--title <new_title>] [--desc <new_desc>]`: Modify task
- `delete <id>`: Remove task
- `exit`: Save and terminate
- `help`: Show command usage (built-in Click feature)

**Output Formatting**:
- Success messages: Green text (Click.style)
- Error messages: Red text (Click.style)
- Task list: Table format with ID, Status ([✓]/[ ]), Title, Description (truncated if long)

#### 4. Interactive Loop (`main.py`)

**Responsibility**: Run REPL for continuous command input

**Behavior**:
- Display welcome message with instructions
- Loop: Read input → Parse as Click command → Execute → Display result
- Handle Ctrl+C: Catch SIGINT, save data, exit gracefully
- Handle invalid commands: Display error, show help hint
- Handle exit command: Save, display goodbye, terminate

### Non-Functional Requirements Implementation

| NFR | Implementation Strategy |
|-----|-------------------------|
| Performance (SC-001, SC-002, SC-007) | In-memory operations (instant), minimal parsing overhead, lazy JSON writes |
| Reliability (SC-003, SC-004) | Comprehensive validation, error handling, auto-save after modifications |
| Usability (SC-005, SC-006) | Clear error messages, inline help, predictable command syntax |
| Data Persistence | JSON format, atomic writes (write temp → rename), corruption recovery |

## Phase 2: Implementation Roadmap

**Note**: Detailed tasks will be generated by `/sp.tasks` command. This section provides high-level implementation order.

### Implementation Order (by User Story Priority)

1. **Foundation Setup** (prerequisite for all stories)
   - Initialize project with UV (pyproject.toml, .python-version)
   - Setup directory structure (src/, tests/)
   - Configure development tools (ruff, pyright, pytest)

2. **P1: Add New Tasks** (User Story 1)
   - Implement Task model with validation
   - Implement Repository.add() method
   - Implement `add` CLI command
   - Unit tests: Task validation, Repository.add()
   - Integration test: CLI add command end-to-end

3. **P1: View All Tasks** (User Story 2)
   - Implement Repository.list_all() method
   - Implement `list` CLI command with formatting
   - Unit tests: Repository.list_all()
   - Integration test: CLI list command end-to-end

4. **P1: Exit and Data Persistence** (User Story 6)
   - Implement Repository._load() and _save() methods
   - Implement `exit` CLI command
   - Add Ctrl+C signal handler in main loop
   - Unit tests: JSON serialization/deserialization
   - Integration tests: Persistence across restarts, corruption handling

5. **P2: Mark Tasks Complete** (User Story 3)
   - Implement Repository.complete() method
   - Implement `complete` CLI command
   - Unit tests: Repository.complete()
   - Integration test: CLI complete command end-to-end

6. **P3: Update Existing Tasks** (User Story 4)
   - Implement Repository.update() method
   - Implement `update` CLI command
   - Unit tests: Repository.update()
   - Integration test: CLI update command end-to-end

7. **P3: Delete Tasks** (User Story 5)
   - Implement Repository.delete() method
   - Implement `delete` CLI command
   - Unit tests: Repository.delete()
   - Integration test: CLI delete command end-to-end

8. **Polish & Documentation**
   - Write README.md with setup and usage instructions
   - Add docstrings to all public methods
   - Final coverage check (>80% requirement)
   - Validate all acceptance criteria pass

### Testing Strategy

**Unit Tests** (tests/unit/):
- `test_models.py`: Task validation (title/description length, type checking)
- `test_repository.py`: All CRUD operations, ID generation, in-memory state
- `test_utils.py`: Formatting helpers, input sanitization

**Integration Tests** (tests/integration/):
- `test_cli_commands.py`: End-to-end CLI command execution with CliRunner
- `test_persistence.py`: JSON save/load cycle, corruption recovery, file permissions

**Coverage Target**: >80% (constitution requirement)

**Test Execution**:
```bash
pytest --cov=src/todo_cli --cov-report=term-missing --cov-report=html
```

### Deployment & Operations

**Setup Instructions** (for README.md):
1. Install UV: `curl -LsSf https://astral.sh/uv/install.sh | sh`
2. Clone repo and navigate to project
3. Create virtual environment: `uv venv`
4. Install dependencies: `uv pip install -e .`
5. Run app: `python -m todo_cli.main`

**Usage Examples**:
```bash
# Interactive mode (recommended)
python -m todo_cli.main

# Direct commands (future enhancement, not Phase 1)
# python -m todo_cli.main add "Buy milk"
```

**Data Location**:
- `tasks.json` created in current working directory
- Users can delete file to reset app state

## Risks & Mitigations

| Risk | Impact | Mitigation |
|------|--------|------------|
| JSON file corruption | Users lose task data | Graceful error handling, start fresh with warning |
| Disk full during save | Data not persisted | Catch IOError, display clear message, continue with in-memory |
| Large task count (>1000) | Slow startup/list | Acceptable for Phase 1 (future: pagination, database) |
| Concurrent file access | Data race if multiple instances | Document single-user limitation in README |
| Python version mismatch | App won't run | Use .python-version file, check in main.py startup |

## Follow-Ups & Future Phases

**Immediate Next Steps**:
1. Generate tasks.md with `/sp.tasks` command
2. Review and approve task breakdown
3. Execute implementation with `/sp.implement` command

**Future Phase Compatibility**:
- **Phase 2 (Web)**: Task model JSON serialization enables REST API
- **Phase 3 (AI)**: CLI commands become MCP tools for AI agent
- **Phase 4 (K8s)**: Containerize CLI for distributed deployment
- **Phase 5 (Cloud)**: Replace JSON with Neon PostgreSQL, add Kafka events

**Potential ADRs** (will suggest if needed):
- None anticipated for Phase 1 (straightforward CLI design)
- Phase 2 transition may need ADR for repository abstraction (file vs. database)

## Acceptance Criteria Mapping

This plan enables all spec acceptance criteria:

**User Story 1 (Add Tasks)**: Task model + Repository.add() + CLI add command
**User Story 2 (List Tasks)**: Repository.list_all() + CLI list command with formatting
**User Story 3 (Complete)**: Repository.complete() + CLI complete command
**User Story 4 (Update)**: Repository.update() + CLI update command
**User Story 5 (Delete)**: Repository.delete() + CLI delete command
**User Story 6 (Persistence)**: Repository._load()/_save() + exit command + SIGINT handler

All edge cases handled through validation in models.py and error handling in commands.py.

---

**Plan Status**: Ready for Phase 0 Research (documented above) and Phase 1 Design (data-model.md, contracts/ to be generated next).
