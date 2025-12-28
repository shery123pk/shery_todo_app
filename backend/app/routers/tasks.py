"""
Tasks Router
Handles task CRUD operations
Author: Sharmeen Asif
"""

from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.ext.asyncio import AsyncSession
from sqlmodel import select
from typing import Optional
from datetime import datetime

from app.database import get_async_session
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
async def get_tasks(
    completed: Optional[bool] = Query(None, description="Filter by completion status"),
    search: Optional[str] = Query(None, description="Search keyword in title or description"),
    priority: Optional[str] = Query(None, description="Filter by priority (low/medium/high)"),
    category: Optional[str] = Query(None, description="Filter by category"),
    tag: Optional[str] = Query(None, description="Filter by tag (any matching)"),
    sort_by: str = Query("created_at", description="Sort by field (created_at/due_date/priority/title)"),
    order: str = Query("desc", description="Sort order (asc/desc)"),
    limit: int = Query(100, ge=1, le=100, description="Number of tasks to return"),
    offset: int = Query(0, ge=0, description="Number of tasks to skip"),
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_async_session)
):
    """
    Get all tasks for the authenticated user.

    Supports advanced filtering, search, sorting, and pagination.

    Args:
        completed: Optional filter by completion status (true/false/null)
        search: Search keyword in title or description
        priority: Filter by priority level (low/medium/high)
        category: Filter by category
        tag: Filter by tag (any matching)
        sort_by: Sort by field (created_at/due_date/priority/title)
        order: Sort order (asc/desc)
        limit: Maximum number of tasks to return (1-100, default 100)
        offset: Number of tasks to skip (for pagination, default 0)
        current_user: Authenticated user (from dependency)
        db: Database session

    Returns:
        TaskListResponse: List of tasks with counts

    Raises:
        HTTPException 401: Not authenticated

    Example:
        GET /api/tasks?search=grocery&priority=medium&sort_by=due_date&order=asc
        Returns tasks matching "grocery" with medium priority, sorted by due date ascending
    """
    # Build base query for user's tasks
    query = select(Task).where(Task.user_id == current_user.id)

    # Apply completed filter if provided
    if completed is not None:
        query = query.where(Task.completed == completed)

    # Apply search filter (case-insensitive)
    if search:
        search_pattern = f"%{search.lower()}%"
        from sqlalchemy import or_, func
        query = query.where(
            or_(
                func.lower(Task.title).like(search_pattern),
                func.lower(Task.description).like(search_pattern)
            )
        )

    # Apply priority filter
    if priority:
        query = query.where(Task.priority == priority.lower())

    # Apply category filter
    if category:
        query = query.where(Task.category == category)

    # Apply tag filter (any matching tag)
    if tag:
        from sqlalchemy import any_
        query = query.where(Task.tags.any(tag))

    # Apply sorting
    sort_column = Task.created_at  # default
    if sort_by == "due_date":
        sort_column = Task.due_date
    elif sort_by == "priority":
        sort_column = Task.priority
    elif sort_by == "title":
        sort_column = Task.title

    if order.lower() == "asc":
        query = query.order_by(sort_column.asc())
    else:
        query = query.order_by(sort_column.desc())

    # Apply pagination
    query = query.offset(offset).limit(limit)

    # Execute query
    result = await db.execute(query)
    tasks = result.scalars().all()

    # Get counts for the user
    total_query = select(Task).where(Task.user_id == current_user.id)
    total_result = await db.execute(total_query)
    all_tasks = total_result.scalars().all()

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
async def get_task(
    task_id: str,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_async_session)
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
    task = await db.get(Task, task_id)

    # Return 404 if task doesn't exist or doesn't belong to user
    # Use 404 instead of 403 to prevent task ID enumeration
    if not task or task.user_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Task not found"
        )

    return task


@router.post("", response_model=TaskResponse, status_code=status.HTTP_201_CREATED)
async def create_task(
    task_data: TaskCreate,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_async_session)
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
    # Create new task
    new_task = Task(
        user_id=current_user.id,
        title=task_data.title,
        description=task_data.description,
        completed=False,
        priority=task_data.priority,
        tags=task_data.tags or [],
        category=task_data.category,
        due_date=task_data.due_date,
        is_recurring=task_data.is_recurring or False,
        recurrence_pattern=task_data.recurrence_pattern,
        created_at=datetime.utcnow(),
        updated_at=datetime.utcnow()
    )

    db.add(new_task)
    await db.commit()
    await db.refresh(new_task)

    return new_task


@router.patch("/{task_id}", response_model=TaskResponse)
async def update_task(
    task_id: str,
    task_data: TaskUpdate,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_async_session)
):
    """
    Update an existing task.

    Only updates fields that are provided in the request.
    Returns 404 if task doesn't exist or doesn't belong to the user.

    Args:
        task_id: UUID of the task
        task_data: TaskUpdate with optional fields to update
        current_user: Authenticated user (from dependency)
        db: Database session

    Returns:
        TaskResponse: Updated task data

    Raises:
        HTTPException 401: Not authenticated
        HTTPException 404: Task not found or unauthorized

    Example:
        PATCH /api/tasks/123e4567-e89b-12d3-a456-426614174000
        {
            "completed": true
        }

        Response (200):
        {
            "id": "123e4567-...",
            "completed": true,
            ...
        }
    """
    # Fetch task
    task = await db.get(Task, task_id)

    # Return 404 if task doesn't exist or doesn't belong to user
    if not task or task.user_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Task not found"
        )

    # Update provided fields
    update_data = task_data.model_dump(exclude_unset=True)

    # Check if marking recurring task as complete
    is_completing_recurring = (
        update_data.get("completed") is True and
        task.is_recurring and
        task.recurrence_pattern and
        task.due_date
    )

    for field, value in update_data.items():
        setattr(task, field, value)

    # Update timestamp
    task.updated_at = datetime.utcnow()

    db.add(task)

    # If completing a recurring task, create next occurrence
    if is_completing_recurring:
        from dateutil.relativedelta import relativedelta

        # Calculate next due date
        next_due_date = task.due_date
        if task.recurrence_pattern == "daily":
            next_due_date = task.due_date + relativedelta(days=1)
        elif task.recurrence_pattern == "weekly":
            next_due_date = task.due_date + relativedelta(weeks=1)
        elif task.recurrence_pattern == "monthly":
            next_due_date = task.due_date + relativedelta(months=1)

        # Create next occurrence
        next_task = Task(
            user_id=task.user_id,
            title=task.title,
            description=task.description,
            completed=False,
            priority=task.priority,
            tags=task.tags,
            category=task.category,
            due_date=next_due_date,
            is_recurring=True,
            recurrence_pattern=task.recurrence_pattern,
            parent_task_id=task.id,
            reminder_sent=False,
            created_at=datetime.utcnow(),
            updated_at=datetime.utcnow()
        )
        db.add(next_task)

    await db.commit()
    await db.refresh(task)

    return task


@router.delete("/{task_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_task(
    task_id: str,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_async_session)
):
    """
    Delete a task.

    Returns 404 if task doesn't exist or doesn't belong to the user.

    Args:
        task_id: UUID of the task
        current_user: Authenticated user (from dependency)
        db: Database session

    Returns:
        None (204 No Content)

    Raises:
        HTTPException 401: Not authenticated
        HTTPException 404: Task not found or unauthorized

    Example:
        DELETE /api/tasks/123e4567-e89b-12d3-a456-426614174000
        Response (204): No content
    """
    # Fetch task
    task = await db.get(Task, task_id)

    # Return 404 if task doesn't exist or doesn't belong to user
    if not task or task.user_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Task not found"
        )

    await db.delete(task)
    await db.commit()

    return None
