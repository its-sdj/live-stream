import unittest
from app import app

class TestApp(unittest.TestCase):
    def setUp(self):
        self.app = app.test_client()
        self.app.testing = True

    def test_login_page(self):
        response = self.app.get('/')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Live Stream Login', response.data)

    def test_login_success(self):
        response = self.app.post('/', data={'username': 'admin', 'password': 'admin123'})
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Welcome, admin!', response.data)

    def test_login_failure(self):
        response = self.app.post('/', data={'username': 'admin', 'password': 'wrong'})
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Invalid credentials', response.data)

if __name__ == '__main__':
    unittest.main() 
