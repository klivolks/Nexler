import asyncio
from flask import g
from functools import wraps
from werkzeug.exceptions import Unauthorized, InternalServerError, Forbidden

from nexler.services.LoggerService import LoggerService
from nexler.utils import token_util, request_util, error_util, config_util


class AuthService:
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
            LoggerService().log("No token found")
            return None
        except Exception as e:
            raise Unauthorized(f'Authentication failed: {e}')

    def has_permission(self, user_id, resource_id):
        """
        Checks if the user has access to the specified resource based on ABAC policies.

        Args:
            user_id (str): The unique identifier of the user.
            resource_id (str): The unique identifier of the resource.

        Returns:
            bool: True if the user has permission, False otherwise.
        """

        if config_util.Config().get("REDIS_CACHING") and config_util.Config().get("REDIS_CACHING") == "on":
            from nexler.services.Caching import RedisService
            cache = RedisService().get_string(f"user:{user_id},resource:{resource_id}")
            if cache:
                if cache == "granted":
                    return True
                return False

        from nexler.services.ApiService import InternalApi
        api = InternalApi('AuthService', "/permission/check", {"user_id": user_id, "resource_id": resource_id})
        response = asyncio.run(api.fetch('post'))
        if response.get('status') == 'success':
            if config_util.Config().get("REDIS_CACHING") and config_util.Config().get("REDIS_CACHING") == "on":
                RedisService().set_string(f"user:{user_id},resource:{resource_id}", response.get('access'))
            if response.get('access') == 'granted':
                return True
            return False

        raise SystemError(response.get('message'))

    def protected(self, resource_id=None):
        """
        Decorator to protect routes by requiring a valid user token.
        Optionally enforces ABAC if resource_id is provided.
        """

        def decorator(f):
            @wraps(f)
            def wrapper(*args, **kwargs):
                g.user_id = self.userId
                if g.user_id:
                    # Perform ABAC check if a resource_id is provided
                    if isinstance(resource_id, str):
                        if not self.has_permission(g.user_id, resource_id):
                            return {"message": "Forbidden: Access denied"}, 403
                    return f(*args, **kwargs)
                return {"message": "Unauthorized: Please log in"}, 401

            return wrapper

        # Return the actual decorator for parameterized use
        if callable(resource_id):
            return decorator(resource_id)
        return decorator

    @property
    def Id(self):
        """
        Get user_id from Flask's global context (g).
        """
        return g.get('user_id')

    @staticmethod
    def logout():
        """
        Invalidate the current user's token by adding it to a blacklist or taking equivalent action.
        If you are not using a blacklist, logout can be treated as a client-side operation which is not safe.
        """
        try:
            auth_header = request_util.headers('Authorization')
            if not auth_header:
                raise Forbidden('No authorisation header present.')

            token_parts = auth_header.split(" ")
            if len(token_parts) != 2 or token_parts[0].lower() != "bearer":
                raise Forbidden('No valid token')

            token = token_parts[1]

            # Add the token to a blacklist (if implemented)
            if token_util.add_to_blacklist(token):
                return True

            raise InternalServerError("Failed to logout")
        except Exception as e:
            raise error_util.handle_http_exception(e)


# Initialize the UserService
user = AuthService()
protected = user.protected
