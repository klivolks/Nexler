from nexler.utils import file_util


def generate_routes(args):
    variables = args.variables.split(',') if args.variables else None
    routes_init_path = 'app/routes/__init__.py'
    content = file_util.read_file(routes_init_path)
    lines = content.split('\n')

    for i, line in enumerate(lines):

        if line.startswith('from app.routes import '):
            if args.moduleName not in line:
                lines[i] = f"{line}, {args.moduleName}Route"
            break

    url_variables_str = '/'.join(f'<{variable}>' for variable in variables) if args.variables else ''
    url_variables_str = f'/{url_variables_str}' if url_variables_str else ''

    url = args.url
    if not url.startswith('/'):
        url = '/' + url
    if url.endswith('/'):
        url = url[:-1]

    route_register_line = f"    {args.moduleName}Route.register(api)"
    lines.append(route_register_line)

    updated_content = '\n'.join(lines)
    file_util.write_file(routes_init_path, updated_content)

    route_content = (f"""from flask_restx import Api, fields, Namespace
from app.components import {args.moduleName}""")
    register_name_space = "\n"
    if args.namespace:
        namespace = args.namespace
        register_name_space = f"\n\n{namespace} = Namespace('{namespace}', 'Edit routes to add description')\n"
    else:
        namespace = "api"

    route_content += register_name_space
    route_content += f"""

def register(api: Api):"""

    if args.namespace:
        route_content += f"""
    api.add_namespace({namespace})"""

    route_content += f"""
    {namespace}.add_resource({args.moduleName}, '{url}{url_variables_str}')\n
    
    post_request_model = api.model('{args.moduleName}PostPayload', {{
        'resource': fields.String(required=True, description='resource to be updated')
    }})
    put_request_model = api.model('{args.moduleName}PutPayload', {{
        'resource': fields.String(required=True, description='The resource to update')
    }})
    delete_request_model = api.model('{args.moduleName}DeletePayload', {{
        'resource': fields.String(required=True, description='The resource to update')
    }})

    # Register models with API
    api.add_model('ProtectedPostRequest', post_request_model)
    api.add_model('ProtectedPutRequest', put_request_model)
    api.add_model('ProtectedPutRequest', delete_request_model)
    """

    route_file_path = f'app/routes/{args.moduleName}Route.py'
    file_util.write_file(route_file_path, route_content)
    group = "" if namespace == "api" else namespace
    return f"{group}{url}"

