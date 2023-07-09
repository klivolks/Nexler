import csv
import os
from PIL import Image
from moviepy.video.io.VideoFileClip import VideoFileClip
from moviepy.video.fx import resize

from app.config import ALLOWED_EXTENSIONS


def allowed_file(filename):
    """Check if the file has an allowed extension."""
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


def read_file(path):
    """Read the contents of the file at the given path."""
    with open(path, 'r', encoding='utf-8') as file:
        return file.read()


def write_file(path, content):
    """Write the given content to the file at the given path. Overwrites existing content."""
    if allowed_file(path):
        with open(path, 'w', encoding='utf-8') as file:
            file.write(content)
    else:
        raise ValueError("File type not allowed")


def append_file(path, content):
    """Append the given content to the file at the given path."""
    if allowed_file(path):
        with open(path, 'a', encoding='utf-8') as file:
            file.write(content)
    else:
        raise ValueError("File type not allowed")


def delete_file(path):
    """Delete the file at the given path."""
    os.remove(path)


def compress_image(path, width=None, height=None):
    """Compress image to target width and/or height."""
    img = Image.open(path)
    if width and height:
        img.thumbnail((width, height))
    elif width:
        ratio = width / img.width
        img.thumbnail((width, int(img.height * ratio)))
    elif height:
        ratio = height / img.height
        img.thumbnail((int(img.width * ratio), height))
    img.save(path)
    return path


def generate_thumbnail(path, sizes=None):
    """Generate thumbnails of the given sizes for the image at the given path."""
    if sizes is None:
        sizes = [(128, 128), (256, 256), (512, 512)]
    img = Image.open(path)
    thumbnails = []
    for size in sizes:
        copy = img.copy()
        copy.thumbnail(size)
        thumbnail_path = f"{os.path.splitext(path)[0]}_{size[0]}x{size[1]}.jpg"
        copy.save(thumbnail_path)
        thumbnails.append(thumbnail_path)
    return thumbnails


def convert_video(path, target_resolution):
    """Convert video to target resolution."""
    clip = VideoFileClip(path)
    clip_resized = resize.resize(clip, height=target_resolution)
    return clip_resized.write_videofile(path, codec='libx264')


def read_file_lines(file_path):
    return read_file(file_path).splitlines()


def process_csv_data(file_data):
    rows = []
    for row in csv.DictReader(file_data.splitlines()):
        rows.append(row)
    return rows
