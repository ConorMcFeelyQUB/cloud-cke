import unittest
from app import app

class TestFunction(unittest.TestCase):

    def setUp(self):
        self.app = app.test_client()

    #testing any changes that have just been made

    def test_response_OK(self):
        rv = self.app.get('/')
        assert rv.status == "200 OK"


if __name__ == '__main__':
    unittest.main()
