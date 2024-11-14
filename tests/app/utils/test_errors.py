import unittest
from unittest.mock import patch
from werkzeug.exceptions import BadRequest, Unauthorized, Forbidden, NotFound, MethodNotAllowed, Conflict, \
    UnsupportedMediaType, InternalServerError, NotImplemented

from nexler.utils import error_util


class TestErrorHandlers(unittest.TestCase):
    error_types = [
        (BadRequest, 'bad_request', 'mock bad request response', 400),
        (Unauthorized, 'unauthorized', 'mock unauthorized response', 401),
        (Forbidden, 'forbidden', 'mock forbidden response', 403),
        (NotFound, 'not_found', 'mock not found response', 404),
        (MethodNotAllowed, 'method_not_allowed', 'mock method not allowed response', 405),
        (Conflict, 'conflict', 'mock conflict response', 409),
        (UnsupportedMediaType, 'unsupported_media_type', 'mock unsupported media type response', 415),
        (InternalServerError, 'server_error', 'mock server error response', 500),
        (NotImplemented, 'not_implemented', 'mock not implemented response', 501)
    ]

    def test_handle_http_exception(self):
        for error_type, response_name, mock_response, status_code in self.error_types:
            with patch(f'nexler.utils.response_util.{response_name}', return_value=mock_response) as mock_response_util:
                try:
                    raise error_type(description=f'Test {response_name} exception')
                except error_type as e:
                    response = error_util.handle_http_exception(e)
                    mock_response_util.assert_called()
                    self.assertEqual(response, mock_response)

    def test_specific_exception_handlers(self):
        specific_errors = [
            ('handle_bad_request', ValueError, 'mock bad request response'),
            ('handle_key_error', KeyError, 'mock key error response'),
            ('handle_value_error', ValueError, 'mock value error response'),
            ('handle_type_error', TypeError, 'mock type error response'),
            ('handle_index_error', IndexError, 'mock index error response'),
            ('handle_attribute_error', AttributeError, 'mock attribute error response'),
            ('handle_zero_division_error', ZeroDivisionError, 'mock zero division error response')
        ]

        for handler, exception_type, mock_response in specific_errors:
            with patch(f'nexler.utils.response_util.bad_request', return_value=mock_response) as mock_response_util:
                exception = exception_type(f'Test {handler} exception')
                response = getattr(error_util, handler)(exception)
                mock_response_util.assert_called()
                self.assertEqual(response, mock_response)


if __name__ == '__main__':
    unittest.main()
