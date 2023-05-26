from setuptools import setup, find_packages


setup(
    name="chatbot_logger",
    version="0.1.0",
    description="A generic logger for chatbots",
    packages=find_packages("src"),
    package_dir={"": "src"},
    zip_safe=False
)
