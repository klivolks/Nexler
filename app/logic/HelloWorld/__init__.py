from app.utils import dir_util


class HelloWorldLogic:
    def __init__(self):
        self.fileType = 'modules'

    def get_all_services(self):

        # List files in 'services' directory
        services_list = dir_util.list_files_by_type('app/services/', self.fileType)

        return services_list

    def get_all_utilities(self):

        # List files in 'utils' directory
        utils_list = dir_util.list_files_by_type('app/utils/', self.fileType)

        return utils_list
