=======
tddspry
=======

Collection of testcases and helpers to test Django projects and applications
with `nose <http://somethingaboutorange.com/mrl/projects/nose/>`_ and
`twill <http://twill.idyll.org/>`_ libraries.

#. `Key features`_
#. `Quick examples`_

   #. `Writing tests`_
   #. `Running tests`_

#. Requirements_
#. Installation_
#. License_
#. Documentation_
#. `Sending bugs and feature requests`_
#. Contacts_

Key features
============

* Support of assert methods from unittest2_ library (``assertIn``, ``assertIs``
  and others).
* Full support of all features from ``django.test.TestCase`` or
  ``django.test.TransationalTestCase`` classes.
* Run tests for Django projects and applications via ``nosetests`` command
  instead of ``python manage.py test``. You don't need to place tests in
  ``tests`` module - ``nosetests`` automaticly find its in project or
  application.
* Assert methods for testing Django models (``assert_create``,
  ``assert_count``, etc).
* Test web responses with ``twill`` library instead of using
  ``django.test.Client``.
* Helpers for make particular actions in tests (create users or superusers,
  login or logout from projects).

.. _unittest2: http://pypi.python.org/pypi/unittest2

Quick examples
==============

Writing tests
-------------

Database test
~~~~~~~~~~~~~

Check that ``username`` field of standart ``auth.User`` model is unique::

    from tddspry.django import TestCase

    from django.contrib.auth.models import User


    TEST_EMAIL = 'test-email@domain.com'
    TEST_PASSWORD = 'test-password'
    TEST_USERNAME = 'test-username'


    class TestUserModel(TestCase):

        def test_unique(self):
            self.assert_create(User,
                               username=TEST_USERNAME,
                               password=TEST_PASSWORD,
                               email=TEST_EMAIL)
            self.assert_raises(Exception,
                               self.assert_create,
                               User,
                               username=TEST_USERNAME,
                               password=TEST_PASSWORD,
                               email=TEST_EMAIL)

Http (twill) test
~~~~~~~~~~~~~~~~~

Login into project and check that login url does not exist in index page and
logout and profile links exist::

    from tddspry.django import TestCase


    class TestHttp(TestCase):

        def setup(self):
            # Create user
            self.user = self.helper('create_user')

            # Login this user into project
            self.login(self.helpers.USERNAME, self.helpers.PASSWORD)

        def test_index_links(self):
            # Login, logout and profile urls
            login_url = self.build_url('auth_login')
            logout_url = self.build_url('auth_logout')
            profile_url = self.build_url('auth_profile')

            # Go to index page
            self.go200('/')

            # Login url does not exist cause user already logged in
            self.notfind(login_url)

            # But logout and profile url exist
            # Profile url must find at page 3 times
            self.find(logout_url)
            self.find(profile_url, count=3)

Running tests
-------------

There are three ways to run tests in your project.

First, using ``nosetests`` command, e.g.::

    $ nosetests --with-django --django-settings=project.settings project
    $ DJANGO_SETTINGS_MODULE=project.settings NOSE_WTIH_DJANGO=1 nosetests project

This way requires install ``tddspry`` to your system.

Second, using ``django-nosetests.py`` script, e.g.::

    $ django-nosetests.py --django-settings=project.settings project
    $ DJANGO_SETTINGS_MODULE=project.settings django-nosetests.py project

This script is wrapper to previous method (you don't need to run ``nosetests``
with ``--with-django`` option or ``NOSE_WTIH_DJANGO`` environment var), but
does not require install ``tddspry`` to your system (it's good idea if you want
use latest development version of ``tddspry``). Script located in ``bin/``
directory.

Third, using ``TEST_RUNNER`` setting in Django >= 1.2 (requires `django-nose
app <http://github.com/jbalogh/django-nose>`_ installed)::

    TEST_RUNNER = 'tddspry.django.runner.TestSuiteRunner'

Then you can use Django's internal ``test`` manage command to run your tests::

    $ ./manage.py test

Otherwise, you can use all `power of nosetests command
<http://somethingaboutorange.com/mrl/projects/nose/0.11.0/usage.html>`_ to run
tests in your Django project or applications.

Requirements
============

* `Python <http://www.python.org/>`_ 2.4 or above
* `Django <http://www.djangoproject.com/>`_ up to trunk
* `nose <http://somethingaboutorange.com/mrl/projects/nose/>`_ 0.11.0 or above
* `twill <http://twill.idyll.org/>`_ 0.9
* `django-nose <http://github.com/jbalogh/django-nose>`_ (*optional*, required
  by test runner)
* `datadiff <http://pypi.python.org/pypi/datadiff>`_ (*optional*, required by
  ``TDDSPRY_USE_DATADIFF`` setting)

Installation
============

*On most UNIX-like systems, you'll probably need to run these commands as root
or using sudo.*

To install use::

    $ pip install tddspry

Or::

    $ python setup.py install

Also, you can retrieve fresh version of ``tddspry`` from `GitHub
<http://github.com/playpauseandstop/tddspry>`_::

    $ git clone git://github.com/playpauseandstop/tddspry.git

and place ``tddspry`` directory somewhere to ``PYTHONPATH`` (or ``sys.path``).

License
=======

``tddspry`` is licensed under the `BSD License
<http://github.com/playpauseandstop/tddspry/blob/master/LICENSE>`_.

Documentation
=============

`Sphinx <http://sphinx.pocoo.org/>`_-generated documentation for ``tddspry``
located at `GitHub pages <http://playpauseandstop.github.com/tddspry/>`_. This
documentation updates after every ``tddspry`` release.

Fresh documentation always can access in ``docs/`` directory.

Sending bugs and feature requests
=================================

Found a bug? Have a good idea for improving tddspry? Head over to `tddspry's
trac <http://trac.khavr.com/agiloprojects/tddspry>`_ to create a new ticket or
to `GitHub`_ to create a new fork.

Contacts
========

:Authors:
    Igor Davydenko *< playpauseandstop [at] gmail >*,
    Volodymyr Hotsyk *< gotsyk [at] gmail >*

:Idea:
    Andriy Khavryuchenko *< akhavr [at] gmail >*
