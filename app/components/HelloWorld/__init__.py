from flask_restful import Resource
import os


class HelloWorld(Resource):
    def get(self):
        # Define base directory
        base_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '../..'))

        # List files in 'services' and 'utils' directories
        services_list = os.listdir(os.path.join(base_dir, 'services'))
        utils_list = os.listdir(os.path.join(base_dir, 'utils'))

        # Format filenames to remove .py extension
        services_list = [file[:-3] for file in services_list if file.endswith('.py')]
        utils_list = [file[:-3] for file in utils_list if file.endswith('.py')]

        services_list.remove("__init__")
        utils_list.remove("__init__")

        return {
            "Message": "This is nexler framework for restful apis by klivolks",
            "Services": services_list,
            "Utilities": utils_list
        }
