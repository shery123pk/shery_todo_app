"""Integration tests for CLI commands using Click testing utilities."""

from pathlib import Path

import pytest
from click.testing import CliRunner

from todo_cli.commands import cli
from todo_cli.repository import InMemoryRepository


@pytest.fixture
def runner() -> CliRunner:
    """Provide Click test runner."""
    return CliRunner()


@pytest.fixture
def isolated_cli(runner: CliRunner, tmp_path: Path):
    """Provide CLI with isolated file system for testing.

    Yields:
        Tuple of (runner, tasks_file_path)
    """
    with runner.isolated_filesystem(temp_dir=tmp_path):
        tasks_file = Path("tasks.json")
        yield runner, tasks_file


class TestAddCommand:
    """Test 'todo add' command."""

    def test_add_task_with_title_only(self, isolated_cli) -> None:
        """Test adding task with only title."""
        runner, _ = isolated_cli
        result = runner.invoke(cli, ["add", "Buy milk"])

        assert result.exit_code == 0
        assert "[OK] Task added successfully!" in result.output
        assert "ID: 1" in result.output
        assert "Title: Buy milk" in result.output

    def test_add_task_with_description_short_flag(self, isolated_cli) -> None:
        """Test adding task with description using -d flag."""
        runner, _ = isolated_cli
        result = runner.invoke(cli, ["add", "Buy groceries", "-d", "Milk and eggs"])

        assert result.exit_code == 0
        assert "[OK] Task added successfully!" in result.output
        assert "Title: Buy groceries" in result.output
        assert "Description: Milk and eggs" in result.output

    def test_add_task_with_description_long_flag(self, isolated_cli) -> None:
        """Test adding task with description using --description flag."""
        runner, _ = isolated_cli
        result = runner.invoke(
            cli, ["add", "Call dentist", "--description", "Annual checkup"]
        )

        assert result.exit_code == 0
        assert "Description: Annual checkup" in result.output

    def test_add_task_with_empty_title_shows_error(self, isolated_cli) -> None:
        """Test that empty title shows validation error."""
        runner, _ = isolated_cli
        result = runner.invoke(cli, ["add", ""])

        assert result.exit_code == 1
        assert "[ERROR]" in result.output
        assert "Title is required" in result.output

    def test_add_task_with_too_long_title_shows_error(self, isolated_cli) -> None:
        """Test that title over 200 chars shows validation error."""
        runner, _ = isolated_cli
        long_title = "x" * 201
        result = runner.invoke(cli, ["add", long_title])

        assert result.exit_code == 1
        assert "[ERROR]" in result.output
        assert "Title too long" in result.output

    def test_add_task_with_too_long_description_shows_error(self, isolated_cli) -> None:
        """Test that description over 1000 chars shows validation error."""
        runner, _ = isolated_cli
        long_desc = "y" * 1001
        result = runner.invoke(cli, ["add", "Valid title", "-d", long_desc])

        assert result.exit_code == 1
        assert "[ERROR]" in result.output
        assert "Description too long" in result.output

    def test_add_multiple_tasks_increments_id(self, isolated_cli) -> None:
        """Test that adding multiple tasks increments IDs."""
        runner, _ = isolated_cli

        result1 = runner.invoke(cli, ["add", "First task"])
        assert "ID: 1" in result1.output

        result2 = runner.invoke(cli, ["add", "Second task"])
        assert "ID: 2" in result2.output

        result3 = runner.invoke(cli, ["add", "Third task"])
        assert "ID: 3" in result3.output

    def test_add_task_persists_to_file(self, isolated_cli) -> None:
        """Test that added task is persisted to JSON file."""
        runner, tasks_file = isolated_cli
        runner.invoke(cli, ["add", "Test task"])

        # Verify file exists and contains task
        assert tasks_file.exists()
        import json

        data = json.loads(tasks_file.read_text())
        assert data["next_id"] == 2
        assert len(data["tasks"]) == 1
        assert data["tasks"][0]["title"] == "Test task"


class TestListCommand:
    """Test 'todo list' command."""

    def test_list_empty_tasks(self, isolated_cli) -> None:
        """Test listing when no tasks exist."""
        runner, _ = isolated_cli
        result = runner.invoke(cli, ["list"])

        assert result.exit_code == 0
        assert "No incomplete tasks found." in result.output

    def test_list_shows_incomplete_tasks_by_default(self, isolated_cli) -> None:
        """Test that list shows only incomplete tasks by default."""
        runner, _ = isolated_cli
        runner.invoke(cli, ["add", "Task 1"])
        runner.invoke(cli, ["add", "Task 2"])
        runner.invoke(cli, ["complete", "1"])

        result = runner.invoke(cli, ["list"])

        assert result.exit_code == 0
        assert "Task 2" in result.output
        assert "Task 1" not in result.output
        assert "Total: 1 tasks (0 completed)" in result.output

    def test_list_all_flag_shows_all_tasks(self, isolated_cli) -> None:
        """Test --all flag shows both complete and incomplete tasks."""
        runner, _ = isolated_cli
        runner.invoke(cli, ["add", "Task 1"])
        runner.invoke(cli, ["add", "Task 2"])
        runner.invoke(cli, ["complete", "1"])

        result = runner.invoke(cli, ["list", "--all"])

        assert result.exit_code == 0
        assert "Task 1" in result.output
        assert "Task 2" in result.output
        assert "[X]" in result.output  # Completed marker
        assert "[ ]" in result.output  # Incomplete marker
        assert "Total: 2 tasks (1 completed)" in result.output

    def test_list_completed_flag_shows_only_completed(self, isolated_cli) -> None:
        """Test --completed flag shows only completed tasks."""
        runner, _ = isolated_cli
        runner.invoke(cli, ["add", "Task 1"])
        runner.invoke(cli, ["add", "Task 2"])
        runner.invoke(cli, ["complete", "1"])

        result = runner.invoke(cli, ["list", "--completed"])

        assert result.exit_code == 0
        assert "Task 1" in result.output
        assert "Task 2" not in result.output
        assert "Total: 1 tasks (1 completed)" in result.output

    def test_list_shows_table_header(self, isolated_cli) -> None:
        """Test that list shows formatted table header."""
        runner, _ = isolated_cli
        runner.invoke(cli, ["add", "Test task"])

        result = runner.invoke(cli, ["list"])

        assert "ID" in result.output
        assert "Status" in result.output
        assert "Title" in result.output
        assert "Description" in result.output
        assert "---" in result.output  # Separator line

    def test_list_truncates_long_description(self, isolated_cli) -> None:
        """Test that long descriptions are truncated in list view."""
        runner, _ = isolated_cli
        long_desc = "x" * 100
        runner.invoke(cli, ["add", "Task", "-d", long_desc])

        result = runner.invoke(cli, ["list"])

        assert result.exit_code == 0
        assert "..." in result.output  # Truncation indicator


class TestCompleteCommand:
    """Test 'todo complete' command."""

    def test_complete_existing_task(self, isolated_cli) -> None:
        """Test marking existing task as complete."""
        runner, _ = isolated_cli
        runner.invoke(cli, ["add", "Buy milk"])

        result = runner.invoke(cli, ["complete", "1"])

        assert result.exit_code == 0
        assert "[OK] Task 1 marked as complete!" in result.output
        assert "Buy milk" in result.output

    def test_complete_nonexistent_task_shows_error(self, isolated_cli) -> None:
        """Test completing nonexistent task shows error."""
        runner, _ = isolated_cli
        result = runner.invoke(cli, ["complete", "999"])

        assert result.exit_code == 1
        assert "[ERROR]" in result.output
        assert "Task 999 not found" in result.output

    def test_complete_task_persists_change(self, isolated_cli) -> None:
        """Test that completed status is persisted."""
        runner, tasks_file = isolated_cli
        runner.invoke(cli, ["add", "Test task"])
        runner.invoke(cli, ["complete", "1"])

        # Verify persistence
        import json

        data = json.loads(tasks_file.read_text())
        assert data["tasks"][0]["completed"] is True

    def test_complete_already_completed_task_is_idempotent(self, isolated_cli) -> None:
        """Test completing already completed task doesn't error."""
        runner, _ = isolated_cli
        runner.invoke(cli, ["add", "Task"])
        runner.invoke(cli, ["complete", "1"])

        # Complete again
        result = runner.invoke(cli, ["complete", "1"])

        assert result.exit_code == 0
        assert "[OK] Task 1 marked as complete!" in result.output


class TestUpdateCommand:
    """Test 'todo update' command."""

    def test_update_title_only(self, isolated_cli) -> None:
        """Test updating only the title."""
        runner, _ = isolated_cli
        runner.invoke(cli, ["add", "Old title", "-d", "Description"])

        result = runner.invoke(cli, ["update", "1", "--title", "New title"])

        assert result.exit_code == 0
        assert "[OK] Task 1 updated successfully!" in result.output
        assert "Title: New title" in result.output
        assert "Description: Description" in result.output

    def test_update_description_only(self, isolated_cli) -> None:
        """Test updating only the description."""
        runner, _ = isolated_cli
        runner.invoke(cli, ["add", "Title", "-d", "Old desc"])

        result = runner.invoke(cli, ["update", "1", "-d", "New desc"])

        assert result.exit_code == 0
        assert "Title: Title" in result.output
        assert "Description: New desc" in result.output

    def test_update_both_fields(self, isolated_cli) -> None:
        """Test updating both title and description."""
        runner, _ = isolated_cli
        runner.invoke(cli, ["add", "Old", "-d", "Old desc"])

        result = runner.invoke(
            cli, ["update", "1", "-t", "New title", "-d", "New desc"]
        )

        assert result.exit_code == 0
        assert "Title: New title" in result.output
        assert "Description: New desc" in result.output

    def test_update_without_options_shows_error(self, isolated_cli) -> None:
        """Test update without title or description shows error."""
        runner, _ = isolated_cli
        runner.invoke(cli, ["add", "Task"])

        result = runner.invoke(cli, ["update", "1"])

        assert result.exit_code == 1
        assert "[ERROR] Must provide at least one of --title or --description" in result.output

    def test_update_nonexistent_task_shows_error(self, isolated_cli) -> None:
        """Test updating nonexistent task shows error."""
        runner, _ = isolated_cli
        result = runner.invoke(cli, ["update", "999", "-t", "Title"])

        assert result.exit_code == 1
        assert "[ERROR]" in result.output
        assert "Task 999 not found" in result.output

    def test_update_with_invalid_title_shows_error(self, isolated_cli) -> None:
        """Test update with empty title shows validation error."""
        runner, _ = isolated_cli
        runner.invoke(cli, ["add", "Task"])

        result = runner.invoke(cli, ["update", "1", "--title", ""])

        assert result.exit_code == 1
        assert "[ERROR]" in result.output
        assert "Title is required" in result.output


class TestDeleteCommand:
    """Test 'todo delete' command."""

    def test_delete_with_confirmation_yes(self, isolated_cli) -> None:
        """Test deleting task with confirmation (user says yes)."""
        runner, _ = isolated_cli
        runner.invoke(cli, ["add", "Task to delete"])

        result = runner.invoke(cli, ["delete", "1"], input="y\n")

        assert result.exit_code == 0
        assert "About to delete task 1: Task to delete" in result.output
        assert "Are you sure?" in result.output
        assert "[OK] Task 1 deleted successfully!" in result.output

    def test_delete_with_confirmation_no(self, isolated_cli) -> None:
        """Test deleting task with confirmation (user says no)."""
        runner, _ = isolated_cli
        runner.invoke(cli, ["add", "Task to keep"])

        result = runner.invoke(cli, ["delete", "1"], input="n\n")

        assert result.exit_code == 0
        assert "Deletion cancelled." in result.output

        # Verify task still exists
        list_result = runner.invoke(cli, ["list"])
        assert "Task to keep" in list_result.output

    def test_delete_with_yes_flag_skips_confirmation(self, isolated_cli) -> None:
        """Test --yes flag skips confirmation prompt."""
        runner, _ = isolated_cli
        runner.invoke(cli, ["add", "Task to delete"])

        result = runner.invoke(cli, ["delete", "1", "--yes"])

        assert result.exit_code == 0
        assert "Are you sure?" not in result.output
        assert "[OK] Task 1 deleted successfully!" in result.output

    def test_delete_with_short_yes_flag(self, isolated_cli) -> None:
        """Test -y flag skips confirmation prompt."""
        runner, _ = isolated_cli
        runner.invoke(cli, ["add", "Task"])

        result = runner.invoke(cli, ["delete", "1", "-y"])

        assert result.exit_code == 0
        assert "[OK] Task 1 deleted successfully!" in result.output

    def test_delete_nonexistent_task_shows_error(self, isolated_cli) -> None:
        """Test deleting nonexistent task shows error."""
        runner, _ = isolated_cli
        result = runner.invoke(cli, ["delete", "999", "-y"])

        assert result.exit_code == 1
        assert "[ERROR]" in result.output
        assert "Task 999 not found" in result.output

    def test_delete_removes_from_persistence(self, isolated_cli) -> None:
        """Test that delete removes task from JSON file."""
        runner, tasks_file = isolated_cli
        runner.invoke(cli, ["add", "Task 1"])
        runner.invoke(cli, ["add", "Task 2"])
        runner.invoke(cli, ["delete", "1", "-y"])

        # Verify persistence
        import json

        data = json.loads(tasks_file.read_text())
        assert len(data["tasks"]) == 1
        assert data["tasks"][0]["id"] == 2
