from app.utils import dir_util, file_util, response_util
import os


def create_component(args):
    try:
        # Construct the directory path
        directory_path = f"app/components/{args.moduleName}"

        # Create the directory
        dir_util.create_directory(directory_path)

        # Construct the file path
        file_path = os.path.join(directory_path, '__init__.py')

        # Construct the class definition
        variables_str = ', '.join(args.variables) if args.variables else ''
        class_definition = f"""
from flask_restful import Resource
from app.utils import response_util

class {args.moduleName}(Resource):
    def get(self, {variables_str}):
        try:
            # Logic goes here
            return response_util.success({{"message": "This is the GET method of {args.url}"}})
        except Exception as e:
            return response_util.error(str(e))

    def post(self, {variables_str}):
        try:
            # Logic goes here
            return response_util.success({{"message": "This is the POST method of {args.url}"}})
        except Exception as e:
            return response_util.error(str(e))

    def put(self, {variables_str}):
        try:
            # Logic goes here
            return response_util.success({{"message": "This is the PUT method of {args.url}"}})
        except Exception as e:
            return response_util.error(str(e))

    def delete(self, {variables_str}):
        try:
            # Logic goes here
            return response_util.success({{"message": "This is the DELETE method of {args.url}"}})
        except Exception as e:
            return response_util.error(str(e))
"""
        # Create the file and write the class definition to it
        file_util.write_file(file_path, class_definition)

        # Append the import line to the components __init__.py
        components_init_path = 'app/components/__init__.py'
        import_line = f"from .{args.moduleName} import {args.moduleName}\n"
        file_util.append_file(components_init_path, import_line)

        # Update the routes __init__.py file
        routes_init_path = 'app/routes/__init__.py'
        content = file_util.read_file(routes_init_path)

        # Split the content by lines
        lines = content.split('\n')

        # Add import to the header
        for i, line in enumerate(lines):
            if line.startswith('from app.components import '):
                lines[i] = f"{line}, {args.moduleName}"
                break

        # Add new route at the end of the file
        url_variables_str = '/'.join(f'<{variable}>' for variable in args.variables) if args.variables else ''
        url_variables_str = f'/{url_variables_str}' if url_variables_str else ''

        # Ensure the url starts with a slash and does not end with one
        url = args.url
        if not url.startswith('/'):
            url = '/' + url
        if url.endswith('/'):
            url = url[:-1]

        route_line = f"    api.add_resource({args.moduleName}, '{url}{url_variables_str}')"
        lines.append(route_line)

        # Join the lines back together and write the updated content back to the file
        updated_content = '\n'.join(lines)
        file_util.write_file(routes_init_path, updated_content)

        print(f"Component '{args.moduleName}' created with url: {url}")

    except Exception as e:
        print(f"An error occurred while creating the component: {e}")
