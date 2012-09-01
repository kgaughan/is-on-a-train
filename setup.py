#!/usr/bin/env python

from setuptools import setup
import re


def read(filename):
    with open(filename, 'r') as fh:
        return fh.read()


def get_metadata(module_path):
    """Extract the metadata from a module file."""
    matches = re.finditer(
        r"^__(\w+?)__ *= *'(.*?)'$",
        read(module_path),
        re.MULTILINE)
    return dict(
        (match.group(1), match.group(2).decode('unicode_escape'))
        for match in matches)


def read_requirements(requirements_path):
    """Read a requirements file, stripping out the detritus."""
    requirements = []
    with open(requirements_path, 'r') as fh:
        for line in fh:
            line = line.strip()
            if line != '' and not line.startswith(('#', 'svn+', 'git+')):
                requirements.append(line)
    return requirements


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
    author_email=META['email']
)
