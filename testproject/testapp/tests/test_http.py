import os
import re
import shutil

from tddspry.django import TestCase
from tddspry.django.decorators import show_on_error
from tddspry.django.helpers import PASSWORD, USERNAME

from django.conf import settings
from django.contrib.auth.models import User

from twill.errors import TwillAssertionError

from testproject.testapp.models import UserProfile


TEST_BIO = 'Something text %d'


@show_on_error
def dummy_error(obj):
    obj.go('/does_not_exist/')
    obj.code(200)


class TestHttp(TestCase):

    def test_build_url(self):
        user = self.helper('create_user')

        self.assert_equal(self.build_url('index'), '/')
        self.assert_equal(self.build_url('user', args=[user.username]),
                          '/user/' + user.username + '/')
        self.assert_equal(self.build_url('user',
                                         kwargs={'username': user.username}),
                          '/user/' + user.username + '/')

    def test_client(self):
        # ``GET`` request
        client = self.client

        response = client.get('/')
        self.assert_equal(response.status_code, 200)

        # ``POST`` request
        client = self.client

        post = {
            'hidden_field_1': 'Value',
            'hidden_field_2': 'Value',
            'some_field_1': 'Value,'
        }
        response = client.post('/edit_hidden_fields/', post)
        self.assert_equal(response.status_code, 200)

    def test_edit_hidden_fields(self):
        self.enable_edit_hidden_fields()

        self.go200('/edit_hidden_fields/')

        self.formvalue(1, 'hidden_field_1', 'Value')
        self.formvalue(1, 'hidden_field_2', 'Value')
        self.formvalue(1, 'some_field_1', 'Value')

        self.submit200(url='/edit_hidden_fields/')

        self.find("hidden_field_1: 'Value'")
        self.find("hidden_field_2: 'Value'")
        self.find("some_field_1: 'Value'")

        self.disable_edit_hidden_fields()

        self.go200('/edit_hidden_fields/')

        self.formvalue(1, 'hidden_field_1', 'Value')
        self.formvalue(1, 'hidden_field_2', 'Value')
        self.formvalue(1, 'some_field_1', 'Value')

        self.submit200(url='/edit_hidden_fields/')

        self.find("hidden_field_1: ''")
        self.notfind("hidden_field_1: 'Value'")
        self.find("hidden_field_2: ''")
        self.notfind("hidden_field_2: 'Value'")
        self.find("some_field_1: 'Value'")

    def test_index(self):
        self.go200('/')
        self.url('/')

        self.find('Index')
        self.find('c++ is good, but python - better ;)', flat=True)

        try:
            self.notfind('c++ is good, but python - better ;)')
        except re.error:
            pass

        try:
            self.notfind('c++ is good, but python - better ;)', flat=True)
        except TwillAssertionError:
            pass

    def test_login(self):
        self.go200('/profile/')
        self.url('/login/')

        user = self.helper('create_user')
        self.login(USERNAME, PASSWORD)

        self.go200('/profile/')
        self.find(user.username)
        self.find(user.email)

    def test_login_to_admin_staff(self):
        staff = self.helper('create_staff')
        self.login_to_admin(USERNAME, PASSWORD)

    def test_login_to_admin_superuser(self):
        superuser = self.helper('create_superuser')
        self.login_to_admin(USERNAME, PASSWORD)

        self.go200('/admin/testapp/userprofile/')
        self.find('Testapp')
        self.find('User profiles')
        self.find('Add user profile')

    @TestCase.raises(TwillAssertionError)
    def test_login_to_admin_regular_user(self):
        user = self.helper('create_user')
        self.login_to_admin(USERNAME, PASSWORD)

    def test_logout(self):
        user = self.helper('create_user')
        self.login(USERNAME, PASSWORD)

        self.go200('/profile/')
        self.find(user.username)
        self.find(user.email)

        self.logout()

        self.go200('/profile/')
        self.url('/login/')

    def test_pages(self):
        profiles, users = [], []

        for i in xrange(10):
            user = User.objects.create_user(username='username%d' % i,
                                            password='password%d' % i,
                                            email='email%d@domain.com' % i)
            profile = UserProfile.objects.create(user=user,
                                                 bio=TEST_BIO % i)

            users.append(user)
            profiles.append(profile)

        self.go200('/users/')

        for i, user in enumerate(users):
            profile = profiles[i]
            self.find(user.username)
            self.find(profile.get_absolute_url())

        for i, user in enumerate(users):
            profile = profiles[i]
            self.go(profile.get_absolute_url())
            self.find('Username: %s' % user.username)
            self.find('Email: %s' % user.email)
            self.find('Bio: %s' % profile.bio)

    def test_redirect(self):
        self.disable_redirect()
        self.go200('/redirect/')
        self.url('/redirect/')

        self.enable_redirect()
        self.go200('/redirect/')
        self.url('/')

    def test_reversed_urls(self):
        self.go200('index')
        self.find('Index')

        user = self.helper('create_user')
        profile = self.helper('create_profile', user, UserProfile)

        self.go200('user', args=[user.username])
        self.find(user.username)
        self.find(user.email)

        self.go200('user', kwargs={'username': user.username})
        self.find(user.username)
        self.find(user.email)

    def test_show_on_error_save_output(self):
        old_dirname = os.environ.get('TWILL_ERROR_DIR', None)

        dirname = os.path.dirname(os.tempnam())
        os.environ['TWILL_ERROR_DIR'] = dirname

        try:
            dummy_error(self)
        except TwillAssertionError:
            pass

        contents = os.listdir(dirname)
        found = False
        filename = '%s.%s-' % (self.__module__, 'dummy_error')

        if old_dirname is not None:
            os.environ['TWILL_ERROR_DIR'] = dirname

        for name in contents:
            if name.startswith(filename):
                os.unlink(os.path.join(dirname, name))
                found = True

        assert found, \
               'Cannot found file started with %r in %r dir.\nDir ' \
               'contents:\n%s' % (filename, dirname, contents)

    def test_static(self):
        self.go(settings.MEDIA_URL)
        self.code(404)

        self.go(settings.MEDIA_URL + 'does_not_exist.exe')
        self.code(404)

        self.go(settings.MEDIA_URL + 'css/screen.css')
        self.code(200)
