import unittest
from app.utils import response_util

class TestResponseUtil(unittest.TestCase):
    def test_check_data_with_dict(self):
        try:
            response_util.check_data({"key": "value"})
        except TypeError:
            self.fail("check_data() raised TypeError unexpectedly!")

    def test_check_data_with_non_dict_or_list(self):
        with self.assertRaises(TypeError):
            response_util.check_data("not a dict or list")

    def test_success(self):
        data = {"key": "value"}
        expected_response = {"status": "success", "data": data}, 200
        self.assertEqual(response_util.success(data), expected_response)

    def test_created(self):
        data = {"key": "value"}
        expected_response = {"status": "success", "data": data}, 201
        self.assertEqual(response_util.created(data), expected_response)

    def test_accepted_with_data(self):
        data = {"key": "value"}
        expected_response = {"status": "success", "data": data}, 202
        self.assertEqual(response_util.accepted(data), expected_response)

    def test_accepted_without_data(self):
        expected_response = {"status": "success", "data": None}, 202
        self.assertEqual(response_util.accepted(), expected_response)

    def test_no_content(self):
        expected_response = {"status": "success", "data": None}, 204
        self.assertEqual(response_util.no_content(), expected_response)

    def test_error(self):
        message = "Error message"
        expected_response = {"status": "error", "message": message}, 400
        self.assertEqual(response_util.error(message), expected_response)

    def test_bad_request(self):
        message = "Bad Request"
        expected_response = {"status": "error", "message": message}, 400
        self.assertEqual(response_util.bad_request(message), expected_response)

    def test_unauthorized(self):
        message = "Unauthorized"
        expected_response = {"status": "error", "message": message}, 401
        self.assertEqual(response_util.unauthorized(message), expected_response)

    def test_forbidden(self):
        message = "Forbidden"
        expected_response = {"status": "error", "message": message}, 403
        self.assertEqual(response_util.forbidden(message), expected_response)

    def test_not_found(self):
        message = "Not found"
        expected_response = {"status": "error", "message": message}, 404
        self.assertEqual(response_util.not_found(message), expected_response)

    def test_method_not_allowed(self):
        message = "Method not allowed"
        expected_response = {"status": "error", "message": message}, 405
        self.assertEqual(response_util.method_not_allowed(message), expected_response)

    def test_conflict(self):
        message = "Conflict"
        expected_response = {"status": "error", "message": message}, 409
        self.assertEqual(response_util.conflict(message), expected_response)

    def test_unsupported_media_type(self):
        message = "Unsupported Media Type"
        expected_response = {"status": "error", "message": message}, 415
        self.assertEqual(response_util.unsupported_media_type(message), expected_response)

    def test_server_error(self):
        message = "Internal Server Error"
        expected_response = {"status": "error", "message": message}, 500
        self.assertEqual(response_util.server_error(message), expected_response)

    def test_not_implemented(self):
        message = "Not Implemented"
        expected_response = {"status": "error", "message": message}, 501
        self.assertEqual(response_util.not_implemented(message), expected_response)


if __name__ == '__main__':
    unittest.main()
