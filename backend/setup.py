from setuptools import setup, find_packages


def fetch_requirements(filename="requirements.txt"):
    with open(filename, "r") as file:
        return file.read().splitlines()


setup(
    name="calistats",
    version="0.1.0",
    description="Calisthenics progress tracker",
    author="Amir Aharon",
    author_email="amir.the.junior@gmail.com",
    packages=find_packages(),
    install_requires=fetch_requirements(),
)
