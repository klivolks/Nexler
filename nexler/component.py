from app.utils import dir_util, file_util, response_util
import os


def create_component(args):
    try:
        directory_path = f"app/components/{args.moduleName}"
        file_path = os.path.join(directory_path, '__init__.py')

        # Check if the file already exists
        if os.path.exists(file_path):
            print(f"Component '{args.moduleName}' already exists, skipping creation.")
            return

        dir_util.create_directory(directory_path)

        variables_str = ', '.join(args.variables) if args.variables else ''

        method_variables = f"(self, {variables_str})" if variables_str else "(self)"

        methods = args.methods.split(',') if args.methods else ['get', 'post', 'put', 'delete']

        method_templates = {
            'get': f"""
    def get{method_variables}:
        try:
            return response_util.success({{"message": "This is the GET method of {args.url}"}})
        except Exception as e:
            return response_util.error(str(e))
""",
            'post': f"""
    def post{method_variables}:
        try:
            return response_util.success({{"message": "This is the POST method of {args.url}"}})
        except Exception as e:
            return response_util.error(str(e))
""",
            'put': f"""
    def put{method_variables}:
        try:
            return response_util.success({{"message": "This is the PUT method of {args.url}"}})
        except Exception as e:
            return response_util.error(str(e))
""",
            'delete': f"""
    def delete{method_variables}:
        try:
            return response_util.success({{"message": "This is the DELETE method of {args.url}"}})
        except Exception as e:
            return response_util.error(str(e))
"""
        }

        method_definitions = [method_templates[method] for method in methods if method in method_templates]

        class_definition = f"""
from flask_restful import Resource
from app.utils import response_util

class {args.moduleName}(Resource):
""" + ''.join(method_definitions)

        file_util.write_file(file_path, class_definition)

        components_init_path = 'app/components/__init__.py'
        import_line = f"from .{args.moduleName} import {args.moduleName}\n"

        # Check if the import already exists
        with open(components_init_path, 'r') as f:
            if import_line in f.read():
                print(f"Import for '{args.moduleName}' already exists, skipping.")
            else:
                file_util.append_file(components_init_path, import_line)

        routes_init_path = 'app/routes/__init__.py'
        content = file_util.read_file(routes_init_path)
        lines = content.split('\n')
        for i, line in enumerate(lines):
            if line.startswith('from app.components import '):
                if args.moduleName not in line:
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
