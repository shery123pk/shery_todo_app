# Feature Specification: In-Memory Python Console Todo App

**Feature Branch**: `001-cli-todo-app`
**Created**: 2025-12-26
**Status**: Draft
**Input**: User description: "Phase 1: In-Memory Python Console Todo App with CRUD operations"

## Problem Statement

Users need a simple, fast way to manage daily tasks from the command line without the overhead of web interfaces or databases. This application establishes the foundational domain model and CRUD operations that will persist semantically across all future phases of the Evolution of Todo project.

The app must enable quick task capture and management through an interactive console interface, with data surviving application restarts through optional JSON file persistence.

## User Scenarios & Testing

### User Story 1 - Add New Tasks (Priority: P1)

As a busy user, I want to quickly add tasks with titles and optional descriptions so that I can capture things I need to do without interrupting my workflow.

**Why this priority**: Task creation is the core value proposition and must work perfectly. Without the ability to add tasks, the application has no purpose.

**Independent Test**: Can be fully tested by launching the app, running the add command with various inputs, and verifying tasks appear in the list. Delivers immediate value by allowing basic task capture.

**Acceptance Scenarios**:

1. **Given** the app is running, **When** I execute `add "Buy groceries" --desc "Milk, eggs, bread"`, **Then** I see "Task 1 created: Buy groceries" and the task appears in the list with description
2. **Given** the app is running, **When** I execute `add "Call dentist"`, **Then** I see "Task 2 created: Call dentist" with no description
3. **Given** I have added 5 tasks, **When** I execute `add "Sixth task"`, **Then** it receives ID 6 and appears at the end of the list
4. **Given** the app is running, **When** I try to add a task with empty title `add ""`, **Then** I see error "Title is required."
5. **Given** the app is running, **When** I try to add a task with 250-character title, **Then** I see error "Title too long (max 200)."
6. **Given** the app is running, **When** I add a task with 1200-character description, **Then** I see error "Description too long (max 1000)."

---

### User Story 2 - View All Tasks (Priority: P1)

As a user, I want to see all my tasks in a clear, organized list so that I can review what needs to be done.

**Why this priority**: Viewing tasks is equally critical as adding them. Users must be able to see what they've captured.

**Independent Test**: Can be tested by adding several tasks, running the list command, and verifying all tasks display with correct information. Delivers value by providing task visibility.

**Acceptance Scenarios**:

1. **Given** I have added 3 tasks, **When** I execute `list`, **Then** I see all 3 tasks with their IDs, titles, descriptions, and completion status
2. **Given** I have no tasks, **When** I execute `list`, **Then** I see "No tasks found."
3. **Given** I have tasks with various completion states, **When** I execute `list`, **Then** completed tasks show with a visual indicator (e.g., [✓]) and incomplete show [ ]
4. **Given** I have 10 tasks, **When** I execute `list`, **Then** they display in order by ID from oldest to newest

---

### User Story 3 - Mark Tasks Complete (Priority: P2)

As a user, I want to mark tasks as complete so that I can track my progress and distinguish finished work from pending items.

**Why this priority**: Completion tracking is essential for task management but users can still capture and view tasks without it. This makes it slightly lower priority than add/list.

**Independent Test**: Can be tested by adding tasks, completing some, and verifying status changes persist in the list view. Delivers value by enabling progress tracking.

**Acceptance Scenarios**:

1. **Given** I have task ID 1 that is incomplete, **When** I execute `complete 1`, **Then** I see "Task 1 marked as complete" and it shows [✓] in list
2. **Given** I have task ID 2 that is already complete, **When** I execute `complete 2`, **Then** I see "Task 2 is already complete"
3. **Given** no task with ID 99 exists, **When** I execute `complete 99`, **Then** I see error "Task 99 not found."
4. **Given** I complete a task, **When** I restart the app and run `list`, **Then** the task still shows as complete

---

### User Story 4 - Update Existing Tasks (Priority: P3)

As a user, I want to edit task titles and descriptions so that I can correct mistakes or update information as circumstances change.

**Why this priority**: While useful, updating is less critical than core CRUD operations. Users can work around this by deleting and re-adding tasks if needed.

**Independent Test**: Can be tested by creating a task, updating its fields, and verifying changes persist. Delivers value by allowing task refinement.

**Acceptance Scenarios**:

1. **Given** task ID 1 exists with title "Old Title", **When** I execute `update 1 --title "New Title"`, **Then** I see "Task 1 updated" and list shows new title
2. **Given** task ID 1 exists, **When** I execute `update 1 --desc "Updated description"`, **Then** only the description changes, title remains same
3. **Given** task ID 1 exists, **When** I execute `update 1 --title "New" --desc "Also new"`, **Then** both fields update
4. **Given** no task with ID 99 exists, **When** I execute `update 99 --title "Test"`, **Then** I see error "Task 99 not found."
5. **Given** task ID 1 exists, **When** I try to update with empty title `update 1 --title ""`, **Then** I see error "Title is required."
6. **Given** task ID 1 exists, **When** I try to update with 250-character title, **Then** I see error "Title too long (max 200)."

---

### User Story 5 - Delete Tasks (Priority: P3)

As a user, I want to delete tasks I no longer need so that my list stays clean and relevant.

**Why this priority**: Deletion is helpful for list maintenance but not critical for basic task management. Users can simply ignore unwanted tasks if needed.

**Independent Test**: Can be tested by creating tasks, deleting some, and verifying they no longer appear in the list. Delivers value by enabling list cleanup.

**Acceptance Scenarios**:

1. **Given** task ID 1 exists, **When** I execute `delete 1`, **Then** I see "Task 1 deleted" and it no longer appears in list
2. **Given** no task with ID 99 exists, **When** I execute `delete 99`, **Then** I see error "Task 99 not found."
3. **Given** I have 5 tasks and delete task 3, **When** I run `list`, **Then** I see 4 tasks (IDs 1, 2, 4, 5)
4. **Given** I delete a task, **When** I restart the app and run `list`, **Then** the deleted task does not reappear

---

### User Story 6 - Exit and Data Persistence (Priority: P1)

As a user, I want my tasks to be saved automatically when I exit so that my work is preserved between sessions.

**Why this priority**: Data persistence is critical for a useful todo app. Without it, all work is lost on exit, making the app nearly worthless.

**Independent Test**: Can be tested by adding tasks, exiting the app, restarting, and verifying all data is intact. Delivers value by ensuring data durability.

**Acceptance Scenarios**:

1. **Given** I have added 5 tasks, **When** I execute `exit`, **Then** app saves to tasks.json and terminates gracefully
2. **Given** I have added tasks and saved, **When** I restart the app and run `list`, **Then** all tasks are restored with correct data
3. **Given** I press Ctrl+C during operation, **When** app receives signal, **Then** it saves data before exiting
4. **Given** tasks.json does not exist on first launch, **When** app starts, **Then** it begins with empty task list
5. **Given** tasks.json is corrupted, **When** app starts, **Then** it shows warning "Could not load tasks, starting fresh" and begins with empty list

---

### Edge Cases

- What happens when user provides no arguments to a command? → Display usage help for that command
- What happens when user enters invalid command? → Display "Unknown command. Type 'help' for available commands."
- What happens when task ID is not a number? → "Invalid task ID. Must be a number."
- What happens when multiple users modify tasks.json simultaneously? → Out of scope for Phase 1 (single-user assumption)
- What happens when tasks.json permissions prevent writing? → Display error "Cannot save tasks: permission denied" but continue running
- What happens when user tries to complete/update/delete using task title instead of ID? → "Task not found" (IDs are required)
- What happens when disk is full during save? → Display error "Cannot save tasks: disk full" and continue running with in-memory data

## Requirements

### Functional Requirements

- **FR-001**: System MUST accept task creation with title (1-200 characters, required) and description (0-1000 characters, optional)
- **FR-002**: System MUST assign unique sequential integer IDs starting from 1 for each new task
- **FR-003**: System MUST initialize all new tasks with completed status set to false
- **FR-004**: System MUST display all tasks with ID, title, description (if present), and completion status
- **FR-005**: System MUST allow marking tasks as complete by ID
- **FR-006**: System MUST allow updating task title and/or description by ID
- **FR-007**: System MUST allow deleting tasks by ID
- **FR-008**: System MUST persist tasks to JSON file (tasks.json) on exit or modification
- **FR-009**: System MUST load existing tasks from JSON file on startup if file exists
- **FR-010**: System MUST provide clear error messages for all validation failures (empty title, length violations, non-existent IDs)
- **FR-011**: System MUST run as interactive command-line interface accepting commands in a loop until exit
- **FR-012**: System MUST support `help` command showing all available commands and their usage
- **FR-013**: System MUST handle Ctrl+C signal gracefully by saving data and exiting
- **FR-014**: System MUST reject title longer than 200 characters with error message
- **FR-015**: System MUST reject description longer than 1000 characters with error message

### Key Entities

- **Task**: Represents a todo item with immutable ID, mutable title and description, and boolean completion status. Attributes:
  - `id`: Unique integer identifier (auto-assigned, immutable)
  - `title`: Text description of what needs to be done (required, 1-200 chars)
  - `description`: Optional additional details (0-1000 chars)
  - `completed`: Boolean flag indicating if task is done (default: false)

## Success Criteria

### Measurable Outcomes

- **SC-001**: Users can add a new task in under 5 seconds from command entry to confirmation
- **SC-002**: Users can view their complete task list in under 2 seconds
- **SC-003**: All task operations (add, list, update, complete, delete) complete without errors in 100% of valid input cases
- **SC-004**: Task data persists correctly across application restarts in 100% of cases when disk write succeeds
- **SC-005**: Users receive clear, actionable error messages for 100% of invalid inputs
- **SC-006**: 90% of users can successfully complete all CRUD operations on first attempt without consulting documentation
- **SC-007**: Application startup time is under 1 second when loading up to 100 tasks

## Assumptions

1. **Single User**: Only one user will interact with the app at a time (no concurrent access to tasks.json)
2. **Local Filesystem**: Application runs with read/write access to local filesystem for JSON persistence
3. **English Language**: All commands and messages are in English (internationalization is Phase 5 bonus)
4. **Terminal Environment**: Users have access to a standard terminal/console with UTF-8 support
5. **Python Availability**: Users have Python 3.13+ installed and configured
6. **Sequential IDs**: Task IDs increment sequentially and are never reused, even after deletion
7. **JSON Format**: Persistence format is human-readable JSON for future phase compatibility
8. **In-Memory First**: All operations work against in-memory data structure; file is purely for persistence between sessions
9. **No Undo**: Delete operations are permanent with no undo capability
10. **Command-Line Proficiency**: Users are comfortable with basic command-line interfaces

## Out of Scope for Phase 1

- Authentication or multi-user support
- Task priority, tags, categories, or due dates
- Database persistence (PostgreSQL/Neon)
- Web interface or REST API
- AI-powered natural language input
- Task search or filtering
- Task sorting or reordering
- Recurring tasks or reminders
- Task assignment to other users
- Undo/redo functionality
- Task export to other formats
- Cloud synchronization
- Mobile or desktop GUI
- Collaboration features
- Audit trail or change history
