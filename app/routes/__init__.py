from flask_restx import Api
from app.routes import ProtectedRoute, HelloWorldRoute, WebhooksRoute


def initialize_routes(api: Api):
    ProtectedRoute.register(api)
    HelloWorldRoute.register(api)
    WebhooksRoute.register(api)  # webhooks/webhooks/kgate