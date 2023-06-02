from flask_restful import Api
from app.components import HelloWorld


def initialize_routes(api: Api):
    api.add_resource(HelloWorld, '/')