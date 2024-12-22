import re
from argon2 import PasswordHasher
from werkzeug.exceptions import BadRequest
from nexler.utils import config_util

ph = PasswordHasher()


def hash_password(password: str) -> str:
    """Generate an Argon2 hash of a password."""
    return ph.hash(password)


def check_password(password: str, hashed_password: str) -> bool:
    """Check a plain-text password against a hashed password."""
    try:
        ph.verify(hashed_password, password)
        return True
    except Exception as e:
        return False


def validate_password(password: str):
    """
    Password validation and hashing
    :param password:
    :return: validated hashed password
    """
    if not password:
        raise BadRequest("Password is required.")

    errors = []
    min_length = config_util.Config().get("PASSWORD_MIN_LENGTH") if config_util.Config().get("PASSWORD_MIN_LENGTH") else 8

    if len(password) < min_length:
        errors.append(f"Password must be at least {min_length} characters long.")
    if not re.search(r'[A-Z]', password):
        errors.append("Password must contain at least one uppercase letter.")
    if not re.search(r'[a-z]', password):
        errors.append("Password must contain at least one lowercase letter.")
    if not re.search(r'[0-9]', password):
        errors.append("Password must contain at least one number.")
    if not re.search(r'[!@#$%^&*(),.?\":{}|<>]', password):
        errors.append("Password must contain at least one special character.")
    if re.search(r'\s', password):
        errors.append("Password must not contain spaces.")

    if errors:
        raise BadRequest(", ".join(errors))

    return hash_password(password)
