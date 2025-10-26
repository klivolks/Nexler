import asyncio
from flask import g
from functools import wraps
from werkzeug.exceptions import Unauthorized, InternalServerError, Forbidden
from nexler.utils import token_util, request_util, error_util, config_util


class AuthService:
    @property
    def userId(self):
        """Extract user_id from JWT token in Authorization header."""
        try:
            auth_header = request_util.headers('Authorization')
            ui_flag = request_util.headers('X-Client-Type') != "internal"

            if auth_header:
                parts = auth_header.split(" ")
                token = parts[1] if len(parts) > 1 else None
                if token and token.lower() != 'null':
                    data = token_util.decode_token(token, ui_flag)
                    return data.get('user_id')
            return None
        except Exception as e:
            raise Unauthorized(f'Authentication failed: {e}')

    @staticmethod
    def has_permission(user_id, resource):
        """Check if user has permission. Resource can be str or dict."""
        from nexler.services.Caching import RedisService
        from nexler.services.ApiService import InternalApi

        redis_on = config_util.Config().get("REDIS_CACHING") == "on"

        cache_key = f"user:{user_id},resource:{resource}" if isinstance(resource, str) else None
        if redis_on and cache_key:
            cache = RedisService().get_string(cache_key)
            if cache:
                return cache == "granted"

        payload = {"user_id": user_id}
        if isinstance(resource, str):
            payload["resource"] = resource
        elif isinstance(resource, dict):
            payload.update(resource)

        api = InternalApi('AuthService', "/permission/check", payload)
        response = api.fetch('post')

        if asyncio.iscoroutine(response):
            try:
                loop = asyncio.get_event_loop()
            except RuntimeError:
                loop = asyncio.new_event_loop()
                asyncio.set_event_loop(loop)
            response = loop.run_until_complete(response)

        if response.get('status') != 'success':
            raise SystemError(response.get('message'))

        access = response.get('access')

        if redis_on and cache_key:
            RedisService().set_string(cache_key, access)

        return access == 'granted'

    def protected(self, resource=None):
        """
        Decorator to protect routes:
        - @protected → only JWT check
        - @protected("resource_id") → static resource ABAC check
        - @protected({...}) → dynamic context ABAC check
        """

        def decorator(f):
            @wraps(f)
            def wrapper(*args, **kwargs):
                g.user_id = self.userId
                if not g.user_id:
                    raise Unauthorized("Unauthorized: Please log in")

                if resource:
                    if not self.has_permission(g.user_id, resource):
                        raise Forbidden("Forbidden: Access denied")

                return f(*args, **kwargs)

            return wrapper

        # Support @protected without parentheses
        if callable(resource) and not hasattr(resource, "__wrapped__"):
            # Used as @protected directly
            return decorator(resource)
        return decorator

    @property
    def Id(self):
        """Get current user_id from Flask context."""
        return g.get('user_id')

    @staticmethod
    def logout():
        """Invalidate the current user's token."""
        try:
            auth_header = request_util.headers('Authorization')
            if not auth_header:
                raise Forbidden('No authorization header present.')

            parts = auth_header.split(" ")
            if len(parts) != 2 or parts[0].lower() != "bearer":
                raise Forbidden('No valid token.')

            token = parts[1]

            if token_util.add_to_blacklist(token):
                return True

            raise InternalServerError("Failed to logout")
        except Exception as e:
            return error_util.handle_http_exception(e)


# Singleton instance
user = AuthService()
protected = user.protected
