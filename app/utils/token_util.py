import traceback

import jwt
from app.utils import config_util, dt_util, error_util

JWT_SECRET_KEY = config_util.Config().get('JWT_SECRET_KEY')
JWT_ALGORITHM = config_util.Config().get('JWT_ALGORITHM')
ACCESS_TOKEN_EXPIRE_MINUTES = int(config_util.Config().get('ACCESS_TOKEN_EXPIRE_MINUTES'))
REFRESH_TOKEN_EXPIRE_DAYS = int(config_util.Config().get('REFRESH_TOKEN_EXPIRE_DAYS'))


def create_access_token(user_id: str):
    try:
        payload = {
            "user_id": user_id,
            "exp": dt_util.add_minutes(dt_util.get_current_time(), ACCESS_TOKEN_EXPIRE_MINUTES),
            "token_type": "access"
        }
        return jwt.encode(payload, JWT_SECRET_KEY, algorithm=JWT_ALGORITHM)
    except Exception as e:
        print(traceback.format_exc())
        return error_util.handle_server_error(e)


def create_refresh_token(user_id: str):
    try:
        payload = {
            "user_id": user_id,
            "exp": dt_util.add_days(dt_util.get_current_time(), REFRESH_TOKEN_EXPIRE_DAYS),
            "token_type": "refresh"
        }
        return jwt.encode(payload, JWT_SECRET_KEY, algorithm=JWT_ALGORITHM)
    except Exception as e:
        return error_util.handle_server_error(e)


def decode_token(token):
    try:
        payload = jwt.decode(token, JWT_SECRET_KEY, algorithms=[JWT_ALGORITHM])
        return payload
    except jwt.ExpiredSignatureError:
        return error_util.handle_unauthorized("Token has expired")
    except jwt.InvalidTokenError:
        return error_util.handle_unauthorized("Invalid token")


def create_tokens(user_id: str):
    access_token = create_access_token(user_id)
    refresh_token = create_refresh_token(user_id)
    return access_token, refresh_token


def generate_access_token_from_refresh_token(refresh_token: str):
    try:
        payload = decode_token(refresh_token)
        if payload.get('token_type') != 'refresh':
            raise jwt.InvalidTokenError
        user_id = payload.get('user_id')
        return create_access_token(user_id)
    except jwt.InvalidTokenError:
        return error_util.handle_unauthorized("Invalid refresh token")
