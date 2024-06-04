import unittest
from quiz_data_structure import QuizDataStructure

class TestQuizDataStructure(unittest.TestCase):

    def setUp(self):
        # Initialize the QuizDataStructure instance
        self.quiz_data = QuizDataStructure()
        
        # Add some sample quiz data for testing
        self.quiz_data.add_category("History")
        self.quiz_data.add_category("Science")
        self.quiz_data.add_question("History", "Who was the first president of the United States?", "George Washington", ["John Adams", "Thomas Jefferson", "James Madison"])
        self.quiz_data.add_question("Science", "What is the chemical symbol for water?", "H2O", ["CO2", "O2", "HCl"])

    def test_quiz_data_structure(self):
        # Test category addition
        categories = self.quiz_data.get_categories()
        self.assertEqual(len(categories), 2)
        self.assertIn("History", categories)
        self.assertIn("Science", categories)

        # Test question addition
        history_questions = self.quiz_data.get_questions("History")
        self.assertEqual(len(history_questions), 1)
        self.assertEqual(history_questions[0]["question"], "Who was the first president of the United States?")

        science_questions = self.quiz_data.get_questions("Science")
        self.assertEqual(len(science_questions), 1)
        self.assertEqual(science_questions[0]["question"], "What is the chemical symbol for water?")

    def test_user_score_tracking(self):
        # Test user score tracking
        self.quiz_data.update_user_score("JohnDoe", "History", 100)
        self.quiz_data.update_user_score("JohnDoe", "Science", 80)
        user_scores = self.quiz_data.get_user_scores("JohnDoe")
        self.assertEqual(user_scores["History"], 100)
        self.assertEqual(user_scores["Science"], 80)

if __name__ == '__main__':
    unittest.main()
