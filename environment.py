import os
from dotenv import load_dotenv, find_dotenv

# Load .env file. find_dotenv() will locate the file automatically.
load_dotenv(find_dotenv(), override=True)


config_name = os.getenv('FLASK_ENV') or 'default'
