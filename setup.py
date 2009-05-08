#!/usr/bin/env python

from distutils.core import setup
import os


readme = open(os.path.join(os.path.dirname(__file__), 'README.rst'))
README = readme.read()
readme.close()

VERSION = __import__('tddspry').VERSION
if VERSION[2] != None:
    if isinstance(VERSION[2], int):
        version = '%d.%d.%d' % VERSION
    else:
        version = '%d.%d_%s' % VERSION
else:
    version = '%d.%d' % VERSION[:2]

setup(name='tddspry',
      version=version,
      description='Utilities to test Django applications with nosetests.',
      long_description=README,
      author='42 Coffee Cups',
      author_email='talk@42coffeecups.com',
      maintainer='Igor Davydenko',
      maintainer_email='playpauseandstop@gmail.com',
      url='http://github.com/playpauseandstop/tddspry',
      packages=['tddspry', 'tddspry.django'],
      classifiers=[
        'Development Status :: 3 - Alpha',
        'Environment :: Web Environment',
        'Framework :: Django',
        'License :: OSI Approved :: GNU General Public License (GPL)',
        'Topic :: Software Development :: Testing',
      ],
      keywords='django mock nose tdd testing tests twill',
      requires=['mock (>=0.5.0)', 'nose (>=0.10.3)', 'twill (>=0.9)'])
