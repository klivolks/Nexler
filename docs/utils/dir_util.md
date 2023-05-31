# `dir_util.py` User Documentation

The `dir_util.py` module provides a set of utility functions for directory and file manipulation. This makes it easy for your application to perform common operations such as creating and deleting directories, copying and moving directories, and listing files.

## Functions

- **create_directory(path: str)**: This function creates a new directory at the given path. If the directory already exists, it raises a Conflict error.

- **delete_directory(path: str)**: This function deletes the directory at the given path. If the directory does not exist, it raises a NotFound error.

- **copy_directory(source_path: str, destination_path: str)**: This function copies the directory at the source path to the destination path. If the source directory does not exist, it raises a NotFound error.

- **move_directory(source_path: str, destination_path: str)**: This function moves the directory from the source path to the destination path. If the source directory does not exist, it raises a NotFound error.

- **list_files(path: str)**: This function returns a list of all files in the directory at the given path. If the directory does not exist, it raises a NotFound error.

- **list_subdirectories(path: str)**: This function returns a list of all subdirectories in the directory at the given path. If the directory does not exist, it raises a NotFound error.

- **get_directory_size(path: str)**: This function returns the total size of the directory at the given path, including the sizes of all files and subdirectories. If the directory does not exist, it raises a NotFound error.

- **change_directory(path: str)**: This function changes the current working directory to the directory at the given path. If the directory does not exist, it raises a NotFound error.

- **get_current_directory()**: This function returns the current working directory.

- **search_file(path: str, filename: str)**: This function searches for a file with the given name in the directory at the given path and all its subdirectories. If the file is found, it returns the file's path. If the file is not found, it raises a NotFound error.

- **list_files_by_type(path: str, file_type: str)**: This function returns a list of all files of the given type in the directory at the given path. If the directory does not exist, it raises a NotFound error. The supported file types are 'modules', 'images', 'videos', and 'docs'. If an unsupported file type is specified, it raises an InternalServerError error.

## Usage

To use these utility functions, import the required functions from the `app.utils.doc_util` module and use them in your code where needed. 

For example:

```python
from app.utils.dir_util import create_directory, list_files

def setup_project():
    create_directory("new_project")
    # ... other setup code ...

def process_files():
    file_list = list_files("new_project")
    for file in file_list:
        # ... process each file ...
```

In this example, the `create_directory` function is used to create a new directory, and the `list_files` function is used to get a list of all files in that directory.