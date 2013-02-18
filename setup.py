#!/usr/bin/env python

from setuptools import setup
from buildkit import *


META = get_metadata('isonatrain.py')


setup(
    name='isonatrain',
    version=META['version'],
    description="Generates files based on trigger text in Twitter streams.",
    long_description=read('README'),
    url='https://github.com/kgaughan/is-on-a-train/',
    license='MIT',
    install_requires=read_requirements('requirements.txt'),
    py_modules=['isonatrain'],
    zip_safe=True,

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

    author=META['author'],
    author_email=META['email'],
)
