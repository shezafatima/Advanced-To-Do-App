from dataclasses import dataclass
from typing import Optional


@dataclass
class TodoItem:
    """
    Represents a single todo task with properties: unique identifier, description text, completion status (boolean)
    """
    id: int
    description: str
    completed: bool = False

    def __post_init__(self):
        """Validate the TodoItem after initialization"""
        if not isinstance(self.id, int) or self.id <= 0:
            raise ValueError(f"ID must be a positive integer, got {self.id}")

        if not isinstance(self.description, str):
            raise ValueError(f"Description must be a string, got {type(self.description)}")

        if not self.description.strip():
            raise ValueError(f"Description cannot be empty or contain only whitespace")

        if not isinstance(self.completed, bool):
            raise ValueError(f"Completed must be a boolean, got {type(self.completed)}")