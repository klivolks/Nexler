from werkzeug.exceptions import HTTPException
from nexler.services.LoggerService import LoggerService
from nexler.utils import response_util


def handle_http_exception(e):
    if isinstance(e, HTTPException):
        error_method = {
            400: response_util.bad_request,
            401: response_util.unauthorized,
            403: response_util.forbidden,
            404: response_util.not_found,
            405: response_util.method_not_allowed,
            409: response_util.conflict,
            415: response_util.unsupported_media_type,
            500: response_util.server_error,
            501: response_util.not_implemented,
        }.get(e.code, response_util.error)

        return error_method(f"{str(e)}")
    else:
        LoggerService().log(e, "Unidentified")
        return response_util.error(f"Internal server error: {e}", 500)


def handle_bad_request(e):
    LoggerService().log(e, "BadRequest")
    return response_util.bad_request(f"{str(e)}")


def handle_unauthorized(e):
    LoggerService().log(e, "UnAuthorised")
    return response_util.unauthorized(f"{str(e)}")


def handle_forbidden(e):
    LoggerService().log(e, "Forbidden")
    return response_util.forbidden(f"{str(e)}")


def handle_not_found(e):
    LoggerService().log(e, "NotFound")
    return response_util.not_found(f"{str(e)}")


def handle_method_not_allowed(e):
    LoggerService().log(e, "MethodNotAllowed")
    return response_util.method_not_allowed(f"{str(e)}")


def handle_conflict(e):
    LoggerService().log(e, "Conflict")
    return response_util.conflict(f"{str(e)}")


def handle_unsupported_media_type(e):
    LoggerService().log(e, "UnsupportedMedia")
    return response_util.unsupported_media_type(f"{str(e)}")


def handle_server_error(e):
    LoggerService().log(e, "ServerError")
    return response_util.server_error(f"{str(e)}")


def handle_not_implemented(e):
    LoggerService().log(e, "NotImplemented")
    return response_util.not_implemented(f"{str(e)}")


def handle_key_error(e):
    LoggerService().log(e, "KeyError")
    return response_util.bad_request(f"KeyError: {str(e)}")


def handle_value_error(e):
    LoggerService().log(e, "ValueError")
    return response_util.bad_request(f"ValueError: {str(e)}")


def handle_type_error(e):
    LoggerService().log(e, "TypeError")
    return response_util.bad_request(f"TypeError: {str(e)}")


def handle_index_error(e):
    LoggerService().log(e, "IndexError")
    return response_util.bad_request(f"IndexError: {str(e)}")


def handle_attribute_error(e):
    LoggerService().log(e, "AttributeError")
    return response_util.bad_request(f"AttributeError: {str(e)}")


def handle_zero_division_error(e):
    LoggerService().log(e, "ZeroDivisionError")
    return response_util.bad_request(f"ZeroDivisionError: {str(e)}")


def register_error_handlers(app):
    app.register_error_handler(400, handle_bad_request)
    app.register_error_handler(401, handle_unauthorized)
    app.register_error_handler(403, handle_forbidden)
    app.register_error_handler(404, handle_not_found)
    app.register_error_handler(405, handle_method_not_allowed)
    app.register_error_handler(409, handle_conflict)
    app.register_error_handler(415, handle_unsupported_media_type)
    app.register_error_handler(500, handle_server_error)
    app.register_error_handler(501, handle_not_implemented)
    app.register_error_handler(Exception, handle_http_exception)
    app.register_error_handler(KeyError, handle_key_error)
    app.register_error_handler(ValueError, handle_value_error)
    app.register_error_handler(TypeError, handle_type_error)
    app.register_error_handler(IndexError, handle_index_error)
    app.register_error_handler(AttributeError, handle_attribute_error)
    app.register_error_handler(ZeroDivisionError, handle_zero_division_error)
