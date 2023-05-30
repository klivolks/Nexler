import os
import unittest
from unittest import mock
from werkzeug.exceptions import NotFound, Conflict

from app.utils import dir_util


class TestDirUtil(unittest.TestCase):
    def test_create_directory_success(self):
        with mock.patch('os.path.exists', return_value=False), mock.patch('os.makedirs') as mock_makedirs:
            response = dir_util.create_directory('/path/to/dir')
            mock_makedirs.assert_called_once_with('/path/to/dir')
            self.assertEqual(response, {"message": "Directory /path/to/dir created."})

    def test_create_directory_failure(self):
        with mock.patch('os.path.exists', return_value=True):
            with self.assertRaises(Conflict):
                dir_util.create_directory('/path/to/dir')

    def test_delete_directory_success(self):
        with mock.patch('os.path.exists', return_value=True), mock.patch('shutil.rmtree') as mock_rmtree:
            response = dir_util.delete_directory('/path/to/dir')
            mock_rmtree.assert_called_once_with('/path/to/dir')
            self.assertEqual(response, {"message": "Directory /path/to/dir deleted."})

    def test_delete_directory_failure(self):
        with mock.patch('os.path.exists', return_value=False):
            with self.assertRaises(NotFound):
                dir_util.delete_directory('/path/to/dir')

    def test_copy_directory_success(self):
        with mock.patch('os.path.exists', return_value=True), mock.patch('shutil.copytree') as mock_copytree:
            response = dir_util.copy_directory('/path/to/source', '/path/to/destination')
            mock_copytree.assert_called_once_with('/path/to/source', '/path/to/destination')
            self.assertEqual(response, {"message": "Directory copied from /path/to/source to /path/to/destination."})

    def test_copy_directory_failure(self):
        with mock.patch('os.path.exists', return_value=False):
            with self.assertRaises(NotFound):
                dir_util.copy_directory('/path/to/source', '/path/to/destination')

    def test_move_directory_success(self):
        with mock.patch('os.path.exists', return_value=True), mock.patch('shutil.move') as mock_move:
            response = dir_util.move_directory('/path/to/source', '/path/to/destination')
            mock_move.assert_called_once_with('/path/to/source', '/path/to/destination')
            self.assertEqual(response, {"message": "Directory moved from /path/to/source to /path/to/destination."})

    def test_move_directory_failure(self):
        with mock.patch('os.path.exists', return_value=False):
            with self.assertRaises(NotFound):
                dir_util.move_directory('/path/to/source', '/path/to/destination')

    def test_list_files_success(self):
        with mock.patch('os.path.exists', return_value=True), \
                mock.patch('os.listdir', return_value=['file1', 'file2']), \
                mock.patch('os.path.isfile', side_effect=[True, True]):
            response = dir_util.list_files('/path/to/dir')
            self.assertEqual(response, ['file1', 'file2'])

    def test_list_files_failure(self):
        with mock.patch('os.path.exists', return_value=False):
            with self.assertRaises(NotFound):
                dir_util.list_files('/path/to/dir')

    def test_list_subdirectories_success(self):
        with mock.patch('os.path.exists', return_value=True), \
                mock.patch('os.listdir', return_value=['dir1', 'dir2']), \
                mock.patch('os.path.isdir', side_effect=[True, True]):
            response = dir_util.list_subdirectories('/path/to/dir')
            self.assertEqual(response, ['dir1', 'dir2'])

    def test_list_subdirectories_failure(self):
        with mock.patch('os.path.exists', return_value=False):
            with self.assertRaises(NotFound):
                dir_util.list_subdirectories('/path/to/dir')

    def test_search_file_success(self):
        with mock.patch('os.walk') as mock_walk:
            mock_walk.return_value = iter([('/path/to', [], ['filename'])])
            response = dir_util.search_file('/path/to', 'filename')
            self.assertEqual(response, {"file_path": "/path/to/filename"})

    def test_search_file_failure(self):
        with mock.patch('os.walk') as mock_walk:
            mock_walk.return_value = iter([])
            with self.assertRaises(NotFound):
                dir_util.search_file('/path/to', 'filename')


if __name__ == '__main__':
    unittest.main()
