import os
import unittest
from unittest import mock
from werkzeug.exceptions import NotFound, Conflict
from tempfile import TemporaryDirectory

from app.utils import dir_util


class TestDirUtil(unittest.TestCase):
    def setUp(self):
        self.APP_DIRECTORY = dir_util.app_directory
        self.temp_dir = TemporaryDirectory(dir=self.APP_DIRECTORY)

    def tearDown(self):
        self.temp_dir.cleanup()

    def test_create_directory_success(self):
        with mock.patch('os.path.exists', return_value=False), \
                mock.patch('os.makedirs') as mock_makedirs:
            response = dir_util.create_directory(self.temp_dir.name)
            mock_makedirs.assert_called_once_with(self.temp_dir.name)
            self.assertEqual(response, {"message": f"Directory {self.temp_dir.name} created."})

    def test_create_directory_outside_app(self):
        outside_dir = "/outside_app"
        with mock.patch('os.path.exists', return_value=False), \
                mock.patch('os.makedirs') as mock_makedirs, \
                mock.patch('app.utils.dir_util.safe_join',
                           side_effect=Exception("Path is not a subpath of the app directory.")):
            with self.assertRaises(Exception):
                dir_util.create_directory(outside_dir)
            mock_makedirs.assert_not_called()

    def test_create_directory_failure(self):
        with mock.patch('os.path.exists', return_value=True):
            with self.assertRaises(Conflict):
                dir_util.create_directory(self.temp_dir.name)

    def test_delete_directory_success(self):
        with mock.patch('os.path.exists', return_value=True), \
                mock.patch('shutil.rmtree') as mock_rmtree:
            response = dir_util.delete_directory(self.temp_dir.name)
            mock_rmtree.assert_called_once_with(self.temp_dir.name)
            self.assertEqual(response, {"message": f"Directory {self.temp_dir.name} deleted."})

    def test_delete_directory_failure(self):
        with mock.patch('os.path.exists', return_value=False):
            with self.assertRaises(NotFound):
                dir_util.delete_directory(self.temp_dir.name)

    def test_copy_directory_success(self):
        with mock.patch('os.path.exists', return_value=True), \
                mock.patch('shutil.copytree') as mock_copytree:
            response = dir_util.copy_directory(os.path.join(self.temp_dir.name, 'source'),
                                               os.path.join(self.temp_dir.name, 'destination'))
            mock_copytree.assert_called_once_with(os.path.join(self.temp_dir.name, 'source'),
                                                  os.path.join(self.temp_dir.name, 'destination'))
            self.assertEqual(response, {
                "message": f"Directory copied from {os.path.join(self.temp_dir.name, 'source')} to {os.path.join(self.temp_dir.name, 'destination')}."})

    def test_copy_directory_failure(self):
        with mock.patch('os.path.exists', return_value=False):
            with self.assertRaises(NotFound):
                dir_util.copy_directory(os.path.join(self.temp_dir.name, 'source'),
                                        os.path.join(self.temp_dir.name, 'destination'))

    def test_move_directory_success(self):
        with mock.patch('os.path.exists', return_value=True), \
                mock.patch('shutil.move') as mock_move:
            response = dir_util.move_directory(os.path.join(self.temp_dir.name, 'source'),
                                               os.path.join(self.temp_dir.name, 'destination'))
            mock_move.assert_called_once_with(os.path.join(self.temp_dir.name, 'source'),
                                              os.path.join(self.temp_dir.name, 'destination'))
            self.assertEqual(response, {
                "message": f"Directory moved from {os.path.join(self.temp_dir.name, 'source')} to {os.path.join(self.temp_dir.name, 'destination')}."})

    def test_move_directory_failure(self):
        with mock.patch('os.path.exists', return_value=False):
            with self.assertRaises(NotFound):
                dir_util.move_directory(os.path.join(self.temp_dir.name, 'source'),
                                        os.path.join(self.temp_dir.name, 'destination'))

    def test_list_files_success(self):
        with mock.patch('os.path.exists', return_value=True), \
                mock.patch('os.listdir', return_value=['file1', 'file2']), \
                mock.patch('os.path.isfile', side_effect=[True, True]):
            response = dir_util.list_files(self.temp_dir.name)
            self.assertEqual(response, ['file1', 'file2'])

    def test_list_files_failure(self):
        with mock.patch('os.path.exists', return_value=False):
            with self.assertRaises(NotFound):
                dir_util.list_files(self.temp_dir.name)

    def test_list_subdirectories_success(self):
        with mock.patch('os.path.exists', return_value=True), \
                mock.patch('os.listdir', return_value=['dir1', 'dir2']), \
                mock.patch('os.path.isdir', side_effect=[True, True]):
            response = dir_util.list_subdirectories(self.temp_dir.name)
            self.assertEqual(response, ['dir1', 'dir2'])

    def test_list_subdirectories_failure(self):
        with mock.patch('os.path.exists', return_value=False):
            with self.assertRaises(NotFound):
                dir_util.list_subdirectories(self.temp_dir.name)

    def test_search_file_success(self):
        with mock.patch('os.path.exists', return_value=True), \
                mock.patch('os.walk', return_value=iter([(self.temp_dir.name, [], ['filename'])])):
            response = dir_util.search_file(self.temp_dir.name, 'filename')
            self.assertEqual(response, {"file_path": os.path.join(self.temp_dir.name, 'filename')})

    def test_search_file_failure(self):
        with mock.patch('os.path.exists', return_value=True), \
                mock.patch('os.walk', return_value=iter([])):
            with self.assertRaises(NotFound):
                dir_util.search_file(self.temp_dir.name, 'filename')


if __name__ == '__main__':
    unittest.main()
