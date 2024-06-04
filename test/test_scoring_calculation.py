#Test Case 3: Verify Scoring Calculation
import unittest
from quiz_application import QuizApplication

class TestScoringCalculation(unittest.TestCase):

    def setUp(self):
        self.app = QuizApplication()

    def test_scoring_calculation(self):
        # Set up user responses and questions
        user_responses = ["A", "B", "C"]
        questions = self.app.load_quiz_questions()

        # Calculate user score
        score = self.app.calculate_score(user_responses, questions)

        # Assert user score calculation is correct
        self.assertEqual(score, 250)  # Example score for correct answers and time bonus

if __name__ == '__main__':
    unittest.main()
