# Data Model: Phase 1 CLI Todo App

**Feature**: 001-cli-todo-app
**Date**: 2025-12-26
**Status**: Approved

## Overview

This document defines the Phase 1 immutable core domain model. All future phases MUST preserve these entities and their semantic meaning. Field additions are permitted in later phases, but the core schema (Task: id, title, description, completed) is frozen and must remain backward-compatible.

## Core Entities

### Task

**Description**: Represents a single todo item with unique identifier, descriptive text, optional details, and completion status.

**Attributes**:

| Field | Type | Constraints | Default | Immutable | Description |
|-------|------|-------------|---------|-----------|-------------|
| `id` | int | > 0, unique, sequential | auto-assigned | ✅ YES | Unique identifier, never changes after creation |
| `title` | str | 1-200 chars, required, trimmed | (none) | ❌ NO | Brief description of what needs to be done |
| `description` | str | 0-1000 chars, optional | "" (empty) | ❌ NO | Additional details, context, or notes |
| `completed` | bool | true/false only | false | ❌ NO | Whether task has been finished |

**Validation Rules**:

1. **Title Validation**:
   - MUST NOT be empty after trimming whitespace
   - MUST be at least 1 character after trimming
   - MUST NOT exceed 200 characters after trimming
   - Leading/trailing whitespace is automatically trimmed
   - Error message: "Title is required." (if empty) or "Title too long (max 200)." (if > 200)

2. **Description Validation**:
   - MAY be empty string (optional field)
   - MUST NOT exceed 1000 characters
   - No trimming applied (preserve user formatting)
   - Error message: "Description too long (max 1000)."

3. **ID Validation**:
   - MUST be positive integer (>= 1)
   - MUST be unique within task collection
   - Auto-assigned by repository (users cannot set)
   - Sequential incrementing (1, 2, 3, ...)
   - Never reused even after deletion

4. **Completed Validation**:
   - MUST be boolean type (not truthy/falsy values)
   - Only accepts `True` or `False` (Python booleans)
   - Default is `False` for new tasks

**JSON Representation**:

```json
{
  "id": 1,
  "title": "Buy groceries",
  "description": "Milk, eggs, bread, coffee",
  "completed": false
}
```

**Minimal Task** (only required fields):
```json
{
  "id": 2,
  "title": "Call dentist",
  "description": "",
  "completed": false
}
```

**Completed Task**:
```json
{
  "id": 3,
  "title": "Finish project report",
  "description": "Send to manager by EOD",
  "completed": true
}
```

### State Transitions

```
[New Task]
    ↓
┌─────────────────┐
│   INCOMPLETE    │ ← default state
│  completed=false │
└─────────────────┘
    │
    │ complete command
    ↓
┌─────────────────┐
│    COMPLETE     │
│  completed=true  │
└─────────────────┘
```

**Valid Transitions**:
- `INCOMPLETE → COMPLETE`: User runs `complete <id>` command
- `COMPLETE → COMPLETE`: Idempotent (no error, just message "already complete")

**Note**: Phase 1 does not support "uncomplete" or "reopen". Completed tasks stay completed.

## Relationships

**Phase 1**: No relationships. Tasks are independent entities.

**Future Phases** (forward compatibility):
- Phase 3: `parent_id` field enables subtasks (one-to-many parent-child)
- Phase 3: `assigned_to` field links to User entity (many-to-one task-user)
- Phase 2: `category` field groups tasks (many-to-one task-category)

These are out of scope for Phase 1 but the JSON schema must remain compatible (additive fields only).

## Data Persistence

### Storage Format: JSON

**File Location**: `tasks.json` in current working directory

**File Structure**:
```json
{
  "next_id": 4,
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
    },
    {
      "id": 3,
      "title": "Finish report",
      "description": "Send to manager",
      "completed": true
    }
  ]
}
```

**Schema Fields**:
- `next_id`: Integer tracking the next available task ID (auto-increment counter)
- `tasks`: Array of Task objects

**Loading Behavior** (startup):
1. Check if `tasks.json` exists in CWD
2. If not exists: Start with empty list, `next_id = 1`
3. If exists and valid JSON:
   - Parse tasks array
   - Restore `next_id` counter
   - Validate each task schema
4. If exists but corrupted JSON:
   - Display warning: "Could not load tasks, starting fresh"
   - Start with empty list, `next_id = 1`

**Saving Behavior** (after modifications):
1. Serialize tasks to JSON (indent=2 for readability)
2. Write to temporary file (`tasks.tmp`)
3. Atomic rename to `tasks.json` (prevents corruption)
4. On I/O error: Display warning but continue with in-memory state

**Atomic Write Pattern** (prevents corruption):
```python
temp_file = Path("tasks.tmp")
temp_file.write_text(json.dumps(data, indent=2))
temp_file.replace(Path("tasks.json"))  # Atomic on POSIX and Windows
```

## Invariants (Must Always Be True)

1. **ID Uniqueness**: No two tasks can have the same ID
2. **ID Immutability**: Once assigned, a task's ID never changes
3. **ID Sequence**: `next_id` is always greater than any existing task ID
4. **Title Non-Empty**: Every task has a non-empty title (after trimming)
5. **Type Strictness**: All fields match their declared types (no `completed: "yes"`)
6. **Length Bounds**: Title ≤ 200 chars, Description ≤ 1000 chars
7. **Completed Binary**: Only `True` or `False`, no intermediate states

**Violation Handling**:
- Violations detected during creation/update: Raise `ValueError` with clear message
- Violations detected during JSON load: Skip invalid task, log warning, continue loading others

## Type Definitions (Python)

```python
from dataclasses import dataclass
from typing import ClassVar

@dataclass
class Task:
    """Immutable core domain model for todo items."""

    id: int
    title: str
    description: str = ""
    completed: bool = False

    # Validation constants
    TITLE_MAX_LENGTH: ClassVar[int] = 200
    TITLE_MIN_LENGTH: ClassVar[int] = 1
    DESC_MAX_LENGTH: ClassVar[int] = 1000

    def __post_init__(self):
        """Validate task fields after initialization."""
        self.title = self.title.strip()  # Trim whitespace

        if len(self.title) < self.TITLE_MIN_LENGTH:
            raise ValueError("Title is required.")
        if len(self.title) > self.TITLE_MAX_LENGTH:
            raise ValueError(f"Title too long (max {self.TITLE_MAX_LENGTH}).")
        if len(self.description) > self.DESC_MAX_LENGTH:
            raise ValueError(f"Description too long (max {self.DESC_MAX_LENGTH}).")
        if not isinstance(self.completed, bool):
            raise ValueError("Completed must be a boolean.")

    def to_dict(self) -> dict:
        """Serialize task to JSON-compatible dictionary."""
        return {
            "id": self.id,
            "title": self.title,
            "description": self.description,
            "completed": self.completed,
        }

    @classmethod
    def from_dict(cls, data: dict) -> "Task":
        """Deserialize task from JSON dictionary."""
        return cls(
            id=data["id"],
            title=data["title"],
            description=data.get("description", ""),
            completed=data.get("completed", False),
        )
```

## Migration Strategy (Future Phases)

**Phase 1 → Phase 2 (Web + Database)**:
- Add fields: `created_at`, `updated_at`, `priority`, `tags`, `category`
- Strategy: Additive only, no removals
- Backward compatibility: Phase 1 JSON files load into Phase 2 (missing fields get defaults)

**JSON Schema Versioning**:
```json
{
  "schema_version": "1.0.0",
  "next_id": 4,
  "tasks": [...]
}
```
Future phases can check `schema_version` and apply migrations if needed.

## Validation Test Cases

**Valid Tasks**:
- ✅ `Task(1, "Buy milk")` → Valid minimal task
- ✅ `Task(2, "x" * 200)` → Valid at max title length
- ✅ `Task(3, "Task", "y" * 1000)` → Valid at max description length
- ✅ `Task(4, "  Trimmed  ", "", True)` → Valid with whitespace trimmed

**Invalid Tasks** (must raise ValueError):
- ❌ `Task(1, "")` → Empty title
- ❌ `Task(2, "   ")` → Whitespace-only title (trimmed to empty)
- ❌ `Task(3, "x" * 201)` → Title too long
- ❌ `Task(4, "Title", "y" * 1001)` → Description too long
- ❌ `Task(5, "Title", "", "yes")` → Completed not boolean

---

**Status**: Data model finalized. Ready for contract generation and implementation.
