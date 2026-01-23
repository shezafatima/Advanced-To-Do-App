import unittest
from src.todo.storage import TodoList
from src.todo.domain import TodoItem


class TestTodoList(unittest.TestCase):
    """Unit tests for TodoList storage class"""

    def setUp(self):
        """Set up test fixtures before each test method."""
        self.todo_list = TodoList()

    def test_initial_state(self):
        """Test initial state of TodoList"""
        self.assertEqual(len(self.todo_list.list_items()), 0)

    def test_add_item_basic(self):
        """Test adding a basic todo item"""
        item = self.todo_list.add_item("Test description")
        self.assertEqual(item.id, 1)
        self.assertEqual(item.description, "Test description")
        self.assertFalse(item.completed)

        items = self.todo_list.list_items()
        self.assertEqual(len(items), 1)
        self.assertEqual(items[0].id, 1)

    def test_add_multiple_items_sequential_ids(self):
        """Test that IDs are assigned sequentially"""
        item1 = self.todo_list.add_item("First item")
        item2 = self.todo_list.add_item("Second item")
        item3 = self.todo_list.add_item("Third item")

        self.assertEqual(item1.id, 1)
        self.assertEqual(item2.id, 2)
        self.assertEqual(item3.id, 3)

    def test_add_item_empty_description_raises_error(self):
        """Test that adding item with empty description raises ValueError"""
        with self.assertRaises(ValueError):
            self.todo_list.add_item("")

    def test_add_item_whitespace_description_raises_error(self):
        """Test that adding item with whitespace description raises ValueError"""
        with self.assertRaises(ValueError):
            self.todo_list.add_item("   ")

    def test_list_items_returns_copy(self):
        """Test that list_items returns a copy of the internal list"""
        self.todo_list.add_item("Test item")
        items_ref1 = self.todo_list.list_items()
        items_ref2 = self.todo_list.list_items()

        # Modifying one reference shouldn't affect the other since they're copies
        self.assertIsNot(items_ref1, items_ref2)

        # Both should have the same content
        self.assertEqual(len(items_ref1), 1)
        self.assertEqual(len(items_ref2), 1)
        self.assertEqual(items_ref1[0].id, items_ref2[0].id)

    def test_get_item_exists(self):
        """Test getting an existing item"""
        added_item = self.todo_list.add_item("Test item")
        retrieved_item = self.todo_list.get_item(1)

        self.assertEqual(added_item.id, retrieved_item.id)
        self.assertEqual(added_item.description, retrieved_item.description)
        self.assertEqual(added_item.completed, retrieved_item.completed)

    def test_get_item_not_found_raises_error(self):
        """Test that getting a non-existent item raises ValueError"""
        with self.assertRaises(ValueError):
            self.todo_list.get_item(999)

    def test_update_item_exists(self):
        """Test updating an existing item's description"""
        self.todo_list.add_item("Original description")
        updated_item = self.todo_list.update_item(1, "Updated description")

        self.assertEqual(updated_item.id, 1)
        self.assertEqual(updated_item.description, "Updated description")
        self.assertFalse(updated_item.completed)  # Should not change completed status

    def test_update_item_not_found_raises_error(self):
        """Test that updating a non-existent item raises ValueError"""
        with self.assertRaises(ValueError):
            self.todo_list.update_item(999, "New description")

    def test_update_item_empty_description_raises_error(self):
        """Test that updating with empty description raises ValueError"""
        self.todo_list.add_item("Original description")
        with self.assertRaises(ValueError):
            self.todo_list.update_item(1, "")

    def test_delete_item_exists(self):
        """Test deleting an existing item"""
        self.todo_list.add_item("Test item")
        success = self.todo_list.delete_item(1)

        self.assertTrue(success)
        self.assertEqual(len(self.todo_list.list_items()), 0)

    def test_delete_item_not_exists(self):
        """Test deleting a non-existent item returns False"""
        self.todo_list.add_item("Test item")
        success = self.todo_list.delete_item(999)

        self.assertFalse(success)
        self.assertEqual(len(self.todo_list.list_items()), 1)

    def test_mark_complete(self):
        """Test marking an item as complete"""
        self.todo_list.add_item("Test item")
        marked_item = self.todo_list.mark_complete(1)

        self.assertEqual(marked_item.id, 1)
        self.assertTrue(marked_item.completed)

    def test_mark_incomplete(self):
        """Test marking an item as incomplete"""
        self.todo_list.add_item("Test item")
        # First mark complete
        completed_item = self.todo_list.mark_complete(1)
        self.assertTrue(completed_item.completed)

        # Then mark incomplete
        incomplete_item = self.todo_list.mark_incomplete(1)
        self.assertEqual(incomplete_item.id, 1)
        self.assertFalse(incomplete_item.completed)

    def test_mark_nonexistent_item_raises_error(self):
        """Test that marking a non-existent item raises ValueError"""
        with self.assertRaises(ValueError):
            self.todo_list.mark_complete(999)

        with self.assertRaises(ValueError):
            self.todo_list.mark_incomplete(999)


if __name__ == '__main__':
    unittest.main()