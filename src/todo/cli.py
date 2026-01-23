import sys
from typing import List
from .storage import TodoList
from .domain import TodoItem


class TodoCLI:
    """
    Command-line interface for the todo application
    Command parsing: split input into command and arguments
    Command dispatch: map commands to appropriate methods
    Error handling: catch and display meaningful error messages
    """

    def __init__(self):
        self.todo_list = TodoList()
        self.running = True

    def run(self):
        """Main CLI loop"""
        print("Todo Console Application - Type 'help' for available commands or 'quit' to exit")

        while self.running:
            try:
                user_input = input("\ntodo> ").strip()
                if not user_input:
                    continue

                self.process_command(user_input)
            except KeyboardInterrupt:
                print("\nGoodbye!")
                break
            except EOFError:
                print("\nGoodbye!")
                break

    def process_command(self, user_input: str):
        """Parse and execute user command"""
        parts = user_input.split()
        if not parts:
            return

        command = parts[0].lower()
        args = parts[1:]

        try:
            if command == "quit" or command == "exit":
                self.running = False
                print("Goodbye!")
            elif command == "help":
                self.handle_help()
            elif command == "add":
                self.handle_add(args)
            elif command == "list":
                self.handle_list(args)
            elif command == "mark":
                self.handle_mark(args)
            elif command == "update":
                self.handle_update(args)
            elif command == "delete":
                self.handle_delete(args)
            else:
                print(f"Unknown command: '{command}'. Type 'help' for available commands.")
        except ValueError as e:
            print(f"Error: {e}")
        except IndexError:
            print(f"Invalid command format. Type 'help' for usage information.")
        except Exception as e:
            print(f"Unexpected error occurred: {e}")

    def handle_help(self):
        """Display help information"""
        print("Available commands:")
        print("  add <description>     - Add a new todo item")
        print("  list                  - List all todo items")
        print("  mark <id> <status>    - Mark item as complete/incomplete")
        print("  update <id> <desc>    - Update item description")
        print("  delete <id>           - Delete an item")
        print("  help                  - Show this help message")
        print("  quit/exit             - Exit the application")

    def handle_add(self, args: List[str]):
        """Handle add command"""
        if len(args) < 1:
            print("Usage: add <description>")
            return

        description = " ".join(args)
        try:
            item = self.todo_list.add_item(description)
            print(f"Added todo item with ID {item.id}: {item.description}")
        except ValueError as e:
            print(f"Error adding item: {e}")

    def handle_list(self, args: List[str]):
        """Handle list command"""
        items = self.todo_list.list_items()

        if not items:
            print("No todo items in the list.")
            return

        print("Todo List:")
        for item in items:
            status = "✓" if item.completed else "○"
            print(f"  [{status}] {item.id}: {item.description}")

    def handle_mark(self, args: List[str]):
        """Handle mark command - mark item as complete/incomplete"""
        if len(args) != 2:
            print("Usage: mark <id> <complete|incomplete>")
            return

        try:
            item_id = int(args[0])
            status = args[1].lower()

            if status == "complete":
                item = self.todo_list.mark_complete(item_id)
                print(f"Marked item {item.id} as complete: {item.description}")
            elif status == "incomplete":
                item = self.todo_list.mark_incomplete(item_id)
                print(f"Marked item {item.id} as incomplete: {item.description}")
            else:
                print(f"Invalid status: {status}. Use 'complete' or 'incomplete'.")
        except ValueError as e:
            print(f"Error: {e}")
        except ValueError:
            print(f"Invalid ID: {args[0]}. Please provide a valid number.")

    def handle_update(self, args: List[str]):
        """Handle update command"""
        if len(args) < 2:
            print("Usage: update <id> <new_description>")
            return

        try:
            item_id = int(args[0])
            new_description = " ".join(args[1:])
            item = self.todo_list.update_item(item_id, new_description)
            print(f"Updated item {item.id}: {item.description}")
        except ValueError as e:
            print(f"Error: {e}")
        except ValueError:
            print(f"Invalid ID: {args[0]}. Please provide a valid number.")

    def handle_delete(self, args: List[str]):
        """Handle delete command"""
        if len(args) != 1:
            print("Usage: delete <id>")
            return

        try:
            item_id = int(args[0])
            success = self.todo_list.delete_item(item_id)
            if success:
                print(f"Deleted item with ID {item_id}")
            else:
                print(f"Item with ID {item_id} not found")
        except ValueError:
            print(f"Invalid ID: {args[0]}. Please provide a valid number.")