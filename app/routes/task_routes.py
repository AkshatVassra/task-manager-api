from typing import List, Optional
from fastapi import APIRouter, HTTPException, Query, status

from app.models.task import TaskCreate, TaskResponse, TaskStatus, TaskUpdate
from app.services.task_service import task_service

router = APIRouter(prefix="/api/v1/tasks", tags=["Tasks"])


@router.post(
    "",
    response_model=TaskResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Create a new task",
    description="Creates a new task with automatic UUID, creation timestamp, and validated payload.",
)
def create_task(task_in: TaskCreate) -> TaskResponse:
    """Create a task with validated title, description, and status."""
    new_task = task_service.create(task_in)
    return TaskResponse(**new_task)


@router.get(
    "",
    response_model=List[TaskResponse],
    status_code=status.HTTP_200_OK,
    summary="Get all tasks",
    description="Retrieve all tasks in the system. Optionally filter by status.",
)
def get_all_tasks(
    status_filter: Optional[TaskStatus] = Query(
        None,
        alias="status",
        description="Filter tasks by status (pending, in_progress, completed)",
    )
) -> List[TaskResponse]:
    """Retrieve all tasks sorted by newest first, with optional status filter."""
    tasks = task_service.get_all(status=status_filter)
    return [TaskResponse(**t) for t in tasks]


@router.get(
    "/{task_id}",
    response_model=TaskResponse,
    status_code=status.HTTP_200_OK,
    summary="Get task by ID",
    description="Retrieve details of a specific task using its unique ID.",
)
def get_task_by_id(task_id: str) -> TaskResponse:
    """Fetch task details or raise HTTP 404 if not found."""
    task = task_service.get_by_id(task_id)
    if not task:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Task with ID '{task_id}' was not found.",
        )
    return TaskResponse(**task)


@router.put(
    "/{task_id}",
    response_model=TaskResponse,
    status_code=status.HTTP_200_OK,
    summary="Update a task",
    description="Update title, description, or status of an existing task.",
)
def update_task(task_id: str, task_update: TaskUpdate) -> TaskResponse:
    """Update an existing task or raise HTTP 404 if not found."""
    updated_task = task_service.update(task_id, task_update)
    if not updated_task:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Task with ID '{task_id}' was not found.",
        )
    return TaskResponse(**updated_task)


@router.delete(
    "/{task_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    summary="Delete a task",
    description="Permanently delete a task by its ID.",
)
def delete_task(task_id: str):
    """Delete a task by ID or raise HTTP 404 if not found."""
    deleted = task_service.delete(task_id)
    if not deleted:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Task with ID '{task_id}' was not found.",
        )
    return None
