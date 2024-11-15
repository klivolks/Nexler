import unittest
import os
from PIL import Image
from moviepy.video.io.VideoFileClip import VideoFileClip
from nexler.utils import file_util


class TestFileUtil(unittest.TestCase):
    def setUp(self):
        self.image_path = 'files/new-orleans.jpg'
        self.video_path = 'files/SampleVideo_1280x720_1mb.mp4'
        self.temp_img_path = 'files/temp_new-orleans.jpg'
        self.temp_video_path = 'files/temp_SampleVideo.mp4'

    def tearDown(self):
        if os.path.exists(self.temp_img_path):
            os.remove(self.temp_img_path)
        if os.path.exists(self.temp_video_path):
            os.remove(self.temp_video_path)

    def test_allowed_file(self):
        self.assertTrue(file_util.allowed_file('test.txt'))
        self.assertFalse(file_util.allowed_file('test.abc'))

    def test_read_file(self):
        with open('test.txt', 'w') as f:
            f.write('Hello World')
        self.assertEqual(file_util.read_file('test.txt'), 'Hello World')

    def test_write_file(self):
        file_util.write_file('test.txt', 'Hello again')
        with open('test.txt', 'r') as f:
            self.assertEqual(f.read(), 'Hello again')

    def test_append_file(self):
        file_util.append_file('test.txt', ' World')
        with open('test.txt', 'r') as f:
            self.assertEqual(f.read(), 'Hello again World')

    def test_delete_file(self):
        file_util.delete_file('test.txt')
        self.assertFalse(os.path.exists('test.txt'))

    def test_compress_image(self):
        import shutil
        shutil.copy2(self.image_path, self.temp_img_path)
        file_util.compress_image(self.temp_img_path, 128, 128)
        img = Image.open(self.temp_img_path)
        self.assertEqual(max(img.size), 128)

    def test_generate_thumbnail(self):
        thumbnails = file_util.generate_thumbnail(self.image_path)
        self.assertEqual(len(thumbnails), 3)  # Expecting 3 thumbnails
        for thumbnail in thumbnails:
            self.assertTrue(os.path.exists(thumbnail))
            os.remove(thumbnail)  # Cleanup thumbnails

    def test_convert_video(self):
        import shutil
        shutil.copy2(self.video_path, self.temp_video_path)
        file_util.convert_video(self.temp_video_path, 480)
        clip = VideoFileClip(self.temp_video_path)
        self.assertEqual(clip.size[1], 480)


if __name__ == '__main__':
    unittest.main()
