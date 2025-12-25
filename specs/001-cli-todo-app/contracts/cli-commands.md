# CLI Command Contracts: Phase 1 Todo App

**Feature**: 001-cli-todo-app
**Date**: 2025-12-26
**Status**: Approved

## Overview

This document specifies the command-line interface contract for the Phase 1 Todo App. All commands follow Click framework conventions with consistent error handling and output formatting.

## Command Invocation

**Interactive Mode** (Primary):
```bash
$ python -m todo_cli.main
Welcome to Todo CLI! Type 'help' for available commands.
> add "Buy groceries" --desc "Milk, eggs, bread"
Task 1 created: Buy groceries
> list
...
> exit
Goodbye!
```

**Shell Integration** (Phase 1 limitation):
- Phase 1 runs in interactive REPL only
- Direct shell commands (`python -m todo_cli.main add "Task"`) are Phase 2+ enhancement

## Command Reference

### 1. `add` - Create New Task

**Syntax**:
```
add <title> [--desc <description>]
```

**Parameters**:
| Parameter | Type | Required | Validation | Description |
|-----------|------|----------|------------|-------------|
| `<title>` | String | Yes | 1-200 chars after trim | Brief description of task |
| `--desc` | String | No | 0-1000 chars | Additional details (flag) |

**Behavior**:
1. Validate title (trim, check length)
2. Validate description (check length)
3. Create Task with auto-assigned ID
4. Save to repository
5. Auto-save to tasks.json
6. Display success message

**Success Output**:
```
Task <id> created: <title>
```

**Examples**:
```
> add "Buy groceries"
Task 1 created: Buy groceries

> add "Call dentist" --desc "Schedule annual checkup"
Task 2 created: Call dentist

> add "  Clean kitchen  "
Task 3 created: Clean kitchen  (note: whitespace trimmed)
```

**Error Cases**:
| Condition | Error Message | Exit Code |
|-----------|---------------|-----------|
| Title empty | `Error: Title is required.` | 1 |
| Title > 200 chars | `Error: Title too long (max 200).` | 1 |
| Description > 1000 chars | `Error: Description too long (max 1000).` | 1 |
| Missing title argument | `Usage: add <title> [--desc <description>]` | 2 |

---

### 2. `list` - Display All Tasks

**Syntax**:
```
list
```

**Parameters**: None

**Behavior**:
1. Retrieve all tasks from repository (sorted by ID)
2. Format as table with columns: ID, Status, Title, Description
3. Display count summary

**Success Output** (tasks exist):
```
ID  Status  Title              Description
──────────────────────────────────────────────────────────────
1   [ ]     Buy groceries      Milk, eggs, bread
2   [✓]     Call dentist       Schedule annual checkup
3   [ ]     Clean kitchen

3 tasks total (1 completed, 2 pending)
```

**Success Output** (no tasks):
```
No tasks found.
```

**Formatting Rules**:
- Status: `[✓]` for completed, `[ ]` for incomplete
- Title: Displayed in full (already <= 200 chars)
- Description: Truncated to 40 chars with `...` if longer (full text in view command)
- Sorted by ID ascending (oldest first)

**Examples**:
```
> list
ID  Status  Title              Description
──────────────────────────────────────────────────────────────
1   [ ]     Buy groceries      Milk, eggs, bread
2   [ ]     Call dentist

2 tasks total (0 completed, 2 pending)
```

**Error Cases**: None (empty list is valid state)

---

### 3. `complete` - Mark Task as Done

**Syntax**:
```
complete <id>
```

**Parameters**:
| Parameter | Type | Required | Validation | Description |
|-----------|------|----------|------------|-------------|
| `<id>` | Integer | Yes | Must be valid task ID | Task identifier to mark complete |

**Behavior**:
1. Validate ID is integer
2. Retrieve task from repository
3. Set `completed = True`
4. Auto-save to tasks.json
5. Display success message

**Success Output**:
```
Task <id> marked as complete: <title>
```

**Idempotent Behavior** (already complete):
```
Task <id> is already complete.
```

**Examples**:
```
> complete 1
Task 1 marked as complete: Buy groceries

> complete 1
Task 1 is already complete.
```

**Error Cases**:
| Condition | Error Message | Exit Code |
|-----------|---------------|-----------|
| Task ID not found | `Error: Task <id> not found.` | 1 |
| ID not a number | `Error: Invalid task ID. Must be a number.` | 2 |
| Missing ID argument | `Usage: complete <id>` | 2 |

---

### 4. `update` - Modify Existing Task

**Syntax**:
```
update <id> [--title <new_title>] [--desc <new_description>]
```

**Parameters**:
| Parameter | Type | Required | Validation | Description |
|-----------|------|----------|------------|-------------|
| `<id>` | Integer | Yes | Must be valid task ID | Task identifier to update |
| `--title` | String | No | 1-200 chars after trim | New title text |
| `--desc` | String | No | 0-1000 chars | New description text |

**Behavior**:
1. Validate ID is integer
2. Retrieve task from repository
3. Validate new title (if provided)
4. Validate new description (if provided)
5. Update specified fields only (partial update)
6. Auto-save to tasks.json
7. Display success message

**Success Output**:
```
Task <id> updated.
```

**Examples**:
```
> update 1 --title "Buy groceries and gas"
Task 1 updated.

> update 1 --desc "Milk, eggs, bread, coffee, fill up car"
Task 1 updated.

> update 1 --title "Shopping" --desc "Groceries and gas station"
Task 1 updated.
```

**Error Cases**:
| Condition | Error Message | Exit Code |
|-----------|---------------|-----------|
| Task ID not found | `Error: Task <id> not found.` | 1 |
| New title empty | `Error: Title is required.` | 1 |
| New title > 200 chars | `Error: Title too long (max 200).` | 1 |
| New desc > 1000 chars | `Error: Description too long (max 1000).` | 1 |
| No flags provided | `Error: Must provide --title or --desc.` | 2 |
| ID not a number | `Error: Invalid task ID. Must be a number.` | 2 |
| Missing ID argument | `Usage: update <id> [--title <text>] [--desc <text>]` | 2 |

---

### 5. `delete` - Remove Task

**Syntax**:
```
delete <id>
```

**Parameters**:
| Parameter | Type | Required | Validation | Description |
|-----------|------|----------|------------|-------------|
| `<id>` | Integer | Yes | Must be valid task ID | Task identifier to delete |

**Behavior**:
1. Validate ID is integer
2. Retrieve task from repository (to confirm exists)
3. Remove task from collection
4. Auto-save to tasks.json
5. Display success message with deleted task title

**Success Output**:
```
Task <id> deleted: <title>
```

**Examples**:
```
> delete 3
Task 3 deleted: Clean kitchen
```

**Error Cases**:
| Condition | Error Message | Exit Code |
|-----------|---------------|-----------|
| Task ID not found | `Error: Task <id> not found.` | 1 |
| ID not a number | `Error: Invalid task ID. Must be a number.` | 2 |
| Missing ID argument | `Usage: delete <id>` | 2 |

**Note**: Deleted IDs are never reused. Next task ID continues incrementing.

---

### 6. `help` - Show Command Help

**Syntax**:
```
help [command]
```

**Parameters**:
| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `[command]` | String | No | Specific command to get help for |

**Behavior**:
1. If no command specified: Show all available commands with brief descriptions
2. If command specified: Show detailed usage for that command

**Success Output** (no command):
```
Available commands:
  add       Create a new task
  list      Display all tasks
  complete  Mark a task as complete
  update    Modify an existing task
  delete    Remove a task
  help      Show this help message
  exit      Save and quit the application

Type 'help <command>' for detailed usage of a specific command.
```

**Success Output** (specific command):
```
> help add
Usage: add <title> [--desc <description>]

Create a new task with the given title and optional description.

Arguments:
  <title>       Brief description of the task (required, 1-200 chars)

Options:
  --desc TEXT   Additional details or notes (optional, max 1000 chars)

Examples:
  add "Buy groceries"
  add "Call dentist" --desc "Schedule annual checkup"
```

**Error Cases**: None (invalid command shows generic help)

---

### 7. `exit` - Save and Quit

**Syntax**:
```
exit
```

**Parameters**: None

**Behavior**:
1. Save current state to tasks.json
2. Display farewell message
3. Terminate application (exit code 0)

**Success Output**:
```
Tasks saved. Goodbye!
```

**Examples**:
```
> exit
Tasks saved. Goodbye!
$
```

**Error Cases**: None (save errors display warning but still exit)

**Equivalent**: Ctrl+C also triggers save and exit (SIGINT handler)

---

## Global Error Handling

**Unknown Command**:
```
> foo
Error: Unknown command 'foo'. Type 'help' for available commands.
```

**Keyboard Interrupt** (Ctrl+C):
```
^C
Tasks saved. Goodbye!
```

**File I/O Errors** (save failure):
```
Warning: Could not save tasks: [permission denied | disk full | etc.]
Continuing with in-memory data.
```

**File Load Errors** (startup):
```
Warning: Could not load tasks.json: [parse error | corrupt file | etc.]
Starting with empty task list.
```

## Output Formatting Standards

**Success Messages**: Normal text (white)
**Error Messages**: Red text via `click.echo(message, err=True, fg='red')`
**Warnings**: Yellow text via `click.echo(message, fg='yellow')`
**Highlights**: Green text for success confirmations via `click.echo(message, fg='green')`

**Table Formatting**:
- Fixed-width columns for alignment
- Header separator: `──────────────...`
- Status column: 5 chars (`[✓]` or `[ ]`)
- ID column: Right-aligned, variable width
- Title column: Left-aligned, 30 chars
- Description column: Left-aligned, 40 chars (truncated with `...`)

## Exit Codes

| Code | Meaning | Example |
|------|---------|---------|
| 0 | Success | Normal exit via `exit` command |
| 1 | Validation error | Empty title, task not found |
| 2 | Usage error | Missing required argument, invalid flag |

## Testing Contracts

**CliRunner Usage** (pytest integration):
```python
from click.testing import CliRunner
from todo_cli.main import cli

def test_add_command():
    runner = CliRunner()
    result = runner.invoke(cli, ['add', 'Test task'])
    assert result.exit_code == 0
    assert 'Task 1 created: Test task' in result.output
```

**Fixture Pattern** (isolated test data):
```python
@pytest.fixture
def temp_tasks_file(tmp_path):
    """Provide isolated tasks.json for each test."""
    tasks_file = tmp_path / "tasks.json"
    yield tasks_file
```

---

**Status**: CLI contracts finalized. Ready for implementation via `/sp.tasks` → `/sp.implement`.
