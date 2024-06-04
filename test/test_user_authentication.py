#Test Case 1: Verify User Authentication
import unittest
from quiz_application import QuizApplication

class TestUserAuthentication(unittest.TestCase):

    def setUp(self):
        self.app = QuizApplication()

    def test_user_authentication(self):
        # Set up valid user credentials
        username = "test_user"
        password = "password123"

        # Attempt to authenticate user
        result = self.app.authenticate_user(username, password)

        # Assert user authentication is successful
        self.assertTrue(result)

if __name__ == '__main__':
    unittest.main()
