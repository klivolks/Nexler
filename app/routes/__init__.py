from flask_restx import Api
from app.components import HelloWorld, Protected


def initialize_routes(api: Api):
    api.add_resource(HelloWorld, '/features')
    api.add_resource(Protected, '/protected')