#!/usr/bin/env python

from distutils.core import setup
from setuptools import find_packages


setup\
    ( name='webdav_backuper'
    , version='1.0'
    , description='Webdav backup cli utility'
    , author='Sergey Nikitin'
    , author_email='nikitinsm@gmail.com'
    , url='https://github.com/nikitinsm/webdav-backuper'
    , packages=find_packages('src')
    , package_dir={'': 'src'}
    , include_package_data=True
    , entry_points =
        { 'console_scripts':
            [ 'webdav-backuper=webdav_backuper.cli:main'
            , ]
        , }
    , install_requires=
        [ 'webdavclient'
        , ]
    )