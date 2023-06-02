# `str_util.py` User Documentation

The `str_util.py` module, a part of the `app.utils` package, offers a set of utility functions for string manipulation, such as encoding, decoding, parsing, etc. Here are the details of each function:

## Functions

- **encode(s, encoding="utf-8", type="base64")**: This function encodes the provided string using the specified encoding and type. The default encoding is 'utf-8' and the default type is 'base64'. It also supports hexadecimal encoding.

- **decode(s, encoding="utf-8", type="base64")**: This function decodes the provided string using the specified encoding and type. The default encoding is 'utf-8' and the default type is 'base64'. It also supports hexadecimal decoding.

- **parse(s, datatype="json")**: This function parses the provided string into the specified datatype. It currently supports 'json', 'xml', and 'yaml'.

- **remove_punctuation(s)**: This function removes punctuation from the provided string.

- **remove_whitespace(s)**: This function removes all kinds of whitespace from the provided string, not only spaces.

- **capitalize(s)**: This function capitalizes the first letter of each word in the provided string.

- **convert_to_snake_case(s)**: This function converts the provided string to snake_case.

- **convert_to_camel_case(s)**: This function converts the provided string to camelCase.

## Usage

To utilize these functions, import the required ones from the `app.utils.str_util` module and use them in your code as needed.

For example:

```python
from app.utils.str_util import str_encode, str_decode, remove_punctuation

def process(self):
    text = 'Hello, World!'
    encoded_text = str_encode(text)
    removed_punctuation_text = remove_punctuation(text)
    # rest of the code
```

In this example, the `encode` function is used to encode the 'Hello, World!' string, and the `remove_punctuation` function is used to remove punctuation from the string. You can choose the functions that best serve your use case.