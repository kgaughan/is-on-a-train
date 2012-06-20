#!/usr/bin/env python

from setuptools import setup, find_packages
import isonatrain

setup(
    name='isonatrain',
    version=isonatrain.__version__,
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

    author=isonatrain.__author__,
    author_email=isonatrain.__email__,
    maintainer=isonatrain.__author__,
    maintainer_email=isonatrain.__email__
)
