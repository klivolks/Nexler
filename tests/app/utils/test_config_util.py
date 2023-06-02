import unittest
import os
from app.utils import config_util


class TestConfigUtil(unittest.TestCase):

    def setUp(self):
        # Creating a temporary environment variable for testing
        os.environ['TEST_CONFIG'] = 'test_value'

        # Creating a Config object with a sample JSON file path
        self.config = config_util.Config('path_to_config_file.json')

    def tearDown(self):
        # Clearing the environment variable after test
        del os.environ['TEST_CONFIG']

    def test_get_config_with_default(self):
        # Testing the get method with default value
        value = self.config.get('NON_EXISTENT_KEY', 'default_value')
        self.assertEqual(value, 'default_value')

    def test_get_config_without_default(self):
        # Testing the get method without default value
        # If the key does not exist, it should return None
        value = self.config.get('NON_EXISTENT_KEY')
        self.assertIsNone(value)

    def test_get_config_from_env(self):
        # Testing the get method with an environment variable
        value = self.config.get('TEST_CONFIG')
        self.assertEqual(value, 'test_value')

    def test_require_config(self):
        # Testing the required method with an environment variable
        value = self.config.require('TEST_CONFIG')
        self.assertEqual(value, 'test_value')

    def test_require_config_non_existent(self):
        # Testing the required method with a non-existent key
        # This should raise a ValueError
        with self.assertRaises(ValueError):
            self.config.require('NON_EXISTENT_KEY')


if __name__ == "__main__":
    unittest.main()
