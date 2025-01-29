from nexler.utils import dir_util, file_util
import traceback
import os
from nexler.component.routes import generate_routes


def create_component(args):
    try:
        if args.main:
            directory_path = f"app/components/{args.main}"
            file_path = os.path.join(directory_path, f'{args.moduleName}.py')
        else:
            directory_path = f"app/components/{args.moduleName}"
            file_path = os.path.join(directory_path, '__init__.py')
        component_exists = False

        variables = args.variables.split(',') if args.variables else None
        variables_str = ', '.join(variables) if args.variables else None
        method_variables = f"(self, {variables_str})" if variables_str else "(self)"

        # Check if the file already exists
        if os.path.exists(file_path):
            print(f"Component '{args.moduleName}' already exists, skipping creation.")
            component_exists = True
        else:
            if not args.main:
                dir_util.create_directory(directory_path)
            if isinstance(args.methods, str):
                methods = args.methods.split(',')
                methods = [method.lower() for method in methods]
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
            return error_util.handle_http_exception(repr(e))
""",
                'post': f"""
    {protected_decorator}@api.expect(post_payload)
    def post{method_variables}:
        try:
            return response_util.success({{"message": "This is the POST method of {args.url}"}})
        except Exception as e:
            return error_util.handle_http_exception(repr(e))
""",
                'put': f"""
    {protected_decorator}@api.expect(put_payload)
    def put{method_variables}:
        try:
            return response_util.success({{"message": "This is the PUT method of {args.url}"}})
        except Exception as e:
            return error_util.handle_http_exception(repr(e))
""",
                'delete': f"""
    {protected_decorator}@api.expect(delete_payload)
    def delete{method_variables}:
        try:
            return response_util.success({{"message": "This is the DELETE method of {args.url}"}})
        except Exception as e:
            return error_util.handle_http_exception(repr(e))
"""
            }
            # Generate method definitions
            method_definitions = [method_templates[method] for method in methods if method in method_templates]

            # Class definition
            class_definition = f"""from flask_restx import Resource, Api
from nexler.utils import response_util, error_util
{"from nexler.services.AuthService import protected, user" if args.protected else ""}

api = Api()"""
            for method in methods:
                if method != 'get':
                    class_definition += f"""
{method}_payload = api.model("{args.moduleName}{method.capitalize()}Payload", {{}})"""

            class_definition += f"""


class {args.moduleName}(Resource):
""" + ''.join(method_definitions)

            # Write the class definition to the file
            file_util.write_file(file_path, class_definition)

        # Add import line to the components init file
        components_init_path = 'app/components/__init__.py'
        if args.main:
            import_line = f"from .{args.main}.{args.moduleName} import {args.moduleName}\n"
        else:
            import_line = f"from .{args.moduleName} import {args.moduleName}\n"

        with open(components_init_path, 'r') as f:
            if import_line not in f.read():
                file_util.append_file(components_init_path, import_line)

        url = generate_routes(args)

        if not component_exists:
            print(f"Component '{args.moduleName}' created with url: {url}")
        else:
            print(f"Route for component '{args.moduleName}' created with url: {url}")

    except Exception as e:
        print(f"An error occurred while creating the component: {e}, Trace: {traceback.format_exc()}")
