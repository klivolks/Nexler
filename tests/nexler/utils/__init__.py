# __init__.py
import os
import unittest

if __name__ == "__main__":
    # Run all tests in the current directory
    loader = unittest.TestLoader()
    start_dir = os.path.dirname(os.path.abspath(__file__))
    suite = loader.discover(start_dir)

    runner = unittest.TextTestRunner()
    runner.run(suite)
