import unittest
from unittest.mock import patch, MagicMock
from flask_restful import reqparse
from werkzeug import datastructures

from app.utils import response_util
from app.utils.request_util import email, phone, money, number, decimal_number, form_data, json_data, query_params, file, headers


class TestValidators(unittest.TestCase):
    def test_email(self):
        self.assertEqual(email("test@test.com"), "test@test.com")
        with self.assertRaises(ValueError):
            email("not_an_email")

    def test_phone(self):
        self.assertEqual(phone("1234567890"), "1234567890")
        with self.assertRaises(ValueError):
            phone("not_a_phone_number")

    def test_money(self):
        self.assertEqual(money("123.45"), 123.45)
        with self.assertRaises(ValueError):
            money("not_money")

    def test_number(self):
        self.assertEqual(number("1234567890"), 1234567890)
        with self.assertRaises(ValueError):
            number("not_a_number")

    def test_decimal_number(self):
        self.assertEqual(decimal_number("123.45"), 123.45)
        with self.assertRaises(ValueError):
            decimal_number("not_a_number")


@patch.object(reqparse.RequestParser, 'parse_args')
class TestRequestFunctions(unittest.TestCase):
    def test_form_data(self, mock_parse_args):
        mock_parse_args.return_value = {'test_field': 'test_value'}
        self.assertEqual(form_data('test_field'), 'test_value')

    def test_json_data(self, mock_parse_args):
        mock_parse_args.return_value = {'test_field': 'test_value'}
        self.assertEqual(json_data('test_field'), 'test_value')

    def test_query_params(self, mock_parse_args):
        mock_parse_args.return_value = {'test_field': 'test_value'}
        self.assertEqual(query_params('test_field'), 'test_value')

    def test_file(self, mock_parse_args):
        mock_file = MagicMock(spec=datastructures.FileStorage)
        mock_parse_args.return_value = {'test_file': mock_file}
        self.assertEqual(file('test_file'), mock_file)

    def test_headers(self, mock_parse_args):
        mock_parse_args.return_value = {'test_header': 'test_value'}
        self.assertEqual(headers('test_header'), 'test_value')

    def test_form_data_error(self, mock_parse_args):
        mock_parse_args.return_value = {'test_field': 'test_value'}

        def error_validator(x):
            raise ValueError('Error message')

        expected_response = response_util.bad_request('Error message')
        actual_response = form_data('test_field', validator=error_validator)  # don't use assertRaises here

        self.assertEqual(expected_response, actual_response)


if __name__ == '__main__':
    unittest.main()
