import os
import json
from dotenv import load_dotenv

load_dotenv()


class Config:
    def __init__(self, config_file_path=None):
        self.config = {}

        # Load configuration from file
        if config_file_path and os.path.isfile(config_file_path):
            with open(config_file_path, 'r') as f:
                self.config.update(json.load(f))

        # Load configuration from environment variables
        for key, value in os.environ.items():
            self.config[key] = value

    def get(self, key, default=None):
        """
        Gets the value of the specified configuration key.
        If the key is not present in the configuration, it returns the specified default value.
        """
        return self.config.get(key, default)

    def require(self, key):
        """
        Gets the value of the specified configuration key.
        If the key is not present in the configuration, it raises an error.
        """
        if key not in self.config:
            raise ValueError(f'Required configuration key "{key}" not found')
        return self.config[key]
