import os
import logging.config
from flask import Flask
from flask_restful import Api
from flask_cors import CORS
from app.routes import initialize_routes
from dotenv import load_dotenv

load_dotenv()


def create_app():
    # Load the correct configuration
    config_name = os.getenv('FLASK_ENV') or 'default'
    app = Flask(__name__)
    config_module = f"config.{config_name.capitalize()}Config"
    app.config.from_object(config_module)

    # Create logs directory if it does not exist
    if not os.path.exists('logs'):
        os.mkdir('logs')

    # Setup logging
    if not app.debug:
        logging.config.fileConfig('logs/logging.ini', disable_existing_loggers=False)
        app.logger.info('Nexler startup')

    # Initialize other components
    api = Api(app)
    if app.debug:
        CORS(app, expose_headers=app.config['CORS_HEADERS'], supports_credentials=True)
    else:
        CORS(app)

    initialize_routes(api)
    return app


app = create_app()


def run():
    app.run(debug=app.config['DEBUG'], host=app.config['HOST'], port=app.config['PORT'])


if __name__ == '__main__':
    run()
