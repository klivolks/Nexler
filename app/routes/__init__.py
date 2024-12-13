from flask_restx import Api
from app.routes import ProtectedRoute, HelloWorldRoute


def initialize_routes(api: Api):
    ProtectedRoute.register(api)
    HelloWorldRoute.register(api)