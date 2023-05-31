# `file_util.py` User Documentation

The `file_util.py` module offers a variety of utility functions to handle file I/O operations, as well as perform image and video file processing. This module is part of the `app.utils` package.

## Functions

Below is a detailed explanation of each function:

### File Management Functions

File management functions are used to perform I/O operations and handle file-specific actions.

- **`allowed_file(filename)`**: This function validates if the input file has an allowed extension. If not, it returns False.

- **`read_file(path)`**: This function reads the contents of the file located at the given path and returns the content as a string.

- **`write_file(path, content)`**: This function writes the provided content to the file at the specified path. It overwrites existing content. If the file type is not allowed, it raises a ValueError.

- **`append_file(path, content)`**: This function appends the given content to the file at the specified path. If the file type is not allowed, it raises a ValueError.

- **`delete_file(path)`**: This function deletes the file at the specified path.

### Image and Video Processing Functions

These functions provide tools for image and video processing.

- **`compress_image(path, width=None, height=None)`**: This function compresses the image at the given path to a specified width and/or height while maintaining the aspect ratio.

- **`generate_thumbnail(path, sizes=None)`**: This function generates thumbnails of the given sizes for the image at the specified path.

- **`convert_video(path, target_resolution)`**: This function converts the video at the given path to a target resolution.

In all of the above functions, `path` is the location of the file to be processed. Additional parameters vary depending on the function.

If any error occurs during the processing of the functions, they return an error message detailing the cause of the failure.

## Usage

To utilize these utility functions, import the required functions from the `app.utils.file_util` module and use them in your code where needed.

For example:

```python
from app.utils.file_util import write_file

def save_content():
    path = "/path/to/file.txt"
    content = "This is some content"
    write_file(path, content)
    # rest of the code
```

In this example, the `write_file` function is used to write the string "This is some content" to the file located at "/path/to/file.txt". If the file extension is not allowed, the function will raise a ValueError. If the operation is successful, the function will write the content to the file.