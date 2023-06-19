# `faker_util.py` User Documentation

The `faker_util.py` module offers a set of functions to generate and write out fake user data. These functions utilize the `Faker` library to generate random user data, and the `csv` and `json` libraries to write this data to CSV and JSON files respectively.

## Functions

Here is a detailed explanation of each function:

### User Data Generation

- **`fake_users(count=10)`**: This function generates a list of `count` user dictionaries where default is 10. Each user dictionary contains the following keys: 'first_name', 'last_name', 'date_of_birth', 'phone', 'email', and 'password'. The values are randomly generated using the `Faker` library and Python's `random` module. The date of birth is fixed to '2000-12-30' for all users.

### File Writing Functions

- **`write_csv()`**: This function first calls `fake_users()` to get a list of user dictionaries. It then writes this data to a CSV file named 'users.csv' in the current directory. The headers of the CSV file correspond to the keys of the user dictionaries.

- **`write_json()`**: This function operates similarly to `write_csv()`, but instead writes the data to a JSON file named 'users.json' in the current directory. The resulting JSON file consists of an array of user objects.

## Usage

To utilize these functions, you must first import them from the `faker_util` module.

For example:

```python
from app.utils import faker_util

# Generate and write fake user data to CSV
faker_util.write_csv()

# Generate and write fake user data to JSON
faker_util.write_json()
```

In the first example, the `write_csv` function is used to generate fake user data and write it to a CSV file. The second example does the same but writes the data to a JSON file instead.