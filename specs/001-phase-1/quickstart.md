# Quickstart Guide: Todo Console Application

**Date**: 2026-01-03
**Feature**: 001-phase-1

## Prerequisites
- Python 3.13+ installed
- Linux/WSL, Windows, or macOS environment

## Setup
1. Navigate to the project directory
2. Ensure Python 3.13+ is available in your PATH
3. No additional setup required (uses only Python standard library)

## Running the Application
```bash
python -m src.todo.cli
```

## Available Commands
- `add <description>` - Add a new todo item
  Example: `add Buy groceries`
- `list` - List all todo items with their status
  Example: `list`
- `update <id> <new_description>` - Update an existing todo item
  Example: `update 1 Buy groceries and milk`
- `delete <id>` - Delete a todo item
  Example: `delete 1`
- `mark <id> <complete|incomplete>` - Mark a todo item as complete/incomplete
  Example: `mark 1 complete`
- `help` - Show available commands
- `quit` or `exit` - Exit the application

## Example Usage Session
```
> add Buy groceries
Added todo: "Buy groceries" (ID: 1)
> add Walk the dog
Added todo: "Walk the dog" (ID: 2)
> list
1. [ ] Buy groceries
2. [ ] Walk the dog
> mark 1 complete
Marked todo 1 as complete
> list
1. [x] Buy groceries
2. [ ] Walk the dog
> update 2 Walk the dog in the morning
Updated todo 2: "Walk the dog in the morning"
> delete 2
Deleted todo 2
> list
1. [x] Buy groceries
> quit
```

## Error Handling
The application provides meaningful error messages for invalid operations:
- Attempting to update/delete/mark a non-existent todo item
- Providing empty descriptions when adding/updating
- Using invalid command formats