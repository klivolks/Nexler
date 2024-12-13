from flask_restx import Api
from app.components import HelloWorld


def register(api: Api):
    api.add_resource(HelloWorld, '/features')
