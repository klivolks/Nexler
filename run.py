import os
from environment import config_name

import logging.config
from flask import Flask, g, render_template
from flask_restx import Api
from flask_cors import CORS
from flask_compress import Compress

from app.routes import initialize_routes
from nexler.utils import error_util, config_util
from nexler.services import ApiService, AuthService


def create_app():
    # Load the correct configuration
    app = Flask(__name__)
    Compress(app)
    config_module = f"config.{config_name.capitalize()}Config"
    app.config.from_object(config_module)
    swagger_flag = config_util.Config().get("SWAGGER")
    authorizations = {"Bearer": {"type": "apiKey", "in": "header", "name": "Authorization"}}

    @app.route('/')
    def hello():
        return render_template('landing_page.html', swagger_flag=swagger_flag)

    # Create logs directory if it does not exist
    if not os.path.exists('logs'):
        os.mkdir('logs')

    # Setup logging
    if not app.debug:
        logging.config.fileConfig('logs/logging.ini', disable_existing_loggers=False)
        app.logger.info('Nexler startup')

    # Initialize other components
    api = Api(app,
              version=config_util.Config().get("SERVICE_VERSION"),
              title=config_util.Config().get("SERVICE_NAME"),
              description="API documentation for your Nexler app using Swagger UI",
              doc="/swagger" if (swagger_flag and swagger_flag == 'on') else None,
              authorizations=authorizations)

    api.security = [{
        'Bearer': []
    }]

    # Define models for API key and Bearer token
    api.models['Bearer'] = {
        'type': 'apiKey',
        'name': 'Authorization',
        'in': 'header'
    }

    if app.debug:
        CORS(app, expose_headers=app.config['CORS_HEADERS'], supports_credentials=True)
    else:
        CORS(app)

    initialize_routes(api)

    error_util.register_error_handlers(app)

    return app


app = create_app()


@app.before_request
def before_request():
    api_service = ApiService()
    user_service = AuthService()
    if config_util.Config().get('API_VERIFICATION') == 'off' or api_service.verified:
        g.user_id = user_service.userId
    else:
        return error_util.handle_forbidden("Please check your api key or referer")


def run():
    app.run(debug=app.config['DEBUG'], host=app.config['HOST'], port=app.config['PORT'])


if __name__ == '__main__':
    run()
