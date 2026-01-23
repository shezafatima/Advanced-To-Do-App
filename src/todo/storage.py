from typing import List, Optional
from .domain import TodoItem


class TodoList:
    """
    Collection of TodoItem objects with methods for add, list, update, delete, and mark operations
    Storage: in-memory using Python data structures
    ID assignment: sequential starting from 1
    """

    def __init__(self):
        self._items: List[TodoItem] = []
        self._next_id = 1

    def add_item(self, description: str) -> TodoItem:
        """
        Creates a new TodoItem with the next available ID and adds to the collection
        Validates description is not empty/whitespace
        Assigns next sequential ID
        Returns the created TodoItem
        """
        if not description or not description.strip():
            raise ValueError("Description cannot be empty or contain only whitespace")

        # Create new item with next available ID
        new_item = TodoItem(
            id=self._next_id,
            description=description.strip(),
            completed=False
        )

        # Add to storage
        self._items.append(new_item)

        # Increment next ID for subsequent items
        self._next_id += 1

        return new_item

    def list_items(self) -> List[TodoItem]:
        """
        Returns all stored TodoItem objects
        Maintains order of insertion
        """
        return self._items.copy()  # Return copy to prevent external modification

    def get_item(self, item_id: int) -> TodoItem:
        """
        Returns specific TodoItem by ID
        Raises ValueError if ID not found
        """
        for item in self._items:
            if item.id == item_id:
                return item

        raise ValueError(f"Todo item with ID {item_id} not found")

    def update_item(self, item_id: int, new_description: str) -> TodoItem:
        """
        Updates description of specified item
        Validates new description is not empty/whitespace
        Returns updated item
        """
        if not new_description or not new_description.strip():
            raise ValueError("Description cannot be empty or contain only whitespace")

        for item in self._items:
            if item.id == item_id:
                item.description = new_description.strip()
                return item

        raise ValueError(f"Todo item with ID {item_id} not found")

    def delete_item(self, item_id: int) -> bool:
        """
        Removes specified item from storage
        Returns True if item was found and deleted, False otherwise
        """
        for i, item in enumerate(self._items):
            if item.id == item_id:
                del self._items[i]
                return True

        return False

    def mark_complete(self, item_id: int) -> TodoItem:
        """
        Finds item by ID and sets completed=True
        Returns updated item
        """
        for item in self._items:
            if item.id == item_id:
                item.completed = True
                return item

        raise ValueError(f"Todo item with ID {item_id} not found")

    def mark_incomplete(self, item_id: int) -> TodoItem:
        """
        Finds item by ID and sets completed=False
        Returns updated item
        """
        for item in self._items:
            if item.id == item_id:
                item.completed = False
                return item

        raise ValueError(f"Todo item with ID {item_id} not found")