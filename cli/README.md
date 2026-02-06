# TaskFlow CLI - Professional Todo App

Professional command-line todo application with ALL 10 features for hackathons.

## Features

### Basic Level (5 features)
- Add tasks with title, description, priority, tags, due dates
- View task list with color-coded priority
- Complete tasks (auto-creates next recurring task)
- Update task details
- Delete tasks with confirmation

### Intermediate Level (3 features)
- **Priorities:** Low, Medium, High with color coding
- **Tags:** Add multiple tags to tasks
- **Search/Filter:** Search by keyword, filter by priority/tag
- **Sort:** Sort by ID, priority, due date, or title

### Advanced Level (2 features)
- **Due Dates:** Full date or shortcuts (today, tomorrow, 2d, 1w)
- **Recurring Tasks:** Daily, Weekly, Monthly patterns
- **Statistics Dashboard:** Overview of all tasks

## Installation

```bash
cd cli
pip install -e .
```

## Two Ways to Use

### 1. Interactive Menu Mode (Recommended)
```bash
taskapp
```
Shows a menu - just press numbers:
```
╔══════════════════════════════════════════╗
║           TODO APP - MAIN MENU           ║
╠══════════════════════════════════════════╣
║  1. Add New Task                         ║
║  2. View All Tasks                       ║
║  3. Search/Filter Tasks                  ║
║  4. Complete a Task                      ║
║  5. Update a Task                        ║
║  6. Delete a Task                        ║
║  7. View Statistics                      ║
║  8. Overdue Tasks                        ║
║  0. Exit                                 ║
╚══════════════════════════════════════════╝

Enter your choice (0-8):
```

### 2. Quick Command Mode
```bash
# Add task with priority and tags
todo add "Team meeting" -p high -t work -t urgent

# Add task with due date
todo add "Weekly report" --due "2025-01-15 14:00"

# Add recurring task
todo add "Daily standup" --recurring --pattern daily

# List tasks (incomplete only by default)
todo list

# Filter by priority
todo list -p high

# Filter by tag
todo list -t work

# Search tasks
todo list -q meeting

# Show all tasks including completed
todo list --all

# Show only completed
todo list -c

# Show overdue tasks
todo list --overdue

# Sort by priority
todo list --sort priority

# Complete a task
todo complete 1

# Update task
todo update 1 -p low --add-tag personal

# Delete task
todo delete 1 -y

# View statistics
todo stats
```

## Command Options

### `todo add`
| Option | Description |
|--------|-------------|
| `-d, --description` | Task description |
| `-p, --priority` | low, medium, high (default: medium) |
| `-t, --tag` | Add tags (can use multiple times) |
| `--due` | Due date (today, tomorrow, 2d, 1w, or date) |
| `--recurring` | Make task recurring |
| `--pattern` | daily, weekly, monthly |

### `todo list`
| Option | Description |
|--------|-------------|
| `-q, --query` | Search keyword |
| `-p, --priority` | Filter by priority |
| `-t, --tag` | Filter by tags |
| `-a, --all` | Show all tasks |
| `-c, --completed` | Show only completed |
| `--overdue` | Show only overdue |
| `--sort` | Sort by: id, priority, due_date, title |
| `--reverse` | Reverse sort order |

## Examples

```bash
# Basic task
todo add "Buy groceries"

# High priority with tags
todo add "Team meeting" -p high -t work -t urgent

# Task with due date
todo add "Submit report" --due tomorrow -p high

# Recurring task
todo add "Daily exercise" --recurring --pattern daily

# Search and filter
todo list -q meeting
todo list -p high -t urgent
todo list --overdue
todo list --sort due_date
```

## Development

```bash
# Run tests
pytest

# Run with coverage
pytest --cov=todo_cli

# Type checking
pyright

# Linting
ruff check .
```

## Architecture

- **models.py**: Task dataclass with validation
- **repository.py**: InMemoryRepository with CRUD, search, filter, sort
- **commands.py**: Click CLI with all commands
- **interactive.py**: Interactive menu-driven interface

## Test Coverage

- 96% code coverage
- 81 tests passing

## Phase Information

**Phase:** 1 - CLI + In-Memory
**Status:** Complete
**Version:** 1.0.0
