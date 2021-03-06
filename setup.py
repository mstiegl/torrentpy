# -*- coding: utf-8 -*-
# Copyright (C) 2018  Thibault Hallouin
from setuptools import setup


with open("README.md", "r") as fh:
    long_desc = fh.read()

setup(
    name='torrentpy',

    version='0.2.0',

    description='TORRENTpy: a tool for TranspORt thRough the catchmEnt NeTwork',
    long_description=long_desc,
    long_description_content_type="text/markdown",

    url='https://github.com/ThibHlln/torrentpy',

    author='Thibault Hallouin, Michael Bruen, and Eva Mockler',
    author_email='thibault.hallouin@ucdconnect.ie',

    license='GPLv3',

    classifiers=[
        'Development Status :: 4 - Beta',

        'Natural Language :: English',

        'Intended Audience :: Science/Research',
        'Intended Audience :: Developers',
        'Topic :: Scientific/Engineering',

        'Operating System :: MacOS',
        'Operating System :: Microsoft :: Windows',
        'Operating System :: POSIX :: Linux',


        'License :: OSI Approved :: GNU General Public License v3 (GPLv3)',

        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: Implementation :: CPython'
    ],

    packages=['torrentpy', 'torrentpy.utils', 'torrentpy.models', 'torrentpy.models.catchment',
              'torrentpy.models.river', 'torrentpy.models.lake', 'examples'],

    install_requires=[
        'numpy',
        'future'
    ],

    extras_require={
        'with_netcdf': ['netCDF4'],
        'with_graphviz': ['graphviz'],
        'with_smartcpp': ['smartcpp'],
        'with_all_extras': ['netCDF4', 'graphviz', 'smartcpp']
    }
)
