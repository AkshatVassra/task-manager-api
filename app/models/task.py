import uuid
from datetime import datetime, timezone
from enum import Enum
from typing import Optional
from pydantic import BaseModel, Field


class TaskStatus(str, Enum):
    PENDING = "pending"
    IN_PROGRESS = "in_progress"
    COMPLETED = "completed"


class TaskBase(BaseModel):
    """Base schema for task attributes."""
    title: str = Field(
        ...,
        min_length=1,
        max_length=100,
        description="Title of the task (must not be empty, max 100 characters)",
        examples=["Complete backend assignment"]
    )
    description: Optional[str] = Field(
        None,
        max_length=500,
        description="Optional detailed description (max 500 characters)",
        examples=["Build and test FastAPI Task Management API with validation"]
    )
    status: TaskStatus = Field(
        default=TaskStatus.PENDING,
        description="Current status of the task",
        examples=[TaskStatus.PENDING]
    )


class TaskCreate(TaskBase):
    """Schema for creating a new task."""
    pass


class TaskUpdate(BaseModel):
    """Schema for updating an existing task (all fields optional)."""
    title: Optional[str] = Field(
        None,
        min_length=1,
        max_length=100,
        description="Updated title (min 1, max 100 characters)",
        examples=["Updated task title"]
    )
    description: Optional[str] = Field(
        None,
        max_length=500,
        description="Updated description",
        examples=["Updated task description"]
    )
    status: Optional[TaskStatus] = Field(
        None,
        description="Updated status: pending, in_progress, completed",
        examples=[TaskStatus.IN_PROGRESS]
    )


class TaskResponse(BaseModel):
    """Schema for task response returned to the client."""
    id: str = Field(..., description="Unique UUID for the task")
    title: str
    description: Optional[str] = None
    status: TaskStatus
    created_at: datetime = Field(..., description="Creation timestamp in ISO-8601 format")

    model_config = {
        "from_attributes": True,
        "json_schema_extra": {
            "example": {
                "id": "c9bf9e57-1685-4c89-bafb-ff5af830be8a",
                "title": "Build Task Management API",
                "description": "Backend API using FastAPI with request validation",
                "status": "pending",
                "created_at": "2026-10-19T16:20:00Z"
            }
        }
    }
