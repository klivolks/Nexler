# Redis Service Documentation

## Overview

Redis is used for in-memory caching purposes to improve server performance. For methods are in this class. To use redis you need following environment variables.

```dotenv
#Redis
REDIS_CACHING=off
REDIS_HOST=localhost
REDIS_PORT=6379
REDIS_AUTH=off
REDIS_USERNAME=your-username
REDIS_PASSWORD=your-password
```

## Importing

Service can be imported using following command.

```python
from nexler.services import RedisService
```

## Usage

```python
from nexler.services import RedisService

redis_db = RedisService()
key = 'token'
value = 'blacklisted'
redis_db.set_string(key, value)
response = redis_db.get_string(key)
key2 = 'user:1'
value2 = {
    "name": "Test"
}
redis_db.set_dict(key2, value2)
response2 = redis_db.get_dict(key2)
```

### Methods

1. **`set_string(key: str, value: str, expiry: int = None) -> bool`**  
   Stores a string value under a specified key.  
   **Parameters:**  
   - `key`: Key to store the value under.  
   - `value`: The string value to store.  
   - `expiry`: (Optional) Expiry time in seconds.  

   **Returns:**  
   - `True` if the operation is successful.  
   - `False` otherwise.  

2. **`get_string(key: str) -> str`**  
   Retrieves the string value stored under a key.  
   **Parameters:**  
   - `key`: Key of the value to retrieve.  

   **Returns:**  
   - The string value if found, `None` otherwise.  

3. **`set_dict(key: str, value: dict, expiry: int = None) -> bool`**  
   Stores a dictionary as a hash under a specified key.  
   **Parameters:**  
   - `key`: Key to store the hash under.  
   - `value`: The dictionary to store.  
   - `expiry`: (Optional) Expiry time in seconds.  

   **Returns:**  
   - `True` if successful, `False` otherwise.  

4. **`get_dict(key: str) -> dict`**  
   Retrieves a dictionary (hash) stored under a key.  
   **Parameters:**  
   - `key`: Key of the hash to retrieve.  

   **Returns:**  
   - The dictionary if found, or an empty dictionary.  

5. **`delete_key(key: str) -> bool`**  
   Deletes a key from Redis.  
   **Parameters:**  
   - `key`: Key to delete.  

   **Returns:**  
   - `True` if the key was deleted, `False` otherwise.  

6. **`key_exists(key: str) -> bool`**  
   Checks if a key exists in Redis.  
   **Parameters:**  
   - `key`: Key to check.  

   **Returns:**  
   - `True` if the key exists, `False` otherwise.  

7. **`set_list(key: str, values: list, expiry: int = None) -> bool`**  
   Stores a list under a specified key.  
   **Parameters:**  
   - `key`: Key to store the list under.  
   - `values`: The list to store.  
   - `expiry`: (Optional) Expiry time in seconds.  

   **Returns:**  
   - `True` if successful, `False` otherwise.  

8. **`get_list(key: str) -> list`**  
   Retrieves a list stored under a key.  
   **Parameters:**  
   - `key`: Key of the list to retrieve.  

   **Returns:**  
   - The list if found, or an empty list.  

9. **`set_set(key: str, values: set, expiry: int = None) -> bool`**  
   Stores a set under a specified key.  
   **Parameters:**  
   - `key`: Key to store the set under.  
   - `values`: The set to store.  
   - `expiry`: (Optional) Expiry time in seconds.  

   **Returns:**  
   - `True` if successful, `False` otherwise.  

10. **`get_set(key: str) -> set`**  
    Retrieves a set stored under a key.  
    **Parameters:**  
    - `key`: Key of the set to retrieve.  

    **Returns:**  
    - The set if found, or an empty set.  

11. **`increment_key(key: str, amount: int = 1) -> int`**  
    Increments the value of a key by a specified amount.  
    **Parameters:**  
    - `key`: Key to increment.  
    - `amount`: (Optional) Amount to increment by (default is 1).  

    **Returns:**  
    - The new value after incrementing, or `None` if an error occurs.  

12. **`decrement_key(key: str, amount: int = 1) -> int`**  
    Decrements the value of a key by a specified amount.  
    **Parameters:**  
    - `key`: Key to decrement.  
    - `amount`: (Optional) Amount to decrement by (default is 1).  

    **Returns:**  
    - The new value after decrementing, or `None` if an error occurs.  

13. **`flush_database() -> bool`**  
    Deletes all keys in the current Redis database.  
    **Returns:**  
    - `True` if successful, `False` otherwise.  

14. **`expire_key(key: str, expiry: int) -> bool`**  
    Sets an expiry time for a key.  
    **Parameters:**  
    - `key`: Key to set the expiry for.  
    - `expiry`: Expiry time in seconds.  

    **Returns:**  
    - `True` if successful, `False` otherwise.  

### Notes
- Ensure `REDIS_CACHING` is set to `on` in your environment variables to enable Redis functionality.
- Use `expiry` parameter to manage cache expiration effectively. Without `expiry`, keys will persist indefinitely unless manually deleted.