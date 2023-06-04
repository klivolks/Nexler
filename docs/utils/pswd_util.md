# `pswd_util.py` User Documentation

`pswd_util.py` module provides utility functions to hash passwords and verify hashed passwords. This module is part of the `app.utils` package.

## Functions

The main functions defined in this module are `hash_password` and `check_password`.

### hash_password

The `hash_password` function is used to generate an Argon2 hash from a given password.

#### Parameters

- **password**: This is a string that represents the plain-text password to be hashed.

#### Returns

This function returns the hashed password as a string.

### check_password

The `check_password` function is used to verify a given plain-text password against a hashed password.

#### Parameters

- **password**: This is a string that represents the plain-text password to be verified.
- **hashed_password**: This is a string that represents the hashed password to verify against.

#### Returns

This function returns a boolean. It returns True if the plain-text password matches the hashed password, and False otherwise.

## Usage

To use these utility functions, simply import the `hash_password` and `check_password` functions from the `app.utils.pswd_util` module and use them in your code where needed.

For example:

```python
from app.utils.pswd_util import hash_password, check_password

# Hash a password
hashed_password = hash_password('my_password')

# Verify a password
is_valid = check_password('my_password', hashed_password)  # This will return True
```

In this example, the `hash_password` function is used to hash the string 'my_password', and the `check_password` function is used to verify the plain-text password 'my_password' against the hashed password. If the hashed password was generated from the plain-text password, the `check_password` function will return True.