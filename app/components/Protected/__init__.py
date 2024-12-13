from flask_restx import Resource, Api
from nexler.utils import response_util, error_util, request_util
from nexler.services.AuthService import protected, user
api = Api()
post_request_model = api.model('ProtectedPostRequest', {})
put_request_model = api.model('ProtectedPutRequest', {})

class Protected(Resource):
    @protected
    def get(self):
        try:
            # Logic goes here
            return response_util.success({"message": f"This is the GET method of /protected. The user is {user.Id}"})
        except Exception as e:
            return error_util.handle_server_error(e)

    @api.expect(post_request_model)
    @protected
    def post(self):
        try:
            Name = request_util.json_data("name")
            # Logic goes here
            return response_util.success({"message": f"Hello, {Name}. The user is {user.Id}"})
        except Exception as e:
            return error_util.handle_server_error(e)

    @api.expect(put_request_model)
    @protected('resource')
    def put(self):
        try:
            # Logic goes here
            return response_util.success({"message": f"This is the PUT method of /protected. The user is {user.Id}"})
        except Exception as e:
            return error_util.handle_server_error(e)

    @protected
    def delete(self):
        try:
            # Logic goes here
            return response_util.success({"message": f"This is the DELETE method of /protected. The user is {user.Id}"})
        except Exception as e:
            return error_util.handle_server_error(e)
