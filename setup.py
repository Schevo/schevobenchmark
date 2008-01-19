__version__ = '3.1a1'

from setuptools import setup, Extension, find_packages
import sys, os
import textwrap


setup(
    name="SchevoBenchmark",

    version=__version__,

    description="Performance benchmarking tool for Schevo",

    long_description=textwrap.dedent("""
    SchevoBenchmark runs a series of benchmarks to evaluate the
    performance of the Schevo_ DBMS.  Typically, developers of Schevo
    or Schevo backends will find this useful when optimizing
    algorithms used by Schevo.
    
    The latest development version is available in a `Subversion
    repository
    <http://getschevo.org/hg/repos.cgi/schevobenchmark-dev/archive/tip.tar.gz#egg=SchevoBenchmark-dev>`__.

    .. _Schevo: http://schevo.org/
    """),

    classifiers=[
    'Development Status :: 4 - Beta',
    'Environment :: Console',
    'Intended Audience :: Developers',
    'License :: OSI Approved :: GNU Library or Lesser General Public License (LGPL)',
    'Operating System :: OS Independent',
    'Programming Language :: Python',
    'Topic :: Database :: Database Engines/Servers',
    'Topic :: Software Development :: Libraries :: Application Frameworks',
    ],

    keywords='database dbms',

    author='Orbtech, L.L.C. and contributors',
    author_email='schevo@googlegroups.com',

    url='http://schevo.org/wiki/SchevoBenchmark',

    license='LGPL',

    platforms=['UNIX', 'Windows'],

    packages=find_packages(exclude=['doc', 'tests']),

    include_package_data=True,

    zip_safe=False,

    install_requires=[
    'Schevo >= 3.1a1dev',
    ],

    tests_require=[
    'nose >= 0.10.1',
    ],
    test_suite='nose.collector',

    extras_require={
    },

    dependency_links = [
    ],

    entry_points = """
    [schevo.schevo_command]
    benchmark = schevobenchmark.script:start
    """,
    )
