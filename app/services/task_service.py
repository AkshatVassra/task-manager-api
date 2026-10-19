import uuid
from datetime import datetime, timezone
from typing import Dict, List, Optional
from app.models.task import TaskCreate, TaskStatus, TaskUpdate


class TaskService:
    """In-memory service managing tasks with CRUD operations."""

    def __init__(self):
        # Store tasks in a dictionary keyed by task ID for O(1) lookups
        self._tasks: Dict[str, dict] = {}

    def get_all(self, status: Optional[TaskStatus] = None) -> List[dict]:
        """Retrieve all tasks, optionally filtered by status."""
        tasks = list(self._tasks.values())
        if status:
            tasks = [t for t in tasks if t["status"] == status]
        # Return tasks sorted newest first
        return sorted(tasks, key=lambda t: t["created_at"], reverse=True)

    def get_by_id(self, task_id: str) -> Optional[dict]:
        """Retrieve a single task by its unique ID."""
        return self._tasks.get(task_id)

    def create(self, task_in: TaskCreate) -> dict:
        """Create a new task with unique ID, timestamp, and validated fields."""
        task_id = str(uuid.uuid4())
        new_task = {
            "id": task_id,
            "title": task_in.title.strip(),
            "description": task_in.description.strip() if task_in.description else None,
            "status": task_in.status,
            "created_at": datetime.now(timezone.utc),
        }
        self._tasks[task_id] = new_task
        return new_task

    def update(self, task_id: str, task_update: TaskUpdate) -> Optional[dict]:
        """Update an existing task's fields if provided."""
        existing_task = self._tasks.get(task_id)
        if not existing_task:
            return None

        update_data = task_update.model_dump(exclude_unset=True)
        if "title" in update_data and update_data["title"] is not None:
            existing_task["title"] = update_data["title"].strip()
        if "description" in update_data:
            existing_task["description"] = (
                update_data["description"].strip()
                if update_data["description"]
                else None
            )
        if "status" in update_data and update_data["status"] is not None:
            existing_task["status"] = update_data["status"]

        return existing_task

    def delete(self, task_id: str) -> bool:
        """Delete a task by ID. Returns True if deleted, False if not found."""
        if task_id in self._tasks:
            del self._tasks[task_id]
            return True
        return False

    def clear(self) -> None:
        """Clear all tasks (primarily for testing)."""
        self._tasks.clear()


# Singleton instance of TaskService for the application lifecycle
task_service = TaskService()
