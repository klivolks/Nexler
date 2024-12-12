from flask import request

from app.logic.HelloWorld import HelloWorldLogic
from flask_restx import Resource
from nexler.utils import response_util, error_util


class HelloWorld(Resource):
    @staticmethod
    def get():
        """
        Get list of utilities and services available
        :param:
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
            return response_util.success(data)
        except Exception as e:
            return error_util.handle_server_error(e)
