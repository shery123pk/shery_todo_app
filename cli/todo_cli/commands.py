"""Click commands for todo CLI application."""

from pathlib import Path

import click

from .models import Task
from .repository import InMemoryRepository
from .utils import format_table_separator, format_task_row, format_task_table_header


def get_repository(ctx: click.Context) -> InMemoryRepository:
    """Get or create repository instance from context.

    Args:
        ctx: Click context object

    Returns:
        InMemoryRepository instance
    """
    if ctx.obj is None:
        ctx.obj = {}
    if "repo" not in ctx.obj:
        ctx.obj["repo"] = InMemoryRepository()
    return ctx.obj["repo"]


@click.group()
@click.pass_context
def cli(ctx: click.Context) -> None:
    """Todo CLI - Manage your tasks from the command line."""
    ctx.ensure_object(dict)


@cli.command()
@click.argument("title")
@click.option(
    "-d", "--description", default="", help="Optional task description (max 1000 chars)"
)
@click.pass_context
def add(ctx: click.Context, title: str, description: str) -> None:
    """Add a new task to your todo list.

    TITLE: Brief description of the task (required, max 200 chars)

    Examples:
        todo add "Buy groceries"
        todo add "Call dentist" -d "Annual checkup appointment"
        todo add "Finish report" --description "Submit by Friday 5pm"
    """
    repo = get_repository(ctx)

    try:
        task = repo.add(title=title, description=description)
        click.secho("[OK] Task added successfully!", fg="green")
        click.echo(f"  ID: {task.id}")
        click.echo(f"  Title: {task.title}")
        if task.description:
            click.echo(f"  Description: {task.description}")

    except ValueError as e:
        click.secho(f"[ERROR] {e}", fg="red", err=True)
        raise click.Abort()


@cli.command()
@click.option(
    "-a", "--all", "show_all", is_flag=True, help="Show all tasks (default: incomplete only)"
)
@click.option(
    "-c", "--completed", "show_completed", is_flag=True, help="Show only completed tasks"
)
@click.pass_context
def list(ctx: click.Context, show_all: bool, show_completed: bool) -> None:
    """List tasks in a formatted table.

    By default, shows only incomplete tasks. Use --all to show everything
    or --completed to show only finished tasks.

    Examples:
        todo list              # Show incomplete tasks
        todo list --all        # Show all tasks
        todo list --completed  # Show only completed tasks
    """
    repo = get_repository(ctx)
    tasks = repo.list_all()

    # Filter based on flags
    if show_completed:
        tasks = [t for t in tasks if t.completed]
    elif not show_all:
        tasks = [t for t in tasks if not t.completed]

    if not tasks:
        filter_msg = (
            "completed tasks"
            if show_completed
            else "tasks" if show_all else "incomplete tasks"
        )
        click.secho(f"No {filter_msg} found.", fg="yellow")
        return

    # Print table header
    click.echo(format_task_table_header())
    click.echo(format_table_separator())

    # Print each task
    for task in tasks:
        task_id, status, title, description = format_task_row(task)
        click.echo(f"{task_id:<4} {status:<7} {title:<30} {description:<40}")

    # Print summary
    completed_count = sum(1 for t in tasks if t.completed)
    total_count = len(tasks)
    click.echo(format_table_separator())
    click.echo(f"Total: {total_count} tasks ({completed_count} completed)")


@cli.command()
@click.argument("task_id", type=int)
@click.pass_context
def complete(ctx: click.Context, task_id: int) -> None:
    """Mark a task as complete.

    TASK_ID: The ID of the task to mark as complete

    Examples:
        todo complete 1
        todo complete 42
    """
    repo = get_repository(ctx)

    try:
        task = repo.complete(task_id)
        click.secho(f"[OK] Task {task.id} marked as complete!", fg="green")
        click.echo(f"  {task.title}")

    except KeyError as e:
        click.secho(f"[ERROR] {e}", fg="red", err=True)
        raise click.Abort()


@cli.command()
@click.argument("task_id", type=int)
@click.option("-t", "--title", help="New title for the task")
@click.option("-d", "--description", help="New description for the task")
@click.pass_context
def update(
    ctx: click.Context, task_id: int, title: str | None, description: str | None
) -> None:
    """Update a task's title or description.

    TASK_ID: The ID of the task to update

    At least one of --title or --description must be provided.

    Examples:
        todo update 1 --title "Buy groceries and supplies"
        todo update 2 -d "Call dentist for annual checkup"
        todo update 3 -t "Finish report" -d "Submit by Friday 5pm"
    """
    if title is None and description is None:
        click.secho(
            "[ERROR] Must provide at least one of --title or --description",
            fg="red",
            err=True,
        )
        raise click.Abort()

    repo = get_repository(ctx)

    try:
        task = repo.update(task_id, title=title, description=description)
        click.secho(f"[OK] Task {task.id} updated successfully!", fg="green")
        click.echo(f"  Title: {task.title}")
        click.echo(f"  Description: {task.description}")

    except (KeyError, ValueError) as e:
        click.secho(f"[ERROR] {e}", fg="red", err=True)
        raise click.Abort()


@cli.command()
@click.argument("task_id", type=int)
@click.option(
    "-y", "--yes", is_flag=True, help="Skip confirmation prompt"
)
@click.pass_context
def delete(ctx: click.Context, task_id: int, yes: bool) -> None:
    """Delete a task permanently.

    TASK_ID: The ID of the task to delete

    This action cannot be undone! Use --yes to skip confirmation.

    Examples:
        todo delete 1       # Prompts for confirmation
        todo delete 2 -y    # Deletes without confirmation
    """
    repo = get_repository(ctx)

    try:
        task = repo.get(task_id)

        # Confirm deletion unless --yes flag is used
        if not yes:
            click.echo(f"About to delete task {task.id}: {task.title}")
            if not click.confirm("Are you sure?"):
                click.secho("Deletion cancelled.", fg="yellow")
                return

        repo.delete(task_id)
        click.secho(f"[OK] Task {task.id} deleted successfully!", fg="green")

    except KeyError as e:
        click.secho(f"[ERROR] {e}", fg="red", err=True)
        raise click.Abort()
