from app.logic.HelloWorld import HelloWorldLogic
from flask_restful import Resource
from app.utils import response_util


class HelloWorld(Resource):
    @staticmethod
    def get():
        """
        :return:
        """
        try:
            logic = HelloWorldLogic()
            services = logic.get_all_services()
            utilities = logic.get_all_utilities()
            data = {
                "Message": "This is Nexler framework for restful APIs by klivolks",
                "Services": services,
                "Utilities": utilities,
            }
            return response_util.success(data)  # HTTP Status Code
        except Exception as e:
            return response_util.server_error(str(e))  # HTTP Status Code
