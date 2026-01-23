# CLI Command Contracts: Todo Console Application

**Date**: 2026-01-03
**Feature**: 001-phase-1

## Command Interface Specification

### Add Command
- **Command**: `add <description>`
- **Input**: String description of the todo item
- **Output**: Success message with assigned ID
- **Errors**:
  - Empty description: "Error: Todo description cannot be empty"
- **Side effects**: Creates new todo item with next available ID

### List Command
- **Command**: `list`
- **Input**: None
- **Output**: Formatted list of all todo items with status and IDs
- **Errors**: None
- **Side effects**: None

### Update Command
- **Command**: `update <id> <new_description>`
- **Input**: Integer ID and new description string
- **Output**: Success confirmation message
- **Errors**:
  - Invalid ID: "Error: Todo item with ID <id> not found"
  - Empty description: "Error: Todo description cannot be empty"
- **Side effects**: Modifies existing todo item's description

### Delete Command
- **Command**: `delete <id>`
- **Input**: Integer ID
- **Output**: Success confirmation message
- **Errors**:
  - Invalid ID: "Error: Todo item with ID <id> not found"
- **Side effects**: Removes todo item from collection

### Mark Command
- **Command**: `mark <id> <complete|incomplete>`
- **Input**: Integer ID and status (complete or incomplete)
- **Output**: Success confirmation message
- **Errors**:
  - Invalid ID: "Error: Todo item with ID <id> not found"
  - Invalid status: "Error: Status must be 'complete' or 'incomplete'"
- **Side effects**: Changes completion status of todo item

### Help Command
- **Command**: `help`
- **Input**: None
- **Output**: List of available commands with usage examples
- **Errors**: None
- **Side effects**: None

### Quit/Exit Command
- **Command**: `quit` or `exit`
- **Input**: None
- **Output**: Exit confirmation message
- **Errors**: None
- **Side effects**: Terminates the application

## Error Handling Contract
- All error messages follow format: "Error: <descriptive message>"
- Application continues running after error (does not crash)
- Invalid commands show usage help
- Invalid arguments show specific error message

## State Management Contract
- In-memory storage persists only during application execution
- IDs are assigned sequentially starting from 1
- IDs are never reused after deletion
- State is not persisted beyond application lifetime