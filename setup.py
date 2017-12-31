from setuptools import setup, find_packages

setup(
    name="genstream",
    version="0.0.4",
    packages=find_packages(exclude=("tests*",)),
    author="lidatong",
    description="Construct stream pipelines backed by generators",
    license="Unlicense",
    keywords="chaining chain generators piping pipes transformations",
    python_requires=">=3.6",
    extras_require={
        "dev": ["pytest"]
    },
    include_package_data=True
)
