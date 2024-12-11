import traceback
from daba.Mongo import collection
from nexler.utils import config_util, dt_util
from nexler.services.AuthService import user
from flask import request


class Logger:
    def __init__(self):
        self.error_log = collection("ErrorLog")

    def log(self, msg):
        route = request.path
        query = request.args
        payload = request.form
        json_payload = request.get_json() if request.headers.get('content-type') == "application/json" else None
        headers = dict(request.headers)
        method = request.method
        data = {
            "App": config_util.Config().get('SERVICE_NAME'),
            "Error": str(msg),
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
