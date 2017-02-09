#!/usr/bin/env python

from setuptools import setup

from xion import xion

setup(
    name='xion',
    version=xion.__version__,
    author='Joseph Sheedy',
    author_email='joseph.sheedy@gmail.com',
    url='https://github.com/jsheedy/xion',
    download_url='https://github.com/jsheedy/xion/tarball/0.0.1',
    keywords=['xion'],
    packages=['xion'],
    classifiers=[],
    license='LICENSE.txt',
    description='Xion AI',
    # long_description=open('README.md').read(),
)
