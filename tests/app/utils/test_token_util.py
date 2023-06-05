import unittest
import datetime
from unittest.mock import patch
import jwt
from app.utils import token_util, config_util, dt_util, error_util


class TestTokenUtil(unittest.TestCase):

    @patch('app.utils.token_util.JWT_SECRET_KEY', config_util.Config().get('JWT_SECRET_KEY'))
    @patch('app.utils.token_util.JWT_ALGORITHM', config_util.Config().get('JWT_ALGORITHM'))
    def setUp(self):
        self.user_id = 'test_user'

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


if __name__ == '__main__':
    unittest.main()
