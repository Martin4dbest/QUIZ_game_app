#Test Case 4: Verify Category Management
import unittest
from quiz_application import QuizApplication

class TestCategoryManagement(unittest.TestCase):

    def setUp(self):
        self.app = QuizApplication()

    def test_add_category(self):
        # Add a new category
        result = self.app.add_category("Geography")

        # Assert category is added successfully
        self.assertTrue(result)

    def test_edit_category(self):
        # Edit an existing category
        result = self.app.edit_category("Science", "Physics")

        # Assert category is edited successfully
        self.assertTrue(result)

    def test_delete_category(self):
        # Delete an existing category
        result = self.app.delete_category("History")

        # Assert category is deleted successfully
        self.assertTrue(result)

if __name__ == '__main__':
    unittest.main()
