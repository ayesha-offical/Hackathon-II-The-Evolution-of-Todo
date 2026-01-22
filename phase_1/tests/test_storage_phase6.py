"""
Tests for Phase 6: Update Task - Storage Layer
Task IDs: T-032, T-033, T-034
Specification Reference: FR-005, FR-008 - Task update with validation
"""

import pytest
from src.models import Task
from src.storage import TaskStorage


# [T-032] - Spec section: FR-005 (Test partial update - title only)
class TestTaskStorageUpdateTitle:
    """Test cases for TaskStorage.update_task() with title only."""

    def test_update_title_only(self) -> None:
        """
        Test updating only task title.

        Acceptance Criteria:
        - Title is updated to new value
        - Description remains unchanged
        - Returns updated Task object
        - Other fields (id, completed, timestamps) unchanged
        - updated_at timestamp is newer

        Per Spec FR-005: Allow updating task title and description.
        """
        storage = TaskStorage()
        task = storage.add_task("Original title", "Original description")
        original_desc = task.description
        original_updated_at = task.updated_at

        result = storage.update_task(task.id, title="New title")

        assert result is not None
        assert result.title == "New title"
        assert result.description == original_desc
        assert result.updated_at > original_updated_at

    def test_update_title_multiple_times(self) -> None:
        """
        Test updating task title multiple times.

        Acceptance Criteria:
        - Each update changes the title
        - Each update updates the timestamp
        - Description remains constant

        Per Spec FR-005.
        """
        storage = TaskStorage()
        task = storage.add_task("Title 1", "Description")
        original_desc = task.description

        storage.update_task(task.id, title="Title 2")
        result1 = storage.get_task(task.id)
        assert result1.title == "Title 2"
        assert result1.description == original_desc

        storage.update_task(task.id, title="Title 3")
        result2 = storage.get_task(task.id)
        assert result2.title == "Title 3"
        assert result2.description == original_desc

    def test_update_title_with_whitespace_trimming(self) -> None:
        """
        Test that update trims leading/trailing whitespace from title.

        Acceptance Criteria:
        - Leading/trailing spaces removed from new title
        - Internal spaces preserved
        - Empty/whitespace-only title rejected

        Per Spec FR-008: Title validation.
        """
        storage = TaskStorage()
        task = storage.add_task("Original", "Desc")

        result = storage.update_task(task.id, title="  Trimmed title  ")

        assert result.title == "Trimmed title"


# [T-033] - Spec section: FR-005 (Test partial update - description only)
class TestTaskStorageUpdateDescription:
    """Test cases for TaskStorage.update_task() with description only."""

    def test_update_description_only(self) -> None:
        """
        Test updating only task description.

        Acceptance Criteria:
        - Description is updated to new value
        - Title remains unchanged
        - Returns updated Task object
        - updated_at timestamp is updated

        Per Spec FR-005: Allow updating description independently.
        """
        storage = TaskStorage()
        task = storage.add_task("Title", "Original description")
        original_title = task.title
        original_updated_at = task.updated_at

        result = storage.update_task(task.id, description="New description")

        assert result is not None
        assert result.title == original_title
        assert result.description == "New description"
        assert result.updated_at > original_updated_at

    def test_update_description_to_empty(self) -> None:
        """
        Test updating description to empty string.

        Acceptance Criteria:
        - Description can be cleared (set to empty)
        - Title unchanged
        - Update succeeds

        Per Spec FR-005.
        """
        storage = TaskStorage()
        task = storage.add_task("Title", "Original description")
        original_title = task.title

        result = storage.update_task(task.id, description="")

        assert result.title == original_title
        assert result.description == ""

    def test_update_description_multiple_times(self) -> None:
        """
        Test updating description multiple times.

        Acceptance Criteria:
        - Each update changes the description
        - Title remains constant
        - Multiple updates work correctly

        Per Spec FR-005.
        """
        storage = TaskStorage()
        task = storage.add_task("Title", "Desc 1")
        original_title = task.title

        storage.update_task(task.id, description="Desc 2")
        result1 = storage.get_task(task.id)
        assert result1.description == "Desc 2"
        assert result1.title == original_title

        storage.update_task(task.id, description="Desc 3")
        result2 = storage.get_task(task.id)
        assert result2.description == "Desc 3"
        assert result2.title == original_title

    def test_update_both_title_and_description(self) -> None:
        """
        Test updating both title and description together.

        Acceptance Criteria:
        - Both fields are updated
        - Both changes persist
        - timestamp updated

        Per Spec FR-005.
        """
        storage = TaskStorage()
        task = storage.add_task("Original title", "Original desc")

        result = storage.update_task(
            task.id, title="New title", description="New desc"
        )

        assert result.title == "New title"
        assert result.description == "New desc"


# [T-034] - Spec section: FR-007, FR-008 (Test error handling)
class TestTaskStorageUpdateErrorHandling:
    """Test cases for error handling in update_task()."""

    def test_update_nonexistent_task(self) -> None:
        """
        Test updating a task that doesn't exist.

        Acceptance Criteria:
        - Returns None (not an error)
        - No exception raised
        - Storage unchanged

        Per Spec FR-007: Graceful error handling.
        """
        storage = TaskStorage()
        storage.add_task("Existing task")

        result = storage.update_task("nonexistent-id", title="New title")

        assert result is None
        assert storage.count_tasks() == 1

    def test_update_with_empty_title(self) -> None:
        """
        Test updating with empty title (should fail).

        Acceptance Criteria:
        - Raises ValueError
        - Task is NOT updated
        - Original title preserved

        Per Spec FR-008: Titles cannot be empty.
        """
        storage = TaskStorage()
        task = storage.add_task("Original title")
        original_title = task.title

        with pytest.raises(ValueError, match="Task title cannot be empty"):
            storage.update_task(task.id, title="")

        # Verify not updated
        assert storage.get_task(task.id).title == original_title

    def test_update_with_whitespace_only_title(self) -> None:
        """
        Test updating with whitespace-only title (should fail).

        Acceptance Criteria:
        - Raises ValueError
        - Task is NOT updated
        - Original title preserved

        Per Spec FR-008.
        """
        storage = TaskStorage()
        task = storage.add_task("Original title")
        original_title = task.title

        with pytest.raises(ValueError, match="Task title cannot be empty"):
            storage.update_task(task.id, title="   ")

        assert storage.get_task(task.id).title == original_title

    def test_update_maintains_id_and_completion(self) -> None:
        """
        Test that update doesn't change ID or completion status.

        Acceptance Criteria:
        - ID remains the same
        - Completion status unchanged
        - Only title/description can change

        Per Spec FR-005.
        """
        storage = TaskStorage()
        task = storage.add_task("Title", "Desc")
        storage.mark_complete(task.id)
        original_id = task.id
        completed_status = storage.get_task(task.id).completed

        storage.update_task(task.id, title="New title", description="New desc")
        result = storage.get_task(task.id)

        assert result.id == original_id
        assert result.completed == completed_status
