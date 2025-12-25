# Research: Technology Decisions for Phase 1 CLI Todo App

**Feature**: 001-cli-todo-app
**Date**: 2025-12-26
**Status**: Completed

## Overview

This document captures technology research and decisions for the Phase 1 CLI Todo App. All decisions align with the project constitution and support the immutable core domain model that future phases will build upon.

## Research Questions

### Q1: Which CLI framework provides the best balance of simplicity and features?

**Context**: Need interactive command parsing, help generation, argument validation without complexity.

**Options Evaluated**:

1. **argparse** (Python stdlib)
   - ✅ Pros: No dependencies, built-in, well-documented
   - ❌ Cons: Verbose boilerplate, poor composability, manual help formatting
   - Verdict: Too much code for simple commands

2. **Click** (external package)
   - ✅ Pros: Decorator-based, automatic help, type validation, testing support (CliRunner)
   - ✅ Pros: Industry standard (used by Flask, pip, AWS CLI)
   - ✅ Pros: Excellent error messages, composable commands
   - ❌ Cons: External dependency (acceptable for single lightweight package)
   - Verdict: **SELECTED** - Best developer experience, minimal code

3. **Typer** (external package)
   - ✅ Pros: Type-hints based, modern, built on Click
   - ❌ Cons: Heavier dependencies, less mature, overkill for simple CLI
   - Verdict: Over-engineered for Phase 1 needs

4. **Fire** (external package)
   - ✅ Pros: Automatic CLI from any Python object
   - ❌ Cons: "Magic" behavior, less explicit, harder to test
   - Verdict: Too implicit, harder to maintain

**Decision**: **Click 8.1+**

**Rationale**:
- Minimal boilerplate (decorators handle parsing/validation)
- Excellent test support (CliRunner for integration tests)
- Industry-proven (millions of downloads, mature ecosystem)
- Clear documentation and error messages
- Single lightweight dependency acceptable for significant productivity gain

### Q2: How should we implement JSON persistence to ensure reliability and future compatibility?

**Context**: Need human-readable format, stdlib support, graceful error handling, Phase 2+ compatibility.

**Options Evaluated**:

1. **pickle** (Python stdlib)
   - ✅ Pros: Fast serialization, native Python types
   - ❌ Cons: Binary format (not human-readable), security risks, Python-specific
   - Verdict: Not suitable - can't inspect/edit manually, incompatible with future web/API phases

2. **JSON** (Python stdlib)
   - ✅ Pros: Human-readable, language-agnostic, stdlib support, web-compatible
   - ✅ Pros: Easy debugging (can edit tasks.json manually)
   - ✅ Pros: Direct mapping to REST API responses (Phase 2)
   - ❌ Cons: Slightly slower than pickle (negligible for <1000 tasks)
   - Verdict: **SELECTED** - Perfect balance of readability and compatibility

3. **SQLite** (Python stdlib)
   - ✅ Pros: Real database, ACID guarantees, queryable
   - ❌ Cons: Over-engineered for in-memory app, binary file, not phase 1 scope
   - Verdict: Phase 2+ feature (will migrate to Neon PostgreSQL)

**Decision**: **JSON with atomic writes**

**Rationale**:
- Human-readable for debugging and manual editing
- Stdlib support (no dependencies)
- Web-compatible (same format as REST API Phase 2)
- Atomic write pattern (write temp → rename) prevents corruption
- Graceful error handling (corrupt file → warn and start fresh)

**Implementation Pattern**:
```python
def _save(self):
    try:
        temp_file = self.file_path.with_suffix('.tmp')
        temp_file.write_text(json.dumps(data, indent=2))
        temp_file.replace(self.file_path)  # Atomic on POSIX/Windows
    except IOError as e:
        click.echo(f"Warning: Could not save tasks: {e}", err=True)
```

### Q3: What testing strategy ensures >80% coverage and confidence in refactoring?

**Context**: Constitution requires >80% coverage, need unit + integration tests, future phases must not break Phase 1.

**Options Evaluated**:

1. **unittest** (Python stdlib)
   - ✅ Pros: No dependencies, built-in
   - ❌ Cons: Verbose (setUp/tearDown boilerplate), poor parametrization, weak fixtures
   - Verdict: Too much test code for small benefit

2. **pytest** (external package)
   - ✅ Pros: Concise (plain assert), powerful fixtures, parametrization, great plugins
   - ✅ Pros: Click integration (CliRunner fixture)
   - ✅ Pros: Coverage plugin (pytest-cov)
   - ✅ Pros: Constitution-standard testing framework
   - ❌ Cons: External dependency (acceptable for testing)
   - Verdict: **SELECTED** - Industry standard, best DX

**Decision**: **pytest 8.0+ with pytest-cov**

**Test Layers**:

1. **Unit Tests** (tests/unit/)
   - `test_models.py`: Task validation, to_dict/from_dict serialization
   - `test_repository.py`: CRUD operations, ID generation, in-memory state
   - Target: High coverage of business logic (90%+)

2. **Integration Tests** (tests/integration/)
   - `test_cli_commands.py`: End-to-end command execution with CliRunner
   - `test_persistence.py`: Save/load cycles, corruption recovery, file errors
   - Target: Cover all user stories acceptance scenarios

**Coverage Enforcement**:
```bash
pytest --cov=src/todo_cli --cov-fail-under=80 --cov-report=term-missing
```

### Q4: How to enforce code quality and Serena compliance (Principle III)?

**Context**: Constitution mandates LSP-based editing, type safety, code quality standards.

**Tooling Decisions**:

1. **Type Checking: Pyright**
   - ✅ LSP-compatible (Serena requirement)
   - ✅ Fast (incremental checking)
   - ✅ VS Code native integration
   - ✅ Strict mode available
   - Alternative: mypy (slower, less LSP-friendly)

2. **Linting/Formatting: Ruff**
   - ✅ Fast (Rust-based, 10-100x faster than black/flake8)
   - ✅ Replaces 10+ tools (black, isort, flake8, pylint, etc.)
   - ✅ Auto-fix capabilities
   - ✅ Complexity checking (mccabe)
   - Alternative: black+flake8+isort (slow, multiple configs)

3. **LSP Server: Pyright Language Server**
   - ✅ Symbol navigation, go-to-definition, find-references
   - ✅ Type-aware refactoring
   - ✅ Enables semantic code edits (Serena compliance)

**Configuration**:
```toml
# pyproject.toml
[tool.ruff]
line-length = 100
select = ["E", "F", "I", "N", "W", "C90"]
ignore = []

[tool.ruff.mccabe]
max-complexity = 10  # Constitution requirement

[tool.pyright]
strict = true
typeCheckingMode = "strict"
```

### Q5: What dependency management approach aligns with constitution and minimizes setup friction?

**Context**: Constitution mandates UV for fast dependency management, need reproducible environments.

**Decision**: **UV (constitution-mandated)**

**Rationale**:
- 10-100x faster than pip (Rust-based)
- Constitution-mandated for all Python projects
- Reproducible installs (lock file)
- Simple CLI (drop-in pip replacement)

**Setup Pattern**:
```bash
# Install UV
curl -LsSf https://astral.sh/uv/install.sh | sh

# Create venv and install deps
uv venv
uv pip install -e ".[dev]"
```

**pyproject.toml Structure**:
```toml
[project]
name = "todo-cli"
version = "0.1.0"
requires-python = ">=3.13"
dependencies = [
    "click>=8.1.0",
]

[project.optional-dependencies]
dev = [
    "pytest>=8.0.0",
    "pytest-cov>=4.1.0",
    "ruff>=0.2.0",
    "pyright>=1.1.0",
]
```

## Summary of Decisions

| Area | Decision | Rationale | Aligns With |
|------|----------|-----------|-------------|
| CLI Framework | Click 8.1+ | Minimal boilerplate, excellent testing, industry standard | Constitution: Python ecosystem best practices |
| Persistence | JSON (stdlib) | Human-readable, web-compatible, atomic writes | Constitution: Simplicity, future phase compatibility |
| Testing | pytest + pytest-cov | Powerful features, >80% coverage enforcement | Constitution Principle V: Test-First |
| Type Checking | Pyright | LSP-compatible, fast, strict mode | Constitution Principle III: Serena compliance |
| Linting | Ruff | Fast, comprehensive, auto-fix, complexity checks | Constitution: Code quality <10 complexity |
| Package Manager | UV | Fast, reproducible, constitution-mandated | Constitution: UV for Python dependency management |

## Open Questions (None)

All technology decisions are finalized. No further research required for Phase 1 implementation.

## References

- Click Documentation: https://click.palletsprojects.com/
- pytest Documentation: https://docs.pytest.org/
- Pyright GitHub: https://github.com/microsoft/pyright
- Ruff Documentation: https://docs.astral.sh/ruff/
- UV Documentation: https://docs.astral.sh/uv/

---

**Status**: Research complete. All decisions documented. Ready for Phase 1 design (data-model.md, contracts/).
