"""Domain models for the todo CLI application."""

from dataclasses import dataclass
from typing import ClassVar


@dataclass
class Task:
    """Represents a todo item with validation.

    This is the immutable core domain model for Phase 1. Future phases may add
    fields but must preserve this schema for backward compatibility.

    Attributes:
        id: Unique integer identifier (auto-assigned, immutable)
        title: Brief description of what needs to be done (required, 1-200 chars)
        description: Optional additional details (0-1000 chars)
        completed: Whether task has been finished (default: False)
    """

    id: int
    title: str
    description: str = ""
    completed: bool = False

    # Validation constants
    TITLE_MAX_LENGTH: ClassVar[int] = 200
    TITLE_MIN_LENGTH: ClassVar[int] = 1
    DESC_MAX_LENGTH: ClassVar[int] = 1000

    def __post_init__(self) -> None:
        """Validate task fields after initialization.

        Raises:
            ValueError: If validation fails (empty title, too long, wrong type)
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

    def to_dict(self) -> dict:
        """Serialize task to JSON-compatible dictionary.

        Returns:
            Dictionary with id, title, description, completed fields
        """
        return {
            "id": self.id,
            "title": self.title,
            "description": self.description,
            "completed": self.completed,
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
        )
