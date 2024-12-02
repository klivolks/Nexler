import unittest
import datetime
from unittest.mock import patch
import jwt
from nexler.utils.token_util import decode_token

from nexler.utils import config_util, dt_util, str_util
from nexler.utils import token_util


class TestTokenUtil(unittest.TestCase):

    @patch('nexler.utils.token_util.JWT_SECRET_KEY', config_util.Config().get('JWT_SECRET_KEY'))
    @patch('nexler.utils.token_util.JWT_ALGORITHM', config_util.Config().get('JWT_ALGORITHM'))
    def setUp(self):
        self.user_id = str_util.generate_random_token(10)

    def test_create_access_token(self):
        token = token_util.create_access_token(self.user_id)
        self.assertIsNotNone(token)

    def test_create_refresh_token(self):
        token = token_util.create_refresh_token(self.user_id)
        self.assertIsNotNone(token)

    def test_create_tokens(self):
        access_token, refresh_token = token_util.create_tokens(self.user_id)
        self.assertIsNotNone(access_token)
        self.assertIsNotNone(refresh_token)

    def test_decode_token(self):
        token = token_util.create_access_token(self.user_id)
        payload = token_util.decode_token(token)
        if isinstance(payload, tuple):  # If error response returned
            payload = payload[0]
        self.assertEqual(payload["user_id"], self.user_id)

    def test_decode_token_expired(self):
        # Simulate a pastime for token's expiration
        past_time = dt_util.get_current_time() - datetime.timedelta(
            minutes=2 * int(config_util.Config().get('ACCESS_TOKEN_EXPIRE_MINUTES')))
        # Create a token with a past expiration time
        payload = {
            "user_id": self.user_id,
            "exp": past_time,
            "token_type": "access"
        }
        token = jwt.encode(payload, token_util.JWT_SECRET_KEY, algorithm=token_util.JWT_ALGORITHM)
        # Now the token should be expired
        response = token_util.decode_token(token)
        if isinstance(response, tuple):  # If error response returned
            response = response[0]
        self.assertEqual(response["message"], "Token has expired")

    def test_generate_access_token_from_invalid_refresh_token(self):
        access_token = token_util.create_access_token(self.user_id)
        token = token_util.generate_access_token_from_refresh_token(access_token)
        if isinstance(token, tuple):  # If error response returned
            token = token[0]
        self.assertEqual(token["message"], "Invalid refresh token")

    @patch('nexler.utils.token_util.is_blacklisted')
    @patch('nexler.utils.token_util.jwt.decode')
    def test_missing_token(self, mock_jwt_decode, mock_is_blacklisted):
        token = decode_token(None)
        if isinstance(token, tuple):  # If error response returned
            token = token[0]
        self.assertEqual(token["message"], "Missing token")

    @patch('nexler.utils.token_util.is_blacklisted')
    @patch('nexler.utils.token_util.jwt.decode')
    def test_revoked_token(self, mock_jwt_decode, mock_is_blacklisted):
        mock_is_blacklisted.return_value = True
        result = decode_token("revoked_token")
        if isinstance(result, tuple):  # If error response returned
            result = result[0]
        self.assertEqual(result["message"], "Token has been revoked.")
        mock_is_blacklisted.assert_called_once_with("revoked_token")

    @patch('nexler.utils.token_util.is_blacklisted')
    @patch('nexler.utils.token_util.jwt.decode')
    def test_expired_token(self, mock_jwt_decode, mock_is_blacklisted):
        mock_is_blacklisted.return_value = False
        mock_jwt_decode.side_effect = jwt.ExpiredSignatureError
        result = decode_token("expired_token")
        if isinstance(result, tuple):  # If error response returned
            result = result[0]
        self.assertEqual(result["message"], "Token has expired")
        mock_jwt_decode.assert_called_once()

    @patch('nexler.utils.token_util.is_blacklisted')
    @patch('nexler.utils.token_util.jwt.decode')
    def test_invalid_token(self, mock_jwt_decode, mock_is_blacklisted):
        mock_is_blacklisted.return_value = False
        mock_jwt_decode.side_effect = jwt.InvalidTokenError
        result = decode_token("invalid_token")
        if isinstance(result, tuple):  # If error response returned
            result = result[0]
        self.assertEqual(result["message"], "Invalid token")
        mock_jwt_decode.assert_called_once()


if __name__ == '__main__':
    unittest.main()
