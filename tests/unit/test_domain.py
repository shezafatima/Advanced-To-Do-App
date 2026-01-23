import unittest
from src.todo.domain import TodoItem


class TestTodoItem(unittest.TestCase):
    """Unit tests for TodoItem domain entity"""

    def test_create_valid_todo_item(self):
        """Test creating a valid TodoItem"""
        item = TodoItem(id=1, description="Test description", completed=False)
        self.assertEqual(item.id, 1)
        self.assertEqual(item.description, "Test description")
        self.assertFalse(item.completed)

    def test_create_todo_item_defaults(self):
        """Test TodoItem with default completed value"""
        item = TodoItem(id=1, description="Test description")
        self.assertEqual(item.id, 1)
        self.assertEqual(item.description, "Test description")
        self.assertFalse(item.completed)

    def test_create_todo_item_completed_true(self):
        """Test TodoItem with completed=True"""
        item = TodoItem(id=1, description="Test description", completed=True)
        self.assertEqual(item.id, 1)
        self.assertEqual(item.description, "Test description")
        self.assertTrue(item.completed)

    def test_invalid_id_negative(self):
        """Test TodoItem with negative ID raises ValueError"""
        with self.assertRaises(ValueError):
            TodoItem(id=-1, description="Test description")

    def test_invalid_id_zero(self):
        """Test TodoItem with zero ID raises ValueError"""
        with self.assertRaises(ValueError):
            TodoItem(id=0, description="Test description")

    def test_invalid_id_not_integer(self):
        """Test TodoItem with non-integer ID raises ValueError"""
        with self.assertRaises(ValueError):
            TodoItem(id="1", description="Test description")

    def test_invalid_description_empty(self):
        """Test TodoItem with empty description raises ValueError"""
        with self.assertRaises(ValueError):
            TodoItem(id=1, description="")

    def test_invalid_description_whitespace_only(self):
        """Test TodoItem with whitespace-only description raises ValueError"""
        with self.assertRaises(ValueError):
            TodoItem(id=1, description="   ")

    def test_invalid_description_none(self):
        """Test TodoItem with None description raises ValueError"""
        with self.assertRaises(ValueError):
            TodoItem(id=1, description=None)

    def test_invalid_completed_not_boolean(self):
        """Test TodoItem with non-boolean completed raises ValueError"""
        with self.assertRaises(ValueError):
            TodoItem(id=1, description="Test", completed="true")


if __name__ == '__main__':
    unittest.main()