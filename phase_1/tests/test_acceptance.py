"""
Acceptance tests for User Story 1 - Add Task
Task ID: T-008, T-009, T-010
Specification Reference: US1 - Add New Task (Priority P1)
"""

import pytest
from src.cli import CommandDispatcher
from src.storage import TaskStorage


class TestUserStory1AddTask:
    """
    Acceptance tests for User Story 1: Add New Task (Priority P1)

    Per Spec: As a user, I want to add a new task to my todo list with a
    title and optional description, so that I can capture things I need to do.

    Acceptance Scenarios:
    1. Given empty task list, when user enters "add Buy groceries", then new
       task is created with title "Buy groceries" and appears in list
    2. Given add task command, when user provides both title and description
       "Buy groceries" "Need milk, eggs, bread", then task is created with both
    3. Given add task command, when user enters only whitespace as title, then
       system rejects input with error message and no task is created
    4. Given task list with existing tasks, when user adds new task, then new
       task gets unique ID and appears in list
    """

    def test_scenario1_add_simple_task(self) -> None:
        """
        Scenario 1: Add a simple task with title only.

        Given: Empty task list
        When: User enters "add Buy groceries"
        Then: New task created with title "Buy groceries" and appears in list
        """
        storage = TaskStorage()
        dispatcher = CommandDispatcher(storage)

        # Given: Empty task list
        assert storage.count_tasks() == 0

        # When: User enters command
        result = dispatcher.dispatch("add Buy groceries")

        # Then: Task created successfully
        assert result is True
        assert storage.count_tasks() == 1

        # Task appears in list with correct title
        tasks = storage.get_all_tasks()
        assert len(tasks) == 1
        assert tasks[0].title == "Buy groceries"
        assert tasks[0].description == ""
        assert tasks[0].completed is False
        assert tasks[0].id is not None

    def test_scenario2_add_task_with_description(self) -> None:
        """
        Scenario 2: Add task with both title and description.

        Given: Add task command
        When: User provides both title and description
        Then: Task created with both title and description
        """
        storage = TaskStorage()
        dispatcher = CommandDispatcher(storage)

        # When: User enters command with description
        result = dispatcher.dispatch(
            "add Buy groceries Need milk, eggs, bread"
        )

        # Then: Task created with both fields
        assert result is True
        tasks = storage.get_all_tasks()
        assert tasks[0].title == "Buy groceries"
        assert tasks[0].description == "Need milk, eggs, bread"

    def test_scenario3_add_invalid_title(self) -> None:
        """
        Scenario 3: Reject empty/whitespace-only title.

        Given: Add task command
        When: User enters only whitespace as title
        Then: System rejects input with error message and no task created
        """
        storage = TaskStorage()
        dispatcher = CommandDispatcher(storage)

        # When: User tries empty title
        result = dispatcher.dispatch("add")

        # Then: Rejected
        assert result is False
        assert storage.count_tasks() == 0

        # When: User tries whitespace-only
        result = dispatcher.dispatch("add    ")

        # Then: Rejected
        assert result is False
        assert storage.count_tasks() == 0

    def test_scenario4_multiple_tasks_unique_ids(self) -> None:
        """
        Scenario 4: Multiple tasks get unique IDs.

        Given: Task list with existing tasks
        When: User adds new task
        Then: New task gets unique ID and appears in list
        """
        storage = TaskStorage()
        dispatcher = CommandDispatcher(storage)

        # Given: Existing tasks
        dispatcher.dispatch("add Task 1")
        dispatcher.dispatch("add Task 2")

        # When: User adds new task
        result = dispatcher.dispatch("add New task")

        # Then: Task added with unique ID
        assert result is True
        assert storage.count_tasks() == 3

        # All tasks have unique IDs
        tasks = storage.get_all_tasks()
        ids = {t.id for t in tasks}
        assert len(ids) == 3  # All unique


class TestUserStory1ListIntegration:
    """
    Integration tests for US1: Verify added tasks appear in list.
    """

    def test_added_tasks_appear_in_list(self) -> None:
        """
        Test that tasks added via CLI appear in list command.

        Acceptance Criteria:
        - Add multiple tasks via CLI
        - List command shows all added tasks
        - Tasks show with correct details and status
        """
        storage = TaskStorage()
        dispatcher = CommandDispatcher(storage)

        # Add tasks
        dispatcher.dispatch("add Task 1 Description for task 1")
        dispatcher.dispatch("add Task 2")
        dispatcher.dispatch("add Task 3 Description for task 3")

        # List command should show all
        result = dispatcher.dispatch("list")

        assert result is True
        assert storage.count_tasks() == 3

        # Verify tasks in storage
        tasks = storage.get_all_tasks()
        titles = {t.title for t in tasks}
        assert "Task 1" in titles
        assert "Task 2" in titles
        assert "Task 3" in titles


class TestUserStory1EndToEnd:
    """
    End-to-end tests for User Story 1.
    """

    def test_complete_us1_workflow(self) -> None:
        """
        Complete User Story 1 workflow: Create and verify task.

        Workflow:
        1. Start with empty list
        2. Add multiple tasks
        3. Verify all tasks appear in list
        4. Verify task details (ID, title, description, status)
        5. Verify task uniqueness
        """
        storage = TaskStorage()
        dispatcher = CommandDispatcher(storage)

        # Step 1: Empty list
        assert storage.count_tasks() == 0

        # Step 2: Add tasks
        dispatcher.dispatch("add Buy groceries Need milk, eggs")
        dispatcher.dispatch("add Clean room")
        dispatcher.dispatch("add Call mom")

        # Step 3: Verify count
        assert storage.count_tasks() == 3

        # Step 4: Verify details
        tasks = storage.get_all_tasks()

        task1 = next(t for t in tasks if t.title == "Buy groceries")
        assert task1.description == "Need milk, eggs"
        assert task1.completed is False
        assert task1.id is not None

        task2 = next(t for t in tasks if t.title == "Clean room")
        assert task2.description == ""
        assert task2.completed is False

        task3 = next(t for t in tasks if t.title == "Call mom")
        assert task3.description == ""
        assert task3.completed is False

        # Step 5: Verify uniqueness
        ids = {t.id for t in tasks}
        assert len(ids) == 3
