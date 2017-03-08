#!/usr/bin/env python

from setuptools import setup, find_packages

setup(
    name='graylog-archiver',
    version='0.1.1',
    description='Archives graylog indices', #noqa
    entry_points={"console_scripts": ['graylog-archiver = graylog_archiver.cli:main']}, #noqa
    author='André Freitas',
    author_email='andre.freitas@ndrive.com',
    url='https://github.com/NDrive/graylog-archiver',
    license='MIT',
    packages=find_packages('.'),
    install_requires=[
        "elasticsearch==5.2.0",
        "invoke==0.15.0"
    ]
)
