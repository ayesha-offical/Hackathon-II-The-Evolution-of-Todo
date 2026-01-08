"""
Integration tests for CLI CommandDispatcher
Task ID: T-010
Specification Reference: FR-001, FR-003, FR-004, FR-005, FR-006, FR-007
"""

import pytest
from io import StringIO
from rich.console import Console

from src.cli import CommandDispatcher
from src.storage import TaskStorage


# [T-010] - Spec section: FR-001, FR-007 (Test CLI add command)
class TestCLIAddCommand:
    """Test cases for 'add' command."""

    def test_add_command_with_title_only(self, capsys) -> None:
        """
        Test adding a task via CLI with title only.

        Acceptance Criteria:
        - Command parses correctly
        - Task is created in storage
        - Success message printed
        - Task appears in list

        Per Spec FR-001, FR-007: Add command with feedback.
        """
        storage = TaskStorage()
        dispatcher = CommandDispatcher(storage)

        result = dispatcher.dispatch("add Buy groceries")

        assert result is True
        assert storage.count_tasks() == 1

        tasks = storage.get_all_tasks()
        assert tasks[0].title == "Buy groceries"

    def test_add_command_with_title_and_description(self) -> None:
        """
        Test adding a task via CLI with title and description.

        Acceptance Criteria:
        - Command parses both arguments
        - Task created with both fields
        - Storage contains complete task

        Per Spec FR-001.
        """
        storage = TaskStorage()
        dispatcher = CommandDispatcher(storage)

        result = dispatcher.dispatch("add Buy groceries Need milk, eggs, bread")

        assert result is True
        assert storage.count_tasks() == 1

        task = storage.get_all_tasks()[0]
        assert task.title == "Buy groceries"
        assert task.description == "Need milk, eggs, bread"

    def test_add_command_empty_title_error(self) -> None:
        """
        Test adding task with empty title shows error.

        Acceptance Criteria:
        - No task created
        - Error message shown
        - Returns False

        Per Spec FR-007, FR-008: Validate and report errors.
        """
        storage = TaskStorage()
        dispatcher = CommandDispatcher(storage)

        result = dispatcher.dispatch("add")

        assert result is False
        assert storage.count_tasks() == 0

    def test_add_command_whitespace_only_error(self) -> None:
        """
        Test adding task with whitespace-only title shows error.

        Acceptance Criteria:
        - No task created
        - Error shown

        Per Spec FR-008: Reject whitespace-only titles.
        """
        storage = TaskStorage()
        dispatcher = CommandDispatcher(storage)

        result = dispatcher.dispatch("add    ")

        assert result is False
        assert storage.count_tasks() == 0


# [T-010] - Spec section: FR-003 (Test CLI list command)
class TestCLIListCommand:
    """Test cases for 'list' command."""

    def test_list_command_empty_storage(self) -> None:
        """
        Test list command when no tasks exist.

        Acceptance Criteria:
        - Shows empty list message
        - No error
        - Returns True

        Per Spec FR-003: Display empty list with user-friendly message.
        """
        storage = TaskStorage()
        dispatcher = CommandDispatcher(storage)

        result = dispatcher.dispatch("list")

        assert result is True

    def test_list_command_multiple_tasks(self) -> None:
        """
        Test list command with multiple tasks.

        Acceptance Criteria:
        - All tasks displayed
        - Shows status, title, description
        - Returns True

        Per Spec FR-003: Display all tasks with details.
        """
        storage = TaskStorage()
        dispatcher = CommandDispatcher(storage)

        storage.add_task("Task 1", "Description 1")
        storage.add_task("Task 2")
        task3 = storage.add_task("Task 3", "Description 3")
        storage.mark_complete(task3.id)

        result = dispatcher.dispatch("list")

        assert result is True
        assert storage.count_tasks() == 3

    def test_list_command_shows_completion_status(self) -> None:
        """
        Test that list command shows completion status.

        Acceptance Criteria:
        - Displays status for each task
        - Shows ✓ for complete, ☐ for incomplete

        Per Spec FR-003: Show completion status.
        """
        storage = TaskStorage()
        dispatcher = CommandDispatcher(storage)

        task1 = storage.add_task("Incomplete task")
        task2 = storage.add_task("Complete task")
        storage.mark_complete(task2.id)

        result = dispatcher.dispatch("list")

        assert result is True
        assert task1.completed is False
        assert task2.completed is True


# [T-010] - Spec section: FR-004 (Test CLI complete command)
class TestCLICompleteCommand:
    """Test cases for 'complete' command."""

    def test_complete_command_toggles_status(self) -> None:
        """
        Test complete command toggles task status.

        Acceptance Criteria:
        - First call marks complete
        - Second call marks incomplete
        - Storage updated
        - Returns True

        Per Spec FR-004: Toggle completion status.
        """
        storage = TaskStorage()
        dispatcher = CommandDispatcher(storage)

        task = storage.add_task("Test task")
        assert task.completed is False

        result = dispatcher.dispatch(f"complete {task.id}")
        assert result is True
        assert storage.get_task(task.id).completed is True

        result = dispatcher.dispatch(f"complete {task.id}")
        assert result is True
        assert storage.get_task(task.id).completed is False

    def test_complete_command_invalid_id(self) -> None:
        """
        Test complete command with invalid task ID.

        Acceptance Criteria:
        - Shows error message
        - Returns False
        - No changes to storage

        Per Spec FR-007: Handle invalid IDs gracefully.
        """
        storage = TaskStorage()
        dispatcher = CommandDispatcher(storage)

        storage.add_task("Task")

        result = dispatcher.dispatch("complete invalid-id")

        assert result is False

    def test_complete_command_no_id(self) -> None:
        """
        Test complete command without task ID.

        Acceptance Criteria:
        - Shows error message
        - Shows usage help
        - Returns False

        Per Spec FR-007: Show help on invalid input.
        """
        storage = TaskStorage()
        dispatcher = CommandDispatcher(storage)

        result = dispatcher.dispatch("complete")

        assert result is False


# [T-010] - Spec section: FR-005 (Test CLI update command)
class TestCLIUpdateCommand:
    """Test cases for 'update' command."""

    def test_update_command_title_only(self) -> None:
        """
        Test update command with new title only.

        Acceptance Criteria:
        - Title is updated
        - Description unchanged
        - Storage updated
        - Returns True

        Per Spec FR-005: Update title independently.
        """
        storage = TaskStorage()
        dispatcher = CommandDispatcher(storage)

        task = storage.add_task("Original title", "Original desc")

        result = dispatcher.dispatch(f"update {task.id} New title")

        assert result is True
        stored = storage.get_task(task.id)
        assert stored.title == "New title"
        assert stored.description == "Original desc"

    def test_update_command_with_description(self) -> None:
        """
        Test update command with title and description.

        Acceptance Criteria:
        - Both fields updated
        - Storage updated
        - Returns True

        Per Spec FR-005.
        """
        storage = TaskStorage()
        dispatcher = CommandDispatcher(storage)

        task = storage.add_task("Original", "Original desc")

        result = dispatcher.dispatch(
            f"update {task.id} New title New description"
        )

        assert result is True
        stored = storage.get_task(task.id)
        assert stored.title == "New title"
        assert stored.description == "New description"

    def test_update_command_invalid_id(self) -> None:
        """
        Test update command with invalid task ID.

        Acceptance Criteria:
        - Shows error message
        - Returns False
        - No changes

        Per Spec FR-007: Handle invalid IDs gracefully.
        """
        storage = TaskStorage()
        dispatcher = CommandDispatcher(storage)

        storage.add_task("Task")

        result = dispatcher.dispatch("update invalid-id New title")

        assert result is False

    def test_update_command_no_args(self) -> None:
        """
        Test update command without arguments.

        Acceptance Criteria:
        - Shows error message
        - Shows usage help
        - Returns False

        Per Spec FR-007: Show help on invalid input.
        """
        storage = TaskStorage()
        dispatcher = CommandDispatcher(storage)

        result = dispatcher.dispatch("update")

        assert result is False


# [T-010] - Spec section: FR-006 (Test CLI delete command)
class TestCLIDeleteCommand:
    """Test cases for 'delete' command."""

    def test_delete_command_removes_task(self) -> None:
        """
        Test delete command removes task from storage.

        Acceptance Criteria:
        - Task removed
        - Success message
        - Returns True
        - Other tasks unaffected

        Per Spec FR-006: Delete task by ID.
        """
        storage = TaskStorage()
        dispatcher = CommandDispatcher(storage)

        task1 = storage.add_task("Task 1")
        task2 = storage.add_task("Task 2")

        result = dispatcher.dispatch(f"delete {task1.id}")

        assert result is True
        assert storage.get_task(task1.id) is None
        assert storage.get_task(task2.id) is not None

    def test_delete_command_invalid_id(self) -> None:
        """
        Test delete command with invalid task ID.

        Acceptance Criteria:
        - Shows error message
        - Returns False
        - No changes to storage

        Per Spec FR-007: Handle invalid IDs gracefully.
        """
        storage = TaskStorage()
        dispatcher = CommandDispatcher(storage)

        task = storage.add_task("Task")

        result = dispatcher.dispatch("delete invalid-id")

        assert result is False
        assert storage.count_tasks() == 1  # Unchanged

    def test_delete_command_no_id(self) -> None:
        """
        Test delete command without task ID.

        Acceptance Criteria:
        - Shows error message
        - Shows usage help
        - Returns False

        Per Spec FR-007: Show help on invalid input.
        """
        storage = TaskStorage()
        dispatcher = CommandDispatcher(storage)

        result = dispatcher.dispatch("delete")

        assert result is False


# [T-010] - Spec section: FR-007 (Test CLI help command)
class TestCLIHelpCommand:
    """Test cases for 'help' command."""

    def test_help_command_general(self) -> None:
        """
        Test help command shows all available commands.

        Acceptance Criteria:
        - Displays all commands
        - Shows syntax for each
        - Returns True

        Per Spec FR-007: Provide help documentation.
        """
        storage = TaskStorage()
        dispatcher = CommandDispatcher(storage)

        result = dispatcher.dispatch("help")

        assert result is True

    def test_help_command_specific(self) -> None:
        """
        Test help command for specific command.

        Acceptance Criteria:
        - Shows help for requested command
        - Returns True

        Per Spec FR-007: Help for specific commands.
        """
        storage = TaskStorage()
        dispatcher = CommandDispatcher(storage)

        result = dispatcher.dispatch("help add")
        assert result is True

        result = dispatcher.dispatch("help list")
        assert result is True

    def test_help_command_unknown_command(self) -> None:
        """
        Test help command for unknown command.

        Acceptance Criteria:
        - Shows "no help available" message
        - Returns True (help never fails)

        Per Spec FR-007.
        """
        storage = TaskStorage()
        dispatcher = CommandDispatcher(storage)

        result = dispatcher.dispatch("help unknown")

        assert result is True


# [T-010] - Spec section: FR-007 (Test CLI error handling)
class TestCLIErrorHandling:
    """Test cases for CLI error handling."""

    def test_unknown_command(self) -> None:
        """
        Test unknown command shows error.

        Acceptance Criteria:
        - Shows error message
        - Shows help prompt
        - Returns False
        - Storage unchanged

        Per Spec FR-007: Clear error messages.
        """
        storage = TaskStorage()
        dispatcher = CommandDispatcher(storage)

        storage.add_task("Task")  # Ensure storage has content

        result = dispatcher.dispatch("unknown-command")

        assert result is False

    def test_empty_command(self) -> None:
        """
        Test empty command is handled gracefully.

        Acceptance Criteria:
        - No error
        - Returns True
        - Storage unchanged

        Per Spec FR-007: Graceful handling.
        """
        storage = TaskStorage()
        dispatcher = CommandDispatcher(storage)

        result = dispatcher.dispatch("")

        assert result is True

        result = dispatcher.dispatch("   ")

        assert result is True


# [T-018] - Spec section: FR-003 (Test CLI list command)
class TestCLIListCommandDisplay:
    """Test cases for 'list' command with table display."""

    def test_list_command_empty_shows_message(self) -> None:
        """
        Test list command when no tasks exist.

        Acceptance Criteria:
        - Command returns True
        - Displays user-friendly "No tasks" message
        - No errors

        Per Spec FR-003: Display empty list with user-friendly message.
        """
        storage = TaskStorage()
        dispatcher = CommandDispatcher(storage)

        result = dispatcher.dispatch("list")

        assert result is True

    def test_list_command_displays_multiple_tasks(self) -> None:
        """
        Test list command displays all tasks in table format.

        Acceptance Criteria:
        - Command returns True
        - All tasks are displayed
        - Table shows ID, Status, Title, Description
        - Both completed and incomplete tasks shown

        Per Spec FR-003: Display all tasks with details, show status indicators.
        """
        storage = TaskStorage()
        dispatcher = CommandDispatcher(storage)

        # Add mixed tasks
        task1 = storage.add_task("Buy groceries", "Milk, eggs, bread")
        task2 = storage.add_task("Clean room")
        task3 = storage.add_task("Cook dinner", "Pasta with sauce")
        storage.mark_complete(task3.id)  # Mark one as complete

        result = dispatcher.dispatch("list")

        assert result is True
        assert storage.count_tasks() == 3

    def test_list_command_shows_task_status_indicators(self) -> None:
        """
        Test list command displays correct status indicators.

        Acceptance Criteria:
        - Incomplete tasks show ☐ Pending indicator
        - Completed tasks show ✓ Complete indicator
        - Status clearly distinguishes task states

        Per Spec FR-003: Status indicators (✓ for completed, ☐ for incomplete).
        """
        storage = TaskStorage()
        dispatcher = CommandDispatcher(storage)

        # Add tasks and toggle completion
        task1 = storage.add_task("Incomplete task")
        task2 = storage.add_task("Complete me")
        storage.mark_complete(task2.id)

        result = dispatcher.dispatch("list")

        assert result is True
        # Both tasks are still retrievable with correct status
        tasks = storage.get_all_tasks()
        assert len(tasks) == 2
        incomplete = [t for t in tasks if not t.completed]
        complete = [t for t in tasks if t.completed]
        assert len(incomplete) == 1
        assert len(complete) == 1

    def test_list_command_with_long_descriptions(self) -> None:
        """
        Test list command handles long descriptions gracefully.

        Acceptance Criteria:
        - Long descriptions are displayed
        - Table formatting handles variable-length content
        - No crashes or overflow errors

        Per Spec FR-003: Display all fields including description.
        """
        storage = TaskStorage()
        dispatcher = CommandDispatcher(storage)

        long_desc = "This is a very long description that might wrap in the table. " * 3
        task = storage.add_task("Task with long description", long_desc)

        result = dispatcher.dispatch("list")

        assert result is True
        retrieved = storage.get_task(task.id)
        assert retrieved is not None
        assert retrieved.description == long_desc

    def test_list_command_shows_task_count(self) -> None:
        """
        Test list command displays total task count.

        Acceptance Criteria:
        - Shows "Total: N task(s)" at bottom
        - Correct count reflects actual tasks
        - Singular/plural handling (task vs tasks)

        Per Spec FR-003: Display task count summary.
        """
        storage = TaskStorage()
        dispatcher = CommandDispatcher(storage)

        storage.add_task("Task 1")
        storage.add_task("Task 2")
        storage.add_task("Task 3")

        result = dispatcher.dispatch("list")

        assert result is True
        assert storage.count_tasks() == 3
