#!/usr/bin/env python

import fiscalyear
import setuptools


with open("README.rst") as readme:
    long_description = readme.read()


setuptools.setup(
    name=fiscalyear.__name__,
    version=fiscalyear.__version__,
    description="Utilities for managing the fiscal calendar",
    long_description=long_description,
    url="https://github.com/adamjstewart/fiscalyear",
    download_url="https://github.com/adamjstewart/fiscalyear/archive/v%s.tar.gz"
    % fiscalyear.__version__,
    author=fiscalyear.__author__,
    author_email="ajstewart426@gmail.com",
    license="MIT",
    classifiers=[
        # Project maturity
        "Development Status :: 3 - Alpha",
        # Intended audience
        "Intended Audience :: Financial and Insurance Industry",
        # License type
        "License :: OSI Approved :: MIT License",
        # Supported Python versions
        "Programming Language :: Python",
        "Programming Language :: Python :: 2",
        "Programming Language :: Python :: 2.5",
        "Programming Language :: Python :: 2.6",
        "Programming Language :: Python :: 2.7",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.0",
        "Programming Language :: Python :: 3.1",
        "Programming Language :: Python :: 3.2",
        "Programming Language :: Python :: 3.3",
        "Programming Language :: Python :: 3.4",
        "Programming Language :: Python :: 3.5",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        # Type of package
        "Topic :: Office/Business :: Financial :: Accounting",
        "Topic :: Office/Business :: Scheduling",
    ],
    keywords=["fiscal year", "fiscal quarter", "calendar", "datetime"],
    py_modules=[fiscalyear.__name__],
    setup_requires=["setuptools"],
    tests_require=["pytest", "pytest-mock"],
)
