# -*- coding: utf-8 -*-

#    Visigoth: A lightweight Python3 library for rendering data visualizations in SVG
#    Copyright (C) 2020  Niall McCarroll
#
#   Permission is hereby granted, free of charge, to any person obtaining a copy of this software
#   and associated documentation files (the "Software"), to deal in the Software without
#   restriction, including without limitation the rights to use, copy, modify, merge, publish,
#   distribute, sublicense, and/or sell copies of the Software, and to permit persons to whom the
#   Software is furnished to do so, subject to the following conditions:
#
#   The above copyright notice and this permission notice shall be included in all copies or
#   substantial portions of the Software.
#
#   THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING
#   BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND
#   NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM,
#   DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
#   OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.

"""setuptools based setup module for visigoth.
"""

from setuptools import setup, find_packages
from visigoth import version, repo_url

setup(
    name='visigoth',

    version=version,

    description='Python3 library for rendering geospatial infographics',

    long_description="Python3 library for creating static data-driven geospatial infographics as SVG files",

    url=repo_url,

    author='Niall McCarroll',
    author_email='',
    python_requires='>=3.5',

    license='License :: OSI Approved :: MIT License',

    classifiers=[
        'Development Status :: 3 - Alpha',

        'Intended Audience :: Developers',

        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.5',
    ],

    keywords='svg geospatial infographics gis data science visualization',

    packages=find_packages(exclude=["tests.*","tests"]),

    install_requires=[],

    extras_require={
    },

    # package_data={'fonts': ['font_dimensions.db','Roboto/*']},

    entry_points={
    },

    include_package_data=True
)
