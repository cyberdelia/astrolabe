# -*- coding: utf-8 -*-
import os
import sys

from setuptools import setup, find_packages, Extension


with open('README.rst') as f:
    readme = f.read()

with open('LICENSE') as f:
    license = f.read()

if 'darwin' in str(sys.platform).lower():
    os.environ['LDFLAGS'] = '-framework CoreServices'

kwargs = {}
if "java" not in sys.version.lower():
    kwargs = dict(ext_modules=[
        Extension("astrolabe._instant", ["astrolabe/_instant.c"],
        )
    ])

setup(
    name='astrolabe',
    version='0.1.3',
    description='Fast, high resolution timer library for recording performance metrics.',
    long_description=readme,
    author='Timothée Peignier',
    author_email='timothee.peignier@tryphon.org',
    url='https://github.com/cyberdelia/astrolabe',
    license=license,
    packages=find_packages(),
    zip_safe=False,
    include_package_data=True,
    classifiers=[
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Topic :: Utilities',
    ],
    **kwargs
)
