"""
``DatabaseTestCase`` and ``HttpTestCase`` can call additional helpers by
``helper(name, *args, **kwargs)`` method. Now ``tddspry.django.helpers``
provides:

.. autofunction :: create_profile
.. autofunction :: create_staff
.. autofunction :: create_superuser
.. autofunction :: create_user
.. autofunction :: registration

Usage
-----

For create new non-active user in test case use next snippet::

    from tddspry.django import DatabaseTestCase


    class TestNonActiveUser(DatabaseTestCase):

        def test_active(self):
            user = self.helper('create_user', active=False)
            self.assert_false(user.is_active)

Also you can to access any additional helper function or var directly by
``helpers`` attribute. For example, to access default values for ``username``,
``password`` and ``email`` user fields use next snippet::

    from tddspry.django import DatabaseTestCase


    class TestHelpersVars(DatabaseTestCase):

        def test_default_values(self):
            user = self.helper('create_user', raw=True)
            self.assert_equal(user.username, self.helpers.USERNAME)
            self.assert_equal(user.password, self.helpers.PASSWORD)
            self.assert_equal(user.email, self.helpers.EMAIL)

**Note:** You don't need to send ``obj`` argument to additional helper via
``helper`` method. But if you want to call additional helper directly you must
send ``DatabaseTestCase`` or ``HttpTestCase`` object as first argument.

"""

from tddspry.django.helpers.auth import *
from tddspry.django.helpers.registration import *
