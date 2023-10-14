import unittest
from unittest.mock import patch, Mock
import asyncio

# Assuming your original file's name is 'api_services.py'
from app.services import ApiService, ExternalApi, InternalApi


class ApiServiceTest(unittest.TestCase):

    @patch('app.utils.request_util.headers')
    @patch('daba.Mongo.collection')
    def test_verify_request(self, MockCollection, MockHeaders):
        # Mock the necessary methods and attributes
        MockHeaders.return_value = "mock_value"

        mock_collection_instance = Mock()
        mock_collection_instance.getAfterCount.return_value = None
        MockCollection.return_value = mock_collection_instance

        api_service = ApiService()
        self.assertFalse(api_service.verified)


class ExternalApiTest(unittest.TestCase):

    def test_init(self):
        ext_api = ExternalApi(url="http://test.com")
        self.assertEqual(ext_api.headers['User-Agent'], "Nexler/1.1")

    @patch('httpx.AsyncClient')
    def test_fetch(self, MockAsyncClient):
        # Create a coroutine mock for the async method
        async def mock_get(*args, **kwargs):
            mock_response = Mock()
            mock_response.status_code = 200
            mock_response.headers = {'content-type': 'application/json'}
            mock_response.text = '{}'
            return mock_response

        MockAsyncClient.return_value.__aenter__.return_value.get = mock_get
        ext_api = ExternalApi(url="http://test.com")

        loop = asyncio.get_event_loop()
        result = loop.run_until_complete(ext_api.fetch('get'))
        self.assertEqual(result, {})


class InternalApiTest(unittest.TestCase):

    @patch('app.utils.config_util.Config.get')
    def test_init(self, MockConfigGet):
        MockConfigGet.return_value = "mock_value"

        int_api = InternalApi()

        # Checking for each header
        self.assertEqual(int_api.headers['User-Agent'], "Nexler/1.1")
        self.assertEqual(int_api.headers['Authorization'], f"Bearer {int_api.token}")
        self.assertEqual(int_api.headers['Accept'], "application/json")
        self.assertEqual(int_api.headers['Content-Type'], "application/json")
        self.assertEqual(int_api.headers['X-API-Key'], "mock_value")
        self.assertEqual(int_api.headers['Referer'], "mock_value")


# More tests can be added based on the above pattern

if __name__ == "__main__":
    unittest.main()
