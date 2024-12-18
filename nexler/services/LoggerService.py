import traceback
from daba.Mongo import collection
from nexler.utils import config_util, dt_util
from flask import request


class LoggerService:
    def __init__(self):
        self.error_log = collection("ErrorLog")
        self.debug_log = collection("DebugLog")

    def log(self, msg, error_type=None):
        from nexler.services.AuthService import user

        route = request.path
        query = request.args
        payload = request.form
        json_payload = request.get_json() if request.headers.get('content-type') == "application/json" else None
        headers = dict(request.headers)
        method = request.method
        data = {
            "App": config_util.Config().get('SERVICE_NAME'),
            "Error": str(msg),
            "ErrorType": error_type,
            "Route": route,
            "Method": method,
            "Headers": headers,
            "FormPayLoad": payload,
            "JSONPayLoad": json_payload,
            "Query": query,
            "User": user.Id,
            "Trace": traceback.format_exc(),
            "Status": "Active",
            "created_at": dt_util.get_current_time(),
            "updated_at": dt_util.get_current_time()
        }
        response = self.error_log.put(data)
        return response

    def debug(self, msg: any, debug_type=None):
        from nexler.services.AuthService import user
        route = request.path
        query = request.args
        payload = request.form
        json_payload = request.get_json() if request.headers.get('content-type') == "application/json" else None
        headers = dict(request.headers)
        method = request.method
        data = {
            "App": config_util.Config().get('SERVICE_NAME'),
            "Data": msg if isinstance(msg, (dict, list, str)) else str(msg),
            "DebugType": debug_type,
            "Route": route,
            "Method": method,
            "Headers": headers,
            "FormPayLoad": payload,
            "JSONPayLoad": json_payload,
            "Query": query,
            "User": user.Id,
            "Status": "Active",
            "created_at": dt_util.get_current_time(),
            "updated_at": dt_util.get_current_time()
        }
        response = self.debug_log.put(data)
        return response
