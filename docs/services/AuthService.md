# Auth Service Documentation

## Overview

The Auth Service is a centralized component that manages user authentication and authorization in your application. It supports two modes of token-based authentication: **JWT (JSON Web Token)** and **JWE (JSON Web Encryption)**.

- **JWT**: Standard token-based authentication.
- **JWE**: Adds a layer of encryption to JWT. To enable JWE, a PEM certificate is required. This certificate must be shared across all your microservices to ensure consistency.

For detailed documentation on JWE, refer to the [Token Utilities Documentation](/docs/utils/token_utils.md).

---

## Usage

### 1. Securing Functions with the `protected` Decorator

The `protected` decorator secures your functions by ensuring that the user is authenticated. If the user is not logged in or has an invalid token, the request will return a `401 Unauthorized` error.

**Example:**
```python
from nexler.services.AuthService import protected

@protected
def MyFunction():
    # Your logic here
    pass
```

---

### 2. Accessing the Current User

You can retrieve the currently logged-in user's ID by combining the `protected` decorator with the `user` service. The `user.Id` property provides seamless access to the authenticated user's unique identifier.

**Example:**
```python
from nexler.services.AuthService import protected, user

@protected
def MyFunction():
    current_user = user.Id
    print(f"Current logged-in user ID: {current_user}")
```

---

### 3. Logging Out the Current User

The `logout` method allows you to log out the current user by blacklisting their token. Once a token is blacklisted, it cannot be used for further authentication.

**Example:**
```python
from nexler.services.AuthService import protected, user

@protected
def MyFunction():
    response = user.logout()
    if response:
        print("User logged out successfully.")
    else:
        print("Failed to log out the user.")
```

---

## Key Features
- **Token-Based Authentication**: Lightweight and stateless user session management.
- **Secure Token Revocation**: Ensures tokens can be invalidated when users log out.
- **Support for Encrypted Tokens (JWE)**: Enhances security for sensitive environments.

This documentation provides the foundational steps to integrate and use the Auth Service effectively in your applications.