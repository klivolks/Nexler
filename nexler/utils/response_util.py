def check_data(data):
    if not isinstance(data, (dict, list, str)):
        raise TypeError(f'The data passed is not of type dict or list. It is of type {type(data)}')


def success(data: (dict, list, str), status_code: int = 200):
    check_data(data)
    return {"status": "success", "data": data}, status_code


def created(data: dict, status_code: int = 201):
    check_data(data)
    return {"status": "success", "data": data}, status_code


def accepted(data: dict = None, status_code: int = 202):
    if data:
        check_data(data)
    return {"status": "success", "data": data}, status_code


def no_content(status_code: int = 204):
    return {"status": "success", "data": None}, status_code


def error(message: str, status_code: int = 400):
    return {"status": "error", "message": message}, status_code


def bad_request(message: str = 'Bad Request'):
    return {"status": "error", "message": message}, 400


def unauthorized(message: str = 'Unauthorized'):
    return {"status": "error", "message": message}, 401


def forbidden(message: str = 'Forbidden'):
    return {"status": "error", "message": message}, 403


def not_found(message: str = 'Not found'):
    return {"status": "error", "message": message}, 404


def method_not_allowed(message: str = 'Method not allowed'):
    return {"status": "error", "message": message}, 405


def conflict(message: str = 'Conflict'):
    return {"status": "error", "message": message}, 409


def unsupported_media_type(message: str = 'Unsupported Media Type'):
    return {"status": "error", "message": message}, 415


def server_error(message: str = 'Internal Server Error'):
    return {"status": "error", "message": message}, 500


def not_implemented(message: str = 'Not Implemented'):
    return {"status": "error", "message": message}, 501
