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

The `@protected(resource_id)` decorator can be used to integrate with the `AuthService` for checking permissions. It simplifies Authorization-based Access Control (ABAC) by validating user access to specific resources.

---

### Configuration Setup

To enable this feature, you must create a configuration file named `AuthService.json` in the `app/config` folder. This file should include the following variables:

```json
{
  "API_URL": "http://your-auth-service-url/",
  "API_KEY": "your-api-key"
}
```

- **`API_URL`**: The base URL of your `AuthService`.
- **`API_KEY`**: The API key required for authenticating requests to the `AuthService`.

---

### How It Works

The `@protected(resource_id)` decorator automatically:
1. Extracts the current `user_id` from the session or token.
2. Passes both `user_id` and `resource_id` to the `/permission/check` endpoint of the `AuthService`.

**Endpoint Example**  
A request is made to the following endpoint:
```
POST {API_URL}/permission/check
```

**Request Payload**:
```json
{
  "user_id": "current-user-id",
  "resource_id": "current-resource-id"
}
```

---

### Usage Example

Here's how you can use the `@protected(resource_id)` decorator:

```python
from nexler.services.AuthService import protected

@protected('resource_id')
def my_function():
    # Code to execute if the user has permission
    print("Access granted!")
```

### Notes
1. If the user does not have the required permission, the decorator will block access and return an "Unauthorized" response.
2. Ensure the `AuthService.json` file is correctly set up with valid API details, or the decorator will not function as intended.


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