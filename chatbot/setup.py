import os
from setuptools import setup, find_packages

here = os.path.abspath(os.path.dirname(__file__))

# Version
version_file = os.path.join(here, 'src', 'chatbot', 'VERSION')
with open(version_file) as vf:
    __version__ = vf.read().strip()

# Requirements
with open(os.path.join(here, 'requirements.txt'), 'r') as f:
    requirements = f.read().splitlines()

# Package info
NAME = 'chatbot'
DESCRIPTION = 'LangChain-based ChatBot'
VERSION = __version__
REQUIRES_PYTHON = '>=3.7.0'

setup(
    name=NAME,
    version=VERSION,
    description=DESCRIPTION,
    python_requires=REQUIRES_PYTHON,
    install_requires=requirements,
    packages=find_packages("src"),
    package_dir={"": "src"},
    zip_safe=False,
    entry_points={
        'console_scripts': [
            'chatbot=chatbot.cli.cli:entrypoint',
        ],
    },
)
