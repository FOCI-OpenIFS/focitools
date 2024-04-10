#!/usr/bin/env python

"""The setup script for FOCI Tools."""

from setuptools import setup, find_packages

#with open("README.rst") as readme_file:
#    readme = readme_file.read()

#with open("HISTORY.rst") as history_file:
#    history = history_file.read()

requirements = [
    "numpy",
    "cftime",
    "xarray",
]

setup_requirements = []

test_requirements = ["pytest"]

setup(
    author="Joakim Kjellsson",
    author_email="jkjellsson@geomar.de",
    classifiers=[
        "Development Status :: 1 - Pre-Alpha",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Natural Language :: English",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.9",
    ],
    description="focitools",
    install_requires=requirements,
    license="LGPL",
    include_package_data=True,
    keywords="focitools",
    name="focitools",
    #packages=["focitools"],
    packages=find_packages(where='focitools'),
    setup_requires=setup_requirements,
    test_suite="tests",
    tests_require=test_requirements,
    version="1.0.0",
    zip_safe=False,
)