# `token_util.py` User Documentation

The `token_util.py` module, part of the `nexler.utils` package, provides a set of utility functions for creating, decoding, and managing JWT (JSON Web Tokens) tokens. These tokens are used for secure user authentication and maintaining sessions in the application. Our system now supports JSON Web Encryption (JWE), offering an additional layer of security essential for financial and healthcare institutions.

## How to Use JWE:
### Set Up Keys:
Ensure that your private and public keys are saved in your app's directory. Define their paths in the environment variables:

```
PRIVATE_KEY_PATH=/path/to/private_key.pem
PUBLIC_KEY_PATH=/path/to/public_key.pem
```

Generate Keys (if needed):
If this is a base app, and you don't already have keys, you can generate them by running the following command in your terminal:

```bash
nexler encrypt generate
```
This will create the required private and public keys.

### Enable JWE:
To activate JWE encryption, add the following to your environment variables:

```JWE_ENCRYPTION=on```

## Functions

- **create_access_token(user_id: str)**: This function creates an access token for the given user ID. The expiration time of the token is fetched from the application's configuration.

- **create_refresh_token(user_id: str)**: This function creates a refresh token for the given user ID. The expiration time of the refresh token is longer than the access token and is fetched from the application's configuration.

- **decode_token(token)**: This function decodes the provided token. If the token has expired, it will return an unauthorized error. Similarly, if the token is invalid, an unauthorized error will be returned.

- **create_tokens(user_id: str)**: This function is a convenience function that creates both an access token and a refresh token for the provided user ID.

- **generate_access_token_from_refresh_token(refresh_token: str)**: This function decodes the provided refresh token and creates a new access token from the user ID contained in the refresh token. If the refresh token is invalid, it will return an unauthorized error.

## Usage

To utilize these functions, import the required ones from the `nexler.utils.token_util` module and use them in your code as needed.

For example:

```python

from nexler.utils import token_util


def login(user_id):
    access_token, refresh_token = token_util.create_tokens(user_id)
    # use the tokens as needed
```

In this example, the `create_tokens` function is used to create both an access token and a refresh token for a given user ID. The returned tokens can then be used to maintain a secure session for the user.