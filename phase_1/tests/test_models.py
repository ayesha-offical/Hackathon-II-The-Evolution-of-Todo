"""
Unit tests for Task model
Task ID: T-008
Specification Reference: FR-001, FR-002, FR-008 - Task creation with ID generation and validation
"""

import pytest
from datetime import datetime
from src.models import Task


# [T-008] - Spec section: FR-001, FR-002 (Test Task model instantiation and ID generation)
class TestTaskCreation:
    """Test cases for Task model creation and initialization."""

    def test_task_creation_with_title_only(self) -> None:
        """
        Test creating a task with title only.

        Acceptance Criteria:
        - Task is created successfully with provided title
        - Description defaults to empty string
        - Task gets unique UUID
        - Completed status defaults to False
        - Timestamps are created (created_at, updated_at)

        Per Spec FR-001, FR-002: System MUST allow task creation with title
        and optional description, assigning unique ID.
        """
        title = "Buy groceries"
        task = Task(title=title)

        assert task.title == title
        assert task.description == ""
        assert task.id is not None
        assert len(task.id) == 36  # UUID format
        assert task.completed is False
        assert isinstance(task.created_at, datetime)
        assert isinstance(task.updated_at, datetime)

    def test_task_creation_with_title_and_description(self) -> None:
        """
        Test creating a task with both title and description.

        Acceptance Criteria:
        - Task is created with both title and description
        - All other fields have correct defaults

        Per Spec FR-001, FR-002.
        """
        title = "Buy groceries"
        description = "Need milk, eggs, bread"
        task = Task(title=title, description=description)

        assert task.title == title
        assert task.description == description
        assert task.id is not None
        assert task.completed is False

    def test_task_unique_ids(self) -> None:
        """
        Test that each task gets a unique ID.

        Acceptance Criteria:
        - Creating multiple tasks results in different IDs
        - No ID collisions

        Per Spec FR-002: System MUST generate and assign a unique ID
        to each task upon creation.
        """
        task1 = Task(title="Task 1")
        task2 = Task(title="Task 2")
        task3 = Task(title="Task 3")

        ids = {task1.id, task2.id, task3.id}
        assert len(ids) == 3  # All IDs are unique

    def test_task_timestamps(self) -> None:
        """
        Test that tasks have correct timestamps.

        Acceptance Criteria:
        - created_at is set to current time
        - updated_at is set to current time
        - Timestamps are ISO 8601 format (datetime objects)

        Per Spec FR-002: Task model MUST have creation and update timestamps.
        """
        before = datetime.now()
        task = Task(title="Test task")
        after = datetime.now()

        assert before <= task.created_at <= after
        assert before <= task.updated_at <= after


# [T-008] - Spec section: FR-008 (Test Task title validation)
class TestTaskValidation:
    """Test cases for Task model validation."""

    def test_empty_title_rejected(self) -> None:
        """
        Test that empty title is rejected.

        Acceptance Criteria:
        - Creating task with empty title raises ValueError
        - No task is created

        Per Spec FR-008: System MUST validate task titles are non-empty
        and not just whitespace.
        """
        with pytest.raises(ValueError, match="Task title cannot be empty"):
            Task(title="")

    def test_whitespace_only_title_rejected(self) -> None:
        """
        Test that whitespace-only title is rejected.

        Acceptance Criteria:
        - Creating task with only whitespace raises ValueError
        - Handles spaces, tabs, newlines

        Per Spec FR-008: System MUST reject whitespace-only titles.
        """
        with pytest.raises(ValueError, match="Task title cannot be empty"):
            Task(title="   ")

        with pytest.raises(ValueError, match="Task title cannot be empty"):
            Task(title="\t\t")

        with pytest.raises(ValueError, match="Task title cannot be empty"):
            Task(title="\n\n")

    def test_title_whitespace_stripped(self) -> None:
        """
        Test that leading/trailing whitespace is removed from title.

        Acceptance Criteria:
        - Title with leading/trailing spaces is stripped
        - Preserves internal spaces

        Per Spec FR-008: Titles should be trimmed.
        """
        task = Task(title="  Buy groceries  ")
        assert task.title == "Buy groceries"

        task2 = Task(title="\tClean room\t")
        assert task2.title == "Clean room"


# [T-008] - Spec section: FR-004, FR-005 (Test Task completion and update)
class TestTaskMethods:
    """Test cases for Task model methods."""

    def test_mark_complete(self) -> None:
        """
        Test marking a task as complete.

        Acceptance Criteria:
        - Task completed flag changes to True
        - updated_at timestamp is updated

        Per Spec FR-004: System MUST allow users to mark tasks as complete.
        """
        task = Task(title="Buy groceries")
        original_updated_at = task.updated_at

        task.mark_complete()

        assert task.completed is True
        assert task.updated_at > original_updated_at

    def test_mark_incomplete(self) -> None:
        """
        Test marking a task as incomplete.

        Acceptance Criteria:
        - Task completed flag changes to False
        - updated_at timestamp is updated

        Per Spec FR-004: System MUST allow toggling completion status.
        """
        task = Task(title="Buy groceries", completed=True)
        original_updated_at = task.updated_at

        task.mark_incomplete()

        assert task.completed is False
        assert task.updated_at > original_updated_at

    def test_toggle_completion(self) -> None:
        """
        Test toggling task completion status.

        Acceptance Criteria:
        - Task status toggles between complete and incomplete
        - Works multiple times
        - Updates timestamp each time

        Per Spec FR-004: System MUST support toggling completion.
        """
        task = Task(title="Buy groceries")
        assert task.completed is False

        task.toggle_completion()
        assert task.completed is True

        task.toggle_completion()
        assert task.completed is False

        task.toggle_completion()
        assert task.completed is True

    def test_update_title(self) -> None:
        """
        Test updating task title.

        Acceptance Criteria:
        - Title is updated to new value
        - Description remains unchanged
        - updated_at timestamp is updated

        Per Spec FR-005: System MUST allow users to update task title.
        """
        task = Task(title="Buy groceries", description="Original description")
        original_updated_at = task.updated_at

        task.update(title="Buy groceries and cook dinner")

        assert task.title == "Buy groceries and cook dinner"
        assert task.description == "Original description"
        assert task.updated_at > original_updated_at

    def test_update_description(self) -> None:
        """
        Test updating task description.

        Acceptance Criteria:
        - Description is updated to new value
        - Title remains unchanged
        - updated_at timestamp is updated

        Per Spec FR-005: System MUST allow users to update task description.
        """
        task = Task(title="Buy groceries", description="Original description")
        original_title = task.title

        task.update(description="Need milk, eggs, bread, butter")

        assert task.title == original_title
        assert task.description == "Need milk, eggs, bread, butter"

    def test_update_both_title_and_description(self) -> None:
        """
        Test updating both title and description.

        Acceptance Criteria:
        - Both fields are updated
        - timestamp is updated

        Per Spec FR-005.
        """
        task = Task(title="Original title", description="Original desc")

        task.update(title="New title", description="New description")

        assert task.title == "New title"
        assert task.description == "New description"

    def test_update_with_empty_title_rejected(self) -> None:
        """
        Test that update with empty title is rejected.

        Acceptance Criteria:
        - Empty title raises ValueError
        - Task is not updated

        Per Spec FR-008: Titles cannot be empty.
        """
        task = Task(title="Original title")
        original_title = task.title

        with pytest.raises(ValueError, match="Task title cannot be empty"):
            task.update(title="")

        assert task.title == original_title  # Unchanged

    def test_to_dict(self) -> None:
        """
        Test converting task to dictionary.

        Acceptance Criteria:
        - Dictionary contains all task fields
        - Timestamps are ISO formatted strings

        Per Spec FR-001, FR-002.
        """
        task = Task(title="Buy groceries", description="Milk and eggs")

        task_dict = task.to_dict()

        assert task_dict["id"] == task.id
        assert task_dict["title"] == "Buy groceries"
        assert task_dict["description"] == "Milk and eggs"
        assert task_dict["completed"] is False
        assert isinstance(task_dict["created_at"], str)
        assert isinstance(task_dict["updated_at"], str)
        assert "T" in task_dict["created_at"]  # ISO format check
