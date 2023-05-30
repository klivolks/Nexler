from werkzeug import datastructures
from flask_restful import reqparse
import re

from app.utils import response_util

parser = reqparse.RequestParser()


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
    parser.add_argument(field_name, type=field_type, location='form')
    args = parser.parse_args()
    try:
        return validator(args.get(field_name)) if validator else args.get(field_name)
    except ValueError as e:
        return response_util.bad_request(str(e))


def json_data(field_name, field_type=str, validator=None):
    parser.add_argument(field_name, type=field_type, location='json')
    args = parser.parse_args()
    try:
        return validator(args.get(field_name)) if validator else args.get(field_name)
    except ValueError as e:
        return response_util.bad_request(str(e))


def query_params(field_name, field_type=str, validator=None):
    parser.add_argument(field_name, type=field_type, location='args')
    args = parser.parse_args()
    try:
        return validator(args.get(field_name)) if validator else args.get(field_name)
    except ValueError as e:
        return response_util.bad_request(str(e))


def file(file_name):
    parser.add_argument(file_name, type=datastructures.FileStorage, location='files')
    args = parser.parse_args()
    return args.get(file_name)


def headers(field_name, field_type=str, validator=None):
    parser.add_argument(field_name, type=field_type, location='headers')
    args = parser.parse_args()
    try:
        return validator(args.get(field_name)) if validator else args.get(field_name)
    except ValueError as e:
        return response_util.bad_request(str(e))
