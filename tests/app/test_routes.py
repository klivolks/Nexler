import os
import unittest
from run import create_app


class RoutesTestCase(unittest.TestCase):
    def setUp(self):
        os.environ["FLASK_ENV"] = "Testing"
        self.app = create_app()
        self.client = self.app.test_client()

    def test_hello_world_route(self):
        response = self.client.get('/')
        self.assertEqual(response.status_code, 200)

        json_response = response.get_json()

        self.assertEqual(json_response['Message'], 'This is nexler framework for restful apis by klivolks')
        self.assertIsInstance(json_response['Services'], list)
        self.assertIsInstance(json_response['Utilities'], list)


if __name__ == '__main__':
    unittest.main()
