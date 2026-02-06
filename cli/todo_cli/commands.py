"""Professional CLI commands with ALL 10 features - Hackathon Version"""

from pathlib import Path
from datetime import datetime, timedelta

import click

from .models import Task
from .repository import InMemoryRepository


def get_repository(ctx: click.Context) -> InMemoryRepository:
    """Get or create repository instance from context."""
    if ctx.obj is None:
        ctx.obj = {}
    if "repo" not in ctx.obj:
        ctx.obj["repo"] = InMemoryRepository()
    return ctx.obj["repo"]


# Create the group
@click.group()
@click.pass_context
def cli(ctx: click.Context) -> None:
    """Professional Todo CLI - ALL 10 Features

    Basic Features:
      add, delete, update, list, complete

    Intermediate Features:
      priorities, tags, search, filter, sort

    Advanced Features:
      recurring tasks, due dates, reminders, stats dashboard
    """
    ctx.ensure_object(dict)


# Create add command
@click.command("add")
@click.pass_context
@click.argument("title")
@click.option("-d", "--description", default="", help="Task description")
@click.option("-p", "--priority", type=click.Choice(["low", "medium", "high"]), default="medium",
              help="Priority level (default: medium)")
@click.option("-t", "--tag", multiple=True, help="Add tags (can use multiple times)")
@click.option("--due", help="Due date (YYYY-MM-DD HH:MM or shortcuts like 'tomorrow', '2h')")
@click.option("--recurring", is_flag=True, help="Make this a recurring task")
@click.option("--pattern", type=click.Choice(["daily", "weekly", "monthly"]),
              help="Recurrence pattern (requires --recurring)")
def add_task(ctx, title, description, priority, tag, due, recurring, pattern):
    """Add a new task with professional features.

    Examples:
      todo add "Buy groceries"
      todo add "Team meeting" -p high -t work -t urgent
      todo add "Weekly report" --due "2025-01-10 14:00" --recurring --pattern weekly
      todo add "Call client" --due tomorrow -p high
    """
    repo = get_repository(ctx)

    # Parse due date shortcuts
    due_date = None
    if due:
        try:
            due_date = parse_due_date(due)
        except ValueError as e:
            click.secho(f"[ERROR] {e}", fg="red")
            raise click.Abort()

    # Validate recurring settings
    if recurring and not pattern:
        click.secho("[ERROR] --pattern required when using --recurring", fg="red")
        raise click.Abort()

    task = repo.add(
        title=title,
        description=description,
        priority=priority,
        tags=list(tag) if tag else [],
        due_date=due_date,
        recurring=recurring,
        recurrence_pattern=pattern if recurring else None,
    )

    priority_colors = {"high": "red", "medium": "yellow", "low": "green"}
    click.secho(f"[OK] Task #{task.id} added!", fg=priority_colors[priority], bold=True)
    click.echo(f"  Title: {task.title}")
    if description:
        click.echo(f"  Description: {description}")
    click.echo(f"  Priority: {priority.upper()}")
    if tag:
        click.echo(f"  Tags: {', '.join(tag)}")
    if due_date:
        click.echo(f"  Due: {due_date}")
    if recurring:
        click.echo(f"  Recurring: {pattern}")


# Create list command
@click.command("list")
@click.pass_context
@click.option("-q", "--query", help="Search keyword in title/description")
@click.option("-p", "--priority", type=click.Choice(["low", "medium", "high"]),
              help="Filter by priority")
@click.option("-t", "--tag", multiple=True, help="Filter by tags")
@click.option("-a", "--all", "show_all", is_flag=True, help="Show all tasks")
@click.option("-c", "--completed", "show_completed", is_flag=True, help="Show only completed")
@click.option("--overdue", is_flag=True, help="Show only overdue tasks")
@click.option("--sort", type=click.Choice(["id", "priority", "due_date", "title"]),
              default="id", help="Sort by field")
@click.option("--reverse", is_flag=True, help="Reverse sort order")
def list_tasks(ctx, query, priority, tag, show_all, show_completed, overdue, sort, reverse):
    """List tasks with advanced search, filter, and sort.

    Examples:
      todo list                           # Incomplete tasks
      todo list --all                     # All tasks
      todo list -q "meeting"              # Search for "meeting"
      todo list -p high --sort priority   # High priority, sorted
      todo list -t work -t urgent         # Tasks with work OR urgent tag
      todo list --overdue                 # Show overdue tasks
      todo list --sort due_date           # Sort by due date
    """
    repo = get_repository(ctx)

    # Determine completion filter
    completed_filter = None
    if show_completed:
        completed_filter = True
    elif not show_all:
        completed_filter = False

    # Search with filters
    tasks = repo.search(
        query=query,
        priority=priority,
        tags=list(tag) if tag else None,
        completed=completed_filter,
        overdue=overdue,
        sort_by=sort,
        reverse=reverse,
    )

    if not tasks:
        filter_desc = []
        if query:
            filter_desc.append(f"matching '{query}'")
        if priority:
            filter_desc.append(f"{priority} priority")
        if tag:
            filter_desc.append(f"tags: {', '.join(tag)}")
        if overdue:
            filter_desc.append("overdue")

        msg = "No tasks found"
        if filter_desc:
            msg += f" ({', '.join(filter_desc)})"
        click.secho(msg, fg="yellow")
        return

    # Print header
    click.secho("\n+-----+---------+----------+-----------------------------+------------------+", fg="cyan")
    click.secho("| ID  | Status  | Priority | Title                       | Due Date         |", fg="cyan", bold=True)
    click.secho("+-----+---------+----------+-----------------------------+------------------+", fg="cyan")

    # Print tasks
    for task in tasks:
        status = "[X]" if task.completed else "[ ]"

        # Color code priority
        priority_colors = {"high": "red", "medium": "yellow", "low": "green"}

        # Format title (truncate if too long)
        title = task.title[:25] + "..." if len(task.title) > 28 else task.title

        # Format due date
        due_str = ""
        if task.due_date:
            try:
                due_dt = datetime.fromisoformat(task.due_date)
                due_str = due_dt.strftime("%Y-%m-%d %H:%M")
                if task.is_overdue():
                    due_str = due_str + " !"
            except:
                due_str = task.due_date[:16]

        # Format tags
        tags_str = ""
        if task.tags:
            tags_str = " " + ",".join(f"#{t}" for t in task.tags[:2])

        # Color based on priority
        color = priority_colors.get(task.priority, "white")
        if task.completed:
            color = "bright_black"

        click.secho(
            f"| {task.id:3} | {status:7} | {task.priority:8} | {title:27}{tags_str[:2]:2} | {due_str:16} |",
            fg=color
        )

    click.secho("+-----+---------+----------+-----------------------------+------------------+\n", fg="cyan")

    # Summary
    completed_count = sum(1 for t in tasks if t.completed)
    click.echo(f"Total: {len(tasks)} tasks ({completed_count} completed)")


# Create stats command
@click.command("stats")
@click.pass_context
def stats(ctx):
    """Show task statistics dashboard.

    Displays overview of all tasks with breakdown by priority, tags, status.
    """
    repo = get_repository(ctx)
    stats_data = repo.get_stats()

    click.secho("\n" + "="*50, fg="cyan", bold=True)
    click.secho("        [STATS] TASK STATISTICS DASHBOARD", fg="cyan", bold=True)
    click.secho("="*50 + "\n", fg="cyan", bold=True)

    # Overall stats
    click.secho("Overall:", fg="white", bold=True)
    click.echo(f"   Total Tasks:      {stats_data['total']}")
    click.echo(f"   Completed:        {stats_data['completed']} ({stats_data['completed']*100//max(stats_data['total'],1)}%)")
    click.echo(f"   Incomplete:       {stats_data['incomplete']}")

    # Priority breakdown
    click.echo()
    click.secho("By Priority (Incomplete):", fg="white", bold=True)
    click.secho(f"   High:   {stats_data['by_priority']['high']}", fg="red")
    click.secho(f"   Medium: {stats_data['by_priority']['medium']}", fg="yellow")
    click.secho(f"   Low:    {stats_data['by_priority']['low']}", fg="green")

    # Special categories
    click.echo()
    click.secho("Special:", fg="white", bold=True)
    if stats_data['overdue'] > 0:
        click.secho(f"   Overdue:    {stats_data['overdue']}", fg="red", bold=True)
    else:
        click.echo(f"   Overdue:    0")
    click.echo(f"   Recurring:  {stats_data['recurring']}")

    # Tags
    if stats_data['by_tags']:
        click.echo()
        click.secho("Top Tags:", fg="white", bold=True)
        sorted_tags = sorted(stats_data['by_tags'].items(), key=lambda x: x[1], reverse=True)[:5]
        for tag, count in sorted_tags:
            click.echo(f"   #{tag}: {count}")

    click.secho("\n" + "="*50 + "\n", fg="cyan", bold=True)


# Create update command
@click.command("update")
@click.pass_context
@click.argument("task_id", type=int)
@click.option("-t", "--title", help="New title")
@click.option("-d", "--description", help="New description")
@click.option("-p", "--priority", type=click.Choice(["low", "medium", "high"]), help="New priority")
@click.option("--add-tag", "add_tags", multiple=True, help="Add tags")
@click.option("--due", help="New due date")
def update(ctx, task_id, title, description, priority, add_tags, due):
    """Update task fields.

    Examples:
      todo update 1 -t "New title"
      todo update 1 -p high --add-tag urgent
      todo update 1 --due "2025-01-15 10:00"
    """
    if not any([title, description, priority, add_tags, due]):
        click.secho("[ERROR] Provide at least one field to update", fg="red")
        raise click.Abort()

    repo = get_repository(ctx)

    try:
        task = repo.get(task_id)

        # Handle tags (add to existing)
        new_tags = None
        if add_tags:
            new_tags = list(set(task.tags + list(add_tags)))

        # Parse due date
        due_date = None
        if due:
            due_date = parse_due_date(due)

        updated = repo.update(
            task_id,
            title=title,
            description=description,
            priority=priority,
            tags=new_tags,
            due_date=due_date,
        )

        click.secho(f"[OK] Task #{task_id} updated!", fg="green", bold=True)
        click.echo(f"  Title: {updated.title}")
        if priority:
            click.echo(f"  Priority: {priority.upper()}")
        if add_tags:
            click.echo(f"  Tags: {', '.join(updated.tags)}")

    except (KeyError, ValueError) as e:
        click.secho(f"[ERROR] {e}", fg="red")
        raise click.Abort()


# Create complete command
@click.command("complete")
@click.pass_context
@click.argument("task_id", type=int)
def complete(ctx, task_id):
    """Mark task as complete (auto-creates recurring tasks)."""
    repo = get_repository(ctx)

    try:
        task = repo.complete(task_id)
        click.secho(f"[OK] Task #{task_id} completed!", fg="green", bold=True)
        click.echo(f"  {task.title}")

    except KeyError as e:
        click.secho(f"[ERROR] {e}", fg="red")
        raise click.Abort()


# Create delete command
@click.command("delete")
@click.pass_context
@click.argument("task_id", type=int)
@click.option("-y", "--yes", is_flag=True, help="Skip confirmation")
def delete(ctx, task_id, yes):
    """Delete a task permanently."""
    repo = get_repository(ctx)

    try:
        task = repo.get(task_id)

        if not yes:
            click.echo(f"Delete task #{task.id}: {task.title}")
            if not click.confirm("Are you sure?"):
                click.secho("Cancelled", fg="yellow")
                return

        repo.delete(task_id)
        click.secho(f"[OK] Task #{task_id} deleted!", fg="green")

    except KeyError as e:
        click.secho(f"[ERROR] {e}", fg="red")
        raise click.Abort()


# Add commands to group
cli.add_command(add_task)
cli.add_command(list_tasks)
cli.add_command(stats)
cli.add_command(update)
cli.add_command(complete)
cli.add_command(delete)


def parse_due_date(due_str: str) -> str:
    """Parse due date string with shortcuts.

    Supports:
    - Full ISO: "2025-01-10 14:00"
    - Shortcuts: "tomorrow", "today", "monday", etc.
    - Relative: "2h", "3d", "1w"
    """
    due_str = due_str.lower().strip()
    now = datetime.now()

    # Shortcuts
    if due_str == "today":
        return now.replace(hour=23, minute=59, second=0, microsecond=0).isoformat()
    elif due_str == "tomorrow":
        return (now + timedelta(days=1)).replace(hour=23, minute=59, second=0, microsecond=0).isoformat()
    elif due_str in ["monday", "mon"]:
        days_ahead = (0 - now.weekday()) % 7
        if days_ahead == 0:
            days_ahead = 7
        return (now + timedelta(days=days_ahead)).replace(hour=23, minute=59, second=0, microsecond=0).isoformat()
    elif due_str in ["tuesday", "tue"]:
        days_ahead = (1 - now.weekday()) % 7
        if days_ahead == 0:
            days_ahead = 7
        return (now + timedelta(days=days_ahead)).replace(hour=23, minute=59, second=0, microsecond=0).isoformat()

    # Relative time (e.g., "2h", "3d")
    if len(due_str) > 1 and due_str[-1] in ['h', 'd', 'w']:
        try:
            amount = int(due_str[:-1])
            unit = due_str[-1]
            if unit == 'h':
                return (now + timedelta(hours=amount)).isoformat()
            elif unit == 'd':
                return (now + timedelta(days=amount)).isoformat()
            elif unit == 'w':
                return (now + timedelta(weeks=amount)).isoformat()
        except ValueError:
            pass

    # Try to parse as ISO format
    try:
        # If it's just a date, add time
        if len(due_str) == 10:  # YYYY-MM-DD
            due_str += " 23:59"
        datetime.fromisoformat(due_str)  # Validate
        return due_str
    except ValueError:
        raise ValueError(f"Invalid due date format: {due_str}")
