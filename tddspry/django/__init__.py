"""
``tddspry.django`` provides ``DatabaseTestCase`` and ``HttpTestCase`` classes
to testing Django applications.

Database tests with ``DatabaseTestCase``
----------------------------------------

For testing Django model classes and anything objects that needed database
connection you should be used ``tddspry.django.DatabaseTestCase``. This
test-case inherits ``tddspry.TestCase``, so consists of all nose tools
functions and decorators.

At ``setup`` ``DatabaseTestCase`` creates test database or flushes it if
needed and loading fixtures if possible (``database_name``,
``database_flush`` and ``fixtures`` attributes).

Also for convenience ``DatabaseTestCase`` has additional helpers:

.. autoclass :: tddspry.django.DatabaseTestCase
   :members: assert_count, assert_create, assert_delete, assert_read,
             assert_update

**Note:** Also ``DatabaseTestCase`` can call additional helper by
``helper`` method. `See below`_ how use it.

Usage
~~~~~

So, for testing CRUD_ of ``django.contrib.auth.models.Group`` model you can
write next test case::

    from tddspry.django import DatabaseTestCase

    from django.contrib.auth.models import Group


    NEW_NAME = 'Super-Test Group'
    TEST_NAME = 'Test Group'


    class TestGroup(DatabaseTestCase):

        def test_create(self):
            self.assert_create(Group, name=TEST_NAME)

        def test_delete(self):
            group = self.assert_create(Group, name=TEST_NAME)
            self.assert_delete(group)

        def test_read(self):
            self.assert_create(Group, name=TEST_NAME)
            self.assert_read(Group, name=TEST_NAME)

        def test_update(self):
            group = self.assert_create(Group, name=TEST_NAME)
            self.assert_update(group, name=NEW_NAME)

.. _`See below`: `Additional helpers`
.. _CRUD: http://en.wikipedia.org/wiki/Create,_read,_update_and_delete

Server-side tests with ``HttpTestCase``
---------------------------------------

In addition to :class:`tddspry.django.DatabaseTestCase` :mod:`tddspry.django`
provides :class:`tddspry.django.HttpTestCase` class to testing HTTP responses
with `Twill browser`_ and `django.test.Client`_.

At setup ``HttpTestCase`` run Django WSGI server and connects it with
twill browser.

For historical reasons ``HttpTestCase`` was developed for testing Django
applications with Twill browser, so its consists of all functions exists
in `twill.commands`_ module as class methods.

And for convenience several twill methods was simplifying and rewriting, there
are:

.. autoclass :: tddspry.django.HttpTestCase
   :members: find, go, notfind, url

And from :ref:`release_0.3` of ``tddspry`` ``HttpTestCase`` consist of ``client``
attribute that stores instance of ``django.test.Client`` class.

Also, ``HttpTestCase`` provides next methods:

.. autoclass :: tddspry.django.HttpTestCase
   :members: build_url, disable_edit_hidden_fields, disable_redirect,
             enable_edit_hidden_fields, enable_redirect, go200, login,
             login_to_admin, logout, submit200

Usage
~~~~~

So, for testing login/logout process in your project you can write next
test-case::

    from tddspry.django import HttpTestCase

    from django.conf import settings


    class TestLoginPage(HttpTestCase):

        def test_login(self):
            user = self.helper('create_user', 'username', 'password')
            self.login('username', 'password')
            self.url(settings.LOGIN_REDIRECT_URL)

        def test_logout(self):
            user = self.helper('create_user', 'username', 'password')
            self.login('username', 'password')
            self.logout()
            self.url('/')

.. _`Twill browser`: http://twill.idyll.org/
.. _`django.test.Client`: http://docs.djangoproject.com/en/dev/topics/testing/#module-django.test.client
.. _`twill.commands`: http://twill.idyll.org/commands.html

"""

from tddspry.django.cases import *

try:
    from tddspry.django.runner import *
except ImportError:
    pass
