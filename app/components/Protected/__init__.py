from flask_restful import Resource
from app.utils import response_util
from app.services.UserService import protected, user


class Protected(Resource):
    @protected
    def get(self):
        try:
            # Logic goes here
            return response_util.success({"message": f"This is the GET method of /protected. The user is {user.Id}"})
        except Exception as e:
            return response_util.error(str(e))

    @protected
    def post(self):
        try:
            # Logic goes here
            return response_util.success({"message": f"This is the POST method of /protected. The user is {user.Id}"})
        except Exception as e:
            return response_util.error(str(e))

    @protected
    def put(self):
        try:
            # Logic goes here
            return response_util.success({"message": f"This is the PUT method of /protected. The user is {user.Id}"})
        except Exception as e:
            return response_util.error(str(e))

    @protected
    def delete(self):
        try:
            # Logic goes here
            return response_util.success({"message": f"This is the DELETE method of /protected. The user is {user.Id}"})
        except Exception as e:
            return response_util.error(str(e))
