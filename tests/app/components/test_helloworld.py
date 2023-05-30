import unittest
from unittest.mock import patch, MagicMock
from app.components.HelloWorld import HelloWorld


class HelloWorldTestCase(unittest.TestCase):
    def setUp(self):
        self.hello_world = HelloWorld()
        self.test_data = {
            "Message": "This is Nexler framework for restful APIs by klivolks",
            "Services": ['service1', 'service2'],
            "Utilities": ['utility1', 'utility2']
        }

    @patch('app.components.HelloWorld.HelloWorldLogic')
    def test_get_success(self, mock_logic):
        mock_logic_instance = mock_logic.return_value
        mock_logic_instance.get_all_services.return_value = self.test_data["Services"]
        mock_logic_instance.get_all_utilities.return_value = self.test_data["Utilities"]

        response, status_code = self.hello_world.get()

        self.assertEqual(status_code, 200)
        self.assertEqual(response["status"], "success")
        self.assertDictEqual(response["data"], self.test_data)
        mock_logic_instance.get_all_services.assert_called_once()
        mock_logic_instance.get_all_utilities.assert_called_once()

    @patch('app.components.HelloWorld.HelloWorldLogic')
    def test_get_server_error(self, mock_logic):
        mock_logic_instance = mock_logic.return_value
        mock_logic_instance.get_all_services.side_effect = Exception("Some server error")

        response, status_code = self.hello_world.get()

        self.assertEqual(status_code, 500)
        self.assertEqual(response["status"], "error")
        self.assertEqual(response["message"], "Some server error")
        mock_logic_instance.get_all_services.assert_called_once()
        mock_logic_instance.get_all_utilities.assert_not_called()


if __name__ == '__main__':
    unittest.main()
