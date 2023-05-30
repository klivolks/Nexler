import unittest
from app.components.HelloWorld import HelloWorld

class HelloWorldTestCase(unittest.TestCase):
    def setUp(self):
        self.hello_world = HelloWorld()

    def test_get(self):
        response = self.hello_world.get()

        self.assertEqual(response['Message'], 'This is nexler framework for restful apis by klivolks')
        self.assertIsInstance(response['Services'], list)
        self.assertIsInstance(response['Utilities'], list)

if __name__ == '__main__':
    unittest.main()
