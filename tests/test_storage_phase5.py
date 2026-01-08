"""
Tests for Phase 5: Mark Task as Complete
Task IDs: T-024, T-025
Specification Reference: FR-004 - Task completion toggle
"""

import pytest
from src.models import Task
from src.storage import TaskStorage


# [T-024] - Spec section: FR-004 (Test TaskStorage toggle completion)
class TestTaskStorageToggleCompletion:
    """Test cases for TaskStorage.mark_complete() toggle behavior."""

    def test_toggle_incomplete_to_complete(self) -> None:
        """
        Test toggling task from incomplete to complete.

        Acceptance Criteria:
        - Task status changes from False to True
        - Returns updated Task object
        - Task timestamp is updated

        Per Spec FR-004: System MUST allow users to mark tasks as complete.
        """
        storage = TaskStorage()
        task = storage.add_task("Test task")
        assert task.completed is False
        original_updated_at = task.updated_at

        result = storage.mark_complete(task.id)

        assert result is not None
        assert result.completed is True
        assert result.updated_at > original_updated_at

    def test_toggle_complete_to_incomplete(self) -> None:
        """
        Test toggling task from complete back to incomplete.

        Acceptance Criteria:
        - Task status changes from True to False
        - Returns updated Task object
        - Works as true toggle (bidirectional)

        Per Spec FR-004: System MUST allow toggling completion.
        """
        storage = TaskStorage()
        task = storage.add_task("Test task")
        # First mark complete
        storage.mark_complete(task.id)
        stored = storage.get_task(task.id)
        assert stored.completed is True

        # Now toggle back to incomplete
        result = storage.mark_complete(task.id)

        assert result is not None
        assert result.completed is False

    def test_multiple_toggles(self) -> None:
        """
        Test toggling completion status multiple times.

        Acceptance Criteria:
        - Status toggles correctly each time
        - Works bidirectionally (on/off/on/off pattern)
        - Final state matches expected

        Per Spec FR-004: Toggle behavior.
        """
        storage = TaskStorage()
        task = storage.add_task("Toggle test")

        # Toggle sequence: False → True → False → True
        assert storage.get_task(task.id).completed is False

        storage.mark_complete(task.id)
        assert storage.get_task(task.id).completed is True

        storage.mark_complete(task.id)
        assert storage.get_task(task.id).completed is False

        storage.mark_complete(task.id)
        assert storage.get_task(task.id).completed is True

    def test_toggle_only_affects_target_task(self) -> None:
        """
        Test that toggling one task doesn't affect others.

        Acceptance Criteria:
        - Only target task's status changes
        - Other tasks remain unchanged
        - Correct task identified by ID

        Per Spec FR-004: Mark specific task by ID.
        """
        storage = TaskStorage()
        task1 = storage.add_task("Task 1")
        task2 = storage.add_task("Task 2")
        task3 = storage.add_task("Task 3")

        # Mark only task2 as complete
        storage.mark_complete(task2.id)

        # Verify states
        assert storage.get_task(task1.id).completed is False
        assert storage.get_task(task2.id).completed is True
        assert storage.get_task(task3.id).completed is False


# [T-025] - Spec section: FR-007 (Test error handling for invalid task ID)
class TestTaskStorageToggleErrorHandling:
    """Test cases for error handling in mark_complete()."""

    def test_toggle_nonexistent_task_id(self) -> None:
        """
        Test toggling a task that doesn't exist.

        Acceptance Criteria:
        - Returns None (not an error/exception)
        - No crash or exception raised
        - Storage unchanged

        Per Spec FR-007: Handle invalid task IDs gracefully.
        """
        storage = TaskStorage()
        storage.add_task("Existing task")

        result = storage.mark_complete("nonexistent-id-12345")

        assert result is None
        assert storage.count_tasks() == 1  # Storage unchanged

    def test_toggle_empty_id_string(self) -> None:
        """
        Test toggling with empty ID string.

        Acceptance Criteria:
        - Returns None gracefully
        - No error
        - Storage unchanged

        Per Spec FR-007.
        """
        storage = TaskStorage()
        storage.add_task("Task")

        result = storage.mark_complete("")

        assert result is None

    def test_toggle_maintains_other_fields(self) -> None:
        """
        Test that toggling only changes completion, not other fields.

        Acceptance Criteria:
        - Title unchanged
        - Description unchanged
        - ID unchanged
        - Only completed and updated_at change

        Per Spec FR-004.
        """
        storage = TaskStorage()
        task = storage.add_task("Original title", "Original description")
        original_id = task.id
        original_title = task.title
        original_desc = task.description

        storage.mark_complete(task.id)
        result = storage.get_task(task.id)

        assert result.id == original_id
        assert result.title == original_title
        assert result.description == original_desc
        assert result.completed is True  # Only this changed
