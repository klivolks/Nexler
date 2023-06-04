from flask import g, request
from functools import wraps
from jwt import decode, PyJWTError
from werkzeug import exceptions

import config
from app.utils import request_util


class UserService:
    @property
    def userId(self):
        try:
            auth_header = request.headers.get('Authorization', None)
            if auth_header:
                token = auth_header.split(" ")[1]
                data = decode(token, config.Config().JWT_SECRET_KEY, algorithms="HS256")
                return data.get('user_id', None)
            return None
        except PyJWTError:
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


user = UserService()
protected = user.protected
