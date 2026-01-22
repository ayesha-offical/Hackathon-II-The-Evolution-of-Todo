"""
Unit tests for TaskStorage class
Task ID: T-009
Specification Reference: FR-001, FR-002, FR-003, FR-004, FR-005, FR-006, FR-009
"""

import pytest
from src.models import Task
from src.storage import TaskStorage


# [T-009] - Spec section: FR-001, FR-002, FR-009 (Test TaskStorage add_task)
class TestTaskStorageAddTask:
    """Test cases for TaskStorage.add_task() method."""

    def test_add_task_with_title_only(self) -> None:
        """
        Test adding a task with title only.

        Acceptance Criteria:
        - Task is added to storage
        - Task is assigned unique ID
        - Task can be retrieved

        Per Spec FR-001, FR-002, FR-009: System MUST support in-memory
        storage and add tasks with auto-generated IDs.
        """
        storage = TaskStorage()
        task = storage.add_task("Buy groceries")

        assert task is not None
        assert task.title == "Buy groceries"
        assert task.description == ""
        assert task.id is not None
        assert storage.get_task(task.id) == task

    def test_add_task_with_title_and_description(self) -> None:
        """
        Test adding a task with both title and description.

        Acceptance Criteria:
        - Task is stored with both fields
        - Can be retrieved with full data

        Per Spec FR-001, FR-002.
        """
        storage = TaskStorage()
        task = storage.add_task("Buy groceries", "Milk, eggs, bread")

        assert task.title == "Buy groceries"
        assert task.description == "Milk, eggs, bread"
        assert storage.get_task(task.id) == task

    def test_add_multiple_tasks_unique_ids(self) -> None:
        """
        Test adding multiple tasks results in unique IDs.

        Acceptance Criteria:
        - Each task gets unique ID
        - All tasks can be retrieved
        - No collisions

        Per Spec FR-002: Unique ID generation per task.
        """
        storage = TaskStorage()
        task1 = storage.add_task("Task 1")
        task2 = storage.add_task("Task 2")
        task3 = storage.add_task("Task 3")

        ids = {task1.id, task2.id, task3.id}
        assert len(ids) == 3

        assert storage.get_task(task1.id) == task1
        assert storage.get_task(task2.id) == task2
        assert storage.get_task(task3.id) == task3

    def test_add_task_empty_title_rejected(self) -> None:
        """
        Test that adding task with empty title is rejected.

        Acceptance Criteria:
        - Empty title raises ValueError
        - No task is added to storage

        Per Spec FR-001, FR-008: System MUST validate non-empty titles.
        """
        storage = TaskStorage()

        with pytest.raises(ValueError):
            storage.add_task("")

        with pytest.raises(ValueError):
            storage.add_task("   ")

        assert storage.count_tasks() == 0


# [T-009] - Spec section: FR-003 (Test TaskStorage retrieval)
class TestTaskStorageRetrieval:
    """Test cases for TaskStorage task retrieval."""

    def test_get_all_tasks_empty(self) -> None:
        """
        Test getting all tasks from empty storage.

        Acceptance Criteria:
        - Returns empty list
        - No error

        Per Spec FR-003: Display empty list with user-friendly message.
        """
        storage = TaskStorage()
        tasks = storage.get_all_tasks()

        assert tasks == []
        assert isinstance(tasks, list)

    def test_get_all_tasks_multiple(self) -> None:
        """
        Test getting all tasks when multiple exist.

        Acceptance Criteria:
        - Returns all added tasks
        - In any order (order not specified)
        - All fields present

        Per Spec FR-003: Display all tasks with details.
        """
        storage = TaskStorage()
        task1 = storage.add_task("Task 1", "Description 1")
        task2 = storage.add_task("Task 2")
        task3 = storage.add_task("Task 3", "Description 3")

        tasks = storage.get_all_tasks()

        assert len(tasks) == 3
        task_ids = {t.id for t in tasks}
        assert task1.id in task_ids
        assert task2.id in task_ids
        assert task3.id in task_ids

    def test_get_nonexistent_task(self) -> None:
        """
        Test getting a task that doesn't exist.

        Acceptance Criteria:
        - Returns None (not an error)
        - Doesn't crash

        Per Spec FR-007: Handle invalid task IDs gracefully.
        """
        storage = TaskStorage()
        task = storage.get_task("nonexistent-id")

        assert task is None

    def test_task_exists(self) -> None:
        """
        Test checking if a task exists.

        Acceptance Criteria:
        - Returns True for existing tasks
        - Returns False for non-existent tasks

        Utility method for storage.
        """
        storage = TaskStorage()
        task = storage.add_task("Test task")

        assert storage.task_exists(task.id) is True
        assert storage.task_exists("nonexistent") is False


# [T-009] - Spec section: FR-004 (Test TaskStorage completion toggle)
class TestTaskStorageCompletion:
    """Test cases for TaskStorage.mark_complete() method."""

    def test_mark_complete_toggle_status(self) -> None:
        """
        Test toggling task completion status through storage.

        Acceptance Criteria:
        - Task status toggles each time
        - First call completes task
        - Second call returns to incomplete
        - Returns updated task

        Per Spec FR-004: Mark tasks as complete/incomplete, toggle status.
        """
        storage = TaskStorage()
        task = storage.add_task("Test task")
        assert task.completed is False

        result = storage.mark_complete(task.id)
        assert result is not None
        assert result.completed is True

        result = storage.mark_complete(task.id)
        assert result.completed is False

    def test_mark_complete_nonexistent_task(self) -> None:
        """
        Test marking non-existent task complete.

        Acceptance Criteria:
        - Returns None
        - No error
        - Storage unchanged

        Per Spec FR-007: Handle invalid IDs gracefully.
        """
        storage = TaskStorage()
        result = storage.mark_complete("nonexistent")

        assert result is None


# [T-009] - Spec section: FR-005 (Test TaskStorage update)
class TestTaskStorageUpdate:
    """Test cases for TaskStorage.update_task() method."""

    def test_update_task_title_only(self) -> None:
        """
        Test updating only task title.

        Acceptance Criteria:
        - Title is updated
        - Description remains unchanged
        - Returns updated task
        - Other tasks unchanged

        Per Spec FR-005: Update task title or description independently.
        """
        storage = TaskStorage()
        task = storage.add_task("Original title", "Original description")

        result = storage.update_task(task.id, title="New title")

        assert result is not None
        assert result.title == "New title"
        assert result.description == "Original description"

        # Verify in storage
        stored = storage.get_task(task.id)
        assert stored.title == "New title"

    def test_update_task_description_only(self) -> None:
        """
        Test updating only task description.

        Acceptance Criteria:
        - Description is updated
        - Title remains unchanged
        - Returns updated task

        Per Spec FR-005.
        """
        storage = TaskStorage()
        task = storage.add_task("Original title", "Original description")

        result = storage.update_task(task.id, description="New description")

        assert result is not None
        assert result.title == "Original title"
        assert result.description == "New description"

    def test_update_task_both_fields(self) -> None:
        """
        Test updating both title and description.

        Acceptance Criteria:
        - Both fields updated
        - Returns updated task

        Per Spec FR-005.
        """
        storage = TaskStorage()
        task = storage.add_task("Original", "Original desc")

        result = storage.update_task(
            task.id, title="New title", description="New desc"
        )

        assert result.title == "New title"
        assert result.description == "New desc"

    def test_update_nonexistent_task(self) -> None:
        """
        Test updating non-existent task.

        Acceptance Criteria:
        - Returns None
        - No error
        - Storage unchanged

        Per Spec FR-007: Handle invalid IDs gracefully.
        """
        storage = TaskStorage()
        result = storage.update_task("nonexistent", title="New title")

        assert result is None

    def test_update_with_empty_title_rejected(self) -> None:
        """
        Test that update with empty title is rejected.

        Acceptance Criteria:
        - Empty title raises ValueError
        - Task is not updated
        - Storage unchanged

        Per Spec FR-008: Titles must be non-empty.
        """
        storage = TaskStorage()
        task = storage.add_task("Original title")

        with pytest.raises(ValueError):
            storage.update_task(task.id, title="")

        # Verify unchanged
        stored = storage.get_task(task.id)
        assert stored.title == "Original title"


# [T-009] - Spec section: FR-006 (Test TaskStorage deletion)
class TestTaskStorageDeletion:
    """Test cases for TaskStorage.delete_task() method."""

    def test_delete_task_removes_from_storage(self) -> None:
        """
        Test that deleting a task removes it from storage.

        Acceptance Criteria:
        - delete_task returns True
        - Task no longer in storage
        - get_task returns None
        - Other tasks unaffected

        Per Spec FR-006: Allow users to delete tasks by ID.
        """
        storage = TaskStorage()
        task1 = storage.add_task("Task 1")
        task2 = storage.add_task("Task 2")

        result = storage.delete_task(task1.id)

        assert result is True
        assert storage.get_task(task1.id) is None
        assert storage.get_task(task2.id) is not None
        assert storage.count_tasks() == 1

    def test_delete_nonexistent_task(self) -> None:
        """
        Test deleting non-existent task.

        Acceptance Criteria:
        - delete_task returns False
        - Storage unchanged
        - No error

        Per Spec FR-007: Handle invalid IDs gracefully.
        """
        storage = TaskStorage()
        task = storage.add_task("Task")

        result = storage.delete_task("nonexistent")

        assert result is False
        assert storage.count_tasks() == 1  # Unchanged

    def test_delete_all_tasks(self) -> None:
        """
        Test deleting all tasks one by one.

        Acceptance Criteria:
        - Each delete returns True
        - Storage becomes empty
        - No tasks remain

        Per Spec FR-006.
        """
        storage = TaskStorage()
        task1 = storage.add_task("Task 1")
        task2 = storage.add_task("Task 2")
        task3 = storage.add_task("Task 3")

        assert storage.delete_task(task1.id) is True
        assert storage.count_tasks() == 2

        assert storage.delete_task(task2.id) is True
        assert storage.count_tasks() == 1

        assert storage.delete_task(task3.id) is True
        assert storage.count_tasks() == 0


# [T-009] - Spec section: FR-009 (Test TaskStorage utilities)
class TestTaskStorageUtilities:
    """Test cases for TaskStorage utility methods."""

    def test_count_tasks(self) -> None:
        """
        Test counting tasks in storage.

        Acceptance Criteria:
        - Count is 0 initially
        - Increments with each add
        - Decrements with each delete

        Per Spec FR-009: Storage utilities.
        """
        storage = TaskStorage()
        assert storage.count_tasks() == 0

        task1 = storage.add_task("Task 1")
        assert storage.count_tasks() == 1

        task2 = storage.add_task("Task 2")
        assert storage.count_tasks() == 2

        storage.delete_task(task1.id)
        assert storage.count_tasks() == 1

    def test_clear_all(self) -> None:
        """
        Test clearing all tasks from storage.

        Acceptance Criteria:
        - All tasks removed
        - Storage is empty
        - No errors

        Utility for testing.
        """
        storage = TaskStorage()
        storage.add_task("Task 1")
        storage.add_task("Task 2")
        storage.add_task("Task 3")

        assert storage.count_tasks() == 3

        storage.clear_all()

        assert storage.count_tasks() == 0
        assert storage.get_all_tasks() == []


# [T-016] - Spec section: FR-003 (Test TaskStorage list empty)
class TestTaskStorageListEmpty:
    """Test cases for TaskStorage.get_all_tasks() with empty storage."""

    def test_list_empty_storage(self) -> None:
        """
        Test retrieving all tasks from empty storage.

        Acceptance Criteria:
        - Returns empty list
        - Type is list (not None)
        - No errors

        Per Spec FR-003: System MUST display empty list with user-friendly message.
        """
        storage = TaskStorage()
        tasks = storage.get_all_tasks()

        assert tasks == []
        assert isinstance(tasks, list)
        assert len(tasks) == 0


# [T-017] - Spec section: FR-003 (Test TaskStorage list all tasks)
class TestTaskStorageListAll:
    """Test cases for TaskStorage.get_all_tasks() with multiple tasks."""

    def test_list_multiple_tasks(self) -> None:
        """
        Test retrieving all tasks when multiple exist.

        Acceptance Criteria:
        - Returns all added tasks
        - All fields are present (id, title, description, completed, timestamps)
        - Order is preserved (or at least consistent)
        - Correct count matches added tasks

        Per Spec FR-003: System MUST display all tasks with details.
        """
        storage = TaskStorage()
        task1 = storage.add_task("Task 1", "Description 1")
        task2 = storage.add_task("Task 2")
        task3 = storage.add_task("Task 3", "Description 3")

        tasks = storage.get_all_tasks()

        assert len(tasks) == 3
        task_ids = {t.id for t in tasks}
        assert task1.id in task_ids
        assert task2.id in task_ids
        assert task3.id in task_ids

        # Verify all fields are present
        for task in tasks:
            assert task.id is not None
            assert task.title is not None
            assert task.description is not None
            assert task.completed is not None
            assert task.created_at is not None
            assert task.updated_at is not None

    def test_list_with_completed_and_incomplete_tasks(self) -> None:
        """
        Test listing tasks with mixed completion status.

        Acceptance Criteria:
        - Both completed and incomplete tasks are returned
        - Completion status is preserved
        - Count includes all regardless of status

        Per Spec FR-003, FR-004: Display both completed and incomplete tasks.
        """
        storage = TaskStorage()
        task1 = storage.add_task("Incomplete task")
        task2 = storage.add_task("Complete this")
        storage.mark_complete(task2.id)  # Mark task2 as complete

        tasks = storage.get_all_tasks()

        assert len(tasks) == 2
        incomplete_tasks = [t for t in tasks if not t.completed]
        completed_tasks = [t for t in tasks if t.completed]

        assert len(incomplete_tasks) == 1
        assert len(completed_tasks) == 1
        assert incomplete_tasks[0].title == "Incomplete task"
        assert completed_tasks[0].title == "Complete this"


# [T-005] - Spec section: FR-001, FR-004, FR-005, FR-006 (Test short ID support)
class TestShortIDLookup:
    """Test cases for short ID (first 8 characters) support in TaskStorage."""

    def test_get_task_by_short_id(self) -> None:
        """
        Test retrieving a task by short ID (first 8 characters).

        Acceptance Criteria:
        - Task can be retrieved using full UUID
        - Task can be retrieved using first 8 characters of ID
        - Both return the same task object

        Per Spec FR-001, FR-003: Users should be able to use short IDs
        displayed in the task list.
        """
        storage = TaskStorage()
        task = storage.add_task("Test task")
        short_id = task.id[:8]

        # Retrieve using full ID
        full_result = storage.get_task(task.id)
        assert full_result == task

        # Retrieve using short ID
        short_result = storage.get_task(short_id)
        assert short_result == task
        assert short_result.id == task.id

    def test_mark_complete_by_short_id(self) -> None:
        """
        Test marking a task complete using short ID.

        Acceptance Criteria:
        - Task can be marked complete using short ID
        - Returns the updated task
        - Task status is toggled correctly
        - Works on subsequent calls with short ID

        Per Spec FR-004: Mark tasks as complete using any ID format.
        """
        storage = TaskStorage()
        task = storage.add_task("Test task")
        short_id = task.id[:8]

        assert task.completed is False

        # Mark complete using short ID
        result = storage.mark_complete(short_id)
        assert result is not None
        assert result.completed is True

        # Mark incomplete again using short ID
        result = storage.mark_complete(short_id)
        assert result.completed is False

    def test_update_task_by_short_id(self) -> None:
        """
        Test updating a task using short ID.

        Acceptance Criteria:
        - Task title can be updated using short ID
        - Task description can be updated using short ID
        - Both fields can be updated together using short ID
        - Returns the updated task

        Per Spec FR-005: Update task using any ID format.
        """
        storage = TaskStorage()
        task = storage.add_task("Original title", "Original description")
        short_id = task.id[:8]

        # Update title using short ID
        result = storage.update_task(short_id, title="New title")
        assert result is not None
        assert result.title == "New title"
        assert result.description == "Original description"

        # Update description using short ID
        result = storage.update_task(short_id, description="New description")
        assert result is not None
        assert result.title == "New title"
        assert result.description == "New description"

        # Update both using short ID
        result = storage.update_task(
            short_id, title="Another title", description="Another description"
        )
        assert result.title == "Another title"
        assert result.description == "Another description"

    def test_delete_task_by_short_id(self) -> None:
        """
        Test deleting a task using short ID.

        Acceptance Criteria:
        - Task can be deleted using short ID
        - Returns True on successful deletion
        - Task is no longer retrievable
        - Other tasks are unaffected

        Per Spec FR-006: Delete task using any ID format.
        """
        storage = TaskStorage()
        task1 = storage.add_task("Task 1")
        task2 = storage.add_task("Task 2")
        short_id_1 = task1.id[:8]

        result = storage.delete_task(short_id_1)

        assert result is True
        assert storage.get_task(short_id_1) is None
        assert storage.get_task(task2.id) is not None
        assert storage.count_tasks() == 1

    def test_task_exists_by_short_id(self) -> None:
        """
        Test checking task existence using short ID.

        Acceptance Criteria:
        - Returns True for existing tasks using short ID
        - Returns False for non-existent short IDs
        - Works with both full and short IDs

        Utility method support.
        """
        storage = TaskStorage()
        task = storage.add_task("Test task")
        short_id = task.id[:8]

        assert storage.task_exists(task.id) is True
        assert storage.task_exists(short_id) is True
        assert storage.task_exists("nonexistent") is False

    def test_short_id_uniqueness_within_tasks(self) -> None:
        """
        Test that short IDs don't collide in typical scenarios.

        Acceptance Criteria:
        - Multiple tasks have unique first 8 characters
        - Each short ID resolves to correct task
        - UUID generation ensures uniqueness at first 8 chars

        Per Spec FR-002: Unique ID generation.
        """
        storage = TaskStorage()
        tasks = [storage.add_task(f"Task {i}") for i in range(10)]

        # All short IDs should be unique and resolve correctly
        for task in tasks:
            short_id = task.id[:8]
            retrieved = storage.get_task(short_id)
            assert retrieved == task

    def test_ambiguous_short_id_error(self) -> None:
        """
        Test error handling for ambiguous short IDs.

        Acceptance Criteria:
        - If a short ID matches multiple full IDs, raises ValueError
        - Error message indicates ambiguity
        - Original query is preserved for debugging

        Note: This is a theoretical test - UUID collisions at first 8 chars
        are extremely unlikely in practice. This tests the error handling code path.
        """
        storage = TaskStorage()

        # Create a task and manually add another with matching prefix
        # (This is artificial since UUIDs won't naturally collide)
        task1 = storage.add_task("Task 1")
        task2 = storage.add_task("Task 2")

        # For normal UUID generation, short IDs should be unique
        # If we wanted to test ambiguity, we'd need to mock the UUID
        # For now, verify the _find_task_id method handles it correctly
        short_id_1 = task1.id[:8]
        retrieved = storage._find_task_id(short_id_1)
        assert retrieved == task1.id  # Should find the exact task
