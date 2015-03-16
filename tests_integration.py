"""
Integration/functional tests to check that the Flask routes
are working properly.
"""

import unittest
import controller
import model


class LoggedInRouting(unittest.TestCase):

    def setUp(self):
        controller.app.config['TESTING'] = True
        controller.app.config['CSRF_ENABLED'] = False
        self.app = controller.app.test_client()

    def login(self):
        with self.app:
            result = self.app.post("/login", data={
                "email": "asd@asd.com", "password": "qwerty"},
                follow_redirects=True)

    def test_home(self):
        result = self.app.get("/")
        self.assertIn("Let's Get Started", result.data)

    def test_profile(self):
        self.login()
        result = self.app.get("/profile", follow_redirects=True)
        self.assertIn("Summary", result.data)

    def test_login(self):
        self.login()
        result = self.app.get("/results", follow_redirects=True)
        self.assertIn("Help Me Understand", result.data)

    def test_investments(self):
        self.login()
        result = self.app.get("/investments", follow_redirects=True)
        self.assertIn("Portfolio Allocation", result.data)


class LoggedOutRouting(unittest.TestCase):

    def setUp(self):
        controller.app.config['TESTING'] = True
        controller.app.config['CSRF_ENABLED'] = False
        self.app = controller.app.test_client()

    def test_home(self):
        result = self.app.get("/")
        self.assertIn("Let's Get Started", result.data)

    def test_profile(self):
        result = self.app.get("/profile", follow_redirects=True)
        self.assertIn("Please Sign In", result.data)

    def test_results(self):
        result = self.app.get("/results", follow_redirects=True)
        self.assertIn("Please Sign In", result.data)

    def test_investments(self):
        result = self.app.get("/investments", follow_redirects=True)
        self.assertIn("Please Sign In", result.data)


if __name__ == "__main__":
    unittest.main()
