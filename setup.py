from setuptools import setup, find_packages
from nexler import __version__ as nexler_version

with open('requirements.txt') as f:
    requirements = f.read().splitlines()

setup(
    name=f'nexler',
    version=nexler_version,
    packages=find_packages(exclude=["tests", "docs", "app", "logs"]),
    include_package_data=True,
    install_requires=requirements,
    entry_points='''
        [console_scripts]
        nexler=nexler.cli_tools:main
    ''',
)
