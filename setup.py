##############################################################################
#
# Copyright (c) 2008 Agendaless Consulting and Contributors.
# All Rights Reserved.
#
# This software is subject to the provisions of the BSD-like license at
# http://www.repoze.org/LICENSE.txt.  A copy of the license should accompany
# this distribution.  THIS SOFTWARE IS PROVIDED "AS IS" AND ANY AND ALL
# EXPRESS OR IMPLIED WARRANTIES ARE DISCLAIMED, INCLUDING, BUT NOT LIMITED TO,
# THE IMPLIED WARRANTIES OF TITLE, MERCHANTABILITY, AGAINST INFRINGEMENT, AND
# FITNESS FOR A PARTICULAR PURPOSE
#
##############################################################################

__version__ = '0.7.6'

import os
import sys

from setuptools import setup, find_packages

here = os.path.abspath(os.path.dirname(__file__))
try:
    README = open(os.path.join(here, 'README.txt')).read()
    CHANGES = open(os.path.join(here, 'CHANGES.txt')).read()
except:
    README = ''
    CHANGES = ''

if sys.version_info >= (2, 6): #pragma NO COVER Python >= 2.6
    requires = [
        'setuptools',
        'zope.component',
        'zope.configuration',
        'zope.interface',
        ]

    tests_require = requires + [
        'zope.testing',
        ]
else: #pragma NO COVER Python < 2.6
    requires = [
        'setuptools',
        'zope.schema<4.0dev',
        'zope.component<3.11dev',
        'zope.configuration<3.7dev',
        'zope.interface<3.8dev',
        ]

    tests_require = requires + [
        'zope.testing<4.1dev',
        ]

testing_extras = ['nose', 'coverage']

_DESC = """ repoze.lemonade is a collection of utilties that make it possible
to create Zope CMF-like applications without requiring any particular
persistence mechanism. It makes use of the Zope component architecture. """

setup(name='repoze.lemonade',
      version=__version__,
      description=_DESC,
      long_description=README + '\n\n' +  CHANGES,
      classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
        "Programming Language :: Python",
        "Programming Language :: Python :: 2.4",
        "Programming Language :: Python :: 2.5",
        "Programming Language :: Python :: 2.6",
        "Programming Language :: Python :: 2.7",
        "Programming Language :: Python :: Implementation :: CPython",
        "Topic :: Internet :: WWW/HTTP",
        "Topic :: Internet :: WWW/HTTP :: Dynamic Content",
        "Topic :: Internet :: WWW/HTTP :: WSGI",
        "Topic :: Internet :: WWW/HTTP :: WSGI :: Middleware",
        ],
      keywords='web wsgi zope',
      author="Agendaless Consulting",
      author_email="repoze-dev@lists.repoze.org",
      url="http://www.repoze.org",
      license="BSD-derived (http://www.repoze.org/LICENSE.txt)",
      packages=find_packages(),
      include_package_data=True,
      namespace_packages=['repoze', 'repoze.lemonade'],
      zip_safe=False,
      tests_require = tests_require,
      install_requires = requires,
      test_suite="repoze.lemonade",
      entry_points = """\
      """,
      extras_require = {
        'testing':  tests_require + testing_extras,
      }
)

