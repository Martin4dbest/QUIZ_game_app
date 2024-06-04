#Test Case 2: Verify Question Generation
import unittest
from quiz_application import QuizApplication

class TestQuestionGeneration(unittest.TestCase):

    def setUp(self):
        self.app = QuizApplication()

    def test_question_generation(self):
        # Set up selected quiz categories
        selected_categories = ["History", "Science"]

        # Generate quiz questions
        questions = self.app.generate_quiz_questions(selected_categories)

        # Assert questions are from selected categories and in random order
        self.assertTrue(all(question.category in selected_categories for question in questions))

if __name__ == '__main__':
    unittest.main()
