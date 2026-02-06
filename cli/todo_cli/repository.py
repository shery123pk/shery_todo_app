"""Repository for in-memory task storage with JSON persistence."""

import json
from datetime import datetime, timedelta
from pathlib import Path
from typing import Optional

import click

from .models import Task


class InMemoryRepository:
    """Manages task collection with JSON file persistence.

    Professional repository with ALL 10 features:
    - Search by keyword
    - Filter by priority, tags, completion status
    - Sort by priority, due date, title
    - Handle recurring tasks
    - Due date management
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

    def add(
        self,
        title: str,
        description: str = "",
        priority: str = "medium",
        tags: Optional[list[str]] = None,
        due_date: Optional[str] = None,
        recurring: bool = False,
        recurrence_pattern: Optional[str] = None,
    ) -> Task:
        """Create new task with all professional features.

        Args:
            title: Task title (required, 1-200 chars)
            description: Optional details (0-1000 chars)
            priority: Priority level (low/medium/high)
            tags: List of category tags (e.g., ['work', 'urgent'])
            due_date: Deadline in ISO format (YYYY-MM-DD HH:MM)
            recurring: Whether task repeats automatically
            recurrence_pattern: How often (daily/weekly/monthly)

        Returns:
            Created task with assigned ID

        Raises:
            ValueError: If validation fails
        """
        task = Task(
            id=self.next_id,
            title=title,
            description=description,
            priority=priority,
            tags=tags or [],
            due_date=due_date,
            recurring=recurring,
            recurrence_pattern=recurrence_pattern,
        )
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

    def search(
        self,
        query: Optional[str] = None,
        priority: Optional[str] = None,
        tags: Optional[list[str]] = None,
        completed: Optional[bool] = None,
        overdue: bool = False,
        sort_by: str = "id",
        reverse: bool = False,
    ) -> list[Task]:
        """Search and filter tasks with advanced options.

        Args:
            query: Search keyword in title/description
            priority: Filter by priority (low/medium/high)
            tags: Filter by tags (any matching tag)
            completed: Filter by completion status
            overdue: Show only overdue tasks
            sort_by: Sort field (id/priority/due_date/title)
            reverse: Sort in descending order

        Returns:
            Filtered and sorted list of tasks
        """
        tasks = list(self.tasks.values())

        # Filter by search query
        if query:
            query_lower = query.lower()
            tasks = [
                t for t in tasks
                if query_lower in t.title.lower() or query_lower in t.description.lower()
            ]

        # Filter by priority
        if priority:
            tasks = [t for t in tasks if t.priority == priority]

        # Filter by tags (any matching tag)
        if tags:
            tasks = [t for t in tasks if any(tag in t.tags for tag in tags)]

        # Filter by completion status
        if completed is not None:
            tasks = [t for t in tasks if t.completed == completed]

        # Filter overdue tasks
        if overdue:
            tasks = [t for t in tasks if t.is_overdue()]

        # Sort tasks
        if sort_by == "priority":
            tasks.sort(key=lambda t: t.priority_value(), reverse=not reverse)
        elif sort_by == "due_date":
            # Put tasks without due_date at the end
            tasks.sort(
                key=lambda t: (t.due_date is None, t.due_date or ""),
                reverse=reverse
            )
        elif sort_by == "title":
            tasks.sort(key=lambda t: t.title.lower(), reverse=reverse)
        else:  # id
            tasks.sort(key=lambda t: t.id, reverse=reverse)

        return tasks

    def list_all(self) -> list[Task]:
        """Return all tasks sorted by ID.

        Returns:
            List of tasks ordered from oldest to newest
        """
        return sorted(self.tasks.values(), key=lambda t: t.id)

    def update(
        self,
        task_id: int,
        title: Optional[str] = None,
        description: Optional[str] = None,
        priority: Optional[str] = None,
        tags: Optional[list[str]] = None,
        due_date: Optional[str] = None,
        recurring: Optional[bool] = None,
        recurrence_pattern: Optional[str] = None,
    ) -> Task:
        """Update task fields (partial update supported).

        Args:
            task_id: Task identifier
            title: New title (None to keep current)
            description: New description (None to keep current)
            priority: New priority (None to keep current)
            tags: New tags list (None to keep current)
            due_date: New due date (None to keep current)
            recurring: New recurring flag (None to keep current)
            recurrence_pattern: New pattern (None to keep current)

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
            priority=priority if priority is not None else task.priority,
            tags=tags if tags is not None else task.tags,
            due_date=due_date if due_date is not None else task.due_date,
            recurring=recurring if recurring is not None else task.recurring,
            recurrence_pattern=recurrence_pattern if recurrence_pattern is not None else task.recurrence_pattern,
        )

        self.tasks[task_id] = updated_task
        self._save()
        return updated_task

    def complete(self, task_id: int) -> Task:
        """Mark task as complete. If recurring, create next occurrence.

        Args:
            task_id: Task identifier

        Returns:
            Updated task with completed=True

        Raises:
            KeyError: If task not found
        """
        task = self.get(task_id)
        task.completed = True

        # Handle recurring tasks
        if task.recurring and task.recurrence_pattern and task.due_date:
            next_task = self._create_next_recurrence(task)
            if next_task:
                click.secho(
                    f"[OK] Created recurring task #{next_task.id}: {next_task.title} (due {next_task.due_date})",
                    fg="cyan"
                )

        self._save()
        return task

    def _create_next_recurrence(self, task: Task) -> Optional[Task]:
        """Create next occurrence of a recurring task.

        Args:
            task: Completed recurring task

        Returns:
            New task for next occurrence, or None if unable to create
        """
        if not task.due_date or not task.recurrence_pattern:
            return None

        try:
            current_due = datetime.fromisoformat(task.due_date)

            # Calculate next due date
            if task.recurrence_pattern == "daily":
                next_due = current_due + timedelta(days=1)
            elif task.recurrence_pattern == "weekly":
                next_due = current_due + timedelta(weeks=1)
            elif task.recurrence_pattern == "monthly":
                # Add roughly a month (30 days)
                next_due = current_due + timedelta(days=30)
            else:
                return None

            # Create next occurrence
            return self.add(
                title=task.title,
                description=task.description,
                priority=task.priority,
                tags=task.tags,
                due_date=next_due.isoformat(),
                recurring=True,
                recurrence_pattern=task.recurrence_pattern,
            )
        except (ValueError, TypeError):
            return None

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

    def get_stats(self) -> dict:
        """Get statistics about tasks.

        Returns:
            Dictionary with total, completed, by_priority, by_tags, overdue counts
        """
        all_tasks = list(self.tasks.values())

        stats = {
            "total": len(all_tasks),
            "completed": sum(1 for t in all_tasks if t.completed),
            "incomplete": sum(1 for t in all_tasks if not t.completed),
            "by_priority": {
                "high": sum(1 for t in all_tasks if t.priority == "high" and not t.completed),
                "medium": sum(1 for t in all_tasks if t.priority == "medium" and not t.completed),
                "low": sum(1 for t in all_tasks if t.priority == "low" and not t.completed),
            },
            "overdue": sum(1 for t in all_tasks if t.is_overdue()),
            "recurring": sum(1 for t in all_tasks if t.recurring and not t.completed),
        }

        # Count all unique tags
        all_tags = {}
        for task in all_tasks:
            if not task.completed:
                for tag in task.tags:
                    all_tags[tag] = all_tags.get(tag, 0) + 1
        stats["by_tags"] = all_tags

        return stats
