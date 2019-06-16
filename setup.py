from setuptools import setup, find_packages
from codecs import open
from os import path

here = path.abspath(path.dirname(__file__))

# Get the long description from the README file
with open(path.join(here, "Readme.md"), encoding="utf-8") as f:
    long_description = f.read()

setup(
    name="fireplace",
    version="2019.6.0",
    description="Fireplace",
    long_description=long_description,
    url="https://github.com/xvzf/fireplace",
    author="HTW Saar VS",
    author_email="me@xvzf.tech",
    python_requires='>=3.7',

    # Classifiers help users find your project by categorizing it.
    #
    # For a list of valid classifiers, see
    # https://pypi.python.org/pypi?%3Aaction=list_classifiers
    classifiers=[
        #   3 - Alpha
        #   4 - Beta
        #   5 - Production/Stable
        "Development Status :: 3 - Alpha",
        "Framework :: AsyncIO",
        "Programming Language :: Python",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.7",
    ],

    keywords="",
    packages=find_packages(exclude=["contrib", "docs", "tests"]),
    install_requires=[],
    tests_require=[],
)

