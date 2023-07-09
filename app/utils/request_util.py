from werkzeug.datastructures import FileStorage
from flask import request
from flask_restful import reqparse
import re

from app.utils import response_util


# Define validation functions
def email(value):
    if not re.match(r"[^@]+@[^@]+\.[^@]+", value):
        raise ValueError("Invalid email address.")
    return value


def phone(value):
    if not re.match(r"^[0-9]{10}$", value):
        raise ValueError("Invalid phone number.")
    return value


def money(value):
    if not re.match(r"^\d+(\.\d{2})?$", value):
        raise ValueError("Invalid money format.")
    return float(value)


def number(value):
    if not str(value).isdigit():
        raise ValueError("Invalid integer format.")
    return int(value)


def decimal_number(value):
    try:
        value = float(value)
    except ValueError:
        raise ValueError("Invalid float format.")
    return value


# Methods to get data and validate
def form_data(field_name, field_type=str, validator=None):
    # Access the form data directly through the request object
    value = request.form.get(field_name)

    if value is not None:
        try:
            # Convert the value to the correct type
            if field_type == int:
                value = int(value)
            elif field_type == float:
                value = float(value)
            # If validator is provided, validate the value
            return validator(value) if validator else value
        except ValueError as e:
            return response_util.bad_request(str(e))
    else:
        # This case will trigger if the field_name is not found in the form data
        return response_util.bad_request(f"{field_name} not found in form data.")


def json_data(field_name, field_type=str, validator=None):
    parser = reqparse.RequestParser()
    parser.add_argument(field_name, type=field_type, location='json')
    args = parser.parse_args()
    try:
        return validator(args.get(field_name)) if validator else args.get(field_name)
    except ValueError as e:
        return response_util.bad_request(str(e))


def query_params(field_name, field_type=str, validator=None):
    # Directly access the query parameters through the request object
    value = request.args.get(field_name)

    if value is not None:
        try:
            # Convert the value to the correct type
            if field_type == int:
                value = int(value)
            elif field_type == float:
                value = float(value)
            # If validator is provided, validate the value
            return validator(value) if validator else value
        except ValueError as e:
            return response_util.bad_request(str(e))
    else:
        # This case will trigger if the field_name is not found in the query parameters
        return response_util.bad_request(f"{field_name} not found in query parameters.")


def file(file_name):
    # Check if the file part is present in the request
    if file_name not in request.files:
        return response_util.bad_request(f"No {file_name} part")

    # If the user does not select a file, the browser submits an empty part without a filename
    files = request.files[file_name]
    if files.filename == '':
        return response_util.bad_request('No selected file')

    # File is present and has a filename, return the file object
    return files


def headers(field_name, field_type=str, validator=None):
    # Access the headers directly through the request object
    value = request.headers.get(field_name)

    if value is not None:
        try:
            # Convert the value to the correct type
            if field_type == int:
                value = int(value)
            elif field_type == float:
                value = float(value)
            # If validator is provided, validate the value
            return validator(value) if validator else value
        except ValueError as e:
            return response_util.bad_request(str(e))
    elif field_name != 'Authorization':
        # This case will trigger if the field_name is not found in the headers
        return response_util.bad_request(f"{field_name} header not found.")
