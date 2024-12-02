import os
from dotenv import load_dotenv

# Load .env file
load_dotenv()


class Config(object):
    DEBUG = False
    TESTING = False
    CSRF_ENABLED = True
    SECRET_KEY = os.getenv('SECRET_KEY')
    if not SECRET_KEY:
        raise ValueError("No SECRET_KEY set for Flask application")
    MONGO_DB = os.getenv('MONGO_DB')
    MONGO_URL = os.getenv('MONGO_URL')
    HOST = os.getenv('HOST')
    PORT = os.getenv('PORT')
    API_VERIFICATION = os.getenv('API_VERIFICATION')
    FLASK_ENV = os.getenv('FLASK_ENV')
    CORS_HEADERS = 'content-disposition'
    JWT_SECRET_KEY = os.getenv('JWT_SECRET_KEY')
    JWT_ALGORITHM = os.getenv('JWT_ALGORITHM')


class DefaultConfig(Config):
    DEVELOPMENT = True
    DEBUG = True


class ProductionConfig(Config):
    DEBUG = False


class StagingConfig(Config):
    DEVELOPMENT = True
    DEBUG = True


class DevelopmentConfig(Config):
    DEVELOPMENT = True
    DEBUG = True


class TestingConfig(Config):
    TESTING = True
    SECRET_KEY = 'test'
