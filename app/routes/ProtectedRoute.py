from flask_restx import Api, fields, Namespace
from app.components import Protected

test = Namespace("protected", "Protected routes")


def register(api: Api):
    api.add_namespace(test)
    test.add_resource(Protected, '')

    post_request_model = api.model('ProtectedPostRequest', {
        'name': fields.String(required=True, description='The name of the user'),
        'email': fields.String(required=False, description="Email of user")
    })
    put_request_model = api.model('ProtectedPutRequest', {
        'resource': fields.String(required=True, description='The resource to update')
    })

    # Register models with API
    api.add_model('ProtectedPostRequest', post_request_model)
    api.add_model('ProtectedPutRequest', put_request_model)
