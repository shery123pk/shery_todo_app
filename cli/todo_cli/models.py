"""Domain models for the todo CLI application."""

from dataclasses import dataclass, field
from datetime import datetime
from typing import ClassVar, Optional


@dataclass
class Task:
    """Represents a todo item with validation.

    Professional todo app with all 10 features:
    - Basic: add, delete, update, view, complete
    - Intermediate: priorities, tags, search, filter, sort
    - Advanced: recurring tasks, due dates, reminders

    Attributes:
        id: Unique integer identifier (auto-assigned, immutable)
        title: Brief description of what needs to be done (required, 1-200 chars)
        description: Optional additional details (0-1000 chars)
        completed: Whether task has been finished (default: False)
        priority: Task priority level: low, medium, or high (default: medium)
        tags: List of category tags (e.g., ['work', 'urgent'])
        due_date: Optional deadline as ISO string (e.g., '2025-12-31 23:59')
        recurring: Whether task repeats automatically (default: False)
        recurrence_pattern: How often task repeats: daily, weekly, monthly
    """

    id: int
    title: str
    description: str = ""
    completed: bool = False
    priority: str = "medium"  # low, medium, high
    tags: list[str] = field(default_factory=list)
    due_date: Optional[str] = None  # ISO format: YYYY-MM-DD HH:MM
    recurring: bool = False
    recurrence_pattern: Optional[str] = None  # daily, weekly, monthly

    # Validation constants
    TITLE_MAX_LENGTH: ClassVar[int] = 200
    TITLE_MIN_LENGTH: ClassVar[int] = 1
    DESC_MAX_LENGTH: ClassVar[int] = 1000
    VALID_PRIORITIES: ClassVar[set[str]] = {"low", "medium", "high"}
    VALID_RECURRENCE: ClassVar[set[str]] = {"daily", "weekly", "monthly"}

    def __post_init__(self) -> None:
        """Validate task fields after initialization.

        Raises:
            ValueError: If validation fails (empty title, invalid priority, etc.)
        """
        # Trim whitespace from title
        self.title = self.title.strip()

        # Validate title
        if len(self.title) < self.TITLE_MIN_LENGTH:
            raise ValueError("Title is required.")
        if len(self.title) > self.TITLE_MAX_LENGTH:
            raise ValueError(f"Title too long (max {self.TITLE_MAX_LENGTH}).")

        # Validate description
        if len(self.description) > self.DESC_MAX_LENGTH:
            raise ValueError(f"Description too long (max {self.DESC_MAX_LENGTH}).")

        # Validate completed is boolean
        if not isinstance(self.completed, bool):
            raise ValueError("Completed must be a boolean.")

        # Validate priority
        if self.priority not in self.VALID_PRIORITIES:
            raise ValueError(f"Priority must be one of: {', '.join(self.VALID_PRIORITIES)}")

        # Validate tags is a list
        if not isinstance(self.tags, list):
            raise ValueError("Tags must be a list.")

        # Validate due_date format if provided
        if self.due_date:
            try:
                datetime.fromisoformat(self.due_date)
            except ValueError:
                raise ValueError("Due date must be in ISO format (YYYY-MM-DD HH:MM)")

        # Validate recurring pattern
        if self.recurring and self.recurrence_pattern not in self.VALID_RECURRENCE:
            raise ValueError(f"Recurrence pattern must be one of: {', '.join(self.VALID_RECURRENCE)}")

    def to_dict(self) -> dict:
        """Serialize task to JSON-compatible dictionary.

        Returns:
            Dictionary with all task fields including new features
        """
        return {
            "id": self.id,
            "title": self.title,
            "description": self.description,
            "completed": self.completed,
            "priority": self.priority,
            "tags": self.tags,
            "due_date": self.due_date,
            "recurring": self.recurring,
            "recurrence_pattern": self.recurrence_pattern,
        }

    @classmethod
    def from_dict(cls, data: dict) -> "Task":
        """Deserialize task from JSON dictionary.

        Args:
            data: Dictionary containing task fields

        Returns:
            Task instance created from dictionary data
        """
        return cls(
            id=data["id"],
            title=data["title"],
            description=data.get("description", ""),
            completed=data.get("completed", False),
            priority=data.get("priority", "medium"),
            tags=data.get("tags", []),
            due_date=data.get("due_date"),
            recurring=data.get("recurring", False),
            recurrence_pattern=data.get("recurrence_pattern"),
        )

    def is_overdue(self) -> bool:
        """Check if task is past its due date.

        Returns:
            True if task has a due date and it's in the past
        """
        if not self.due_date or self.completed:
            return False
        due = datetime.fromisoformat(self.due_date)
        return datetime.now() > due

    def priority_value(self) -> int:
        """Get numeric value for priority (for sorting).

        Returns:
            3 for high, 2 for medium, 1 for low
        """
        return {"high": 3, "medium": 2, "low": 1}[self.priority]
