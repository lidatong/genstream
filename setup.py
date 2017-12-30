from setuptools import setup, find_packages
setup(
    name="genstream",
    version="0.0.1",
    packages=find_packages(),
    author="lidatong",
    description="Construct stream pipelines backed by generators",
    license="Unlicense",
    keywords="chaining chain generators piping pipes transformations",
    python_requires=">=3.6"
)