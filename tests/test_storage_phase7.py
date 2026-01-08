"""
Tests for Phase 7: Delete Task - Storage Layer
Task IDs: T-042, T-043
Specification Reference: FR-006, FR-007 - Task deletion
"""

import pytest
from src.models import Task
from src.storage import TaskStorage


# [T-042] - Spec section: FR-006 (Test task deletion)
class TestTaskStorageDeleteTask:
    """Test cases for TaskStorage.delete_task() method."""

    def test_delete_task_by_valid_id(self) -> None:
        """
        Test deleting a task by valid ID.

        Acceptance Criteria:
        - Task is removed from storage
        - Returns True (success)
        - Task no longer retrievable
        - Other tasks unaffected

        Per Spec FR-006: System MUST allow users to delete tasks by ID.
        """
        storage = TaskStorage()
        task1 = storage.add_task("Task 1")
        task2 = storage.add_task("Task 2")
        task3 = storage.add_task("Task 3")

        assert storage.count_tasks() == 3

        result = storage.delete_task(task2.id)

        assert result is True
        assert storage.count_tasks() == 2
        assert storage.get_task(task2.id) is None
        assert storage.get_task(task1.id) is not None
        assert storage.get_task(task3.id) is not None

    def test_delete_single_task_empties_storage(self) -> None:
        """
        Test deleting the only task empties storage.

        Acceptance Criteria:
        - Task is deleted
        - Storage becomes empty
        - get_all_tasks() returns empty list

        Per Spec FR-006.
        """
        storage = TaskStorage()
        task = storage.add_task("Only task")

        result = storage.delete_task(task.id)

        assert result is True
        assert storage.count_tasks() == 0
        assert storage.get_all_tasks() == []

    def test_delete_multiple_tasks_sequentially(self) -> None:
        """
        Test deleting multiple tasks one by one.

        Acceptance Criteria:
        - Each deletion succeeds
        - Count decrements correctly
        - Final storage empty
        - All deleted tasks gone

        Per Spec FR-006.
        """
        storage = TaskStorage()
        task1 = storage.add_task("Task 1")
        task2 = storage.add_task("Task 2")
        task3 = storage.add_task("Task 3")

        assert storage.count_tasks() == 3

        storage.delete_task(task1.id)
        assert storage.count_tasks() == 2

        storage.delete_task(task3.id)
        assert storage.count_tasks() == 1

        storage.delete_task(task2.id)
        assert storage.count_tasks() == 0

    def test_delete_completed_task(self) -> None:
        """
        Test deleting a task that is marked as complete.

        Acceptance Criteria:
        - Completed tasks can be deleted
        - Deletion works regardless of status
        - Task removed from storage

        Per Spec FR-006: Delete completed task like any other.
        """
        storage = TaskStorage()
        task = storage.add_task("Complete me")
        storage.mark_complete(task.id)
        assert storage.get_task(task.id).completed is True

        result = storage.delete_task(task.id)

        assert result is True
        assert storage.get_task(task.id) is None

    def test_delete_task_doesnt_affect_others(self) -> None:
        """
        Test that deleting one task doesn't affect others.

        Acceptance Criteria:
        - Only target task deleted
        - Other tasks remain unchanged
        - All fields of remaining tasks preserved

        Per Spec FR-006: Only specified task removed.
        """
        storage = TaskStorage()
        task1 = storage.add_task("Task 1", "Desc 1")
        task2 = storage.add_task("Task 2", "Desc 2")
        task3 = storage.add_task("Task 3", "Desc 3")

        storage.mark_complete(task1.id)

        storage.delete_task(task2.id)

        remaining1 = storage.get_task(task1.id)
        remaining3 = storage.get_task(task3.id)

        assert remaining1.title == "Task 1"
        assert remaining1.description == "Desc 1"
        assert remaining1.completed is True
        assert remaining3.title == "Task 3"
        assert remaining3.description == "Desc 3"
        assert remaining3.completed is False


# [T-043] - Spec section: FR-007 (Test error handling)
class TestTaskStorageDeleteErrorHandling:
    """Test cases for error handling in delete_task()."""

    def test_delete_nonexistent_task(self) -> None:
        """
        Test deleting a task that doesn't exist.

        Acceptance Criteria:
        - Returns False (not error/exception)
        - No crash
        - Storage unchanged

        Per Spec FR-007: Handle invalid IDs gracefully.
        """
        storage = TaskStorage()
        storage.add_task("Existing task")

        result = storage.delete_task("nonexistent-id-12345")

        assert result is False
        assert storage.count_tasks() == 1

    def test_delete_already_deleted_task(self) -> None:
        """
        Test deleting a task that was already deleted.

        Acceptance Criteria:
        - Returns False (not error)
        - No crash
        - Storage unchanged

        Per Spec FR-007.
        """
        storage = TaskStorage()
        task = storage.add_task("Task to delete twice")

        result1 = storage.delete_task(task.id)
        assert result1 is True
        assert storage.count_tasks() == 0

        result2 = storage.delete_task(task.id)
        assert result2 is False
        assert storage.count_tasks() == 0

    def test_delete_with_empty_id(self) -> None:
        """
        Test deleting with empty ID string.

        Acceptance Criteria:
        - Returns False gracefully
        - No error
        - Storage unchanged

        Per Spec FR-007.
        """
        storage = TaskStorage()
        storage.add_task("Task")

        result = storage.delete_task("")

        assert result is False
        assert storage.count_tasks() == 1

    def test_delete_preserves_other_task_properties(self) -> None:
        """
        Test that delete doesn't affect other tasks' properties.

        Acceptance Criteria:
        - Other tasks' timestamps unchanged
        - Other tasks' IDs unchanged
        - Other tasks' status unchanged

        Per Spec FR-006.
        """
        storage = TaskStorage()
        task1 = storage.add_task("Task 1")
        task2 = storage.add_task("Task 2")
        task3 = storage.add_task("Task 3")

        original_id1 = task1.id
        original_created1 = task1.created_at
        original_updated1 = task1.updated_at

        storage.delete_task(task2.id)

        remaining = storage.get_task(task1.id)
        assert remaining.id == original_id1
        assert remaining.created_at == original_created1
        assert remaining.updated_at == original_updated1
