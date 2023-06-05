# `token_util.py` User Documentation

The `token_util.py` module, part of the `app.utils` package, provides a set of utility functions for creating, decoding, and managing JWT (JSON Web Tokens) tokens. These tokens are used for secure user authentication and maintaining sessions in the application. 

## Functions

- **create_access_token(user_id: str)**: This function creates an access token for the given user ID. The expiration time of the token is fetched from the application's configuration.

- **create_refresh_token(user_id: str)**: This function creates a refresh token for the given user ID. The expiration time of the refresh token is longer than the access token and is fetched from the application's configuration.

- **decode_token(token)**: This function decodes the provided token. If the token has expired, it will return an unauthorized error. Similarly, if the token is invalid, an unauthorized error will be returned.

- **create_tokens(user_id: str)**: This function is a convenience function that creates both an access token and a refresh token for the provided user ID.

- **generate_access_token_from_refresh_token(refresh_token: str)**: This function decodes the provided refresh token and creates a new access token from the user ID contained in the refresh token. If the refresh token is invalid, it will return an unauthorized error.

## Usage

To utilize these functions, import the required ones from the `app.utils.token_util` module and use them in your code as needed.

For example:

```python
from app.utils import token_util

def login(user_id):
    access_token, refresh_token = token_util.create_tokens(user_id)
    # use the tokens as needed
```

In this example, the `create_tokens` function is used to create both an access token and a refresh token for a given user ID. The returned tokens can then be used to maintain a secure session for the user.