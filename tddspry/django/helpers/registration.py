# -*- coding: utf-8 -*-
"""
@version: 1.0
@copyright: 2007-2008 KDS Software Group http://www.kds.com.ua/
@license: TBD
@status: beta
@summary: Basic django operations.
"""
from django.core.urlresolvers import reverse
from django.contrib.auth.models import User
from django.conf import settings
from django.core import mail
from django.test import utils

from twill.commands import *
from twill import add_wsgi_intercept
from twill.errors import TwillAssertionError
from twill.extensions.check_links import check_links

from db_mock import *
from twill_mock import *

import re

USERNAME = 'test_user'
PASSWORD = 'test_password'
EMAIL = 'test.user@test.com'


def create_user(username=None, password=None, email=None, active=True,
                staff=False, superuser=False, raw=False):
    """
    @summary: Create Django (django.contrib.auth.models.User) user with
    given names or with default if absent.
    """
    method = raw and 'create' or 'create_user'
    user = getattr(User.objects, method)(username=username or USERNAME,
                                         password=password or PASSWORD,
                                         email=email or EMAIL)

    if not active:
        user.is_active = False

    if staff:
        user.is_staff = True
    else:
        user.is_staff = False

    if superuser:
        user.is_superuser = True
    else:
        user.is_superuser = False

    user.save()
    return user

def create_staff(username=None, password=None, email=None):
    """
    @summary: Create Django (django.contrib.auth.models.User) user with
    staff rights.
    """
    return create_user(username, password, email, staff=True)

def create_superuser(username=None, password=None, email=None):
    """
    @summary: Create Django (django.contrib.auth.models.User) user with
    superuser and staff rights.
    """
    return create_user(username, password, email, staff=True, superuser=True)

def create_profile(user, profile_klass, **kwargs):
    """
    @summary: Create profile for given user
    @param profile_klass: Class of user profile
    @param kwargs: all params needed to be sent to profile __init__
    """
    profile = profile_klass(**kwargs)
    profile.user = user
    profile.save()

    return profile

def load_fixtures(path_to_fixture):
    """
    @summary: Load fixture from given path
    """
    from os import path
    call_command('loaddata', path_to_fixture, verbosity=True)


#========================
# TWILL HELPERS
#========================
@show_on_error
def goto200(url, check=False):
    """
    @summary: Simple twill script: go to url, code(200) check_links()
    """
    go(url)
    code(200)
    if check:
        check_links()

@show_on_error
def code200(check=False):
    """
    @summary: Simple twill script: code(200) check_links()
    """
    code(200)
    if check:
        check_links()

@show_on_error
def login_to_admin(username, password):
    """
    @summary: Login to standart Django admin
    @param username: Username
    @param password: Password
    """
    goto200(SITE+"/admin/")
    formvalue(1, 'id_username',  username)
    formvalue(1, 'id_password', password)
    submit()
    code200()

@show_on_error
def login(username, password, login_reverse_url='login', formid=1):
    """
    @summary: Login to standart Django admin
    @param username: Username
    @param password: Password
    """
    goto200(SITE+reverse(login_reverse_url))
    formvalue(formid, 'id_username',  username)
    formvalue(formid, 'id_password', password)
    submit()
    code200()

@show_on_error
def goto_signin_url(reverse_url='registration_register'):
    """
    @summary: Go to registration url. If you use django-registration, you,
    probably, not have to pass reverse_url to this function
    """
    goto200(SITE+reverse(reverse_url))

@show_on_error
def submit_registration_form(username=USERNAME, email=EMAIL, password=PASSWORD,
                             formid=1, tos=False):
    """
    @summary: Submit form for register new user. Note - if you have captcha
    in the form, you have to mock it.
    """
    formvalue(formid, 'username', username)
    formvalue(formid, 'email', email)
    formvalue(formid, 'password1', password)
    formvalue(formid, 'password2', password)
    if tos:
        formvalue(formid, 'tos', 'on')
    submit()
    code200()

@show_on_error
def activate(activate_word='activate', reverse_url='registration_activate'):
    """
    @summary: For registered user get activation code from mailbox.
    """
    assert len(mail.outbox) == 1, '%s\n, %s' % (mail.outbox, show())
    body = mail.outbox[0].body
    match = re.search('.*%s/(.*)' % activate_word, body)
    assert match, 'Failed to find proper activation link in the mail: %s' % body
    activation_code = match.groups()[0]
    goto200(SITE+reverse(reverse_url, args=[activation_code[:-1],]))

@show_on_error
def register(username=USERNAME, email=EMAIL, password=PASSWORD,
             verbosity=False, formsignin_id=1, formtos=False,
             activate_word='activate',
             reverse_sigin_url='registration_register',
             reverse_activate_url='registration_activate',
             login_reverse_url='auth_login',
             formlogin_id=1, tos=False):
    """
    @summary: Register new user and login
    @param username: username
    @param email: email
    @param password: password
    @param verbosity: should registration info be shown in output
    @param formsignin_id: id of the registration form
    @param formtos: should be tos field be pushed to registration form
    @param activate_word: activation url part
    @param reverse_sigin_url: reverse word for signin url
    @param reverse_activate_url: reverse word for activate url
    @param formlogin_id:  id of login form
    """

    goto_signin_url(reverse_sigin_url)
    find('<input id="id_username" type="text" class="required" name="username')
    submit_registration_form(username, email, password, formsignin_id, tos)
    if verbosity:
        show()

    #Get created user
    user = User.objects.get(username=USERNAME)

    #Created user should not be active
    assert not user.is_active, 'User is already activated and should not.'

    activate()

    # Test user exists and is_active
    user = User.objects.get(username=USERNAME)
    assert user.is_active, 'User is not activated yet.'

    # Test login
    login(USERNAME, PASSWORD, login_reverse_url, formlogin_id)


