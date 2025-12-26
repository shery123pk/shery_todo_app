"""
Task SQLModel Entity
Represents todo tasks with user ownership
Author: Sharmeen Asif
"""

from sqlmodel import SQLModel, Field, Column
from sqlalchemy import Text, ARRAY, String
from uuid import UUID, uuid4
from datetime import datetime
from typing import Optional, List


class Task(SQLModel, table=True):
    """
    Task entity for todo items with user isolation.

    Attributes:
        id: UUID primary key
        user_id: Foreign key to users table (CASCADE delete)
        title: Task title (max 200 chars)
        description: Optional detailed description
        completed: Completion status (indexed for filtering)
        priority: Optional priority level (low/medium/high)
        tags: Array of string tags for categorization
        category: Optional category string
        created_at: Timestamp of task creation (indexed for sorting)
        updated_at: Timestamp of last update
    """

    __tablename__ = "tasks"

    id: UUID = Field(default_factory=uuid4, primary_key=True)
    user_id: UUID = Field(
        foreign_key="users.id",
        index=True,
        nullable=False,
        ondelete="CASCADE"
    )
    title: str = Field(max_length=200, nullable=False)
    description: Optional[str] = Field(default=None, sa_column=Column(Text))
    completed: bool = Field(default=False, index=True, nullable=False)
    priority: Optional[str] = Field(default=None, max_length=10)
    tags: List[str] = Field(default_factory=list, sa_column=Column(ARRAY(String)))
    category: Optional[str] = Field(default=None, max_length=50)
    created_at: datetime = Field(
        default_factory=datetime.utcnow,
        index=True,
        nullable=False
    )
    updated_at: datetime = Field(
        default_factory=datetime.utcnow,
        nullable=False,
        sa_column_kwargs={"onupdate": datetime.utcnow}
    )

    class Config:
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
