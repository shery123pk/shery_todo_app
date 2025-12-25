# Todo CLI

A command-line todo application demonstrating Spec-Driven Development (SDD).

## Installation

```bash
uv pip install -e .
```

## Usage

```bash
todo add "Task title" --description "Optional description"
todo list
todo complete <task-id>
todo update <task-id> --title "New title"
todo delete <task-id>
```

## Development

Run tests:
```bash
uv run pytest
```

Run with coverage:
```bash
uv run pytest --cov=todo_cli --cov-report=html
```

## License

MIT
