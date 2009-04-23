"""
==============
tddspry.django
==============

TestCases
=========

``tddspry.django`` serves several custom ``TestCase``'s for test your Django's
applications.

DatabaseTestCase
----------------

Depends on ``NoseTestCase``. On ``setup`` ``DatabaseTestCase`` creates test
``sqlite3`` database in ``:memory:`` and on ``teardown`` removes it.

Custom methods
~~~~~~~~~~~~~~

* check_create(model, \*\*kwargs)

* check_delete(instance)

* check_update(instance, \*\*kwargs)

HttpTestCase
------------

Depends on ``DatabaseTestCase``. On ``setup`` ``HttpTestCase`` creates test
database via ``django.db.connection.creation.create_test_db`` and on
``teardown`` removes it.

Also this ``TestCase`` consists of all twill_ functions as class methods.

.. _twill: http://twill.idyll.org/commands.html

Custom methods
~~~~~~~~~~~~~~

* find(what, flags='', flat=False)

  Use ``flat=True`` to disable regexp matching and use raw ``what in html``
  expression.

* notfind(what, flags='', flat=False)

  Use ``flat=True`` to disable regexp matching and use raw ``not what in html``
  expression.

More custom helpers for http tests you can find in Helpers_ section.

Helpers
=======

Also ``tddspry.django`` gives several custom helpers to easying your http
tests. To import it use::

    from tddspry.django.helpers import *

List of helpers:

* go200(url)

* login(USERNAME, PASSWORD, login_url=settings.LOGIN_URL, form_id=1)

* login_to_admin(USERNAME, PASSWORD)

* logout(logout_url=settings.LOGOUT_URL)

* submit200()

"""

from tddspry.django.cases import *
