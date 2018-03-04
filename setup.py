from setuptools import setup, find_packages

setup(
    name="genstream",
    version="0.0.9",
    packages=find_packages(exclude=("tests*",)),
    author="lidatong",
    author_email="charles.dt.li@gmail.com",
    description="Construct stream pipelines backed by generators",
    url="https://github.com/lidatong/genstream",
    license="Unlicense",
    keywords="chaining chain generators piping pipes transformations",
    python_requires=">=3.6",
    extras_require={
        "dev": ["pytest"]
    },
    include_package_data=True
)
