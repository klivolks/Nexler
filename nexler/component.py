from app.utils import dir_util, file_util, response_util
import os


def create_component(args):
    try:
        directory_path = f"app/components/{args.moduleName}"
        dir_util.create_directory(directory_path)
        file_path = os.path.join(directory_path, '__init__.py')

        variables_str = ', '.join(args.variables) if args.variables else ''

        get_method_variables = f"(self, {variables_str})" if variables_str else "(self)"
        post_method_variables = get_method_variables
        put_method_variables = get_method_variables
        delete_method_variables = get_method_variables

        if args.protected:
            class_definition = f"""
from flask_restful import Resource
from app.utils import response_util
from app.services.UserService import protected, user


class {args.moduleName}(Resource):
    @protected
    def get{get_method_variables}:
        try:
            return response_util.success({{"message": f"This is the GET method of {args.url}. The user is {{user.Id}}"}})
        except Exception as e:
            return response_util.error(str(e))

    @protected
    def post{post_method_variables}:
        try:
            return response_util.success({{"message": f"This is the POST method of {args.url}. The user is {{user.Id}}"}})
        except Exception as e:
            return response_util.error(str(e))

    @protected
    def put{put_method_variables}:
        try:
            return response_util.success({{"message": f"This is the PUT method of {args.url}. The user is {{user.Id}}"}})
        except Exception as e:
            return response_util.error(str(e))

    @protected
    def delete{delete_method_variables}:
        try:
            return response_util.success({{"message": f"This is the DELETE method of {args.url}. The user is {{user.Id}}"}})
        except Exception as e:
            return response_util.error(str(e))
"""
        else:
            class_definition = f"""
from flask_restful import Resource
from app.utils import response_util


class {args.moduleName}(Resource):
    def get{get_method_variables}:
        try:
            return response_util.success({{"message": "This is the GET method of {args.url}"}})
        except Exception as e:
            return response_util.error(str(e))

    def post{post_method_variables}:
        try:
            return response_util.success({{"message": "This is the POST method of {args.url}"}})
        except Exception as e:
            return response_util.error(str(e))

    def put{put_method_variables}:
        try:
            return response_util.success({{"message": "This is the PUT method of {args.url}"}})
        except Exception as e:
            return response_util.error(str(e))

    def delete{delete_method_variables}:
        try:
            return response_util.success({{"message": "This is the DELETE method of {args.url}"}})
        except Exception as e:
            return response_util.error(str(e))
"""

        file_util.write_file(file_path, class_definition)
        components_init_path = 'app/components/__init__.py'
        import_line = f"from .{args.moduleName} import {args.moduleName}\n"
        file_util.append_file(components_init_path, import_line)

        routes_init_path = 'app/routes/__init__.py'
        content = file_util.read_file(routes_init_path)
        lines = content.split('\n')
        for i, line in enumerate(lines):
            if line.startswith('from app.components import '):
                lines[i] = f"{line}, {args.moduleName}"
                break

        url_variables_str = '/'.join(f'<{variable}>' for variable in args.variables) if args.variables else ''
        url_variables_str = f'/{url_variables_str}' if url_variables_str else ''

        url = args.url
        if not url.startswith('/'):
            url = '/' + url
        if url.endswith('/'):
            url = url[:-1]

        route_line = f"    api.add_resource({args.moduleName}, '{url}{url_variables_str}')"
        lines.append(route_line)

        updated_content = '\n'.join(lines)
        file_util.write_file(routes_init_path, updated_content)

        print(f"Component '{args.moduleName}' created with url: {url}")

    except Exception as e:
        print(f"An error occurred while creating the component: {e}")
