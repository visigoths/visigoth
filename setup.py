"""setuptools based setup module for visigoth.
"""

from setuptools import setup, find_packages

setup(
    name='visigoth',

    version='0.2.1',

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
