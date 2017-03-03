#!/usr/bin/env python

from setuptools import setup, find_packages

setup(
    name='Graylog Archiver',
    version='1.0',
    description='Archives Graylog closed indices with rsync.',
    entry_points={"console_scripts": ['graylog-archiver = graylog_archiver.cli:main']}, #noqa
    author='André Freitas',
    author_email='andre.freitas@ndrive.com',
    url='https://github.com/NDrive/graylog-archiver',
    license='MIT',
    packages=find_packages('.'),
    install_requires=[
        "elasticsearch==5.2.0"
    ]
)
