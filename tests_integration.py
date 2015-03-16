"""
Integration/functional tests to check that the Flask routes
are working properly.
"""

import unittest
import controller
import model


class LoggedInRouting(unittest.TestCase):
   
    def setUp(self):
        self.app = controller.app.test_client()

    def tearDown(self):
        pass

    def get_user():
        user = getattr(g, "user", None)
        if user is None:
            user = fetch_current_user_from_database()
            g.user = user
        return user

    def test_profile(self):
        with self.app:
            result = self.app.post("/login", data={
                "email": "asd@asd.com", "password": "qwerty"})
            self.assertIn("<h3> Summary </h3>", result.data)

    def test_home(self):
        result = self.app.get("/")
        self.assertIn("Let's Get Started", result.data)

    
if __name__ == "__main__":
    unittest.main()
