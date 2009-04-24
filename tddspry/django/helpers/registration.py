import re

from django.core import mail
from django.contrib.auth.models import User

from tddspry.django.helpers import EMAIL, PASSWORD, USERNAME


__all__ = ('registration', )


def activate(cls, word='activate', url='registration_activate'):
    """
    For registered user get activation code from mailbox.
    """
    cls.assert_equal(len(mail.outbox), 1)

    body = mail.outbox[0].body
    match = re.search('.*%s/(.*)' % word, body)

    assert match, \
          'Failed to find proper activation link in the mail: %s' % body

    code = match.groups()[0]
    cls.go200(url, args=[code[:-1]])


def registration(cls, username=None, email=None, password=None,
                 verbosity=False,
                 registration_url='registration_register',
                 registration_formid=1,
                 registration_tos=False,
                 activate_word='activate',
                 activation_url='registration_activate',
                 login_url='auth_login',
                 login_formid=1):
    """
    Register new user, activate it and login.
    """
    # Go to registration page
    cls.go200(registration_url)
    cls.find('<input id="id_username" type="text" class="required" ' \
             'name="username"')

    submit(cls, username, email, password, registration_formid,
           registration_tos)

    if verbosity:
        cls.show()

    # Get created user
    user = User.objects.get(username=USERNAME)

    # Created user should not be active
    cls.assert_false(user.is_active,
                     'User is already activated and should not.')

    activate(cls, activate_word, activation_url)

    if verbosity:
        cls.show()

    # Test user exists and is_active
    user = User.objects.get(username=USERNAME)
    cls.assert_true(user.is_active, 'User is not activated yet.')

    # Test login
    cls.login(USERNAME, PASSWORD, login_url, login_formid)


def submit(cls, username=None, email=None, password=None, formid=None,
           tos=False):
    """
    Submit form for register new user. Note - if you have captcha
    in the form, you need to mock it.
    """
    formid = formid or 1

    cls.formvalue(formid, 'username', username or USERNAME)
    cls.formvalue(formid, 'email', email or EMAIL)
    cls.formvalue(formid, 'password1', password or PASSWORD)
    cls.formvalue(formid, 'password2', password or PASSWORD)

    if tos:
        cls.formvalue(formid, 'tos', 'on')

    cls.submit200()
