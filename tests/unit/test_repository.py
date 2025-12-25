"""Unit tests for InMemoryRepository data access layer."""

import json
from pathlib import Path

import pytest

from todo_cli.models import Task
from todo_cli.repository import InMemoryRepository


class TestRepositoryInitialization:
    """Test repository initialization and file loading."""

    def test_init_with_nonexistent_file(self, temp_tasks_file: Path) -> None:
        """Test initializing repository when file doesn't exist."""
        repo = InMemoryRepository(str(temp_tasks_file))
        assert len(repo.tasks) == 0
        assert repo.next_id == 1
        assert repo.file_path == temp_tasks_file

    def test_init_loads_existing_tasks(
        self, temp_tasks_file: Path, sample_tasks_data: dict
    ) -> None:
        """Test loading tasks from existing JSON file."""
        temp_tasks_file.write_text(json.dumps(sample_tasks_data))
        repo = InMemoryRepository(str(temp_tasks_file))

        assert len(repo.tasks) == 3
        assert repo.next_id == 4
        assert repo.tasks[1].title == "Buy groceries"
        assert repo.tasks[3].completed is True

    def test_init_handles_corrupted_json(self, corrupted_json_file: Path) -> None:
        """Test graceful handling of corrupted JSON file."""
        repo = InMemoryRepository(str(corrupted_json_file))
        # Should start with empty state, not crash
        assert len(repo.tasks) == 0
        assert repo.next_id == 1

    def test_init_skips_invalid_tasks(self, tmp_path: Path) -> None:
        """Test that invalid tasks are skipped during load."""
        bad_data = {
            "next_id": 3,
            "tasks": [
                {"id": 1, "title": "Valid task", "completed": False},
                {"id": 2, "title": "", "completed": False},  # Invalid: empty title
            ],
        }
        file_path = tmp_path / "bad_tasks.json"
        file_path.write_text(json.dumps(bad_data))

        repo = InMemoryRepository(str(file_path))
        # Should load only the valid task
        assert len(repo.tasks) == 1
        assert 1 in repo.tasks
        assert 2 not in repo.tasks


class TestRepositoryAdd:
    """Test adding tasks to repository."""

    def test_add_task_with_title_only(self, temp_tasks_file: Path) -> None:
        """Test adding task with only title."""
        repo = InMemoryRepository(str(temp_tasks_file))
        task = repo.add(title="Buy milk")

        assert task.id == 1
        assert task.title == "Buy milk"
        assert task.description == ""
        assert task.completed is False
        assert repo.next_id == 2

    def test_add_task_with_description(self, temp_tasks_file: Path) -> None:
        """Test adding task with title and description."""
        repo = InMemoryRepository(str(temp_tasks_file))
        task = repo.add(title="Buy groceries", description="Milk and eggs")

        assert task.id == 1
        assert task.title == "Buy groceries"
        assert task.description == "Milk and eggs"
        assert task.completed is False

    def test_add_multiple_tasks_increments_id(self, temp_tasks_file: Path) -> None:
        """Test that adding multiple tasks increments IDs correctly."""
        repo = InMemoryRepository(str(temp_tasks_file))

        task1 = repo.add("First task")
        task2 = repo.add("Second task")
        task3 = repo.add("Third task")

        assert task1.id == 1
        assert task2.id == 2
        assert task3.id == 3
        assert repo.next_id == 4

    def test_add_persists_to_file(self, temp_tasks_file: Path) -> None:
        """Test that add() saves to JSON file."""
        repo = InMemoryRepository(str(temp_tasks_file))
        repo.add("Test task")

        # Verify file was created and contains data
        assert temp_tasks_file.exists()
        data = json.loads(temp_tasks_file.read_text())
        assert data["next_id"] == 2
        assert len(data["tasks"]) == 1
        assert data["tasks"][0]["title"] == "Test task"

    def test_add_with_empty_title_raises_error(self, temp_tasks_file: Path) -> None:
        """Test that empty title raises ValueError."""
        repo = InMemoryRepository(str(temp_tasks_file))
        with pytest.raises(ValueError, match="Title is required"):
            repo.add(title="")

    def test_add_with_whitespace_title_raises_error(
        self, temp_tasks_file: Path
    ) -> None:
        """Test that whitespace-only title raises ValueError."""
        repo = InMemoryRepository(str(temp_tasks_file))
        with pytest.raises(ValueError, match="Title is required"):
            repo.add(title="   ")

    def test_add_with_too_long_title_raises_error(self, temp_tasks_file: Path) -> None:
        """Test that title over 200 chars raises ValueError."""
        repo = InMemoryRepository(str(temp_tasks_file))
        long_title = "x" * 201
        with pytest.raises(ValueError, match="Title too long"):
            repo.add(title=long_title)


class TestRepositoryGet:
    """Test retrieving tasks from repository."""

    def test_get_existing_task(
        self, temp_tasks_file: Path, sample_tasks_data: dict
    ) -> None:
        """Test retrieving task by ID."""
        temp_tasks_file.write_text(json.dumps(sample_tasks_data))
        repo = InMemoryRepository(str(temp_tasks_file))

        task = repo.get(2)
        assert task.id == 2
        assert task.title == "Call dentist"

    def test_get_nonexistent_task_raises_error(self, temp_tasks_file: Path) -> None:
        """Test that getting nonexistent task raises KeyError."""
        repo = InMemoryRepository(str(temp_tasks_file))
        with pytest.raises(KeyError, match="Task 999 not found"):
            repo.get(999)

    def test_get_after_add(self, temp_tasks_file: Path) -> None:
        """Test retrieving task immediately after adding."""
        repo = InMemoryRepository(str(temp_tasks_file))
        added_task = repo.add("New task")
        retrieved_task = repo.get(added_task.id)

        assert retrieved_task.id == added_task.id
        assert retrieved_task.title == added_task.title


class TestRepositoryListAll:
    """Test listing all tasks."""

    def test_list_all_empty_repository(self, temp_tasks_file: Path) -> None:
        """Test listing tasks from empty repository."""
        repo = InMemoryRepository(str(temp_tasks_file))
        tasks = repo.list_all()
        assert len(tasks) == 0

    def test_list_all_returns_sorted_tasks(
        self, temp_tasks_file: Path, sample_tasks_data: dict
    ) -> None:
        """Test that list_all returns tasks sorted by ID."""
        temp_tasks_file.write_text(json.dumps(sample_tasks_data))
        repo = InMemoryRepository(str(temp_tasks_file))

        tasks = repo.list_all()
        assert len(tasks) == 3
        assert tasks[0].id == 1
        assert tasks[1].id == 2
        assert tasks[2].id == 3

    def test_list_all_after_adding_tasks(self, temp_tasks_file: Path) -> None:
        """Test listing tasks after adding multiple tasks."""
        repo = InMemoryRepository(str(temp_tasks_file))
        repo.add("Task 1")
        repo.add("Task 2")
        repo.add("Task 3")

        tasks = repo.list_all()
        assert len(tasks) == 3
        assert [t.title for t in tasks] == ["Task 1", "Task 2", "Task 3"]


class TestRepositoryUpdate:
    """Test updating task fields."""

    def test_update_title_only(
        self, temp_tasks_file: Path, sample_tasks_data: dict
    ) -> None:
        """Test updating only the title field."""
        temp_tasks_file.write_text(json.dumps(sample_tasks_data))
        repo = InMemoryRepository(str(temp_tasks_file))

        updated = repo.update(1, title="Buy groceries and supplies")
        assert updated.id == 1
        assert updated.title == "Buy groceries and supplies"
        assert updated.description == "Milk, eggs, bread"  # Unchanged
        assert updated.completed is False

    def test_update_description_only(
        self, temp_tasks_file: Path, sample_tasks_data: dict
    ) -> None:
        """Test updating only the description field."""
        temp_tasks_file.write_text(json.dumps(sample_tasks_data))
        repo = InMemoryRepository(str(temp_tasks_file))

        updated = repo.update(1, description="Milk, eggs, bread, butter")
        assert updated.title == "Buy groceries"  # Unchanged
        assert updated.description == "Milk, eggs, bread, butter"

    def test_update_both_fields(
        self, temp_tasks_file: Path, sample_tasks_data: dict
    ) -> None:
        """Test updating both title and description."""
        temp_tasks_file.write_text(json.dumps(sample_tasks_data))
        repo = InMemoryRepository(str(temp_tasks_file))

        updated = repo.update(2, title="Schedule dentist", description="Annual checkup")
        assert updated.title == "Schedule dentist"
        assert updated.description == "Annual checkup"

    def test_update_persists_to_file(
        self, temp_tasks_file: Path, sample_tasks_data: dict
    ) -> None:
        """Test that update() saves changes to JSON file."""
        temp_tasks_file.write_text(json.dumps(sample_tasks_data))
        repo = InMemoryRepository(str(temp_tasks_file))

        repo.update(1, title="Updated title")

        # Reload from file
        data = json.loads(temp_tasks_file.read_text())
        task_data = next(t for t in data["tasks"] if t["id"] == 1)
        assert task_data["title"] == "Updated title"

    def test_update_nonexistent_task_raises_error(
        self, temp_tasks_file: Path
    ) -> None:
        """Test that updating nonexistent task raises KeyError."""
        repo = InMemoryRepository(str(temp_tasks_file))
        with pytest.raises(KeyError, match="Task 999 not found"):
            repo.update(999, title="New title")

    def test_update_with_invalid_title_raises_error(
        self, temp_tasks_file: Path, sample_tasks_data: dict
    ) -> None:
        """Test that updating with invalid title raises ValueError."""
        temp_tasks_file.write_text(json.dumps(sample_tasks_data))
        repo = InMemoryRepository(str(temp_tasks_file))

        with pytest.raises(ValueError, match="Title is required"):
            repo.update(1, title="")

    def test_update_preserves_completed_status(
        self, temp_tasks_file: Path, sample_tasks_data: dict
    ) -> None:
        """Test that update preserves the completed flag."""
        temp_tasks_file.write_text(json.dumps(sample_tasks_data))
        repo = InMemoryRepository(str(temp_tasks_file))

        # Task 3 is completed
        updated = repo.update(3, title="Updated completed task")
        assert updated.completed is True


class TestRepositoryComplete:
    """Test marking tasks as complete."""

    def test_complete_task(
        self, temp_tasks_file: Path, sample_tasks_data: dict
    ) -> None:
        """Test marking incomplete task as complete."""
        temp_tasks_file.write_text(json.dumps(sample_tasks_data))
        repo = InMemoryRepository(str(temp_tasks_file))

        completed = repo.complete(1)
        assert completed.id == 1
        assert completed.completed is True

    def test_complete_already_completed_task(
        self, temp_tasks_file: Path, sample_tasks_data: dict
    ) -> None:
        """Test completing already completed task is idempotent."""
        temp_tasks_file.write_text(json.dumps(sample_tasks_data))
        repo = InMemoryRepository(str(temp_tasks_file))

        # Task 3 is already completed
        completed = repo.complete(3)
        assert completed.completed is True

    def test_complete_persists_to_file(
        self, temp_tasks_file: Path, sample_tasks_data: dict
    ) -> None:
        """Test that complete() saves changes to JSON file."""
        temp_tasks_file.write_text(json.dumps(sample_tasks_data))
        repo = InMemoryRepository(str(temp_tasks_file))

        repo.complete(1)

        # Reload from file
        data = json.loads(temp_tasks_file.read_text())
        task_data = next(t for t in data["tasks"] if t["id"] == 1)
        assert task_data["completed"] is True

    def test_complete_nonexistent_task_raises_error(
        self, temp_tasks_file: Path
    ) -> None:
        """Test that completing nonexistent task raises KeyError."""
        repo = InMemoryRepository(str(temp_tasks_file))
        with pytest.raises(KeyError, match="Task 999 not found"):
            repo.complete(999)

    def test_complete_preserves_other_fields(
        self, temp_tasks_file: Path, sample_tasks_data: dict
    ) -> None:
        """Test that complete() only changes completed flag."""
        temp_tasks_file.write_text(json.dumps(sample_tasks_data))
        repo = InMemoryRepository(str(temp_tasks_file))

        original = repo.get(1)
        completed = repo.complete(1)

        assert completed.id == original.id
        assert completed.title == original.title
        assert completed.description == original.description
        assert completed.completed is True  # Only this changed


class TestRepositoryDelete:
    """Test deleting tasks from repository."""

    def test_delete_existing_task(
        self, temp_tasks_file: Path, sample_tasks_data: dict
    ) -> None:
        """Test deleting task by ID."""
        temp_tasks_file.write_text(json.dumps(sample_tasks_data))
        repo = InMemoryRepository(str(temp_tasks_file))

        repo.delete(2)
        assert 2 not in repo.tasks
        assert len(repo.tasks) == 2

    def test_delete_persists_to_file(
        self, temp_tasks_file: Path, sample_tasks_data: dict
    ) -> None:
        """Test that delete() removes task from JSON file."""
        temp_tasks_file.write_text(json.dumps(sample_tasks_data))
        repo = InMemoryRepository(str(temp_tasks_file))

        repo.delete(2)

        # Reload from file
        data = json.loads(temp_tasks_file.read_text())
        assert len(data["tasks"]) == 2
        assert not any(t["id"] == 2 for t in data["tasks"])

    def test_delete_nonexistent_task_raises_error(
        self, temp_tasks_file: Path
    ) -> None:
        """Test that deleting nonexistent task raises KeyError."""
        repo = InMemoryRepository(str(temp_tasks_file))
        with pytest.raises(KeyError, match="Task 999 not found"):
            repo.delete(999)

    def test_delete_all_tasks(
        self, temp_tasks_file: Path, sample_tasks_data: dict
    ) -> None:
        """Test deleting all tasks results in empty repository."""
        temp_tasks_file.write_text(json.dumps(sample_tasks_data))
        repo = InMemoryRepository(str(temp_tasks_file))

        repo.delete(1)
        repo.delete(2)
        repo.delete(3)

        assert len(repo.tasks) == 0
        tasks = repo.list_all()
        assert len(tasks) == 0


class TestRepositoryPersistence:
    """Test atomic file writes and persistence patterns."""

    def test_atomic_write_uses_temp_file(self, temp_tasks_file: Path) -> None:
        """Test that saves use atomic write pattern."""
        repo = InMemoryRepository(str(temp_tasks_file))
        repo.add("Test task")

        # After save, temp file should not exist
        temp_file = temp_tasks_file.with_suffix(".tmp")
        assert not temp_file.exists()
        assert temp_tasks_file.exists()

    def test_persistence_roundtrip(self, temp_tasks_file: Path) -> None:
        """Test that data survives repository reload."""
        # Create first repository and add tasks
        repo1 = InMemoryRepository(str(temp_tasks_file))
        repo1.add("Task 1", "Description 1")
        repo1.add("Task 2", "Description 2")
        repo1.complete(1)

        # Create second repository from same file
        repo2 = InMemoryRepository(str(temp_tasks_file))

        assert len(repo2.tasks) == 2
        assert repo2.tasks[1].title == "Task 1"
        assert repo2.tasks[1].completed is True
        assert repo2.tasks[2].title == "Task 2"
        assert repo2.next_id == 3

    def test_json_format_is_human_readable(self, temp_tasks_file: Path) -> None:
        """Test that JSON file is formatted with indentation."""
        repo = InMemoryRepository(str(temp_tasks_file))
        repo.add("Test task")

        content = temp_tasks_file.read_text()
        # Should be indented (contains newlines and spaces)
        assert "\n" in content
        assert "  " in content  # 2-space indent
