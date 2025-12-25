"""Unit tests for Task model validation and serialization."""

import pytest

from todo_cli.models import Task


class TestTaskValidation:
    """Test Task model validation logic."""

    def test_valid_task_creation(self) -> None:
        """Test creating task with valid data."""
        task = Task(id=1, title="Buy groceries", description="Milk and eggs")
        assert task.id == 1
        assert task.title == "Buy groceries"
        assert task.description == "Milk and eggs"
        assert task.completed is False

    def test_task_with_minimal_fields(self) -> None:
        """Test creating task with only required fields."""
        task = Task(id=2, title="Call dentist")
        assert task.id == 2
        assert task.title == "Call dentist"
        assert task.description == ""
        assert task.completed is False

    def test_task_title_trimming(self) -> None:
        """Test that task title whitespace is trimmed."""
        task = Task(id=3, title="  Clean kitchen  ")
        assert task.title == "Clean kitchen"

    def test_empty_title_raises_error(self) -> None:
        """Test that empty title raises ValueError."""
        with pytest.raises(ValueError, match="Title is required"):
            Task(id=1, title="")

    def test_whitespace_only_title_raises_error(self) -> None:
        """Test that whitespace-only title raises ValueError."""
        with pytest.raises(ValueError, match="Title is required"):
            Task(id=1, title="   ")

    def test_title_too_long_raises_error(self) -> None:
        """Test that title over 200 chars raises ValueError."""
        long_title = "x" * 201
        with pytest.raises(ValueError, match="Title too long"):
            Task(id=1, title=long_title)

    def test_title_max_length_allowed(self) -> None:
        """Test that title with exactly 200 chars is valid."""
        max_title = "x" * 200
        task = Task(id=1, title=max_title)
        assert len(task.title) == 200

    def test_description_too_long_raises_error(self) -> None:
        """Test that description over 1000 chars raises ValueError."""
        long_desc = "y" * 1001
        with pytest.raises(ValueError, match="Description too long"):
            Task(id=1, title="Valid title", description=long_desc)

    def test_description_max_length_allowed(self) -> None:
        """Test that description with exactly 1000 chars is valid."""
        max_desc = "y" * 1000
        task = Task(id=1, title="Valid title", description=max_desc)
        assert len(task.description) == 1000

    def test_completed_must_be_boolean(self) -> None:
        """Test that non-boolean completed raises ValueError."""
        with pytest.raises(ValueError, match="Completed must be a boolean"):
            Task(id=1, title="Test", completed="yes")  # type: ignore


class TestTaskSerialization:
    """Test Task serialization and deserialization."""

    def test_to_dict_complete_task(self) -> None:
        """Test serializing complete task to dict."""
        task = Task(id=1, title="Buy milk", description="2% milk", completed=False)
        data = task.to_dict()

        assert data == {
            "id": 1,
            "title": "Buy milk",
            "description": "2% milk",
            "completed": False,
        }

    def test_to_dict_minimal_task(self) -> None:
        """Test serializing task with no description."""
        task = Task(id=2, title="Call dentist")
        data = task.to_dict()

        assert data == {
            "id": 2,
            "title": "Call dentist",
            "description": "",
            "completed": False,
        }

    def test_from_dict_complete_task(self) -> None:
        """Test deserializing complete task from dict."""
        data = {
            "id": 3,
            "title": "Finish report",
            "description": "Submit by Friday",
            "completed": True,
        }
        task = Task.from_dict(data)

        assert task.id == 3
        assert task.title == "Finish report"
        assert task.description == "Submit by Friday"
        assert task.completed is True

    def test_from_dict_minimal_data(self) -> None:
        """Test deserializing task with missing optional fields."""
        data = {"id": 4, "title": "Review PR"}
        task = Task.from_dict(data)

        assert task.id == 4
        assert task.title == "Review PR"
        assert task.description == ""
        assert task.completed is False

    def test_roundtrip_serialization(self) -> None:
        """Test that to_dict -> from_dict preserves data."""
        original = Task(id=5, title="Deploy app", description="Production", completed=True)
        data = original.to_dict()
        restored = Task.from_dict(data)

        assert restored.id == original.id
        assert restored.title == original.title
        assert restored.description == original.description
        assert restored.completed == original.completed
