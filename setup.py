from setuptools import setup, find_packages

setup(
    name='weather',
    version='0.1.0',
    packages=find_packages(include=['weather', 'weather.*']),
)
