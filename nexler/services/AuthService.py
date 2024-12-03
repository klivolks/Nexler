from flask import g
from functools import wraps
from nexler.utils import token_util, request_util, error_util


class UserService:
    @property
    def userId(self):
        """
        Extract user_id from JWT token in Authorization header.
        """
        try:
            auth_header = request_util.headers('Authorization')
            if auth_header:
                token_parts = auth_header.split(" ")
                token = token_parts[1] if len(token_parts) > 1 else None
                if token and token != 'null':
                    data = token_util.decode_token(token)
                    return data.get('user_id')
            return None
        except Exception as e:
            raise error_util.handle_server_error(f'Authentication failed: {e}')

    def protected(self, f):
        """
        Decorator to protect routes by requiring a valid user token.
        """
        @wraps(f)
        def wrapper(*args, **kwargs):
            g.user_id = self.userId
            if g.user_id:
                return f(*args, **kwargs)
            return {"message": "Unauthorized"}, 401

        return wrapper

    @property
    def Id(self):
        """
        Get user_id from Flask's global context (g).
        """
        return g.get('user_id')


# Initialize the UserService
user = UserService()
protected = user.protected
