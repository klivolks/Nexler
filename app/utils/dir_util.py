import os
import shutil
from typing import List, Any
from werkzeug.exceptions import Conflict, NotFound, BadRequest, InternalServerError
from dotenv import load_dotenv
from app.utils import response_util

load_dotenv()
app_directory = os.getenv('PROJECT_ROOT', os.path.dirname(os.path.abspath(__file__)))


def safe_join(*args):
    """Joins a path and ensures that it's within the app directory."""
    path = os.path.join(*args)
    if os.path.abspath(path).startswith(app_directory):
        return path
    else:
        raise BadRequest(response_util.error(f"Path {path} is outside of the app directory."))


def create_directory(path: str):
    absolute_path = safe_join(app_directory, path)
    if not os.path.exists(absolute_path):
        os.makedirs(absolute_path)
        return {"message": f"Directory {absolute_path} created."}
    else:
        raise Conflict(response_util.error("Directory already exists."))


def delete_directory(path: str):
    absolute_path = safe_join(app_directory, path)
    if os.path.exists(absolute_path):
        shutil.rmtree(absolute_path)
        return {"message": f"Directory {absolute_path} deleted."}
    else:
        raise NotFound(response_util.error("Directory does not exist."))


def copy_directory(source_path: str, destination_path: str):
    absolute_source_path = safe_join(app_directory, source_path)
    absolute_destination_path = safe_join(app_directory, destination_path)
    if os.path.exists(absolute_source_path):
        shutil.copytree(absolute_source_path, absolute_destination_path)
        return {"message": f"Directory copied from {absolute_source_path} to {absolute_destination_path}."}
    else:
        raise NotFound(response_util.error("Source directory does not exist."))


def move_directory(source_path: str, destination_path: str):
    absolute_source_path = safe_join(app_directory, source_path)
    absolute_destination_path = safe_join(app_directory, destination_path)
    if os.path.exists(absolute_source_path):
        shutil.move(absolute_source_path, absolute_destination_path)
        return {"message": f"Directory moved from {absolute_source_path} to {absolute_destination_path}."}
    else:
        raise NotFound(response_util.error("Source directory does not exist."))


def list_files(path: str):
    absolute_path = safe_join(app_directory, path)
    if os.path.exists(absolute_path):
        return [f for f in os.listdir(absolute_path) if os.path.isfile(os.path.join(absolute_path, f))]
    else:
        raise NotFound(response_util.error(f"Directory does not exist."))


def list_subdirectories(path: str):
    absolute_path = safe_join(app_directory, path)
    if os.path.exists(absolute_path):
        return [f for f in os.listdir(absolute_path) if os.path.isdir(os.path.join(absolute_path, f))]
    else:
        raise NotFound(response_util.error("Directory does not exist."))


def get_directory_size(path: str):
    absolute_path = safe_join(app_directory, path)
    if os.path.exists(absolute_path):
        total = 0
        with os.scandir(absolute_path) as it:
            for entry in it:
                if entry.is_file():
                    total += entry.stat().st_size
                elif entry.is_dir():
                    total += get_directory_size(entry.path)
        return {"size": total}
    else:
        raise NotFound(response_util.error("Directory does not exist."))


def change_directory(path: str):
    absolute_path = safe_join(app_directory, path)
    if os.path.exists(absolute_path):
        os.chdir(absolute_path)
        return {"message": f"Changed directory to {absolute_path}"}
    else:
        raise NotFound(response_util.error("Directory does not exist."))


def get_current_directory():
    return {"current_directory": os.getcwd()}


def app_path():
    return app_directory


def search_file(path: str, filename: str):
    absolute_path = safe_join(app_directory, path)
    for root, dirs, files in os.walk(absolute_path):
        if filename in files:
            return {"file_path": os.path.join(root, filename)}
    raise NotFound(response_util.error("File not found in directory."))


def list_files_by_type(path: str, file_type: str) -> list[Any] | list[bytes]:
    absolute_path = safe_join(app_directory, path)
    if not os.path.exists(absolute_path):
        raise NotFound(response_util.error("Directory does not exist."))
    if file_type == 'modules':
        return [os.path.splitext(f)[0] for f in os.listdir(absolute_path)
                if os.path.isfile(os.path.join(absolute_path, f))
                and os.path.splitext(f)[1] == '.py'
                and f != '__init__.py']
    elif file_type == 'images':
        img_ext = ['.png', '.jpg', '.jpeg', '.gif', '.bmp', '.ico', '.jfif', '.webp', '.tiff']
        return [f for f in os.listdir(absolute_path)
                if os.path.isfile(os.path.join(absolute_path, f))
                and os.path.splitext(f)[1].lower() in img_ext]
    elif file_type == 'videos':
        vid_ext = ['.mp4', '.mkv', '.flv', '.avi', '.mov', '.wmv']
        return [f for f in os.listdir(absolute_path)
                if os.path.isfile(os.path.join(absolute_path, f))
                and os.path.splitext(f)[1].lower() in vid_ext]
    elif file_type == 'docs':
        doc_ext = ['.pdf', '.doc', '.docx', '.xls', '.xlsx', '.csv']
        return [f for f in os.listdir(absolute_path)
                if os.path.isfile(os.path.join(absolute_path, f))
                and os.path.splitext(f)[1].lower() in doc_ext]
    elif file_type == 'json':
        doc_ext = ['.json']
        return [os.path.splitext(f)[0] for f in os.listdir(absolute_path)
                if os.path.isfile(os.path.join(absolute_path, f))
                and os.path.splitext(f)[1].lower() in doc_ext]
    else:
        raise InternalServerError(response_util.error(f"Invalid file type: {file_type}"))
