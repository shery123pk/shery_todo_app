# MCP Tools Design: Phase 1 CLI Task Management

**Feature**: `001-cli-todo-app`
**Created**: 2025-12-26
**Status**: Design
**Agent**: AI Engineer
**Version**: 1.0

## Overview

This document defines Model Context Protocol (MCP) tool schemas that expose the Phase 1 CLI task management functionality to AI agents. Each CLI command is mapped to an MCP tool with appropriate parameter validation, error handling, and response formatting.

### Design Principles

1. **Direct CLI Mapping**: Each MCP tool directly corresponds to a CLI command
2. **Parameter Fidelity**: MCP parameters match CLI arguments/options exactly
3. **Rich Responses**: Return structured data suitable for LLM consumption
4. **Error Transparency**: Expose validation errors with actionable messages
5. **Stateless Operations**: Each tool call is independent (repository handles state)

### Technology Context

- **Backend**: Python CLI with Click framework
- **Data Model**: Task (id, title, description, completed)
- **Storage**: JSON file (tasks.json) via InMemoryRepository
- **Validation**: Built into Task model and Repository methods

---

## MCP Tool Schemas

### 1. `todo_add` - Create New Task

**Purpose**: Add a new task to the todo list with automatic ID assignment

**CLI Command Mapping**: `todo add <title> [--description <desc>]`

#### Schema Definition

```json
{
  "name": "todo_add",
  "description": "Add a new task to your todo list with title and optional description",
  "inputSchema": {
    "type": "object",
    "properties": {
      "title": {
        "type": "string",
        "description": "Brief description of the task (required, 1-200 characters)",
        "minLength": 1,
        "maxLength": 200
      },
      "description": {
        "type": "string",
        "description": "Optional detailed description (0-1000 characters)",
        "maxLength": 1000,
        "default": ""
      }
    },
    "required": ["title"]
  }
}
```

#### Parameter Mapping

| MCP Parameter | CLI Argument/Option | Type | Required | Validation |
|---------------|---------------------|------|----------|------------|
| `title` | `<title>` (positional) | string | Yes | 1-200 chars, trimmed |
| `description` | `--description` / `-d` | string | No | 0-1000 chars |

#### Implementation Flow

```python
# Pseudo-code for MCP tool handler
def handle_todo_add(title: str, description: str = "") -> dict:
    """
    1. Validate parameters (already done by JSON schema)
    2. Call repository.add(title, description)
    3. Format response with task details
    4. Handle ValueError exceptions
    """
    try:
        repo = InMemoryRepository()
        task = repo.add(title=title, description=description)

        return {
            "success": True,
            "task": {
                "id": task.id,
                "title": task.title,
                "description": task.description,
                "completed": task.completed
            },
            "message": f"Task {task.id} created: {task.title}"
        }
    except ValueError as e:
        return {
            "success": False,
            "error": str(e),
            "error_type": "ValidationError"
        }
```

#### Success Response Format

```json
{
  "success": true,
  "task": {
    "id": 1,
    "title": "Buy groceries",
    "description": "Milk, eggs, bread",
    "completed": false
  },
  "message": "Task 1 created: Buy groceries"
}
```

#### Error Response Examples

**Empty Title**:
```json
{
  "success": false,
  "error": "Title is required.",
  "error_type": "ValidationError"
}
```

**Title Too Long**:
```json
{
  "success": false,
  "error": "Title too long (max 200).",
  "error_type": "ValidationError"
}
```

**Description Too Long**:
```json
{
  "success": false,
  "error": "Description too long (max 1000).",
  "error_type": "ValidationError"
}
```

---

### 2. `todo_list` - View All Tasks

**Purpose**: Retrieve all tasks with optional filtering by completion status

**CLI Command Mapping**: `todo list [--all] [--completed]`

#### Schema Definition

```json
{
  "name": "todo_list",
  "description": "List all tasks with optional filtering by completion status",
  "inputSchema": {
    "type": "object",
    "properties": {
      "filter": {
        "type": "string",
        "description": "Filter tasks by status: 'all', 'incomplete', or 'completed'",
        "enum": ["all", "incomplete", "completed"],
        "default": "incomplete"
      }
    }
  }
}
```

#### Parameter Mapping

| MCP Parameter | CLI Argument/Option | Type | Required | Validation |
|---------------|---------------------|------|----------|------------|
| `filter` | `--all` / `--completed` (flags) | enum | No | One of: all, incomplete, completed |

**Note**: CLI uses two boolean flags, MCP uses single enum for clarity

#### Implementation Flow

```python
def handle_todo_list(filter: str = "incomplete") -> dict:
    """
    1. Get all tasks from repository
    2. Apply filter based on parameter
    3. Format tasks for LLM consumption
    4. Include summary statistics
    """
    repo = InMemoryRepository()
    all_tasks = repo.list_all()

    # Apply filter
    if filter == "completed":
        tasks = [t for t in all_tasks if t.completed]
    elif filter == "incomplete":
        tasks = [t for t in all_tasks if not t.completed]
    else:  # "all"
        tasks = all_tasks

    return {
        "success": True,
        "tasks": [
            {
                "id": t.id,
                "title": t.title,
                "description": t.description,
                "completed": t.completed
            }
            for t in tasks
        ],
        "summary": {
            "total_count": len(tasks),
            "completed_count": sum(1 for t in tasks if t.completed),
            "incomplete_count": sum(1 for t in tasks if not t.completed),
            "filter_applied": filter
        }
    }
```

#### Success Response Format

**With Tasks**:
```json
{
  "success": true,
  "tasks": [
    {
      "id": 1,
      "title": "Buy groceries",
      "description": "Milk, eggs, bread",
      "completed": false
    },
    {
      "id": 2,
      "title": "Call dentist",
      "description": "",
      "completed": false
    }
  ],
  "summary": {
    "total_count": 2,
    "completed_count": 0,
    "incomplete_count": 2,
    "filter_applied": "incomplete"
  }
}
```

**Empty List**:
```json
{
  "success": true,
  "tasks": [],
  "summary": {
    "total_count": 0,
    "completed_count": 0,
    "incomplete_count": 0,
    "filter_applied": "all"
  }
}
```

---

### 3. `todo_complete` - Mark Task as Complete

**Purpose**: Mark a specific task as completed

**CLI Command Mapping**: `todo complete <task_id>`

#### Schema Definition

```json
{
  "name": "todo_complete",
  "description": "Mark a task as complete by its ID",
  "inputSchema": {
    "type": "object",
    "properties": {
      "task_id": {
        "type": "integer",
        "description": "The ID of the task to mark as complete",
        "minimum": 1
      }
    },
    "required": ["task_id"]
  }
}
```

#### Parameter Mapping

| MCP Parameter | CLI Argument/Option | Type | Required | Validation |
|---------------|---------------------|------|----------|------------|
| `task_id` | `<task_id>` (positional) | integer | Yes | Must be >= 1 |

#### Implementation Flow

```python
def handle_todo_complete(task_id: int) -> dict:
    """
    1. Validate task_id is positive integer (schema handles this)
    2. Call repository.complete(task_id)
    3. Return updated task details
    4. Handle KeyError if task not found
    """
    try:
        repo = InMemoryRepository()
        task = repo.complete(task_id)

        return {
            "success": True,
            "task": {
                "id": task.id,
                "title": task.title,
                "description": task.description,
                "completed": task.completed
            },
            "message": f"Task {task.id} marked as complete: {task.title}"
        }
    except KeyError as e:
        return {
            "success": False,
            "error": str(e),
            "error_type": "NotFoundError"
        }
```

#### Success Response Format

```json
{
  "success": true,
  "task": {
    "id": 1,
    "title": "Buy groceries",
    "description": "Milk, eggs, bread",
    "completed": true
  },
  "message": "Task 1 marked as complete: Buy groceries"
}
```

#### Error Response Examples

**Task Not Found**:
```json
{
  "success": false,
  "error": "Task 99 not found.",
  "error_type": "NotFoundError"
}
```

---

### 4. `todo_update` - Update Task Fields

**Purpose**: Update task title and/or description

**CLI Command Mapping**: `todo update <task_id> [--title <new_title>] [--description <new_desc>]`

#### Schema Definition

```json
{
  "name": "todo_update",
  "description": "Update a task's title and/or description by ID",
  "inputSchema": {
    "type": "object",
    "properties": {
      "task_id": {
        "type": "integer",
        "description": "The ID of the task to update",
        "minimum": 1
      },
      "title": {
        "type": "string",
        "description": "New title for the task (1-200 characters, optional)",
        "minLength": 1,
        "maxLength": 200
      },
      "description": {
        "type": "string",
        "description": "New description for the task (0-1000 characters, optional)",
        "maxLength": 1000
      }
    },
    "required": ["task_id"],
    "anyOf": [
      {"required": ["title"]},
      {"required": ["description"]}
    ]
  }
}
```

#### Parameter Mapping

| MCP Parameter | CLI Argument/Option | Type | Required | Validation |
|---------------|---------------------|------|----------|------------|
| `task_id` | `<task_id>` (positional) | integer | Yes | Must be >= 1 |
| `title` | `--title` / `-t` | string | No* | 1-200 chars if provided |
| `description` | `--description` / `-d` | string | No* | 0-1000 chars if provided |

**Note**: At least one of `title` or `description` must be provided

#### Implementation Flow

```python
def handle_todo_update(
    task_id: int,
    title: str | None = None,
    description: str | None = None
) -> dict:
    """
    1. Validate at least one field provided (schema handles this)
    2. Call repository.update(task_id, title, description)
    3. Return updated task
    4. Handle KeyError (not found) and ValueError (validation)
    """
    try:
        repo = InMemoryRepository()
        task = repo.update(task_id, title=title, description=description)

        return {
            "success": True,
            "task": {
                "id": task.id,
                "title": task.title,
                "description": task.description,
                "completed": task.completed
            },
            "message": f"Task {task.id} updated successfully",
            "updated_fields": {
                "title": title is not None,
                "description": description is not None
            }
        }
    except KeyError as e:
        return {
            "success": False,
            "error": str(e),
            "error_type": "NotFoundError"
        }
    except ValueError as e:
        return {
            "success": False,
            "error": str(e),
            "error_type": "ValidationError"
        }
```

#### Success Response Format

**Update Title Only**:
```json
{
  "success": true,
  "task": {
    "id": 1,
    "title": "Buy groceries and supplies",
    "description": "Milk, eggs, bread",
    "completed": false
  },
  "message": "Task 1 updated successfully",
  "updated_fields": {
    "title": true,
    "description": false
  }
}
```

**Update Both Fields**:
```json
{
  "success": true,
  "task": {
    "id": 2,
    "title": "Call dentist",
    "description": "Annual checkup appointment",
    "completed": false
  },
  "message": "Task 2 updated successfully",
  "updated_fields": {
    "title": true,
    "description": true
  }
}
```

#### Error Response Examples

**Task Not Found**:
```json
{
  "success": false,
  "error": "Task 99 not found.",
  "error_type": "NotFoundError"
}
```

**Empty Title**:
```json
{
  "success": false,
  "error": "Title is required.",
  "error_type": "ValidationError"
}
```

**Title Too Long**:
```json
{
  "success": false,
  "error": "Title too long (max 200).",
  "error_type": "ValidationError"
}
```

---

### 5. `todo_delete` - Delete Task

**Purpose**: Permanently remove a task from the list

**CLI Command Mapping**: `todo delete <task_id> [--yes]`

#### Schema Definition

```json
{
  "name": "todo_delete",
  "description": "Permanently delete a task by its ID (cannot be undone)",
  "inputSchema": {
    "type": "object",
    "properties": {
      "task_id": {
        "type": "integer",
        "description": "The ID of the task to delete",
        "minimum": 1
      },
      "confirm": {
        "type": "boolean",
        "description": "Confirmation flag to proceed with deletion (recommended: true for AI agents)",
        "default": true
      }
    },
    "required": ["task_id"]
  }
}
```

#### Parameter Mapping

| MCP Parameter | CLI Argument/Option | Type | Required | Validation |
|---------------|---------------------|------|----------|------------|
| `task_id` | `<task_id>` (positional) | integer | Yes | Must be >= 1 |
| `confirm` | `--yes` / `-y` | boolean | No | Default: true (AI agents skip prompt) |

**Note**: CLI prompts for confirmation unless `--yes` flag is used. MCP defaults to `confirm=true` since AI agents should explicitly decide to delete.

#### Implementation Flow

```python
def handle_todo_delete(task_id: int, confirm: bool = True) -> dict:
    """
    1. Validate task_id (schema handles this)
    2. Get task details before deletion (for response message)
    3. Call repository.delete(task_id)
    4. Return confirmation with deleted task info
    5. Handle KeyError if task not found

    Note: 'confirm' parameter is informational for AI agents;
    MCP implementation assumes AI made deliberate decision to delete
    """
    try:
        repo = InMemoryRepository()

        # Get task before deleting (for confirmation message)
        task = repo.get(task_id)
        task_title = task.title

        # Delete the task
        repo.delete(task_id)

        return {
            "success": True,
            "deleted_task": {
                "id": task_id,
                "title": task_title
            },
            "message": f"Task {task_id} deleted successfully: {task_title}",
            "warning": "This action cannot be undone"
        }
    except KeyError as e:
        return {
            "success": False,
            "error": str(e),
            "error_type": "NotFoundError"
        }
```

#### Success Response Format

```json
{
  "success": true,
  "deleted_task": {
    "id": 1,
    "title": "Buy groceries"
  },
  "message": "Task 1 deleted successfully: Buy groceries",
  "warning": "This action cannot be undone"
}
```

#### Error Response Examples

**Task Not Found**:
```json
{
  "success": false,
  "error": "Task 99 not found.",
  "error_type": "NotFoundError"
}
```

---

## Error Handling Patterns

### Error Type Classification

All MCP tool responses include standardized error handling:

| Error Type | Python Exception | HTTP Equivalent | MCP Response Field |
|------------|-----------------|-----------------|-------------------|
| `ValidationError` | `ValueError` | 400 Bad Request | `error_type: "ValidationError"` |
| `NotFoundError` | `KeyError` | 404 Not Found | `error_type: "NotFoundError"` |
| `IOError` | `OSError` | 500 Internal Server Error | `error_type: "IOError"` |

### Error Response Template

```json
{
  "success": false,
  "error": "<Human-readable error message>",
  "error_type": "<ErrorTypeClassification>",
  "context": {
    "parameter": "<which parameter caused error>",
    "value": "<invalid value if applicable>"
  }
}
```

### Example Error Handling Implementation

```python
def format_error_response(exception: Exception, context: dict = None) -> dict:
    """
    Standardize error responses across all MCP tools

    Args:
        exception: The caught exception
        context: Optional dict with parameter/value info

    Returns:
        Standardized error response dict
    """
    error_type_map = {
        ValueError: "ValidationError",
        KeyError: "NotFoundError",
        OSError: "IOError"
    }

    error_type = error_type_map.get(type(exception), "UnknownError")

    response = {
        "success": False,
        "error": str(exception),
        "error_type": error_type
    }

    if context:
        response["context"] = context

    return response
```

---

## Repository State Management

### State Handling Strategy

MCP tools are **stateless** - each tool call creates a fresh `InMemoryRepository` instance that:
1. Loads current state from `tasks.json` on initialization
2. Performs the requested operation
3. Auto-saves to `tasks.json` on modification
4. Returns result

This matches the CLI behavior and ensures consistency.

### Repository Lifecycle per MCP Call

```python
# Example lifecycle for todo_add tool
def handle_todo_add(title: str, description: str = "") -> dict:
    # 1. Initialize repository (loads tasks.json)
    repo = InMemoryRepository()

    # 2. Perform operation
    task = repo.add(title, description)  # auto-saves to tasks.json

    # 3. Return result
    return format_success_response(task)

    # 4. Repository goes out of scope (no cleanup needed)
```

### Concurrency Considerations

**Current Limitation**: JSON file-based storage is not safe for concurrent access
- **Phase 1 Scope**: Single-user, single-process assumption documented
- **MCP Impact**: AI agent calls are sequential (Click ensures this)
- **Future Phase**: Replace with database (PostgreSQL) for true concurrency

**Workaround for MCP**:
- Document that tools should not be called concurrently
- Each tool call is atomic (read → modify → write)
- File locking can be added if needed (not in Phase 1 scope)

---

## Response Format Standards

### Success Response Structure

All successful MCP tool calls return:

```json
{
  "success": true,
  "task": { /* task object if single task */ },
  "tasks": [ /* array if multiple tasks */ ],
  "message": "Human-readable success message",
  "summary": { /* optional metadata */ }
}
```

### Task Object Format

Consistent across all tools:

```json
{
  "id": 1,
  "title": "Task title",
  "description": "Optional description",
  "completed": false
}
```

**Field Guarantees**:
- `id`: Always present, positive integer
- `title`: Always present, non-empty string (1-200 chars)
- `description`: Always present, may be empty string (0-1000 chars)
- `completed`: Always present, boolean

### Response Size Considerations

**List Tool Optimization**:
- For large task lists (>100 tasks), consider pagination in future phases
- Phase 1: Return all tasks (acceptable for up to 1000 tasks per spec)
- LLM consumption: Structured JSON is efficient for Claude models

---

## Integration Guide for Backend Engineer

### Step 1: Create MCP Server Module

**File**: `src/todo_cli/mcp_server.py`

```python
"""MCP server implementation for todo CLI tools."""

from mcp.server import Server
from mcp.types import Tool

from .repository import InMemoryRepository

# Initialize MCP server
server = Server("todo-cli")

# Register tool: todo_add
@server.tool()
async def todo_add(title: str, description: str = "") -> dict:
    """Add a new task (see schema above for details)"""
    # Implementation from handle_todo_add above
    pass

# Register tool: todo_list
@server.tool()
async def todo_list(filter: str = "incomplete") -> dict:
    """List tasks (see schema above for details)"""
    # Implementation from handle_todo_list above
    pass

# Register tool: todo_complete
@server.tool()
async def todo_complete(task_id: int) -> dict:
    """Mark task complete (see schema above for details)"""
    # Implementation from handle_todo_complete above
    pass

# Register tool: todo_update
@server.tool()
async def todo_update(
    task_id: int,
    title: str | None = None,
    description: str | None = None
) -> dict:
    """Update task fields (see schema above for details)"""
    # Implementation from handle_todo_update above
    pass

# Register tool: todo_delete
@server.tool()
async def todo_delete(task_id: int, confirm: bool = True) -> dict:
    """Delete task (see schema above for details)"""
    # Implementation from handle_todo_delete above
    pass
```

### Step 2: Add MCP Server Entry Point

**File**: `src/todo_cli/mcp_main.py`

```python
"""Entry point for MCP server."""

import asyncio
from .mcp_server import server

async def main():
    """Run MCP server."""
    await server.run()

if __name__ == "__main__":
    asyncio.run(main())
```

### Step 3: Update Dependencies

**Add to `pyproject.toml`**:
```toml
[project.optional-dependencies]
mcp = [
    "mcp>=1.0.0",  # Model Context Protocol SDK
]
```

### Step 4: Configure MCP Client

**Claude Code Configuration** (`.claude/config.json`):
```json
{
  "mcpServers": {
    "todo-cli": {
      "command": "python",
      "args": ["-m", "todo_cli.mcp_main"],
      "env": {}
    }
  }
}
```

---

## Testing Strategy for MCP Tools

### Unit Tests

**File**: `tests/unit/test_mcp_tools.py`

```python
"""Unit tests for MCP tool handlers."""

import pytest
from todo_cli.mcp_server import (
    todo_add, todo_list, todo_complete,
    todo_update, todo_delete
)

@pytest.mark.asyncio
async def test_todo_add_success():
    """Test successful task creation via MCP tool."""
    result = await todo_add(title="Test task", description="Test desc")

    assert result["success"] is True
    assert result["task"]["title"] == "Test task"
    assert result["task"]["description"] == "Test desc"
    assert result["task"]["completed"] is False

@pytest.mark.asyncio
async def test_todo_add_validation_error():
    """Test MCP tool handles validation errors."""
    result = await todo_add(title="")  # Empty title

    assert result["success"] is False
    assert result["error_type"] == "ValidationError"
    assert "required" in result["error"].lower()

# ... additional tests for each tool and error case
```

### Integration Tests

**File**: `tests/integration/test_mcp_integration.py`

```python
"""Integration tests for MCP server."""

import pytest
from mcp.client import Client

@pytest.mark.asyncio
async def test_mcp_server_lifecycle():
    """Test full MCP server request/response cycle."""
    async with Client("todo-cli") as client:
        # Test add
        add_result = await client.call_tool("todo_add", {
            "title": "Integration test task"
        })
        assert add_result["success"] is True
        task_id = add_result["task"]["id"]

        # Test list
        list_result = await client.call_tool("todo_list", {})
        assert len(list_result["tasks"]) >= 1

        # Test complete
        complete_result = await client.call_tool("todo_complete", {
            "task_id": task_id
        })
        assert complete_result["task"]["completed"] is True

        # Test delete
        delete_result = await client.call_tool("todo_delete", {
            "task_id": task_id
        })
        assert delete_result["success"] is True
```

### Coverage Requirements

- **Unit Tests**: 100% coverage of all MCP tool handlers
- **Integration Tests**: Cover all success and error paths
- **Edge Cases**: Empty lists, large datasets, concurrent calls

---

## Performance Considerations

### Expected Latency

| Tool | Operation | Expected Latency | Notes |
|------|-----------|------------------|-------|
| `todo_add` | Create task | <50ms | Includes JSON write |
| `todo_list` | Read all tasks | <100ms | For up to 1000 tasks |
| `todo_complete` | Update status | <50ms | Includes JSON write |
| `todo_update` | Update fields | <50ms | Includes JSON write |
| `todo_delete` | Delete task | <50ms | Includes JSON write |

### Optimization Notes

1. **JSON File I/O**: Atomic writes ensure data integrity but add ~20ms overhead
2. **In-Memory Operations**: All CRUD operations are O(1) dict lookups
3. **List Sorting**: O(n log n) but negligible for n < 1000
4. **Future Optimization**: Replace JSON with database in Phase 2+

---

## Security Considerations

### Input Validation

All MCP tools enforce strict input validation:

1. **Parameter Types**: JSON schema enforces type checking (string, integer, boolean)
2. **Length Limits**: Title (1-200 chars), Description (0-1000 chars)
3. **ID Validation**: Must be positive integers (minimum: 1)
4. **Enum Values**: Filter parameter limited to predefined set

### Data Sanitization

- **Title/Description**: Trimmed of leading/trailing whitespace
- **No HTML/Script Injection**: Plain text storage only
- **No SQL Injection**: Not applicable (JSON file storage)

### File System Security

- **JSON File Access**: Read/write operations use Python pathlib (safe)
- **No Path Traversal**: File path is fixed (`tasks.json` in current directory)
- **Atomic Writes**: Temp file + rename prevents corruption

### Future Security Enhancements (Phase 2+)

- Add authentication/authorization for multi-user support
- Implement rate limiting for MCP tool calls
- Add audit logging for all operations
- Encrypt sensitive task data at rest

---

## Migration Path to Future Phases

### Phase 2: Web API Integration

MCP tools will map to FastAPI REST endpoints:

| MCP Tool | REST Endpoint | HTTP Method |
|----------|---------------|-------------|
| `todo_add` | `POST /api/tasks` | POST |
| `todo_list` | `GET /api/tasks?filter={filter}` | GET |
| `todo_complete` | `PATCH /api/tasks/{id}/complete` | PATCH |
| `todo_update` | `PATCH /api/tasks/{id}` | PATCH |
| `todo_delete` | `DELETE /api/tasks/{id}` | DELETE |

### Phase 3: Enhanced AI Capabilities

MCP tools will add:
- Natural language intent parsing (e.g., "add task buy milk tomorrow")
- Batch operations (e.g., complete multiple tasks)
- Smart suggestions (e.g., recommend task prioritization)

### Phase 4: Database Migration

Replace `InMemoryRepository` with database-backed repository:
- PostgreSQL/Neon for persistent storage
- Maintain same MCP tool interfaces (contract preservation)
- Add transaction support for data integrity

---

## Acceptance Criteria

This MCP tools design satisfies the following criteria:

- [ ] All 5 CLI commands mapped to MCP tools
- [ ] Parameter validation matches CLI requirements (1-200 char title, 0-1000 char description)
- [ ] Error handling provides clear, actionable messages
- [ ] Response formats are LLM-friendly (structured JSON)
- [ ] Tool schemas follow MCP specification standards
- [ ] Integration guide provided for Backend Engineer agent
- [ ] Testing strategy covers unit and integration tests
- [ ] Performance expectations documented (<100ms for all operations)
- [ ] Security considerations addressed (input validation, file safety)
- [ ] Future phase migration path defined

---

## Next Steps

1. **Review**: AI Engineer agent reviews this design with Architect
2. **Implementation**: Backend Engineer agent implements MCP server module
3. **Testing**: QA & Testing agent creates comprehensive test suite
4. **Documentation**: Update README.md with MCP usage instructions
5. **Validation**: Test MCP tools with Claude Code client

---

**Document Status**: Ready for Review
**Approver**: Architect (Human)
**Implementation Agent**: Backend Engineer
**Testing Agent**: QA & Testing
