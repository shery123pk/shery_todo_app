"""Interactive menu-driven CLI for Todo App"""

import sys
from datetime import datetime, timedelta

import click

from .models import Task
from .repository import InMemoryRepository

# ANSI colors for Windows
RED = "\033[91m"
GREEN = "\033[92m"
YELLOW = "\033[93m"
CYAN = "\033[96m"
BOLD = "\033[1m"
RESET = "\033[0m"

# Windows compatibility
try:
    import ctypes
    kernel32 = ctypes.windll.kernel32
    kernel32.SetConsoleMode(kernel32.GetStdHandle(-11), 7)
except:
    pass


def print_header(title: str) -> None:
    """Print colored header."""
    print(f"\n{CYAN}{BOLD}{'=' * 50}{RESET}")
    print(f"{CYAN}{BOLD}        {title}{RESET}")
    print(f"{CYAN}{BOLD}{'=' * 50}{RESET}\n")


def print_menu() -> None:
    """Print main menu."""
    print(f"\n{BOLD}╔══════════════════════════════════════════╗{RESET}")
    print(f"{BOLD}║           TODO APP - MAIN MENU           ║{RESET}")
    print(f"{BOLD}╠══════════════════════════════════════════╣{RESET}")
    print(f"{BOLD}║  {GREEN}1{RESET}. Add New Task                      ║{RESET}")
    print(f"{BOLD}║  {GREEN}2{RESET}. View All Tasks                   ║{RESET}")
    print(f"{BOLD}║  {GREEN}3{RESET}. Search/Filter Tasks              ║{RESET}")
    print(f"{BOLD}║  {GREEN}4{RESET}. Complete a Task                  ║{RESET}")
    print(f"{BOLD}║  {GREEN}5{RESET}. Update a Task                    ║{RESET}")
    print(f"{BOLD}║  {GREEN}6{RESET}. Delete a Task                    ║{RESET}")
    print(f"{BOLD}║  {GREEN}7{RESET}. View Statistics                  ║{RESET}")
    print(f"{BOLD}║  {GREEN}8{RESET}. Overdue Tasks                    ║{RESET}")
    print(f"{BOLD}║  {GREEN}0{RESET}. Exit                             ║{RESET}")
    print(f"{BOLD}╚══════════════════════════════════════════╝{RESET}")
    print(f"\n{BOLD}Enter your choice (0-8): {RESET}", end="")


def print_tasks(tasks: list, title: str = "TASKS") -> None:
    """Print tasks in a formatted table."""
    if not tasks:
        print(f"\n{YELLOW}No tasks found{RESET}")
        return

    print_header(f"[{title}]")
    print(f"{CYAN}+-----+---------+----------+-----------------------------+{RESET}")
    print(f"{CYAN}| ID  | Status  | Priority | Title                       |{RESET}")
    print(f"{CYAN}+-----+---------+----------+-----------------------------+{RESET}")

    priority_colors = {"high": RED, "medium": YELLOW, "low": GREEN}

    for task in tasks:
        status = f"{GREEN}[X]{RESET}" if task.completed else f"{YELLOW}[ ]{RESET}"
        color = priority_colors.get(task.priority, "")
        if task.completed:
            color = "\033[90m"  # dim

        # Format title
        title = task.title[:25] + "..." if len(task.title) > 28 else task.title

        # Format tags
        tags_str = ""
        if task.tags:
            tags_str = " " + ",".join(f"#{t}" for t in task.tags[:2])
            if len(tags_str) > 2:
                tags_str = tags_str[:2]

        print(f"| {task.id:3} | {status} | {task.priority:8} | {color}{title:27}{RESET}{tags_str[:2]:2} |")

    print(f"{CYAN}+-----+---------+----------+-----------------------------+{RESET}")
    completed = sum(1 for t in tasks if t.completed)
    print(f"Total: {len(tasks)} tasks ({completed} completed)")


def get_choice() -> int:
    """Get user input choice."""
    try:
        return int(input().strip())
    except (ValueError, EOFError):
        return -1


def add_task(repo: InMemoryRepository) -> None:
    """Add a new task interactively."""
    print_header("[ADD NEW TASK]")

    title = input("Enter task title: ").strip()
    if not title:
        print(f"{RED}Title cannot be empty!{RESET}")
        return

    description = input("Enter description (optional): ").strip()

    print("\nPriority: 1=Low, 2=Medium, 3=High")
    priority_map = {"1": "low", "2": "medium", "3": "high"}
    priority_choice = input("Choose priority (1-3) [2]: ").strip() or "2"
    priority = priority_map.get(priority_choice, "medium")

    tags_input = input("Enter tags (comma separated, e.g., work,urgent): ").strip()
    tags = [t.strip() for t in tags_input.split(",") if t.strip()]

    print("\nDue date: 'today', 'tomorrow', '2d', '1w', or date like '2025-01-15'")
    due = input("Enter due date (optional): ").strip() or None

    print("\nRecurring: 1=Daily, 2=Weekly, 3=Monthly")
    recurring_choice = input("Make recurring? (1-3 or Enter for none): ").strip()
    recurring = recurring_choice in ["1", "2", "3"]
    pattern_map = {"1": "daily", "2": "weekly", "3": "monthly"}
    recurrence_pattern = pattern_map.get(recurring_choice) if recurring else None

    # Parse due date
    due_date = None
    if due:
        try:
            from .commands import parse_due_date
            due_date = parse_due_date(due)
        except:
            due_date = None

    task = repo.add(
        title=title,
        description=description,
        priority=priority,
        tags=tags,
        due_date=due_date,
        recurring=recurring,
        recurrence_pattern=recurrence_pattern,
    )

    print(f"\n{GREEN}{BOLD}[OK] Task #{task.id} added successfully!{RESET}")


def view_tasks(repo: InMemoryRepository) -> None:
    """View all tasks - simple, no extra questions."""
    tasks = repo.list_all()
    print_tasks(tasks, "ALL TASKS")


def search_tasks(repo: InMemoryRepository) -> None:
    """Search and filter tasks."""
    print_header("[SEARCH/FILTER TASKS]")

    print("1. Search by keyword")
    print("2. Filter by priority")
    print("3. Filter by tag")
    print("4. Show completed tasks")
    print("5. Show incomplete tasks")
    choice = input("Choose search type (1-5): ").strip()

    query = None
    priority = None
    tags = None
    completed = None

    if choice == "1":
        query = input("Enter search keyword: ").strip()
    elif choice == "2":
        print("Priority: 1=Low, 2=Medium, 3=High")
        p = input("Choose: ").strip()
        priority = {"1": "low", "2": "medium", "3": "high"}.get(p)
    elif choice == "3":
        tag = input("Enter tag to filter: ").strip()
        tags = [tag]
    elif choice == "4":
        completed = True
    elif choice == "5":
        completed = False

    tasks = repo.search(query=query, priority=priority, tags=tags, completed=completed)
    print_tasks(tasks, "SEARCH RESULTS")


def complete_task(repo: InMemoryRepository) -> None:
    """Complete a task."""
    print_header("[COMPLETE TASK]")

    incomplete = repo.search(completed=False)
    if not incomplete:
        print(f"{YELLOW}No incomplete tasks!{RESET}")
        return

    print_tasks(incomplete, "INCOMPLETE TASKS")

    try:
        task_id = int(input("\nEnter task ID to complete: ").strip())
        task = repo.get(task_id)
        if task.completed:
            print(f"{YELLOW}Task #{task_id} is already completed!{RESET}")
        else:
            repo.complete(task_id)
            print(f"\n{GREEN}{BOLD}[OK] Task #{task_id} completed!{RESET}")
    except (ValueError, KeyError):
        print(f"{RED}Invalid task ID!{RESET}")


def update_task(repo: InMemoryRepository) -> None:
    """Update a task."""
    print_header("[UPDATE TASK]")

    tasks = repo.list_all()
    if not tasks:
        print(f"{YELLOW}No tasks to update!{RESET}")
        return

    print_tasks(tasks, "ALL TASKS")

    try:
        task_id = int(input("\nEnter task ID to update: ").strip())
        task = repo.get(task_id)

        print(f"\n{BOLD}Current: {task.title} (Priority: {task.priority}){RESET}")
        print("Leave field empty to keep current value.")

        # Title
        new_title = input("New title: ").strip()
        if not new_title:
            new_title = None

        # Description
        new_desc = input("New description: ").strip()
        if not new_desc:
            new_desc = None

        # Priority
        print("Priority: 1=Low, 2=Medium, 3=High")
        p = input("New priority: ").strip()
        new_priority = {"1": "low", "2": "medium", "3": "high"}.get(p)

        # Due date
        new_due = input("New due date (today/tomorrow/date): ").strip()
        due_date = None
        if new_due:
            try:
                from .commands import parse_due_date
                due_date = parse_due_date(new_due)
            except:
                pass

        # Add tags
        add_tag = input("Add tag: ").strip()
        new_tags = None
        if add_tag:
            new_tags = list(set(task.tags + [add_tag]))

        repo.update(task_id, title=new_title, description=new_desc,
                    priority=new_priority, due_date=due_date, tags=new_tags)
        print(f"\n{GREEN}{BOLD}[OK] Task #{task_id} updated!{RESET}")

    except (ValueError, KeyError):
        print(f"{RED}Invalid task ID!{RESET}")


def delete_task(repo: InMemoryRepository) -> None:
    """Delete a task."""
    print_header("[DELETE TASK]")

    tasks = repo.list_all()
    if not tasks:
        print(f"{YELLOW}No tasks to delete!{RESET}")
        return

    print_tasks(tasks, "ALL TASKS")

    try:
        task_id = int(input("\nEnter task ID to delete: ").strip())
        task = repo.get(task_id)

        confirm = input(f"Delete '{task.title}'? (y/n): ").strip().lower()
        if confirm == "y":
            repo.delete(task_id)
            print(f"\n{GREEN}{BOLD}[OK] Task #{task_id} deleted!{RESET}")
        else:
            print("Cancelled.")
    except (ValueError, KeyError):
        print(f"{RED}Invalid task ID!{RESET}")


def view_stats(repo: InMemoryRepository) -> None:
    """View statistics dashboard."""
    stats = repo.get_stats()

    print_header("[STATISTICS DASHBOARD]")

    print(f"{BOLD}Overall:{RESET}")
    print(f"   Total Tasks:      {stats['total']}")
    print(f"   Completed:        {stats['completed']} ({stats['completed']*100//max(stats['total'],1)}%)")
    print(f"   Incomplete:       {stats['incomplete']}")

    print(f"\n{BOLD}By Priority (Incomplete):{RESET}")
    print(f"   {RED}High:   {stats['by_priority']['high']}{RESET}")
    print(f"   {YELLOW}Medium: {stats['by_priority']['medium']}{RESET}")
    print(f"   {GREEN}Low:    {stats['by_priority']['low']}{RESET}")

    print(f"\n{BOLD}Special:{RESET}")
    if stats['overdue'] > 0:
        print(f"   {RED}Overdue:    {stats['overdue']}{RESET}")
    else:
        print(f"   Overdue:    0")
    print(f"   Recurring:  {stats['recurring']}")

    if stats['by_tags']:
        print(f"\n{BOLD}Top Tags:{RESET}")
        sorted_tags = sorted(stats['by_tags'].items(), key=lambda x: x[1], reverse=True)[:5]
        for tag, count in sorted_tags:
            print(f"   #{tag}: {count}")


def view_overdue(repo: InMemoryRepository) -> None:
    """View overdue tasks."""
    tasks = repo.search(overdue=True)
    print_tasks(tasks, "OVERDUE TASKS")


def main() -> None:
    """Main interactive loop."""
    repo = InMemoryRepository()

    print(f"\n{GREEN}{BOLD}")
    print(r"""
   _______  _        _        _______  _______  _______
  (  ____ )( \      ( \      (  ____ \(  ___  )(  ____ )
  | (    )|| (      | |      | (    \/| (   ) || (    )|
  | (____)|| |      | |      | |      | |   | || (____)|
  |  _____)| |      | |      | |      | |   | ||  _____)
  | (      | |      | |      | |      | |   | || (
  | )      | (____/\| (____/\| (____/\| (___) || )
  |/       (______/(______/(_______/(_______)|/
    """)
    print(f"{RESET}")
    print(f"{CYAN}{BOLD}       Professional Todo CLI - Interactive Mode{RESET}")
    print(f"{CYAN}{BOLD}       Type '0' to exit anytime{RESET}\n")

    while True:
        print_menu()
        choice = get_choice()

        if choice == 0:
            print(f"\n{GREEN}Goodbye!{RESET}\n")
            break

        actions = {
            1: add_task,
            2: view_tasks,
            3: search_tasks,
            4: complete_task,
            5: update_task,
            6: delete_task,
            7: view_stats,
            8: view_overdue,
        }

        action = actions.get(choice)
        if action:
            action(repo)
        else:
            print(f"\n{RED}Invalid choice! Please try again.{RESET}")


if __name__ == "__main__":
    main()
