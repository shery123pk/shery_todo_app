# Todo CLI - Phase 1

Command-line todo application with in-memory storage and JSON persistence.

## Installation

```bash
# From the cli directory
uv pip install -e .
```

## Usage

```bash
# Add a task
todo add "Buy groceries" -d "Milk and eggs"

# List tasks
todo list                # Show incomplete tasks
todo list --all          # Show all tasks
todo list --completed    # Show only completed tasks

# Complete a task
todo complete 1

# Update a task
todo update 1 --title "Buy groceries and supplies"
todo update 1 -d "New description"

# Delete a task
todo delete 1            # With confirmation
todo delete 1 -y         # Skip confirmation
```

## Development

```bash
# Run tests
uv run pytest

# Run with coverage
uv run pytest --cov=todo_cli

# Type checking
uv run pyright

# Linting
uv run ruff check .
```

## Architecture

- **Domain Layer** (`models.py`): Task dataclass with validation
- **Data Layer** (`repository.py`): InMemoryRepository with CRUD operations
- **Presentation Layer** (`commands.py`): Click CLI with 5 commands
- **Utilities** (`utils.py`): Formatting functions

## Test Coverage

- 96% code coverage
- 81 tests (15 model + 36 repository + 30 CLI integration)
- All tests passing

## Phase Information

**Phase:** 1 - CLI + In-Memory
**Status:** Complete ✓
**Version:** 0.1.0

See `../specs/001-cli-todo-app/` for complete specification.
