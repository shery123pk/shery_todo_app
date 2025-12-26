"""
Task Pydantic Schemas
Request/Response models for task endpoints
Author: Sharmeen Asif
"""

from pydantic import BaseModel, Field
from uuid import UUID
from datetime import datetime
from typing import Optional, List


class TaskCreate(BaseModel):
    """
    Request model for creating a new task.

    Attributes:
        title: Task title (required, max 200 chars)
        description: Optional detailed description
        priority: Optional priority level (low/medium/high)
        tags: Optional list of tags
        category: Optional category string
    """

    title: str = Field(..., min_length=1, max_length=200, description="Task title")
    description: Optional[str] = Field(None, description="Task description")
    priority: Optional[str] = Field(None, max_length=10, description="Priority (low/medium/high)")
    tags: Optional[List[str]] = Field(default_factory=list, description="Tags for categorization")
    category: Optional[str] = Field(None, max_length=50, description="Category")

    class Config:
        json_schema_extra = {
            "example": {
                "title": "Buy groceries",
                "description": "Milk, eggs, bread",
                "priority": "medium",
                "tags": ["shopping", "urgent"],
                "category": "personal"
            }
        }


class TaskUpdate(BaseModel):
    """
    Request model for updating an existing task.

    All fields are optional - only provided fields will be updated.

    Attributes:
        title: New task title
        description: New description
        completed: New completion status
        priority: New priority level
        tags: New tags list
        category: New category
    """

    title: Optional[str] = Field(None, min_length=1, max_length=200)
    description: Optional[str] = None
    completed: Optional[bool] = None
    priority: Optional[str] = Field(None, max_length=10)
    tags: Optional[List[str]] = None
    category: Optional[str] = Field(None, max_length=50)

    class Config:
        json_schema_extra = {
            "example": {
                "title": "Buy groceries and cook dinner",
                "completed": True,
                "priority": "high"
            }
        }


class TaskResponse(BaseModel):
    """
    Response model for task data.

    Attributes:
        id: Task UUID
        user_id: Owner's UUID
        title: Task title
        description: Task description
        completed: Completion status
        priority: Priority level
        tags: Tags list
        category: Category
        created_at: Creation timestamp
        updated_at: Last update timestamp
    """

    id: UUID
    user_id: UUID
    title: str
    description: Optional[str]
    completed: bool
    priority: Optional[str]
    tags: List[str]
    category: Optional[str]
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True
        json_schema_extra = {
            "example": {
                "id": "123e4567-e89b-12d3-a456-426614174000",
                "user_id": "550e8400-e29b-41d4-a716-446655440000",
                "title": "Buy groceries",
                "description": "Milk, eggs, bread",
                "completed": False,
                "priority": "medium",
                "tags": ["shopping", "urgent"],
                "category": "personal",
                "created_at": "2025-12-26T09:00:00Z",
                "updated_at": "2025-12-26T09:00:00Z"
            }
        }


class TaskListResponse(BaseModel):
    """
    Response model for task list endpoint.

    Attributes:
        tasks: List of tasks
        total: Total number of tasks
        completed: Number of completed tasks
        incomplete: Number of incomplete tasks
    """

    tasks: List[TaskResponse]
    total: int
    completed: int
    incomplete: int

    class Config:
        json_schema_extra = {
            "example": {
                "tasks": [
                    {
                        "id": "123e4567-e89b-12d3-a456-426614174000",
                        "user_id": "550e8400-e29b-41d4-a716-446655440000",
                        "title": "Buy groceries",
                        "description": "Milk, eggs, bread",
                        "completed": False,
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
        }
