# -*- coding: utf-8 -*-
import io

from setuptools import setup, find_packages


with io.open('README.rst', encoding='utf-8') as f:
    readme = f.read()

with io.open('LICENSE', encoding='utf-8') as f:
    license = f.read()

setup(
    name='astrolabe',
    version='0.4.0',
    description='Timer library for recording performance metrics.',
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
        'Programming Language :: Python :: 3',
        'Topic :: Utilities',
    ]
)
