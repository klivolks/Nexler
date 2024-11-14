from argon2 import PasswordHasher

ph = PasswordHasher()


def hash_password(password: str) -> str:
    """Generate an Argon2 hash of a password."""
    return ph.hash(password)


def check_password(password: str, hashed_password: str) -> bool:
    """Check a plain-text password against a hashed password."""
    try:
        ph.verify(hashed_password, password)
        return True
    except:
        return False
