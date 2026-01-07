"""
Module: In-memory task storage implementation
Task ID: T-005
Specification Reference: FR-009 - System MUST support in-memory storage for all tasks
"""

from typing import Optional

from src.models import Task


# [T-005] - Spec section: FR-009 (In-memory storage for tasks)
class TaskStorage:
    """
    In-memory storage for managing tasks during a single application session.

    This storage maintains tasks in a dictionary keyed by task ID, allowing
    O(1) lookups and updates. Storage is lost when the application exits.

    Attributes:
        _tasks: Dictionary mapping task IDs to Task objects
    """

    def __init__(self) -> None:
        """Initialize empty task storage."""
        self._tasks: dict[str, Task] = {}

    def add_task(self, title: str, description: str = "") -> Task:
        """
        Add a new task to storage.

        Args:
            title: Task title (required, non-empty)
            description: Optional task description

        Returns:
            The newly created Task object with auto-generated ID

        Raises:
            ValueError: If title is empty or whitespace-only

        Per Spec FR-001, FR-002: System MUST allow users to add tasks with
        title (required) and optional description, and assign unique ID.
        """
        # [T-005] - Spec section: FR-001, FR-002 (Add task with ID generation)
        task = Task(title=title, description=description)
        self._tasks[task.id] = task
        return task

    def get_task(self, task_id: str) -> Optional[Task]:
        """
        Retrieve a task by ID.

        Args:
            task_id: The unique identifier of the task

        Returns:
            The Task object if found, None otherwise
        """
        return self._tasks.get(task_id)

    def get_all_tasks(self) -> list[Task]:
        """
        Retrieve all tasks from storage.

        Returns:
            List of all Task objects in storage (empty list if no tasks)

        Per Spec FR-003: System MUST display all tasks in readable format.
        """
        return list(self._tasks.values())

    def update_task(
        self,
        task_id: str,
        title: str | None = None,
        description: str | None = None,
    ) -> Optional[Task]:
        """
        Update a task's title and/or description.

        Args:
            task_id: The unique identifier of the task to update
            title: New task title (optional, must be non-empty if provided)
            description: New task description (optional)

        Returns:
            The updated Task object, or None if task not found

        Raises:
            ValueError: If title is provided but empty/whitespace-only

        Per Spec FR-005, FR-008: System MUST allow users to update task
        details and validate titles are non-empty.
        """
        # [T-005] - Spec section: FR-005 (Update task)
        task = self._tasks.get(task_id)
        if task is None:
            return None

        task.update(title=title, description=description)
        return task

    def mark_complete(self, task_id: str) -> Optional[Task]:
        """
        Toggle a task's completion status.

        Args:
            task_id: The unique identifier of the task

        Returns:
            The updated Task object, or None if task not found

        Per Spec FR-004: System MUST allow users to mark tasks as complete
        or incomplete, and toggle status.
        """
        # [T-005] - Spec section: FR-004 (Mark task as complete)
        task = self._tasks.get(task_id)
        if task is None:
            return None

        task.toggle_completion()
        return task

    def delete_task(self, task_id: str) -> bool:
        """
        Delete a task from storage by ID.

        Args:
            task_id: The unique identifier of the task to delete

        Returns:
            True if task was deleted, False if task not found

        Per Spec FR-006: System MUST allow users to delete tasks by task ID.
        """
        # [T-005] - Spec section: FR-006 (Delete task)
        if task_id in self._tasks:
            del self._tasks[task_id]
            return True
        return False

    def task_exists(self, task_id: str) -> bool:
        """
        Check if a task exists in storage.

        Args:
            task_id: The unique identifier to check

        Returns:
            True if task exists, False otherwise
        """
        return task_id in self._tasks

    def count_tasks(self) -> int:
        """
        Get the total number of tasks in storage.

        Returns:
            Number of tasks currently stored
        """
        return len(self._tasks)

    def clear_all(self) -> None:
        """
        Clear all tasks from storage (for testing).

        Warning: This operation is irreversible during the session.
        """
        self._tasks.clear()
