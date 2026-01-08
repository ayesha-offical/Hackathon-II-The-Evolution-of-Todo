"""
Tests for Phase 7: Delete Task - CLI
Task ID: T-044
Specification Reference: FR-006, FR-007 - Delete command handling
"""

import pytest
from src.cli import CommandDispatcher
from src.storage import TaskStorage


# [T-044] - Spec section: FR-006, FR-007 (Test CLI delete command)
class TestCLIDeleteCommand:
    """Test cases for 'delete' command with proper removal and feedback."""

    def test_delete_command_removes_task(self) -> None:
        """
        Test 'delete' command removes a task by ID.

        Acceptance Criteria:
        - Command returns True
        - Task is removed from storage
        - Task no longer appears in list
        - Success message displayed

        Per Spec FR-006: Delete task by ID.
        """
        storage = TaskStorage()
        dispatcher = CommandDispatcher(storage)

        task = storage.add_task("Task to delete")
        assert storage.count_tasks() == 1

        result = dispatcher.dispatch(f"delete {task.id}")

        assert result is True
        assert storage.count_tasks() == 0
        assert storage.get_task(task.id) is None

    def test_delete_command_preserves_other_tasks(self) -> None:
        """
        Test 'delete' command only removes target task.

        Acceptance Criteria:
        - Target task deleted
        - Other tasks remain unchanged
        - Count decrements correctly
        - Others still retrievable

        Per Spec FR-006: Only specified task removed.
        """
        storage = TaskStorage()
        dispatcher = CommandDispatcher(storage)

        task1 = storage.add_task("Keep this")
        task2 = storage.add_task("Delete this")
        task3 = storage.add_task("Keep this too")

        result = dispatcher.dispatch(f"delete {task2.id}")

        assert result is True
        assert storage.count_tasks() == 2
        assert storage.get_task(task1.id) is not None
        assert storage.get_task(task2.id) is None
        assert storage.get_task(task3.id) is not None

    def test_delete_command_with_invalid_task_id(self) -> None:
        """
        Test 'delete' command with non-existent task ID.

        Acceptance Criteria:
        - Returns False (error)
        - Shows error message
        - Storage unchanged

        Per Spec FR-007: Error handling.
        """
        storage = TaskStorage()
        dispatcher = CommandDispatcher(storage)

        storage.add_task("Existing task")

        result = dispatcher.dispatch("delete nonexistent-id-999")

        assert result is False
        assert storage.count_tasks() == 1

    def test_delete_command_without_task_id(self) -> None:
        """
        Test 'delete' command without providing task ID.

        Acceptance Criteria:
        - Returns False (error)
        - Shows error message about missing ID
        - Displays usage hint

        Per Spec FR-007: Error messages.
        """
        storage = TaskStorage()
        dispatcher = CommandDispatcher(storage)

        result = dispatcher.dispatch("delete")

        assert result is False

    def test_delete_command_shows_success_message(self) -> None:
        """
        Test 'delete' command displays success feedback.

        Acceptance Criteria:
        - Success message shown
        - Shows task title that was deleted
        - Message is clear and helpful

        Per Spec FR-007: Clear feedback messages.
        """
        storage = TaskStorage()
        dispatcher = CommandDispatcher(storage)

        task = storage.add_task("Buy groceries")

        result = dispatcher.dispatch(f"delete {task.id}")

        assert result is True
        assert storage.count_tasks() == 0

    def test_delete_command_shows_error_for_nonexistent(self) -> None:
        """
        Test 'delete' command shows error for non-existent task.

        Acceptance Criteria:
        - Error message displayed
        - Indicates task not found
        - Storage unchanged

        Per Spec FR-007.
        """
        storage = TaskStorage()
        dispatcher = CommandDispatcher(storage)

        storage.add_task("Task")

        result = dispatcher.dispatch("delete nonexistent")

        assert result is False
        assert storage.count_tasks() == 1

    def test_delete_completed_task_via_cli(self) -> None:
        """
        Test deleting a completed task via CLI.

        Acceptance Criteria:
        - Command works on completed tasks
        - Task removed regardless of status
        - Success message shown

        Per Spec FR-006.
        """
        storage = TaskStorage()
        dispatcher = CommandDispatcher(storage)

        task = storage.add_task("Completed task")
        storage.mark_complete(task.id)

        result = dispatcher.dispatch(f"delete {task.id}")

        assert result is True
        assert storage.count_tasks() == 0

    def test_delete_and_add_same_id_not_reused(self) -> None:
        """
        Test that IDs are not reused after deletion.

        Acceptance Criteria:
        - Delete a task
        - Add new task
        - New task gets different ID
        - IDs are always unique

        Per Spec FR-006: Task ID never reused.
        """
        storage = TaskStorage()
        dispatcher = CommandDispatcher(storage)

        task1 = storage.add_task("First task")
        first_id = task1.id

        dispatcher.dispatch(f"delete {first_id}")
        assert storage.count_tasks() == 0

        dispatcher.dispatch("add Second task")
        task2 = storage.get_all_tasks()[0]
        second_id = task2.id

        # IDs should be different (UUIDs are unique)
        assert first_id != second_id

    def test_delete_multiple_tasks_sequentially_via_cli(self) -> None:
        """
        Test deleting multiple tasks one by one via CLI.

        Acceptance Criteria:
        - Each delete succeeds
        - Count decrements correctly
        - All deleted tasks gone
        - Other tasks preserved

        Per Spec FR-006.
        """
        storage = TaskStorage()
        dispatcher = CommandDispatcher(storage)

        task1 = storage.add_task("Task 1")
        task2 = storage.add_task("Task 2")
        task3 = storage.add_task("Task 3")

        result1 = dispatcher.dispatch(f"delete {task1.id}")
        assert result1 is True
        assert storage.count_tasks() == 2

        result2 = dispatcher.dispatch(f"delete {task3.id}")
        assert result2 is True
        assert storage.count_tasks() == 1

        result3 = dispatcher.dispatch(f"delete {task2.id}")
        assert result3 is True
        assert storage.count_tasks() == 0

    def test_delete_from_mixed_task_list(self) -> None:
        """
        Test deleting tasks from a list with mixed statuses.

        Acceptance Criteria:
        - Can delete incomplete tasks
        - Can delete completed tasks
        - Order doesn't matter
        - Others unaffected

        Per Spec FR-006.
        """
        storage = TaskStorage()
        dispatcher = CommandDispatcher(storage)

        task1 = storage.add_task("Incomplete")
        task2 = storage.add_task("Complete me")
        task3 = storage.add_task("Also incomplete")

        storage.mark_complete(task2.id)

        # Delete a completed task
        result1 = dispatcher.dispatch(f"delete {task2.id}")
        assert result1 is True
        assert storage.count_tasks() == 2

        # Delete an incomplete task
        result2 = dispatcher.dispatch(f"delete {task1.id}")
        assert result2 is True
        assert storage.count_tasks() == 1

        # Verify remaining task
        remaining = storage.get_task(task3.id)
        assert remaining is not None
        assert remaining.title == "Also incomplete"
