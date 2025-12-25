---

description: "Task list for Phase 1 CLI Todo App implementation"
---

# Tasks: In-Memory Python Console Todo App

**Input**: Design documents from `specs/001-cli-todo-app/`
**Prerequisites**: plan.md (required), spec.md (required), data-model.md, contracts/cli-commands.md

**Tests**: Unit and integration tests are included as this is a test-first development approach per constitution Principle V (>80% coverage requirement).

**Organization**: Tasks are grouped by user story to enable independent implementation and testing of each story.

## Format: `[ID] [P?] [Story] Description`

- **[P]**: Can run in parallel (different files, no dependencies)
- **[Story]**: Which user story this task belongs to (e.g., US1, US2, US3)
- Include exact file paths in descriptions

## Path Conventions

- **Single project**: `src/`, `tests/` at repository root
- Paths shown below use single project structure per plan.md

## Phase 1: Setup (Shared Infrastructure)

**Purpose**: Project initialization and basic structure

- [ ] T001 Create project directory structure (src/todo_cli/, tests/unit/, tests/integration/)
- [ ] T002 Initialize pyproject.toml with UV configuration and dependencies (click>=8.1.0)
- [ ] T003 [P] Create .python-version file pinning Python 3.13
- [ ] T004 [P] Create .gitignore file (exclude __pycache__, .venv, tasks.json, *.pyc)
- [ ] T005 [P] Create src/todo_cli/__init__.py (empty module initializer)
- [ ] T006 [P] Configure ruff in pyproject.toml (max-complexity=10, line-length=100)
- [ ] T007 [P] Configure pyright in pyproject.toml (strict mode, typeCheckingMode=strict)
- [ ] T008 [P] Create tests/conftest.py with pytest fixtures for isolated tasks.json

---

## Phase 2: Foundational (Blocking Prerequisites)

**Purpose**: Core infrastructure that MUST be complete before ANY user story can be implemented

**⚠️ CRITICAL**: No user story work can begin until this phase is complete

- [ ] T009 Create Task dataclass in src/todo_cli/models.py with all fields (id, title, description, completed)
- [ ] T010 Add __post_init__ validation to Task model (title 1-200 chars, description 0-1000 chars, completed boolean)
- [ ] T011 Add to_dict() method to Task model for JSON serialization
- [ ] T012 Add from_dict() classmethod to Task model for JSON deserialization
- [ ] T013 Create InMemoryRepository class in src/todo_cli/repository.py with __init__ method (tasks dict, next_id counter, file_path)
- [ ] T014 Add _load() private method to Repository for JSON file loading with error handling
- [ ] T015 Add _save() private method to Repository for atomic JSON file writing (temp file + rename)
- [ ] T016 Create utility functions in src/todo_cli/utils.py for task formatting (format_task_row, format_status_icon)

**Checkpoint**: Foundation ready - user story implementation can now begin in parallel

---

## Phase 3: User Story 1 - Add New Tasks (Priority: P1) 🎯 MVP

**Goal**: Enable users to create tasks with titles and optional descriptions

**Independent Test**: Launch app, run add command with various inputs (valid/invalid titles/descriptions), verify tasks appear in list with correct IDs and data

### Tests for User Story 1 ⚠️

> **NOTE: Write these tests FIRST, ensure they FAIL before implementation**

- [ ] T017 [P] [US1] Unit test Task model validation in tests/unit/test_models.py (empty title, too-long title, too-long description, valid task)
- [ ] T018 [P] [US1] Unit test Task serialization (to_dict/from_dict) in tests/unit/test_models.py
- [ ] T019 [P] [US1] Unit test Repository.add() method in tests/unit/test_repository.py (ID assignment, task storage, validation errors)

### Implementation for User Story 1

- [ ] T020 [US1] Implement Repository.add(title, description) method in src/todo_cli/repository.py (create Task, assign next_id, store, increment counter, save, return task)
- [ ] T021 [US1] Create Click command group in src/todo_cli/commands.py (@click.group decorator)
- [ ] T022 [US1] Implement add command in src/todo_cli/commands.py (@click.command with title argument, --desc option)
- [ ] T023 [US1] Add error handling to add command for validation errors (catch ValueError, display red error message)
- [ ] T024 [US1] Add success message formatting to add command (green text: "Task {id} created: {title}")
- [ ] T025 [P] [US1] Integration test for add command in tests/integration/test_cli_commands.py (valid add, empty title, too-long title, too-long description)

**Checkpoint**: At this point, User Story 1 should be fully functional and testable independently

---

## Phase 4: User Story 2 - View All Tasks (Priority: P1)

**Goal**: Display all tasks in a formatted table with IDs, status, titles, descriptions

**Independent Test**: Add multiple tasks with various states, run list command, verify table formatting, completion indicators, empty state message

### Tests for User Story 2 ⚠️

- [ ] T026 [P] [US2] Unit test Repository.list_all() method in tests/unit/test_repository.py (empty list, multiple tasks, sorted by ID)
- [ ] T027 [P] [US2] Unit test utility formatting functions in tests/unit/test_utils.py (format_status_icon, format_task_row, description truncation)

### Implementation for User Story 2

- [ ] T028 [US2] Implement Repository.list_all() method in src/todo_cli/repository.py (return sorted list of tasks by ID)
- [ ] T029 [US2] Implement list command in src/todo_cli/commands.py (call list_all, format as table, handle empty state)
- [ ] T030 [US2] Add table formatting to list command (header row, separator, status icons [✓]/[ ], description truncation to 40 chars)
- [ ] T031 [US2] Add summary line to list command (total count, completed count, pending count)
- [ ] T032 [P] [US2] Integration test for list command in tests/integration/test_cli_commands.py (empty list, multiple tasks, formatting verification)

**Checkpoint**: At this point, User Stories 1 AND 2 should both work independently

---

## Phase 5: User Story 6 - Exit and Data Persistence (Priority: P1)

**Goal**: Save tasks to JSON file on exit or modifications, load tasks on startup

**Independent Test**: Add tasks, exit app, restart app, verify tasks restored; test corrupted JSON recovery

### Tests for User Story 6 ⚠️

- [ ] T033 [P] [US6] Unit test Repository._load() method in tests/unit/test_repository.py (file not found, valid JSON, corrupted JSON)
- [ ] T034 [P] [US6] Unit test Repository._save() method in tests/unit/test_repository.py (successful save, I/O error handling)
- [ ] T035 [P] [US6] Integration test for persistence in tests/integration/test_persistence.py (save on add, load on startup, corruption recovery)

### Implementation for User Story 6

- [ ] T036 [US6] Update Repository.add() to call _save() after adding task in src/todo_cli/repository.py
- [ ] T037 [US6] Implement exit command in src/todo_cli/commands.py (call _save, display "Tasks saved. Goodbye!", exit code 0)
- [ ] T038 [US6] Create main interactive loop in src/todo_cli/main.py (while loop reading input, invoking Click commands)
- [ ] T039 [US6] Add SIGINT handler (Ctrl+C) to main.py (catch signal, call save, exit gracefully)
- [ ] T040 [US6] Add unknown command handling to main loop (display error message, suggest help command)
- [ ] T041 [US6] Add welcome message to main loop startup (display instructions and available commands)
- [ ] T042 [P] [US6] Integration test for interactive loop in tests/integration/test_cli_commands.py (unknown command, Ctrl+C handling, exit command)

**Checkpoint**: All P1 user stories (Add, List, Persistence) should now be independently functional

---

## Phase 6: User Story 3 - Mark Tasks Complete (Priority: P2)

**Goal**: Mark tasks as complete by ID, update completion status

**Independent Test**: Add tasks, complete some by ID, verify status changes persist across restarts

### Tests for User Story 3 ⚠️

- [ ] T043 [P] [US3] Unit test Repository.complete() method in tests/unit/test_repository.py (mark incomplete task, already complete task, non-existent ID)

### Implementation for User Story 3

- [ ] T044 [US3] Implement Repository.complete(task_id) method in src/todo_cli/repository.py (get task, set completed=True, save, return task)
- [ ] T045 [US3] Implement complete command in src/todo_cli/commands.py (@click.command with id argument)
- [ ] T046 [US3] Add idempotent handling to complete command (check if already complete, display appropriate message)
- [ ] T047 [US3] Add error handling to complete command (task not found, invalid ID format)
- [ ] T048 [P] [US3] Integration test for complete command in tests/integration/test_cli_commands.py (complete task, already complete, non-existent ID)

**Checkpoint**: User Stories 1, 2, 3, AND 6 should all work independently

---

## Phase 7: User Story 4 - Update Existing Tasks (Priority: P3)

**Goal**: Modify task titles and/or descriptions by ID

**Independent Test**: Create task, update title only, update description only, update both, verify changes persist

### Tests for User Story 4 ⚠️

- [ ] T049 [P] [US4] Unit test Repository.update() method in tests/unit/test_repository.py (update title, update description, update both, validation errors, non-existent ID)

### Implementation for User Story 4

- [ ] T050 [US4] Implement Repository.update(task_id, title, description) method in src/todo_cli/repository.py (get task, validate new values, update fields, save, return task)
- [ ] T051 [US4] Implement update command in src/todo_cli/commands.py (@click.command with id argument, --title and --desc options)
- [ ] T052 [US4] Add partial update logic to update command (allow title-only, description-only, or both updates)
- [ ] T053 [US4] Add validation to update command (require at least one flag, validate new title/description)
- [ ] T054 [US4] Add error handling to update command (task not found, invalid ID, validation errors)
- [ ] T055 [P] [US4] Integration test for update command in tests/integration/test_cli_commands.py (update title, update description, update both, validation errors)

**Checkpoint**: User Stories 1, 2, 3, 4, AND 6 should all work independently

---

## Phase 8: User Story 5 - Delete Tasks (Priority: P3)

**Goal**: Remove tasks by ID permanently

**Independent Test**: Create tasks, delete some by ID, verify they no longer appear in list, verify deletion persists

### Tests for User Story 5 ⚠️

- [ ] T056 [P] [US5] Unit test Repository.delete() method in tests/unit/test_repository.py (delete existing task, non-existent ID, verify ID not reused)

### Implementation for User Story 5

- [ ] T057 [US5] Implement Repository.delete(task_id) method in src/todo_cli/repository.py (get task for confirmation, remove from dict, save)
- [ ] T058 [US5] Implement delete command in src/todo_cli/commands.py (@click.command with id argument)
- [ ] T059 [US5] Add confirmation message to delete command (display deleted task title)
- [ ] T060 [US5] Add error handling to delete command (task not found, invalid ID format)
- [ ] T061 [P] [US5] Integration test for delete command in tests/integration/test_cli_commands.py (delete task, non-existent ID, verify persistence)

**Checkpoint**: All user stories should now be independently functional

---

## Phase 9: Polish & Cross-Cutting Concerns

**Purpose**: Improvements that affect multiple user stories

- [ ] T062 [P] Implement help command in src/todo_cli/commands.py (display all available commands with descriptions)
- [ ] T063 [P] Add command-specific help to all commands (Click automatic help via docstrings)
- [ ] T064 [P] Create README.md with installation instructions (UV setup, venv creation, dependency installation)
- [ ] T065 [P] Add usage examples to README.md (interactive mode walkthrough, common workflows)
- [ ] T066 [P] Add troubleshooting section to README.md (common errors, solutions)
- [ ] T067 [P] Add docstrings to all public methods in models.py, repository.py, commands.py
- [ ] T068 [P] Run ruff linter and fix any code quality issues (src/ and tests/)
- [ ] T069 [P] Run pyright type checker and fix any type errors (enable strict mode)
- [ ] T070 Run pytest with coverage report and ensure >80% coverage (pytest --cov=src/todo_cli --cov-report=term-missing)
- [ ] T071 Verify all acceptance criteria from spec.md pass (run through all user story scenarios manually)

---

## Dependencies & Execution Order

### Phase Dependencies

- **Setup (Phase 1)**: No dependencies - can start immediately
- **Foundational (Phase 2)**: Depends on Setup completion - BLOCKS all user stories
- **User Stories (Phase 3-8)**: All depend on Foundational phase completion
  - User stories can then proceed in parallel (if staffed)
  - Or sequentially in priority order (P1 → P2 → P3)
- **Polish (Phase 9)**: Depends on all user stories being complete

### User Story Dependencies

- **User Story 1 (P1 - Add)**: Can start after Foundational (Phase 2) - No dependencies on other stories
- **User Story 2 (P1 - List)**: Can start after Foundational (Phase 2) - No dependencies on other stories
- **User Story 6 (P1 - Persistence)**: Can start after US1 (needs Repository.add to test auto-save)
- **User Story 3 (P2 - Complete)**: Can start after Foundational (Phase 2) - May need US1 for testing but independently testable
- **User Story 4 (P3 - Update)**: Can start after Foundational (Phase 2) - May need US1 for testing but independently testable
- **User Story 5 (P3 - Delete)**: Can start after Foundational (Phase 2) - May need US1 for testing but independently testable

### Within Each User Story

- Tests (if included) MUST be written and FAIL before implementation
- Repository methods before CLI commands (commands depend on repository)
- Core implementation before error handling
- Story complete before moving to next priority

### Parallel Opportunities

- All Setup tasks marked [P] can run in parallel (T003-T008)
- All Foundational tasks NOT marked [P] must run sequentially (T009-T016)
- Once Foundational phase completes, user stories 1, 2, 3, 4, 5 can start in parallel (if team capacity allows)
- All tests for a user story marked [P] can run in parallel
- All Polish tasks marked [P] can run in parallel (T062-T069)

---

## Parallel Example: User Story 1

```bash
# Launch all tests for User Story 1 together:
Task: "Unit test Task model validation in tests/unit/test_models.py"
Task: "Unit test Task serialization in tests/unit/test_models.py"
Task: "Unit test Repository.add() in tests/unit/test_repository.py"

# After tests written and failing, launch implementation:
# (These must be sequential as they have dependencies)
Task: "Implement Repository.add() method" (T020)
Task: "Create Click command group" (T021)
Task: "Implement add command" (T022)
...
```

---

## Implementation Strategy

### MVP First (User Stories 1, 2, 6 Only)

1. Complete Phase 1: Setup (T001-T008)
2. Complete Phase 2: Foundational (T009-T016) - CRITICAL, blocks all stories
3. Complete Phase 3: User Story 1 - Add Tasks (T017-T025)
4. Complete Phase 4: User Story 2 - List Tasks (T026-T032)
5. Complete Phase 5: User Story 6 - Persistence (T033-T042)
6. **STOP and VALIDATE**: Test all P1 stories independently
7. Deploy/demo if ready

### Incremental Delivery

1. Complete Setup + Foundational → Foundation ready (T001-T016)
2. Add User Story 1 (Add) → Test independently → Deploy/Demo (MVP!)
3. Add User Story 2 (List) → Test independently → Deploy/Demo
4. Add User Story 6 (Persistence) → Test independently → Deploy/Demo
5. Add User Story 3 (Complete) → Test independently → Deploy/Demo
6. Add User Story 4 (Update) → Test independently → Deploy/Demo
7. Add User Story 5 (Delete) → Test independently → Deploy/Demo
8. Each story adds value without breaking previous stories

### Parallel Team Strategy

With multiple developers:

1. Team completes Setup + Foundational together (T001-T016)
2. Once Foundational is done:
   - Developer A: User Story 1 (Add) - T017-T025
   - Developer B: User Story 2 (List) - T026-T032
   - Developer C: User Story 6 (Persistence) - T033-T042
3. Then:
   - Developer A: User Story 3 (Complete) - T043-T048
   - Developer B: User Story 4 (Update) - T049-T055
   - Developer C: User Story 5 (Delete) - T056-T061
4. Stories complete and integrate independently

---

## Notes

- [P] tasks = different files, no dependencies
- [Story] label maps task to specific user story for traceability (US1=Add, US2=List, US3=Complete, US4=Update, US5=Delete, US6=Persistence)
- Each user story should be independently completable and testable
- Verify tests fail before implementing (red-green-refactor cycle)
- Commit after each task or logical group
- Stop at any checkpoint to validate story independently
- Avoid: vague tasks, same file conflicts, cross-story dependencies that break independence

---

**Total Tasks**: 71
**Tasks per User Story**:
- Setup: 8 tasks
- Foundational: 8 tasks (blocking)
- US1 (Add - P1): 9 tasks
- US2 (List - P1): 7 tasks
- US6 (Persistence - P1): 10 tasks
- US3 (Complete - P2): 6 tasks
- US4 (Update - P3): 7 tasks
- US5 (Delete - P3): 5 tasks
- Polish: 11 tasks

**Parallel Opportunities**: 21 tasks marked [P] can run concurrently
**Critical Path**: Setup → Foundational → User Stories (in priority order) → Polish
**MVP Scope**: User Stories 1, 2, 6 (26 tasks total including Setup/Foundational)
