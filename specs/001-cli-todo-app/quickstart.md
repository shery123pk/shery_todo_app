# Quickstart Guide: Phase 1 CLI Todo App

**Feature**: 001-cli-todo-app
**Date**: 2025-12-26
**Audience**: End users, developers, testers

## Overview

This guide helps you quickly set up and start using the Phase 1 CLI Todo App. By the end of this guide, you'll be managing your daily tasks from the command line.

**What you'll learn**:
- How to install and run the app
- Basic task management (add, list, complete, update, delete)
- Data persistence and recovery

**Time required**: 5 minutes

## Prerequisites

- Python 3.13 or higher installed
- Command-line terminal access (Windows CMD/PowerShell, macOS/Linux Terminal)
- UV package manager (optional but recommended)

**Check your Python version**:
```bash
python --version
# Should show: Python 3.13.0 or higher
```

## Installation

### Option 1: Using UV (Recommended - Fast!)

```bash
# 1. Install UV (if not already installed)
curl -LsSf https://astral.sh/uv/install.sh | sh

# 2. Clone the repository
git clone <repo-url>
cd hackathon-todo

# 3. Create virtual environment and install
uv venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate
uv pip install -e .

# 4. Run the app
python -m todo_cli.main
```

### Option 2: Using pip (Standard)

```bash
# 1. Clone the repository
git clone <repo-url>
cd hackathon-todo

# 2. Create virtual environment
python -m venv .venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate

# 3. Install the app
pip install -e .

# 4. Run the app
python -m todo_cli.main
```

## Quick Start: Your First Tasks

### 1. Launch the App

```bash
python -m todo_cli.main
```

You'll see:
```
Welcome to Todo CLI! Type 'help' for available commands.
>
```

### 2. Add Your First Task

```
> add "Buy groceries"
Task 1 created: Buy groceries
```

Add a task with more details:
```
> add "Call dentist" --desc "Schedule annual checkup for next week"
Task 2 created: Call dentist
```

### 3. View Your Tasks

```
> list
ID  Status  Title              Description
──────────────────────────────────────────────────────────────
1   [ ]     Buy groceries
2   [ ]     Call dentist       Schedule annual checkup for next week

2 tasks total (0 completed, 2 pending)
```

### 4. Complete a Task

```
> complete 1
Task 1 marked as complete: Buy groceries
```

Check the updated list:
```
> list
ID  Status  Title              Description
──────────────────────────────────────────────────────────────
1   [✓]     Buy groceries
2   [ ]     Call dentist       Schedule annual checkup for next week

2 tasks total (1 completed, 1 pending)
```

### 5. Update a Task

Change the title:
```
> update 2 --title "Call dentist for appointment"
Task 2 updated.
```

Change the description:
```
> update 2 --desc "Schedule for next Tuesday if possible"
Task 2 updated.
```

Update both at once:
```
> update 2 --title "Dentist appointment" --desc "Tuesday 2pm"
Task 2 updated.
```

### 6. Delete a Task

```
> delete 1
Task 1 deleted: Buy groceries
```

### 7. Exit the App

```
> exit
Tasks saved. Goodbye!
```

Your tasks are automatically saved to `tasks.json` in the current directory.

## Common Workflows

### Daily Task Management

**Morning routine** (plan your day):
```
> add "Review emails"
> add "Team standup meeting" --desc "9:00 AM daily sync"
> add "Work on project report" --desc "Due Friday"
> list
```

**Throughout the day** (update progress):
```
> complete 1  # Finished reviewing emails
> complete 2  # Standup done
> list        # See what's left
```

**End of day** (review and plan tomorrow):
```
> add "Prepare presentation slides" --desc "For Monday's client meeting"
> list        # Review tomorrow's tasks
> exit        # Save and quit
```

### Handling Mistakes

**Wrong title?**
```
> add "Buy milk"
Task 3 created: Buy milk

> update 3 --title "Buy milk and eggs"
Task 3 updated.
```

**Added wrong task?**
```
> add "Duplicate task"
Task 4 created: Duplicate task

> delete 4
Task 4 deleted: Duplicate task
```

**Need more details?**
```
> add "Meeting"
Task 5 created: Meeting

> update 5 --desc "Client review meeting at 3pm in conference room B"
Task 5 updated.
```

## Data Persistence

### Where is my data stored?

Your tasks are saved in `tasks.json` in the directory where you run the app.

**View the file** (outside the app):
```bash
cat tasks.json
```

**Example content**:
```json
{
  "next_id": 4,
  "tasks": [
    {
      "id": 1,
      "title": "Buy groceries",
      "description": "",
      "completed": true
    },
    {
      "id": 2,
      "title": "Call dentist",
      "description": "Schedule annual checkup",
      "completed": false
    }
  ]
}
```

### Backup your data

```bash
cp tasks.json tasks.backup.json
```

### Reset the app

```bash
rm tasks.json
# Next launch will start with empty task list
```

### Move tasks to another computer

```bash
# On old computer
cp tasks.json ~/Dropbox/my-tasks.json

# On new computer
cp ~/Dropbox/my-tasks.json tasks.json
python -m todo_cli.main
```

## Tips & Tricks

### 1. Use Short, Actionable Titles

✅ **Good**: `"Review Q4 budget proposal"`
❌ **Bad**: `"I need to look at the budget thing sometime"`

### 2. Add Context in Descriptions

```
> add "Submit expense report" --desc "For December travel: conference in NYC, receipts in folder"
```

### 3. Review Your List Regularly

```
> list  # Quick check of what's pending
```

### 4. Keep Your List Clean

Complete or delete old tasks:
```
> complete 5  # Finished task
> delete 7    # No longer relevant
```

### 5. Use Ctrl+C for Quick Exit

Press `Ctrl+C` instead of typing `exit` - your data still saves!

## Troubleshooting

### Problem: "Command not found" error

**Solution**: Make sure you're in the virtual environment:
```bash
source .venv/bin/activate  # Linux/Mac
.venv\Scripts\activate     # Windows
```

### Problem: "Python 3.13 not found"

**Solution**: Install Python 3.13+ from python.org or use pyenv:
```bash
pyenv install 3.13
pyenv local 3.13
```

### Problem: "Could not load tasks" warning on startup

**Possible causes**:
- `tasks.json` is corrupted (invalid JSON syntax)
- File permissions issue

**Solution**:
- App will start with empty list (data preserved in `tasks.json.backup` if created)
- Fix the JSON manually or delete the file to start fresh

### Problem: "Cannot save tasks" warning

**Possible causes**:
- Disk full
- No write permissions
- Directory is read-only

**Solution**:
- Free up disk space
- Check directory permissions: `ls -la tasks.json`
- Run from a writable directory
- Your tasks remain in memory until you can save

### Problem: Tasks disappeared after crash

**Solution**: Check for backup files:
```bash
ls -la tasks*.json
# Look for tasks.json.backup or tasks.tmp
```

## Getting Help

### In-App Help

```
> help
Available commands:
  add, list, complete, update, delete, help, exit

> help add
Usage: add <title> [--desc <description>]
...
```

### Command Quick Reference

| Command | Example | What it does |
|---------|---------|--------------|
| `add` | `add "Task title" --desc "Details"` | Create new task |
| `list` | `list` | Show all tasks |
| `complete` | `complete 3` | Mark task 3 as done |
| `update` | `update 3 --title "New title"` | Change task 3 |
| `delete` | `delete 3` | Remove task 3 |
| `help` | `help add` | Show command help |
| `exit` | `exit` | Save and quit |

## Next Steps

- **Phase 2**: Web interface and REST API (coming soon)
- **Phase 3**: AI-powered natural language commands
- **Phase 4**: Cloud sync and mobile apps
- **Phase 5**: Team collaboration features

---

**Questions or issues?** This is Phase 1 (CLI foundation). Refer to the spec.md for full feature details.
