import re

from django.core import mail
from django.contrib.auth.models import User

from tddspry.django.helpers import EMAIL, PASSWORD, USERNAME


__all__ = ('registration', )


def activate(obj, word='activate', url='registration_activate'):
    """
    For registered user get activation code from mailbox.
    """
    obj.assert_equal(len(mail.outbox), 1)

    body = mail.outbox[0].body
    match = re.search('.*%s/(.*)' % word, body)

    assert match, \
          'Failed to find proper activation link in the mail: %s' % body

    code = match.groups()[0]
    obj.go200(url, args=[code[:-1]])


def registration(obj, username=None, email=None, password=None,
                 verbosity=False,
                 registration_url='registration_register',
                 registration_formid=1,
                 registration_tos=False,
                 activate_word='activate',
                 activation_url='registration_activate',
                 login_url=None,
                 login_formid=1):
    """
    Register new user, activate it and login. Registers new user, activates it
    and tries to log in. Helper covers all registration process provided by
    `django-registration`_.

    .. _`django-registration`: http://code.google.com/p/django-registration/

    """
    # Go to registration page
    obj.go200(registration_url)
    obj.find('<input id="id_username" type="text" class="required" ' \
             'name="username"')

    submit(obj, username, email, password, registration_formid,
           registration_tos)

    if verbosity:
        obj.show()

    # Get created user
    user = User.objects.get(username=USERNAME)

    # Created user should not be active
    obj.assert_false(user.is_active,
                     'User is already activated and should not.')

    activate(obj, activate_word, activation_url)

    if verbosity:
        obj.show()

    # Test user exists and is_active
    user = User.objects.get(username=USERNAME)
    obj.assert_true(user.is_active, 'User is not activated yet.')

    # Test login
    obj.login(USERNAME, PASSWORD, login_url, login_formid)


def submit(obj, username=None, email=None, password=None, formid=None,
           tos=False):
    """
    Submit form for register new user. Note - if you have captcha
    in the form, you need to mock it.
    """
    formid = formid or 1

    obj.formvalue(formid, 'username', username or USERNAME)
    obj.formvalue(formid, 'email', email or EMAIL)
    obj.formvalue(formid, 'password1', password or PASSWORD)
    obj.formvalue(formid, 'password2', password or PASSWORD)

    if tos:
        obj.formvalue(formid, 'tos', 'on')

    obj.submit200()
