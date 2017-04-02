#!/usr/bin/env python

import setuptools


setuptools.setup(
    name='fiscalyear',
    version='0.1.0',
    description='Utilities for managing the fiscal calendar',
    long_description='',
    url='https://github.com/adamjstewart/fiscalyear',
    author='Adam J. Stewart',
    author_email='ajstewart426@gmail.com',
    license='MIT',
    classifiers=[
        # Project maturity
        'Development Status :: 2 - Pre-Alpha',

        # Intended audience
        'Intended Audience :: Financial and Insurance Industry',

        # License type
        'License :: OSI Approved :: MIT License',

        # Supported Python versions
        'Programming Language :: Python',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.5',
        'Programming Language :: Python :: 2.6',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.0',
        'Programming Language :: Python :: 3.1',
        'Programming Language :: Python :: 3.2',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',

        # Type of package
        'Topic :: Office/Business :: Financial :: Accounting',
        'Topic :: Office/Business :: Scheduling',
    ],
    keywords=['fiscal year', 'fiscal quarter', 'calendar', 'datetime'],
    py_modules='fiscalyear'
)
