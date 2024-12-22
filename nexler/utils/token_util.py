import jwt

from nexler.utils import config_util, dt_util, error_util, dir_util
import base64
from cryptography.hazmat.primitives.asymmetric import padding
from cryptography.hazmat.primitives import hashes, serialization
from nexler.services.Caching import RedisService
from werkzeug.exceptions import Unauthorized

JWT_SECRET_KEY = config_util.Config().get('JWT_SECRET_KEY')
JWT_ALGORITHM = config_util.Config().get('JWT_ALGORITHM')
ACCESS_TOKEN_EXPIRE_MINUTES = int(config_util.Config().get('ACCESS_TOKEN_EXPIRE_MINUTES'))
REFRESH_TOKEN_EXPIRE_DAYS = int(config_util.Config().get('REFRESH_TOKEN_EXPIRE_DAYS'))
JWE_ENCRYPTION = config_util.Config().get('JWE_ENCRYPTION')
PUBLIC_KEY_PATH = f'{dir_util.app_directory}/encryption/public_key.pem' if config_util.Config().get(
    'PUBLIC_KEY_PATH') is None else config_util.Config().get(
    'PUBLIC_KEY_PATH')
PRIVATE_KEY_PATH = f'{dir_util.app_directory}/encryption/private_key.pem' if config_util.Config().get(
    'PRIVATE_KEY_PATH') is None else config_util.Config().get(
    'PRIVATE_KEY_PATH')
SESSION_MANAGEMENT = config_util.Config().get('SESSION_MANAGEMENT')  # app/redis/db

if not SESSION_MANAGEMENT or SESSION_MANAGEMENT == 'app':
    blacklisted_tokens = set()


# Load RSA private key
def load_private_key():
    try:
        with open(PRIVATE_KEY_PATH, "rb") as f:
            return serialization.load_pem_private_key(f.read(), password=None)
    except Exception as e:
        print("Error: ", e)


# Load RSA public key
def load_public_key():
    with open(PUBLIC_KEY_PATH, "rb") as f:
        return serialization.load_pem_public_key(f.read())


def encrypt_jwt(jwt_token: str) -> str:
    public_key = load_public_key()
    """Encrypt JWT token using RSA public key to create JWE token"""
    encrypted_token = public_key.encrypt(
        jwt_token.encode(),
        padding.OAEP(
            mgf=padding.MGF1(algorithm=hashes.SHA256()),
            algorithm=hashes.SHA256(),
            label=None
        )
    )
    return base64.urlsafe_b64encode(encrypted_token).decode('utf-8')


def decrypt_jwe(jwe_token: str) -> str:
    """Decrypt JWE token using RSA private key to retrieve the original JWT token"""
    try:
        private_key = load_private_key()
        encrypted_token = base64.urlsafe_b64decode(jwe_token.encode('utf-8'))
        decrypted_token = private_key.decrypt(
            encrypted_token,
            padding.OAEP(
                mgf=padding.MGF1(algorithm=hashes.SHA256()),
                algorithm=hashes.SHA256(),
                label=None
            )
        )
        return decrypted_token.decode('utf-8')
    except Exception as e:
        return error_util.handle_unauthorized("Invalid or corrupted token")


def create_access_token(data: (str, dict), jwe=True):
    try:
        payload = {
            "exp": dt_util.add_minutes(dt_util.get_current_time(), ACCESS_TOKEN_EXPIRE_MINUTES),
            "token_type": "access"
        }
        if isinstance(data, str):
            payload.update({
                "user_id": data
            })
        else:
            payload.update(data)
        jwt_token = jwt.encode(payload, JWT_SECRET_KEY, algorithm=JWT_ALGORITHM)
        if JWE_ENCRYPTION == 'on' and jwe:
            return encrypt_jwt(jwt_token)
        return jwt_token
    except Exception as e:
        return error_util.handle_server_error(e)


def create_refresh_token(user_id: str):
    try:
        payload = {
            "user_id": user_id,
            "exp": dt_util.add_days(dt_util.get_current_time(), REFRESH_TOKEN_EXPIRE_DAYS),
            "token_type": "refresh"
        }
        jwt_token = jwt.encode(payload, JWT_SECRET_KEY, algorithm=JWT_ALGORITHM)
        if JWE_ENCRYPTION == 'on':
            return encrypt_jwt(jwt_token)
        return jwt_token
    except Exception as e:
        return error_util.handle_server_error(e)


def decode_token(token):
    """
    Decodes a JWT token, with optional JWE decryption.

    :param token: The JWT token to decode.
    :return: The decoded payload or an error response.
    """
    try:
        if not token:
            raise Unauthorized("Missing token")

        if is_blacklisted(token):
            raise Unauthorized("Token has been revoked.")

        # Optional JWE decryption
        if JWE_ENCRYPTION.lower() == 'on':
            token = decrypt_jwe(token)

        # Decode the JWT
        payload = jwt.decode(
            token,
            JWT_SECRET_KEY,
            algorithms=[JWT_ALGORITHM or "HS256"]
        )
        return payload

    except jwt.ExpiredSignatureError:
        raise Unauthorized("Token has expired")

    except jwt.InvalidTokenError:
        raise Unauthorized("Invalid token")

    except Exception as e:
        raise Unauthorized("Token decoding failed")


def create_tokens(data: (str, dict)):
    if isinstance(data, str):
        user_id = data
        access_token = create_access_token(user_id)
    else:
        user_id = data.get('user_id')
        access_token = create_access_token(data)
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


def add_to_blacklist(token):
    """
    Add a token to the blacklist.
    """
    if not SESSION_MANAGEMENT or SESSION_MANAGEMENT == 'app':
        blacklisted_tokens.add(token)
    elif SESSION_MANAGEMENT == 'redis':
        RedisService().set_string(f'token: {token}', 'blacklisted')
    return True


def is_blacklisted(token):
    """
    Check if a token is blacklisted.
    """
    if not SESSION_MANAGEMENT or SESSION_MANAGEMENT == 'app':
        return token in blacklisted_tokens
    elif SESSION_MANAGEMENT == 'redis':
        if RedisService().get_string(f'token: {token}') == 'blacklisted':
            return True
    return False
