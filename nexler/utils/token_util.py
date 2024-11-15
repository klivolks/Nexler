import traceback

import jwt
from nexler.utils import config_util, dt_util, error_util, dir_util
import base64
from cryptography.hazmat.primitives.asymmetric import padding
from cryptography.hazmat.primitives import hashes, serialization

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
        print(traceback.format_exc())
        return error_util.handle_unauthorized("Invalid or corrupted token")


def create_access_token(user_id: str):
    try:
        payload = {
            "user_id": user_id,
            "exp": dt_util.add_minutes(dt_util.get_current_time(), ACCESS_TOKEN_EXPIRE_MINUTES),
            "token_type": "access"
        }
        jwt_token = jwt.encode(payload, JWT_SECRET_KEY, algorithm=JWT_ALGORITHM)
        if JWE_ENCRYPTION == 'on':
            return encrypt_jwt(jwt_token)
        return jwt_token
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
        jwt_token = jwt.encode(payload, JWT_SECRET_KEY, algorithm=JWT_ALGORITHM)
        if JWE_ENCRYPTION == 'on':
            return encrypt_jwt(jwt_token)
        return jwt_token
    except Exception as e:
        return error_util.handle_server_error(e)


def decode_token(token):
    try:
        if JWE_ENCRYPTION == 'on':
            token = decrypt_jwe(token)
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
