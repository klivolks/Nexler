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

        self.assertEqual(json_response['data']['Message'], 'This is Nexler framework for restful APIs by klivolks')
        self.assertIsInstance(json_response['data']['Services'], list)
        self.assertIsInstance(json_response['data']['Utilities'], list)


if __name__ == '__main__':
    unittest.main()
