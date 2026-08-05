import hashlib
import hmac

from flask import request
from flask_restx import Resource, Api

from app.kGateActions import despatch
from nexler.utils import response_util, error_util, request_util
from nexler.utils.config_util import Config

api = Api()
post_payload = api.model("WebhooksPostPayload", {})


class Webhooks(Resource):

    @api.expect(post_payload)
    def post(self):
        try:
            signature = request_util.headers("X-Signature")
            secret = Config().get("KGATE_CLIENT_ID")
            body = request.body()

            computed = hmac.new(
                secret.encode(),
                body.encode(),
                hashlib.sha256
            ).hexdigest()
            if signature != computed:
                return error_util.handle_bad_request("signature mismatch")
            channel = request_util.json_data("channel")
            payload = request_util.json_data("payload")
            despatch(channel, payload)
            return response_util.success({"status": "ok"})
        except Exception as e:
            return error_util.handle_http_exception(repr(e))
