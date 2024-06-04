#Test Case 5: Verify Timer Functionality
import unittest
from quiz_application import QuizApplication

class TestTimerFunctionality(unittest.TestCase):

    def setUp(self):
        self.app = QuizApplication()

    def testtimer_functionality(self):
        # Start a quiz session
        self.app.start_quiz_session()

        # Simulate timer countdown
        for _ in range(10):
            self.app.update_timer()  # Update timer every second

        # Assert timer countdown is working correctly
        self.assertEqual(self.app.get_timer(), 0)  # Timer should reach zero after 10 seconds

if __name__ == '__main__':
    unittest.main()
