import ast
from flask import request
from flask_restx import reqparse
from markupsafe import escape
from werkzeug import exceptions
import re

from nexler.utils import response_util


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
def form_data(field_name, field_type=str, validator=None, is_required_field=True):
    # Access the form data directly through the request object
    value = escape(request.form.get(field_name))

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
            raise exceptions.BadRequest(str(e))
    else:
        if is_required_field:
            raise exceptions.BadRequest(f"{field_name} not found in form data.")
        return None


def json_data(field_name, field_type=str, validator=None, is_required_field=True):
    try:
        parser = reqparse.RequestParser()
        parser.add_argument(field_name, field_type, location='json')
        args = parser.parse_args()

        # Retrieve the field value
        raw_value = args.get(field_name)

        # Check for required field condition
        if (raw_value is None or raw_value == "") and is_required_field:
            raise exceptions.Forbidden(f"{field_name} is required")

        # If field_type is dict, attempt to parse the string as JSON
        if field_type == dict:
            try:
                parsed_value = ast.literal_eval(raw_value)
                if not isinstance(parsed_value, dict):
                    raise ValueError(f"{field_name} must be a valid dictionary")
            except Exception as e:
                raise exceptions.BadRequest(f"{field_name} is not valid dict: {e}")
        elif field_type == list:
            try:
                parsed_value = ast.literal_eval(raw_value)
                if not isinstance(parsed_value, list):
                    raise ValueError(f"{field_name} must be a valid list")
            except Exception as e:
                raise exceptions.BadRequest(f"{field_name} is not valid dict: {e}")
        else:
            # For other types, cast the value
            parsed_value = escape(field_type(raw_value))

        # Validate if a custom validator is provided
        return validator(escape(parsed_value)) if validator else parsed_value

    except ValueError as e:
        raise exceptions.BadRequest(str(e))


def query_params(field_name, field_type=str, validator=None, is_required_field=True):
    # Directly access the query parameters through the request object
    value = escape(request.args.get(field_name))

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
            raise exceptions.BadRequest(str(e))
    else:
        if is_required_field:
            # This case will trigger if the field_name is not found in the query parameters
            raise exceptions.BadRequest(f"{field_name} not found in query parameters.")
        return None


def file(file_name, is_required_field=True):
    # Check if the file part is present in the request
    if file_name not in request.files:
        if is_required_field:
            raise exceptions.BadRequest(f"No {file_name} part")
        return None

    # If the user does not select a file, the browser submits an empty part without a filename
    files = request.files[file_name]
    if files.filename == '':
        if is_required_field:
            raise exceptions.BadRequest('No selected file')
        return None

    # File is present and has a filename, return the file object
    return files


def headers(field_name, field_type=str, validator=None):
    # Access the headers directly through the request object
    value = escape(request.headers.get(field_name))

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
