import os
from setuptools import setup, find_packages

here = os.path.abspath(os.path.dirname(__file__))

# Requirements
with open(os.path.join(here, 'requirements.txt'), 'r') as f:
    requirements = f.read().splitlines()

# Package info
NAME = 'chatbot_logger'
DESCRIPTION = 'A generic logger for chatbots'
VERSION = '0.1.0'
REQUIRES_PYTHON = '>=3.7.0'

setup(
    name=NAME,
    version=VERSION,
    description=DESCRIPTION,
    python_requires=REQUIRES_PYTHON,
    install_requires=requirements,
    packages=find_packages("src"),
    package_dir={"": "src"},
    zip_safe=False
)
