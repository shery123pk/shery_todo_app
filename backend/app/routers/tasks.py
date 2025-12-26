"""
Tasks Router
Handles task CRUD operations
Author: Sharmeen Asif
"""

from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlmodel import Session, select
from typing import Optional

from app.database import get_session
from app.models.user import User
from app.models.task import Task
from app.schemas.task import (
    TaskCreate,
    TaskUpdate,
    TaskResponse,
    TaskListResponse
)
from app.dependencies import get_current_user


router = APIRouter()


@router.get("", response_model=TaskListResponse)
def get_tasks(
    completed: Optional[bool] = Query(None, description="Filter by completion status"),
    limit: int = Query(100, ge=1, le=100, description="Number of tasks to return"),
    offset: int = Query(0, ge=0, description="Number of tasks to skip"),
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_session)
):
    """
    Get all tasks for the authenticated user.

    Returns tasks sorted by created_at DESC (newest first).
    Supports filtering by completion status and pagination.

    Args:
        completed: Optional filter by completion status (true/false/null)
        limit: Maximum number of tasks to return (1-100, default 100)
        offset: Number of tasks to skip (for pagination, default 0)
        current_user: Authenticated user (from dependency)
        db: Database session

    Returns:
        TaskListResponse: List of tasks with counts

    Raises:
        HTTPException 401: Not authenticated

    Example:
        GET /api/tasks
        Response (200):
        {
            "tasks": [
                {
                    "id": "123e4567-...",
                    "user_id": "550e8400-...",
                    "title": "Buy groceries",
                    "description": "Milk, eggs, bread",
                    "completed": false,
                    "priority": "medium",
                    "tags": ["shopping"],
                    "category": "personal",
                    "created_at": "2025-12-26T09:00:00Z",
                    "updated_at": "2025-12-26T09:00:00Z"
                }
            ],
            "total": 15,
            "completed": 5,
            "incomplete": 10
        }

        GET /api/tasks?completed=false&limit=10&offset=0
        Returns first 10 incomplete tasks
    """
    # Build base query for user's tasks
    query = select(Task).where(Task.user_id == current_user.id)

    # Apply completed filter if provided
    if completed is not None:
        query = query.where(Task.completed == completed)

    # Sort by created_at DESC (newest first)
    query = query.order_by(Task.created_at.desc())

    # Apply pagination
    query = query.offset(offset).limit(limit)

    # Execute query
    tasks = db.exec(query).all()

    # Get counts for the user
    total_query = select(Task).where(Task.user_id == current_user.id)
    all_tasks = db.exec(total_query).all()

    total = len(all_tasks)
    completed_count = sum(1 for task in all_tasks if task.completed)
    incomplete_count = total - completed_count

    return TaskListResponse(
        tasks=tasks,
        total=total,
        completed=completed_count,
        incomplete=incomplete_count
    )


@router.get("/{task_id}", response_model=TaskResponse)
def get_task(
    task_id: str,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_session)
):
    """
    Get a specific task by ID.

    Returns 404 if task doesn't exist or doesn't belong to the user.

    Args:
        task_id: UUID of the task
        current_user: Authenticated user (from dependency)
        db: Database session

    Returns:
        TaskResponse: Task data

    Raises:
        HTTPException 401: Not authenticated
        HTTPException 404: Task not found or unauthorized

    Example:
        GET /api/tasks/123e4567-e89b-12d3-a456-426614174000
        Response (200):
        {
            "id": "123e4567-...",
            "title": "Buy groceries",
            ...
        }
    """
    # Fetch task
    task = db.get(Task, task_id)

    # Return 404 if task doesn't exist or doesn't belong to user
    # Use 404 instead of 403 to prevent task ID enumeration
    if not task or task.user_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Task not found"
        )

    return task


@router.post("", response_model=TaskResponse, status_code=status.HTTP_201_CREATED)
def create_task(
    task_data: TaskCreate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_session)
):
    """
    Create a new task for the authenticated user.

    Args:
        task_data: TaskCreate with title, description, priority, tags, category
        current_user: Authenticated user (from dependency)
        db: Database session

    Returns:
        TaskResponse: Created task data

    Raises:
        HTTPException 401: Not authenticated
        HTTPException 400: Invalid input data

    Example:
        POST /api/tasks
        {
            "title": "Buy groceries",
            "description": "Milk, eggs, bread",
            "priority": "medium",
            "tags": ["shopping"],
            "category": "personal"
        }

        Response (201):
        {
            "id": "123e4567-...",
            "user_id": "550e8400-...",
            "title": "Buy groceries",
            "description": "Milk, eggs, bread",
            "completed": false,
            "priority": "medium",
            "tags": ["shopping"],
            "category": "personal",
            "created_at": "2025-12-26T10:00:00Z",
            "updated_at": "2025-12-26T10:00:00Z"
        }
    """
    from datetime import datetime

    # Create new task
    new_task = Task(
        user_id=current_user.id,
        title=task_data.title,
        description=task_data.description,
        completed=False,
        priority=task_data.priority,
        tags=task_data.tags or [],
        category=task_data.category,
        created_at=datetime.utcnow(),
        updated_at=datetime.utcnow()
    )

    db.add(new_task)
    db.commit()
    db.refresh(new_task)

    return new_task
