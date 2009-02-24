=======
tddspry
=======

1. Introduction_
2. Requirements_
3. Installation_
4. `What's next?`_

Introduction
------------

**tddspry** is collection of utilities for testing Django applications with
nosetests_ library.

**NOTE: tddspry still in hardly development. Use tddspry with your own risk!**

.. _nosetests: http://code.google.com/p/python-nose/

Requirements
------------

- nose_ >= 0.10.3
- twill_ >= 0.9

.. _nose: http://pypi.python.org/pypi/nose/
.. _twill: http://pypi.python.org/pypi/twill/

Installation
------------

To install:

    python setup.py install

Or via easy_install_:

    easy_install tddspry

Also you can retrieve fresh version of tddspry from GitHub_:

    git clone git://github.com/playpauseandstop/tddspry.git

.. _easy_install: http://pypi.python.org/pypi/setuptools/
.. _GitHub: http://github.com/

What's next?
------------

We using **tddspry** to test Django projects and applications with nose and
twill libraries. Some samples are below.

Using tddspry to test Django with nosetests
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Sorry, no explanation yet, just code:

**test_simple.py**

::

    from nose.tools import assert_equal
    from tddspry.django.db_mock import DbMock

    from django.contrib.auth.models import User

    from project.accounts.models import UserProfile


    class TestAutoCreateProfile(DbMock):
        def test_auto_create_profile(self):
            old_counter = UserProfile.objects.count()

            user = User.objects.create_user(username='username',
                                            password='password',
                                            email='email@domain.com')

            new_counter = UserProfile.objects.count()

            assert_equal(new_counter - old_counter, 1)

            try:
                profile = UserProfile.objects.get(user=user)
            except UserProfile.DoesNotExists:
                assert False, 'Profile was not created for %r.' % user

Now execute this test, by::

    DJANGO_SETTINGS_MODULE=project.settings nosetests test_simple.py

Using tddspry to test Django with nosetests and twill
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Yeah, no explanation again :( But, there's code:

**test_login_logout.py**

::

    from tddspry.django.djangohelper import USERNAME, PASSWORD, create_user
    from tddspry.django.twill_mock import *

    from django.conf import settings
    from django.core.urlresolvers import reverse


    class TestLoginLogout(TwillMock):
        def setup(self):
            super(TestLoginLogout, self).setup()
            self.user = create_user(USERNAME, PASSWORD)

        def test_login(self):
            go(SITE + reverse('auth_login'))
            code(200)

            find('Username')
            find('Password')

            formvalue(1, 'id_username', USERNAME)
            formvalue(1, 'id_password', PASSWORD)
            submit()

            code(200)
            url(settings.LOGIN_REDIRECT_URL)

        def test_logout(self):
            go(SITE + reverse('auth_login'))
            code(200)

            formvalue(1, 'id_username', USERNAME)
            formvalue(1, 'id_password', PASSWORD)
            submit()

            go(SITE + reverse('auth_logout'))
            code(200)

Now execute this test, by::

    DJANGO_SETTINGS_MODULE=project.settings nosetests test_login_logout.py
