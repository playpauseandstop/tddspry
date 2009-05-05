=======
tddspry
=======

1. Introduction_
2. Requirements_
3. Installation_
4. Usage_

Introduction
============

**tddspry** is collection of utilities for testing Django applications with
nosetests_ library.

.. _nosetests: http://code.google.com/p/python-nose/

Requirements
============

- Django_ >= 1.0
- mock_ >= 0.5.0
- nose_ >= 0.10.3
- twill_ >= 0.9

.. _Django: http://www.djangoproject.com/download/
.. _mock: http://pypi.python.org/pypi/mock/
.. _nose: http://pypi.python.org/pypi/nose/
.. _twill: http://pypi.python.org/pypi/twill/

Installation
============

To install:

    python setup.py install

Or via easy_install_:

    easy_install tddspry

Also you can retrieve fresh version of tddspry from GitHub_:

    git clone git://github.com/playpauseandstop/tddspry.git

.. _easy_install: http://pypi.python.org/pypi/setuptools/
.. _GitHub: http://github.com/

Usage
=====

We create **tddspry** to easying testing Django projects and applications.
Okay, let's see, to test login and logout pages in your Django project, you
need only::

    from tddspry.django import HttpTestCase
    from tddspry.django.helpers import create_user

    from django.conf import settings


    class TestLoginPage(HttpTestCase):

        def test_login(self):
            user = create_user('username', 'password')
            self.login('username', 'password')
            self.url(settings.LOGIN_REDIRECT_URL)

        def test_logout(self):
            user = create_user('username', 'password')
            self.login('username', 'password')
            self.logout()
            self.url('/')

That's all ;) But really for ``test_login``,

* First, ``HttpTestCase`` creates test ``sqlite3`` database in memory and
  starts Django WSGI-server.

* Then, we creates test user by ``create_user`` helper.

* Next, twill browser goes to your ``'auth_login'`` page and checks that
  response code is 200.

* Next, twill browser fill out login form with ``username`` and ``password``
  values and submits it. Also here twill browser again checks that response
  code is 200.

* And finally, we check that current url after success login is our
  ``LOGIN_REDIRECT_URL`` that set in projects settings.

And for ``test_logout`` we repeate these steps and adding logging out from
current Django session and simple check that after logout we go to index page.

Easy? No? Okay, `create new issue`_ on GitHub and say how exactly create easy
tests for Django applications :)

**ps.** More examples how-to usage **tddspry** exist in tests for
``testproject`` project in `tddspry repository`_.

.. _`create new issue`: http://github.com/playpauseandstop/tddspry/issues
.. _`tddspry repository`: http://github.com/playpauseandstop/tddspry
