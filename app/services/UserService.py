from flask import g
from functools import wraps
from jwt import decode, PyJWTError

import config
from app.utils import request_util


class UserService:
    @property
    def userId(self):
        try:
            data = decode(request_util.headers('X-Access-Token'), config.Config().JWT_SECRET_KEY, algorithms="HS256")
            return data.get('user_id', None)
        except PyJWTError:
            return None

    def protected(self, f):
        @wraps(f)
        def wrapper(*args, **kwargs):
            if not g.get('user_id', None):
                return {"message": "Unauthorized"}, 401
            else:
                return f(*args, **kwargs)

        return wrapper


user = UserService()
protected = user.protected
