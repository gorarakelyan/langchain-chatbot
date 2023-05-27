import os
from setuptools import setup, find_packages


version_file = 'src/chatbot/VERSION'
with open(version_file) as vf:
    __version__ = vf.read().strip()

here = os.path.abspath(os.path.dirname(__file__))

NAME = 'chatbot'
DESCRIPTION = 'LangChain-based ChatBot'
VERSION = __version__
REQUIRES_PYTHON = '>=3.7.0'

setup(
    name=NAME,
    version=VERSION,
    description=DESCRIPTION,
    python_requires=REQUIRES_PYTHON,
    packages=find_packages("src"),
    package_dir={"": "src"},
    zip_safe=False,
    entry_points={
        'console_scripts': [
            'chatbot=chatbot.cli.cli:entrypoint',
        ],
    },
)
