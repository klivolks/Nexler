from flask import Flask
from werkzeug import exceptions
from io import BytesIO
import unittest
from werkzeug.datastructures import Headers
from app.utils import request_util


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
            with self.assertRaises(exceptions.BadRequest) as context:
                request_util.form_data('test_field', validator=error_validator)

            self.assertEqual(str(context.exception), '400 Bad Request: Error message')


if __name__ == '__main__':
    unittest.main()
