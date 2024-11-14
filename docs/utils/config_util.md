# `config_util.py` User Documentation

`config_util.py` module provides utility functions to fetch and handle configuration from environment variables or config files. This module is part of the `nexler.utils` package.

## Class

The main class defined in this module is `Config`.

### Config

The `Config` class is used to manage configuration values. 

When a `Config` object is created, it loads configuration values from the specified configuration file and from environment variables. If a configuration key is defined both in the configuration file and as an environment variable, the value from the environment variable is used.

#### Methods

- **__init__(config_file_path)**: This method initializes a new `Config` object. It loads configuration values from the specified configuration file and from environment variables.

- **get(key, default=None)**: This method returns the value of the specified configuration key. If the key is not present in the configuration, it returns the specified default value.

- **require(key)**: This method returns the value of the specified configuration key. If the key is not present in the configuration, it raises a ValueError.

## Usage

To use these utility functions, simply import the `Config` class from the `nexler.utils.config_util` module and use it in your code where needed.

For example:

```python
from nexler.utils.config_util import Config

# Initialize a new Config object
config = Config("/path/to/config.json")

# Get configuration values
db_host = config.get('DB_HOST', 'localhost')  # Use 'localhost' as the default value if 'DB_HOST' is not defined
db_user = config.require('DB_USER')  # This will raise an error if 'DB_USER' is not defined
```

In this example, `get` method is used to retrieve the 'DB_HOST' configuration value with a default value of 'localhost' if it is not defined. The `require` method is used to retrieve the 'DB_USER' configuration value. If 'DB_USER' is not defined, the method raises a ValueError.