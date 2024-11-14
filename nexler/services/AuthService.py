from flask import g
from functools import wraps
from jwt import decode, ExpiredSignatureError, InvalidTokenError
from werkzeug import exceptions

import config
from nexler.utils import request_util


class UserService:
    @property
    def userId(self):
        try:
            auth_header = request_util.headers('Authorization')
            if auth_header:
                token = auth_header.split(" ")[1]
                if token and token != 'null':
                    data = decode(token, config.Config().JWT_SECRET_KEY, algorithms="HS256")
                    return data.get('user_id', None)
            return None
        except ExpiredSignatureError:
            raise exceptions.Unauthorized(description="Token has expired.")
        except InvalidTokenError:
            raise exceptions.BadRequest

    def protected(self, f):
        @wraps(f)
        def wrapper(*args, **kwargs):
            g.user_id = self.userId
            if not g.user_id:
                return {"message": "Unauthorized"}, 401
            else:
                return f(*args, **kwargs)

        return wrapper

    @property
    def Id(self):
        return g.get('user_id')


user = UserService()
protected = user.protected
