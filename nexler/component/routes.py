from nexler.utils import file_util


def generate_routes(args):
    variables = args.variables.split(',') if args.variables else None
    routes_init_path = 'app/routes/__init__.py'
    content = file_util.read_file(routes_init_path)
    lines = content.split('\n')
    routeName = f"{args.moduleName}Route"

    for i, line in enumerate(lines):

        if line.startswith('from app.routes import '):
            if routeName not in line:
                lines[i] = f"{line}, {routeName}"
            break

    url_variables_str = '/'.join(f'<{variable}>' for variable in variables) if args.variables else ''
    url_variables_str = f'/{url_variables_str}' if url_variables_str else ''

    url = args.url
    if not url.startswith('/'):
        url = '/' + url
    if url.endswith('/'):
        url = url[:-1]

    route_register_line = f"    {routeName}.register(api)  # {args.namespace}{url}"
    lines.append(route_register_line)

    updated_content = '\n'.join(lines)
    file_util.write_file(routes_init_path, updated_content)

    route_content = (f"""from flask_restx import Api, fields, Namespace
from app.components import {args.moduleName}""")
    register_name_space = "\n"
    if args.namespace:
        namespace = f"{args.namespace}_namespace"
        register_name_space = f"\n\n{namespace} = Namespace('{args.namespace}', 'Edit routes to add description')\n"
    else:
        namespace = "api"

    route_content += register_name_space
    route_content += f"""

def register(api: Api):"""

    if args.namespace:
        route_content += f"""
    api.add_namespace({namespace})"""

    if isinstance(args.methods, str):
        methods = args.methods.split(',')
        methods = [method.lower() for method in methods if method.lower() != 'get']
    else:
        methods = ['post', 'put', 'delete']
    route_content += f"""
    {namespace}.add_resource({args.moduleName}, '{url}{url_variables_str}')
"""
    for method in methods:
        route_content += f"""
    {method}_request_model = api.model('{args.moduleName}{method.capitalize()}Payload', {{
        'resource': fields.String(required=True, description='resource to be updated')
    }})"""

    route_content += """\n
    # Register models with API"""

    for method in methods:
        route_content += f"""
    api.add_model('{args.moduleName}{method.capitalize()}Request', {method}_request_model)
    """

    route_file_path = f'app/routes/{routeName}.py'
    file_util.write_file(route_file_path, route_content)
    group = "" if namespace == "api" else args.namespace
    return f"{group}{url}"

