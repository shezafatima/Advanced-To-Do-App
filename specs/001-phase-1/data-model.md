# Data Model: Phase I — Todo In-Memory Python Console Application

**Date**: 2026-01-03
**Feature**: 001-phase-1

## TodoItem Entity

### Fields
- **id**: `int` - Unique identifier assigned sequentially starting from 1
- **description**: `str` - Text description of the todo item (non-empty)
- **completed**: `bool` - Completion status (default: False)

### Validation Rules
- `id` must be a positive integer
- `description` must not be empty or contain only whitespace
- `completed` must be a boolean value

### State Transitions
- Initial state: `completed = False`
- Transition to completed: `completed = True` (via mark complete operation)
- Transition to incomplete: `completed = False` (via mark incomplete operation)

## TodoList Collection

### Operations
- **add_item(description: str)**: Creates a new TodoItem with the next available ID and adds to the collection
- **list_items()**: Returns all TodoItem objects in the collection
- **get_item(id: int)**: Returns the TodoItem with the specified ID or raises exception if not found
- **update_item(id: int, new_description: str)**: Updates the description of the specified TodoItem
- **delete_item(id: int)**: Removes the TodoItem with the specified ID from the collection
- **mark_complete(id: int)**: Sets the completed status of the specified TodoItem to True
- **mark_incomplete(id: int)**: Sets the completed status of the specified TodoItem to False

### Constraints
- IDs must be unique within the collection
- IDs must be assigned sequentially starting from 1
- No two TodoItems may have the same ID
- The collection maintains the order of insertion for display purposes