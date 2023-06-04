from app.utils import dir_util, file_util, response_util
import os


def create_component(args):
    try:
        directory_path = f"app/components/{args.moduleName}"
        file_path = os.path.join(directory_path, '__init__.py')
        component_exists = False

        # Check if the file already exists
        if os.path.exists(file_path):
            print(f"Component '{args.moduleName}' already exists, skipping creation.")
            component_exists = True
        else:
            dir_util.create_directory(directory_path)
            variables_str = ', '.join(args.variables) if args.variables else ''
            method_variables = f"(self, {variables_str})" if variables_str else "(self)"
            if isinstance(args.methods, list):
                methods = args.methods
            elif isinstance(args.methods, str):
                methods = [method.strip() for method in args.methods.split(',')]
            else:
                methods = ['get', 'post', 'put', 'delete']
            # Define method templates for different HTTP methods
            protected_decorator = "@protected\n    " if args.protected else ""

            method_templates = {
                'get': f"""
    {protected_decorator}def get{method_variables}:
        try:
            return response_util.success({{"message": "This is the GET method of {args.url}"}})
        except Exception as e:
            return response_util.error(str(e))
""",
                'post': f"""
    {protected_decorator}def post{method_variables}:
        try:
            return response_util.success({{"message": "This is the POST method of {args.url}"}})
        except Exception as e:
            return response_util.error(str(e))
""",
                'put': f"""
    {protected_decorator}def put{method_variables}:
        try:
            return response_util.success({{"message": "This is the PUT method of {args.url}"}})
        except Exception as e:
            return response_util.error(str(e))
""",
                'delete': f"""
    {protected_decorator}def delete{method_variables}:
        try:
            return response_util.success({{"message": "This is the DELETE method of {args.url}"}})
        except Exception as e:
            return response_util.error(str(e))
"""
            }
            # Generate method definitions
            method_definitions = [method_templates[method] for method in methods if method in method_templates]

            # Class definition
            class_definition = f"""
from flask_restful import Resource
from app.utils import response_util
{"from app.services.UserService import protected, user" if args.protected else ""}

class {args.moduleName}(Resource):
""" + ''.join(method_definitions)

            # Write the class definition to the file
            file_util.write_file(file_path, class_definition)

        # Add import line to the components init file
        components_init_path = 'app/components/__init__.py'
        import_line = f"from .{args.moduleName} import {args.moduleName}\n"

        with open(components_init_path, 'r') as f:
            if import_line not in f.read():
                file_util.append_file(components_init_path, import_line)

        # Edit routes init file
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

        if not component_exists:
            print(f"Component '{args.moduleName}' created with url: {url}")
        else:
            print(f"Route for component '{args.moduleName}' created with url: {url}")

    except Exception as e:
        print(f"An error occurred while creating the component: {e}")
