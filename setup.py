#!/usr/bin/env python
import os

try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup
    kwargs = {}
else:
    kwargs = {
        'entry_points': """
        [nose.plugins.0.10]
        django = tddspry.noseplugins:DjangoPlugin
        """
    }



readme = open(os.path.join(os.path.dirname(__file__), 'README.rst'))
README = readme.read()
readme.close()

requires = ['Django (>= 1.0)', 'nose (>= 0.10.4)', 'twill (>= 0.9)']
version = __import__('tddspry').get_version()

setup(name='tddspry',
      version=version,
      description='Collection of test cases and additional helpers to test ' \
                  'Django applications with nose library.',
      long_description=README,

      author='42 Coffee Cups',
      author_email='talk@42coffeecups.com',
      maintainer='Igor Davydenko',
      maintainer_email='playpauseandstop@gmail.com',
      url='http://github.com/42/tddspry',

      packages=['tddspry', 'tddspry.django', 'tddspry.django.helpers',
                'tddspry.noseplugins'],
      scripts=['bin/django-nosetests.py'],

      classifiers=[
          'Development Status :: 4 - Beta',
          'Environment :: Web Environment',
          'Framework :: Django',
          'License :: OSI Approved :: GNU General Public License (GPL)',
          'Topic :: Software Development :: Testing',
      ],
      keywords='django nose tdd testing tests twill',

      setup_requires=[r.replace('(', '').replace(')', '') for r in requires \
                      if not r.startswith('Django')],
      requires=requires,

      **kwargs)
