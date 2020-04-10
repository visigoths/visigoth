# -*- coding: utf-8 -*-

#    Visigoth: A lightweight Python3 library for rendering data visualizations in SVG
#    Copyright (C) 2020  Niall McCarroll
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU Affero General Public License as published by
#    the Free Software Foundation, either version 3 of the License, or
#    (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU Affero General Public License for more details.
#
#    You should have received a copy of the GNU Affero General Public License
#    along with this program.  If not, see <https://www.gnu.org/licenses/>.

"""setuptools based setup module for visigoth.
"""

from setuptools import setup, find_packages

setup(
    name='visigoth',

    version='0.2.2',

    description='Python3 library for rendering geospatial infographics',
    long_description="Python3 library for creating static data-driven geospatial infographics as SVG files",

    url='https://github.com/visigoths/visigoth',

    author='Niall McCarroll',
    author_email='',
    python_requires='>=3.5',

    license='License :: OSI Approved :: GNU Affero General Public License v3 or later (GPLv3+)',

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
