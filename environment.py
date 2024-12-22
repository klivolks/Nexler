import os
from dotenv import load_dotenv, find_dotenv
load_dotenv(find_dotenv(), override=True)
config_name = os.getenv('FLASK_ENV') or 'default'
