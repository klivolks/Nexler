# `request_util.py` User Documentation

`request_util.py` module provides utility functions to validate and extract data from the request in different ways. This module is part of `app.utils` package. 

## Functions

Below is a detailed explanation of each function:

### Validation Functions

Validation functions are used to validate and sanitize user input.

- **email(value)**: This function validates if the input value is a properly formed email address. If not, it raises a ValueError.

- **phone(value)**: This function validates if the input value is a 10-digit phone number. If not, it raises a ValueError.

- **money(value)**: This function validates if the input value is a properly formatted monetary amount. If not, it raises a ValueError.

- **number(value)**: This function validates if the input value is a properly formatted integer. If not, it raises a ValueError.

- **decimal_number(value)**: This function validates if the input value is a properly formatted floating-point number. If not, it raises a ValueError.

### Request Data Extraction and Validation Functions

These functions extract data from different parts of the request and optionally validate them using provided validator functions.

- **form_data(field_name, field_type=str, validator=None, is_required_field=True)**: This function extracts the field named `field_name` from the form data of the request, optionally validating it using `validator` if provided.

- **json_data(field_name, field_type=str, validator=None, is_required_field=True)**: This function extracts the field named `field_name` from the JSON body of the request, optionally validating it using `validator` if provided.

- **query_params(field_name, field_type=str, validator=None, is_required_field=True)**: This function extracts the field named `field_name` from the query parameters of the request, optionally validating it using `validator` if provided.

- **file(file_name, is_required_field=True)**: This function extracts the file named `file_name` from the files in the request.

- **headers(field_name, field_type=str, validator=None)**: This function extracts the field named `field_name` from the headers of the request, optionally validating it using `validator` if provided.

In all of the above functions, `field_name` is the name of the field to be extracted from the respective part of the request. `field_type` is an optional type parameter to indicate the expected type of the field. `validator` is an optional function that takes the extracted value as input and performs some validation on it. `is_required_field` is a bool that check whether the field is required and if so raises an error if not present.

If the validation fails in any of the above functions, they raise a "bad request" exception with an error message detailing the cause of the failure.

## Usage

To use these utility functions, simply import the required functions from the `app.utils.request_util` module and use them in your code where needed.

For example:

```python
from app.utils.request_util import form_data, email

def post(self):
    user_email = form_data('email', validator=email)
    # rest of the code
```

In this example, `form_data` function is used to extract the 'email' field from the form data of the request and validate it using the `email` validation function. If the validation fails, the function will return a "bad request" response. If the validation passes, the function will return the extracted and validated email address.