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
        """,
    }


readme = open(os.path.join(os.path.dirname(__file__), 'README.rst'))
README = readme.read()
readme.close()

requires = ['Django (>= 1.0)', 'nose (>= 0.11.0)', 'twill (>= 0.9)']
version = __import__('tddspry').get_version()

if kwargs:
    install_requires = [r.replace('(', '').replace(')', '') for r in requires \
                        if not r.startswith('Django')]
    kwargs.update({'install_requires': install_requires,
                   'setup_requires': install_requires})

setup(name='tddspry',
      version=version,
      description='Collection of test cases and additional helpers to test ' \
                  'Django applications with nose library.',
      long_description=README,

      author='Igor Davydenko',
      author_email='playpauseandstop@gmail.com',
      url='http://github.com/playpauseandstop/tddspry',

      packages=['tddspry', 'tddspry.django', 'tddspry.django.helpers',
                'tddspry.noseplugins'],
      scripts=['bin/django-nosetests.py'],

      classifiers=[
          'Development Status :: 4 - Beta',
          'Environment :: Web Environment',
          'Framework :: Django',
          'License :: OSI Approved :: BSD License',
          'Topic :: Software Development :: Testing',
      ],
      keywords='django nose tdd testing tests twill',

      requires=requires,

      **kwargs)
