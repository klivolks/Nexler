from flask_restful import Api
from app.components import HelloWorld, Protected


def initialize_routes(api: Api):
    api.add_resource(HelloWorld, '/')
    api.add_resource(Protected, '/protected')