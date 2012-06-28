#!/usr/bin/env python

from setuptools import setup, find_packages

setup(
    name='isonatrain',
    version='1.0.1',
    description="Generates files based on trigger text in Twitter streams.",
    long_description=open('README').read(),
    url='https://github.com/kgaughan/is-on-a-train/',
    install_requires=[line.rstrip() for line in open('requirements.txt')],
    py_modules=['isonatrain'],

    entry_points={
        'console_scripts': [
            'isonatrain = isonatrain:main'
        ]
    },

    classifiers=[
        'Development Status :: 4 - Beta',
        'Environment :: No Input/Output (Daemon)',
        'Intended Audience :: Other Audience',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
    ],

    author='Keith Gaughan',
    author_email='k@stereochro.me',
    maintainer='Keith Gaughan',
    maintainer_email='k@stereochro.me'
)
