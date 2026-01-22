"""
Module: Task model implementation
Task ID: T-004
Specification Reference: FR-001, FR-002 - System MUST support task creation with metadata
"""

from dataclasses import dataclass, field
from datetime import datetime
from uuid import uuid4


# [T-004] - Spec section: FR-001, FR-002 (Task model with ID generation and timestamps)
@dataclass
class Task:
    """
    Represents a single todo task with auto-generated unique ID and timestamps.

    Attributes:
        id: Unique identifier (auto-generated UUID string)
        title: Task title (required, non-empty string)
        description: Optional task description (default empty string)
        completed: Task completion status (default False)
        created_at: ISO 8601 timestamp of task creation (auto-set)
        updated_at: ISO 8601 timestamp of last update (auto-set)
    """

    title: str
    description: str = ""
    id: str = field(default_factory=lambda: str(uuid4()))
    completed: bool = False
    created_at: datetime = field(default_factory=datetime.now)
    updated_at: datetime = field(default_factory=datetime.now)

    def __post_init__(self) -> None:
        """
        Validate task attributes after initialization.

        Raises:
            ValueError: If title is empty or contains only whitespace
        """
        # [T-004] - Spec section: FR-008 (Task title validation)
        if not self.title or not self.title.strip():
            raise ValueError("Task title cannot be empty")

        # Ensure title is stripped of leading/trailing whitespace
        self.title = self.title.strip()

    def mark_complete(self) -> None:
        """
        Mark task as completed and update timestamp.

        Per Spec FR-004: System MUST allow users to mark tasks as complete.
        """
        self.completed = True
        self.updated_at = datetime.now()

    def mark_incomplete(self) -> None:
        """
        Mark task as incomplete and update timestamp.

        Per Spec FR-004: System MUST allow users to mark tasks as incomplete.
        """
        self.completed = False
        self.updated_at = datetime.now()

    def toggle_completion(self) -> None:
        """
        Toggle task completion status between completed and incomplete.

        Per Spec FR-004: System MUST allow users to toggle task status.
        """
        if self.completed:
            self.mark_incomplete()
        else:
            self.mark_complete()

    def update(self, title: str | None = None, description: str | None = None) -> None:
        """
        Update task title and/or description.

        Args:
            title: New task title (optional, must be non-empty if provided)
            description: New task description (optional)

        Raises:
            ValueError: If provided title is empty or whitespace-only

        Per Spec FR-005, FR-008: System MUST allow users to update task details
        and validate titles are non-empty.
        """
        if title is not None:
            if not title or not title.strip():
                raise ValueError("Task title cannot be empty")
            self.title = title.strip()

        if description is not None:
            self.description = description

        self.updated_at = datetime.now()

    def to_dict(self) -> dict:
        """
        Convert task to dictionary representation.

        Returns:
            Dictionary with all task attributes including ISO formatted timestamps
        """
        return {
            "id": self.id,
            "title": self.title,
            "description": self.description,
            "completed": self.completed,
            "created_at": self.created_at.isoformat(),
            "updated_at": self.updated_at.isoformat(),
        }

    def __repr__(self) -> str:
        """Return string representation of task."""
        status = "✓" if self.completed else "☐"
        return f"Task({status} {self.id[:8]}... {self.title})"
