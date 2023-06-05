import os
import sys
from dotenv import load_dotenv
from importlib.util import spec_from_file_location, module_from_spec

load_dotenv()

# Your directory
directory_to_add = os.getenv('PROJECT_ROOT')

# Add your directory to the sys.path
if directory_to_add not in sys.path:
    sys.path.insert(0, directory_to_add)

# Here's how you can import your config module
spec = spec_from_file_location("config", os.path.join(directory_to_add, "config.py"))
config_module = module_from_spec(spec)
spec.loader.exec_module(config_module)

from run import run

def serve():
    run()
