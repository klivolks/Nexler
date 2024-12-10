from redis import Redis
from nexler.utils import config_util, error_util


class RedisService:
    def __init__(self):
        redis_host = config_util.Config().require("REDIS_HOST")
        redis_port = config_util.Config().require("REDIS_PORT")
        redis_auth = config_util.Config().require("REDIS_AUTH")
        if redis_auth == 'on':
            redis_username = config_util.Config().require("REDIS_USERNAME")
            redis_password = config_util.Config().require("REDIS_PASSWORD")
            self.r = Redis(
                host=redis_host,
                port=redis_port,
                username=redis_username,
                password=redis_password,
                decode_responses=True
            )
        else:
            self.r = Redis(
                host=redis_host,
                port=redis_port,
                decode_responses=True
            )

    def set_string(self, key: str, value: str, expiry: int = None) -> bool:
        """
        Store a string value in Redis.
        :param key: The key to store the value under.
        :param value: The string value to store.
        :param expiry: Optional expiry time in seconds.
        :return: True if successful, False otherwise.
        """
        try:
            self.r.set(key, value)
            if expiry:
                self.r.expire(key, expiry)
            return True
        except Exception as e:
            error_util.handle_server_error(e)
            return False

    def get_string(self, key: str) -> str:
        """
        Retrieve a string value from Redis.
        :param key: The key of the value to retrieve.
        :return: The string value or None if not found.
        """
        try:
            value = self.r.get(key)
            return value.decode('utf-8') if value else None
        except Exception as e:
            error_util.handle_server_error(e)
            return None

    def set_dict(self, key: str, value: dict, expiry: int = None) -> bool:
        """
        Store a dictionary as a hash in Redis.
        :param key: The key to store the hash under.
        :param value: The dictionary to store.
        :param expiry: Optional expiry time in seconds.
        :return: True if successful, False otherwise.
        """
        if not isinstance(value, dict):
            raise ValueError("The value must be a dictionary.")
        try:
            self.r.hset(key, mapping=value)
            if expiry:
                self.r.expire(key, expiry)
            return True
        except Exception as e:
            error_util.handle_server_error(e)
            return False

    def get_dict(self, key: str) -> dict:
        """
        Retrieve a dictionary (hash) from Redis.
        :param key: The key of the hash to retrieve.
        :return: The dictionary or an empty dictionary if not found.
        """
        try:
            data = self.r.hgetall(key)
            return {k.decode('utf-8'): v.decode('utf-8') for k, v in data.items()} if data else {}
        except Exception as e:
            error_util.handle_server_error(e)
            return {}

    def delete_key(self, key: str) -> bool:
        """
        Delete a key from Redis.
        :param key: The key to delete.
        :return: True if the key was deleted, False otherwise.
        """
        try:
            result = self.r.delete(key)
            return result > 0
        except Exception as e:
            error_util.handle_server_error(e)
            return False

    def key_exists(self, key: str) -> bool:
        """
        Check if a key exists in Redis.
        :param key: The key to check.
        :return: True if the key exists, False otherwise.
        """
        try:
            return self.r.exists(key) > 0
        except Exception as e:
            error_util.handle_server_error(e)
            return False

    def set_list(self, key: str, values: list, expiry: int = None) -> bool:
        """
        Store a list in Redis.
        :param key: The key to store the list under.
        :param values: The list to store.
        :param expiry: Optional expiry time in seconds.
        :return: True if successful, False otherwise.
        """
        if not isinstance(values, list):
            raise ValueError("The values must be a list.")
        try:
            self.r.delete(key)  # Clear any existing data at the key
            self.r.rpush(key, *values)
            if expiry:
                self.r.expire(key, expiry)
            return True
        except Exception as e:
            error_util.handle_server_error(e)
            return False

    def get_list(self, key: str) -> list:
        """
        Retrieve a list from Redis.
        :param key: The key of the list to retrieve.
        :return: The list or an empty list if not found.
        """
        try:
            return [item.decode('utf-8') for item in self.r.lrange(key, 0, -1)]
        except Exception as e:
            error_util.handle_server_error(e)
            return []

    def set_set(self, key: str, values: set, expiry: int = None) -> bool:
        """
        Store a set in Redis.
        :param key: The key to store the set under.
        :param values: The set to store.
        :param expiry: Optional expiry time in seconds.
        :return: True if successful, False otherwise.
        """
        if not isinstance(values, set):
            raise ValueError("The values must be a set.")
        try:
            self.r.delete(key)  # Clear any existing data at the key
            self.r.sadd(key, *values)
            if expiry:
                self.r.expire(key, expiry)
            return True
        except Exception as e:
            error_util.handle_server_error(e)
            return False

    def get_set(self, key: str) -> set:
        """
        Retrieve a set from Redis.
        :param key: The key of the set to retrieve.
        :return: The set or an empty set if not found.
        """
        try:
            return {item.decode('utf-8') for item in self.r.smembers(key)}
        except Exception as e:
            error_util.handle_server_error(e)
            return set()

    def increment_key(self, key: str, amount: int = 1) -> int:
        """
        Increment the value of a key by a given amount.
        :param key: The key to increment.
        :param amount: The amount to increment by (default is 1).
        :return: The new value after incrementing.
        """
        try:
            return self.r.incr(key, amount)
        except Exception as e:
            error_util.handle_server_error(e)
            return None

    def decrement_key(self, key: str, amount: int = 1) -> int:
        """
        Decrement the value of a key by a given amount.
        :param key: The key to decrement.
        :param amount: The amount to decrement by (default is 1).
        :return: The new value after decrementing.
        """
        try:
            return self.r.decr(key, amount)
        except Exception as e:
            error_util.handle_server_error(e)
            return None

    def flush_database(self) -> bool:
        """
        Delete all keys in the current Redis database.
        :return: True if successful, False otherwise.
        """
        try:
            self.r.flushdb()
            return True
        except Exception as e:
            error_util.handle_server_error(e)
            return False

    def expire_key(self, key: str, expiry: int) -> bool:
        """
        Set an expiry time on a key.
        :param key: The key to set the expiry on.
        :param expiry: The expiry time in seconds.
        :return: True if successful, False otherwise.
        """
        try:
            return self.r.expire(key, expiry)
        except Exception as e:
            error_util.handle_server_error(e)
            return False
