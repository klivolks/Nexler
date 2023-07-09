from flask import Flask
from flask.testing import FlaskClient
from io import BytesIO
import unittest
from werkzeug.datastructures import Headers
from app.utils import response_util, request_util


class TestRequestFunctions(unittest.TestCase):
    def setUp(self):
        self.app = Flask(__name__)
        self.client = self.app.test_client()

    def test_form_data(self):
        with self.app.test_request_context(data={'test_field': 'test_value'}):
            self.assertEqual(request_util.form_data('test_field'), 'test_value')

    def test_json_data(self):
        with self.app.test_request_context(json={'test_field': 'test_value'}):
            self.assertEqual(request_util.json_data('test_field'), 'test_value')

    def test_query_params(self):
        with self.app.test_request_context(query_string={'test_field': 'test_value'}):
            self.assertEqual(request_util.query_params('test_field'), 'test_value')

    def test_file(self):
        data = {'test_file': (BytesIO(b'my file contents'), 'test_file.txt')}
        with self.app.test_request_context(data=data):
            file = request_util.file('test_file')
            self.assertEqual(file.filename, 'test_file.txt')

    def test_headers(self):
        with self.app.test_request_context(headers=Headers([('test_header', 'test_value')])):
            self.assertEqual(request_util.headers('test_header'), 'test_value')

    def test_form_data_error(self):
        def error_validator(x):
            raise ValueError('Error message')

        with self.app.test_request_context(data={'test_field': 'test_value'}):
            expected_response = response_util.bad_request('Error message')
            actual_response = request_util.form_data('test_field', validator=error_validator)  # don't use assertRaises here
            self.assertEqual(expected_response, actual_response)


if __name__ == '__main__':
    unittest.main()
