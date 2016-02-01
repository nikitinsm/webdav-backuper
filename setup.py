#!/usr/bin/env python

from distutils.core import setup
from setuptools import find_packages

setup\
    ( name='webdav_backuper'
    , version='1.0'
    , description='Webdav cli utility'
    , author='Sergey Nikitin'
    , author_email='nikitinsm@gmail.com'
    , url='https://github.com/nikitinsm/python-dict-tools'
    , packages = find_packages('src')
    , package_dir = {'': 'src'}
    , include_package_data = True
    )