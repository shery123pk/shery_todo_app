"""Repository for in-memory task storage with JSON persistence."""

import json
from pathlib import Path
from typing import Optional

import click

from .models import Task


class InMemoryRepository:
    """Manages task collection with JSON file persistence.

    All operations work against in-memory dict. File I/O is only for
    persistence between sessions. Uses atomic writes to prevent corruption.
    """

    def __init__(self, file_path: str = "tasks.json") -> None:
        """Initialize repository and load existing tasks if available.

        Args:
            file_path: Path to JSON file for persistence (default: tasks.json)
        """
        self.tasks: dict[int, Task] = {}
        self.next_id: int = 1
        self.file_path = Path(file_path)
        self._load()

    def _load(self) -> None:
        """Load tasks from JSON file with error handling.

        If file doesn't exist or is corrupted, starts with empty state.
        Displays warning but doesn't crash.
        """
        if not self.file_path.exists():
            return  # Start with empty state

        try:
            data = json.loads(self.file_path.read_text())
            self.next_id = data.get("next_id", 1)

            for task_data in data.get("tasks", []):
                try:
                    task = Task.from_dict(task_data)
                    self.tasks[task.id] = task
                except (ValueError, KeyError) as e:
                    # Skip invalid tasks, log warning
                    click.echo(
                        f"Warning: Skipping invalid task {task_data.get('id', '?')}: {e}",
                        err=True,
                    )

        except (json.JSONDecodeError, OSError) as e:
            click.secho(
                f"Warning: Could not load tasks from {self.file_path}: {e}. "
                "Starting with empty task list.",
                fg="yellow",
            )

    def _save(self) -> None:
        """Save tasks to JSON file with atomic write.

        Uses temp file + rename pattern to prevent corruption. Handles
        I/O errors gracefully with user-friendly messages.
        """
        try:
            data = {
                "next_id": self.next_id,
                "tasks": [task.to_dict() for task in sorted(self.tasks.values(), key=lambda t: t.id)],
            }

            # Atomic write: write to temp file, then rename
            temp_file = self.file_path.with_suffix(".tmp")
            temp_file.write_text(json.dumps(data, indent=2))
            temp_file.replace(self.file_path)

        except OSError as e:
            click.secho(
                f"Warning: Could not save tasks to {self.file_path}: {e}. "
                "Continuing with in-memory data.",
                fg="yellow",
                err=True,
            )

    def add(self, title: str, description: str = "") -> Task:
        """Create new task with auto-assigned ID.

        Args:
            title: Task title (required, 1-200 chars)
            description: Optional details (0-1000 chars)

        Returns:
            Created task with assigned ID

        Raises:
            ValueError: If validation fails
        """
        task = Task(id=self.next_id, title=title, description=description)
        self.tasks[task.id] = task
        self.next_id += 1
        self._save()
        return task

    def get(self, task_id: int) -> Task:
        """Retrieve task by ID.

        Args:
            task_id: Task identifier

        Returns:
            Task with given ID

        Raises:
            KeyError: If task not found
        """
        if task_id not in self.tasks:
            raise KeyError(f"Task {task_id} not found.")
        return self.tasks[task_id]

    def list_all(self) -> list[Task]:
        """Return all tasks sorted by ID.

        Returns:
            List of tasks ordered from oldest to newest
        """
        return sorted(self.tasks.values(), key=lambda t: t.id)

    def update(
        self, task_id: int, title: Optional[str] = None, description: Optional[str] = None
    ) -> Task:
        """Update task fields (partial update supported).

        Args:
            task_id: Task identifier
            title: New title (None to keep current)
            description: New description (None to keep current)

        Returns:
            Updated task

        Raises:
            KeyError: If task not found
            ValueError: If validation fails
        """
        task = self.get(task_id)

        # Create updated task to trigger validation
        updated_task = Task(
            id=task.id,
            title=title if title is not None else task.title,
            description=description if description is not None else task.description,
            completed=task.completed,
        )

        self.tasks[task_id] = updated_task
        self._save()
        return updated_task

    def complete(self, task_id: int) -> Task:
        """Mark task as complete.

        Args:
            task_id: Task identifier

        Returns:
            Updated task with completed=True

        Raises:
            KeyError: If task not found
        """
        task = self.get(task_id)
        task.completed = True
        self._save()
        return task

    def delete(self, task_id: int) -> None:
        """Remove task permanently.

        Args:
            task_id: Task identifier

        Raises:
            KeyError: If task not found
        """
        if task_id not in self.tasks:
            raise KeyError(f"Task {task_id} not found.")

        del self.tasks[task_id]
        self._save()
