import unittest
import io
import sys
from unittest.mock import patch, MagicMock
from src.todo.cli import TodoCLI


class TestTodoCLIIntegration(unittest.TestCase):
    """Integration tests for TodoCLI functionality"""

    def setUp(self):
        """Set up test fixtures before each test method."""
        self.cli = TodoCLI()

    def test_add_and_list_integration(self):
        """Test adding an item and then listing it"""
        # Add an item
        self.cli.todo_list.add_item("Buy groceries")

        # Verify it exists in the list
        items = self.cli.todo_list.list_items()
        self.assertEqual(len(items), 1)
        self.assertEqual(items[0].description, "Buy groceries")
        self.assertFalse(items[0].completed)

    def test_add_update_and_list_integration(self):
        """Test adding, updating, and listing an item"""
        # Add an item
        item = self.cli.todo_list.add_item("Buy groceries")

        # Update the item
        updated_item = self.cli.todo_list.update_item(item.id, "Buy milk and bread")

        # Verify the update worked
        self.assertEqual(updated_item.description, "Buy milk and bread")

        # Verify it's still in the list with the new description
        items = self.cli.todo_list.list_items()
        self.assertEqual(len(items), 1)
        self.assertEqual(items[0].description, "Buy milk and bread")

    def test_add_mark_complete_list_integration(self):
        """Test adding, marking complete, and listing an item"""
        # Add an item
        item = self.cli.todo_list.add_item("Complete project")

        # Mark it as complete
        completed_item = self.cli.todo_list.mark_complete(item.id)

        # Verify it's marked as complete
        self.assertTrue(completed_item.completed)

        # Verify the change is reflected when listing
        items = self.cli.todo_list.list_items()
        self.assertEqual(len(items), 1)
        self.assertTrue(items[0].completed)

    def test_add_delete_integration(self):
        """Test adding and then deleting an item"""
        # Add an item
        item = self.cli.todo_list.add_item("Temporary task")

        # Verify it exists
        items = self.cli.todo_list.list_items()
        self.assertEqual(len(items), 1)

        # Delete the item
        success = self.cli.todo_list.delete_item(item.id)
        self.assertTrue(success)

        # Verify it's gone
        items = self.cli.todo_list.list_items()
        self.assertEqual(len(items), 0)

    def test_multiple_operations_integration(self):
        """Test multiple operations in sequence"""
        # Add multiple items
        item1 = self.cli.todo_list.add_item("First task")
        item2 = self.cli.todo_list.add_item("Second task")
        item3 = self.cli.todo_list.add_item("Third task")

        # Verify all items exist
        items = self.cli.todo_list.list_items()
        self.assertEqual(len(items), 3)

        # Mark the second item as complete
        completed_item = self.cli.todo_list.mark_complete(item2.id)
        self.assertTrue(completed_item.completed)

        # Update the third item
        updated_item = self.cli.todo_list.update_item(item3.id, "Updated third task")
        self.assertEqual(updated_item.description, "Updated third task")

        # Delete the first item
        success = self.cli.todo_list.delete_item(item1.id)
        self.assertTrue(success)

        # Verify final state: 2 items left, one complete, one updated
        final_items = self.cli.todo_list.list_items()
        self.assertEqual(len(final_items), 2)

        # Find the completed item
        completed_found = False
        updated_found = False
        for item in final_items:
            if item.id == item2.id and item.completed:
                completed_found = True
            if item.id == item3.id and item.description == "Updated third task":
                updated_found = True

        self.assertTrue(completed_found, "Completed item should still exist")
        self.assertTrue(updated_found, "Updated item should still exist")


class TestTodoCLIMethods(unittest.TestCase):
    """Test individual CLI methods"""

    def setUp(self):
        """Set up test fixtures before each test method."""
        self.cli = TodoCLI()

    @patch('sys.stdout', new_callable=io.StringIO)
    def test_handle_add_valid(self, mock_stdout):
        """Test handle_add with valid input"""
        self.cli.handle_add(["Buy", "groceries"])
        output = mock_stdout.getvalue().strip()
        self.assertIn("Added todo item with ID 1: Buy groceries", output)

    @patch('sys.stdout', new_callable=io.StringIO)
    def test_handle_list_empty(self, mock_stdout):
        """Test handle_list when list is empty"""
        self.cli.handle_list([])
        output = mock_stdout.getvalue().strip()
        self.assertIn("No todo items in the list.", output)

    @patch('sys.stdout', new_callable=io.StringIO)
    def test_handle_list_with_items(self, mock_stdout):
        """Test handle_list with items in the list"""
        # Add an item first
        self.cli.todo_list.add_item("Test item")

        # Now list items
        self.cli.handle_list([])
        output = mock_stdout.getvalue().strip()
        self.assertIn("Todo List:", output)
        self.assertIn("[○] 1: Test item", output)

    @patch('sys.stdout', new_callable=io.StringIO)
    def test_handle_mark_complete(self, mock_stdout):
        """Test handle_mark for complete"""
        # Add an item first
        self.cli.todo_list.add_item("Test item")

        # Mark as complete
        self.cli.handle_mark(["1", "complete"])
        output = mock_stdout.getvalue().strip()
        self.assertIn("Marked item 1 as complete: Test item", output)

    @patch('sys.stdout', new_callable=io.StringIO)
    def test_handle_update(self, mock_stdout):
        """Test handle_update"""
        # Add an item first
        self.cli.todo_list.add_item("Old description")

        # Update the item
        self.cli.handle_update(["1", "New", "description"])
        output = mock_stdout.getvalue().strip()
        self.assertIn("Updated item 1: New description", output)

    @patch('sys.stdout', new_callable=io.StringIO)
    def test_handle_delete(self, mock_stdout):
        """Test handle_delete"""
        # Add an item first
        self.cli.todo_list.add_item("Test item")

        # Delete the item
        self.cli.handle_delete(["1"])
        output = mock_stdout.getvalue().strip()
        self.assertIn("Deleted item with ID 1", output)


if __name__ == '__main__':
    unittest.main()