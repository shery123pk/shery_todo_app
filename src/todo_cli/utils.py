"""Utility functions for task formatting and display."""

from .models import Task


def format_status_icon(completed: bool) -> str:
    """Format completion status as icon.

    Args:
        completed: Whether task is complete

    Returns:
        "[X]" for completed, "[ ]" for incomplete
    """
    return "[X]" if completed else "[ ]"


def format_task_row(task: Task, max_desc_length: int = 40) -> tuple[int, str, str, str]:
    """Format task as table row components.

    Args:
        task: Task to format
        max_desc_length: Maximum description length before truncation

    Returns:
        Tuple of (id, status, title, description) for table display
    """
    status = format_status_icon(task.completed)
    description = task.description

    # Truncate description if too long
    if len(description) > max_desc_length:
        description = description[: max_desc_length - 3] + "..."

    return (task.id, status, task.title, description)


def format_task_table_header() -> str:
    """Generate table header for task list.

    Returns:
        Formatted header row
    """
    return f"{'ID':<4} {'Status':<7} {'Title':<30} {'Description':<40}"


def format_table_separator() -> str:
    """Generate table separator line.

    Returns:
        Horizontal separator matching header width
    """
    return "-" * 85
