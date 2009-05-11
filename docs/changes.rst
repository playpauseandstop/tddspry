==================
Changes in tddspry
==================

.. _release_0.3.1:

Release 0.3.1__ (latest release)
================================

* Updates documentation (adds :doc:`changes`).
* Adds ``tddspry.get_version`` function to get human-readable version of your
  **tddspry** installation.

.. __: http://pypi.python.org/pypi/tddspry/0.3.1

.. _release_0.3:

Release 0.3__
=============

* Adds :doc:`documentation <index>`.
* Re-writes init database connection for ``:original:`` and ``custom``
  databases in :class:`tddspry.django.DatabaseTestCase` class.
* Adds object of ``django.test.Client`` to
  :class:`tddspry.django.HttpTestCase` class.
* Rewrites :mod:`test helpers <tddspry.django.helpers>`.
* Adds :ref:`django-nosetests-py`.

.. __: http://pypi.python.org/pypi/tddspry/0.3

.. _release_0.2.3:

Release 0.2.3__
===============

.. warning:: Do not use this version of **tddspry** for testing your projects.
   This version may corrupt data in your database.

.. __: http://pypi.python.org/pypi/tddspry/0.2.3

* Fixes for testing with in-memory SQLite3 databases (again).

.. _release_0.2.2:

Release 0.2.2__
===============

.. warning:: Do not use this version of **tddspry** for testing your projects.
   This version may corrupt data in your database.

.. __: http://pypi.python.org/pypi/tddspry/0.2.2

* Fixes for testing with in-memory SQLite3 databases.

.. _release_0.2.1:

Release 0.2.1__
===============

.. warning:: Do not use this version of **tddspry** for testing your projects.
   This version may corrupt data in your database.

.. __: http://pypi.python.org/pypi/tddspry/0.2.1

* First refactoring of :mod:`tddspry.django.helpers` module.

.. _release_0.2:

Release 0.2__
=============

.. warning:: Do not use this version of **tddspry** for testing your projects.
   This version may corrupt data in your database.

.. __: http://pypi.python.org/pypi/tddspry/0.2

* Full refactoring of **tddspry** library:

  * Adds :class:`tddspry.NoseTestCase` class.

  * Rewrites old ``DbMock`` and ``TwillMock`` classes to
    :class:`DatabaseTestCase <tddspry.django.DatabaseTestCase>` and
    :class:`HttpTestCase <tddspry.django.HttpTestCase>`.

  * Removes ``tddspry.mock`` module and adds `mock python module`_ to
    requirements.

.. _`mock python module`: http://pypi.python.org/pypi/mock

.. _release_0.1:

Release 0.1__
=============

.. warning:: Do not use this version of **tddspry** for any reasons. This
   version is deprecated.

* Initial release.

.. __: http://pypi.python.org/pypi/tddspry/0.1
