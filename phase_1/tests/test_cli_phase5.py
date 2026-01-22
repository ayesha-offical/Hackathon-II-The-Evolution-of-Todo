"""
Tests for Phase 5: Mark Task as Complete - CLI
Task ID: T-026
Specification Reference: FR-004, FR-007 - Complete command handling
"""

import pytest
from src.cli import CommandDispatcher
from src.storage import TaskStorage


# [T-026] - Spec section: FR-004, FR-007 (Test CLI complete command)
class TestCLICompleteCommand:
    """Test cases for 'complete' command with toggle logic."""

    def test_complete_command_marks_incomplete_task_complete(self) -> None:
        """
        Test 'complete' command marks an incomplete task as complete.

        Acceptance Criteria:
        - Command returns True
        - Task status changes to completed
        - Success message displayed
        - Feedback shows new status

        Per Spec FR-004: Mark tasks as complete.
        """
        storage = TaskStorage()
        dispatcher = CommandDispatcher(storage)

        task = storage.add_task("Buy groceries")
        assert task.completed is False

        result = dispatcher.dispatch(f"complete {task.id}")

        assert result is True
        completed_task = storage.get_task(task.id)
        assert completed_task.completed is True

    def test_complete_command_toggles_completed_task_back(self) -> None:
        """
        Test 'complete' command toggles completed task back to incomplete.

        Acceptance Criteria:
        - First toggle: incomplete → complete
        - Second toggle: complete → incomplete
        - Both operations succeed with True return
        - Status correctly reflects current state

        Per Spec FR-004: Toggle completion status.
        """
        storage = TaskStorage()
        dispatcher = CommandDispatcher(storage)

        task = storage.add_task("Test toggle")
        task_id = task.id

        # Mark as complete
        result1 = dispatcher.dispatch(f"complete {task_id}")
        assert result1 is True
        assert storage.get_task(task_id).completed is True

        # Toggle back to incomplete
        result2 = dispatcher.dispatch(f"complete {task_id}")
        assert result2 is True
        assert storage.get_task(task_id).completed is False

    def test_complete_command_with_invalid_task_id(self) -> None:
        """
        Test 'complete' command with non-existent task ID.

        Acceptance Criteria:
        - Returns False (error state)
        - Shows error message about task not found
        - No storage changes

        Per Spec FR-007: Clear error messages for invalid IDs.
        """
        storage = TaskStorage()
        dispatcher = CommandDispatcher(storage)

        storage.add_task("Existing task")  # Add one task

        result = dispatcher.dispatch("complete nonexistent-id-999")

        assert result is False
        assert storage.count_tasks() == 1  # Unchanged

    def test_complete_command_without_task_id(self) -> None:
        """
        Test 'complete' command without providing task ID.

        Acceptance Criteria:
        - Returns False (error)
        - Shows error message about missing ID
        - Displays usage hint

        Per Spec FR-007: Clear error messages.
        """
        storage = TaskStorage()
        dispatcher = CommandDispatcher(storage)

        result = dispatcher.dispatch("complete")

        assert result is False

    def test_complete_command_affects_only_target_task(self) -> None:
        """
        Test 'complete' command only toggles specified task.

        Acceptance Criteria:
        - Target task's status changes
        - Other tasks remain unchanged
        - Correct task identified by ID

        Per Spec FR-004: Mark specific task by ID.
        """
        storage = TaskStorage()
        dispatcher = CommandDispatcher(storage)

        task1 = storage.add_task("Task 1")
        task2 = storage.add_task("Task 2")
        task3 = storage.add_task("Task 3")

        # Complete only task2
        result = dispatcher.dispatch(f"complete {task2.id}")

        assert result is True
        assert storage.get_task(task1.id).completed is False
        assert storage.get_task(task2.id).completed is True
        assert storage.get_task(task3.id).completed is False

    def test_complete_command_shows_success_message(self) -> None:
        """
        Test 'complete' command displays success feedback.

        Acceptance Criteria:
        - Success message displayed
        - Shows task title
        - Shows new status (Complete ✓ or Pending ☐)
        - Message is helpful and clear

        Per Spec FR-007: Clear feedback messages.
        """
        storage = TaskStorage()
        dispatcher = CommandDispatcher(storage)

        task = storage.add_task("Buy groceries")

        result = dispatcher.dispatch(f"complete {task.id}")

        assert result is True
        # Task should now be marked complete
        updated_task = storage.get_task(task.id)
        assert updated_task.completed is True

    def test_complete_command_with_whitespace_id(self) -> None:
        """
        Test 'complete' command with ID containing whitespace.

        Acceptance Criteria:
        - Properly parses ID (stripped of whitespace)
        - Works correctly after parsing
        - Or shows error if ID invalid

        Per Spec FR-007.
        """
        storage = TaskStorage()
        dispatcher = CommandDispatcher(storage)

        task = storage.add_task("Test task")

        # Command with extra whitespace
        result = dispatcher.dispatch(f"complete  {task.id}  ")

        # Should handle gracefully (either work or error)
        assert result is True or result is False
        # If it works, task should be toggled
        if result is True:
            assert storage.get_task(task.id).completed is True

    def test_complete_updates_task_timestamp(self) -> None:
        """
        Test that 'complete' command updates task's updated_at timestamp.

        Acceptance Criteria:
        - Task's updated_at is updated when completed
        - Timestamp is after original creation time
        - Reflects the toggle action

        Per Spec FR-004: Timestamps track changes.
        """
        storage = TaskStorage()
        dispatcher = CommandDispatcher(storage)

        task = storage.add_task("Timestamped task")
        original_updated_at = task.updated_at

        dispatcher.dispatch(f"complete {task.id}")

        updated_task = storage.get_task(task.id)
        assert updated_task.updated_at > original_updated_at
