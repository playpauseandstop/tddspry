from tddspry.django import DatabaseTestCase
from tddspry.django.helpers import *

from django.contrib.auth.models import User, check_password

from testproject.testapp.models import UserProfile


TEST_BIO = u'Some bio text'


class TestHelpers(DatabaseTestCase):

    def test_create_profile(self):
        old_counter = UserProfile.objects.count()

        user = create_user()
        profile = create_profile(user, UserProfile, bio=TEST_BIO)

        new_counter = UserProfile.objects.count()
        self.assert_equal(new_counter - 1, old_counter)

        self.assert_equal(profile.user, user)
        self.assert_equal(profile.bio, TEST_BIO)

    def test_create_staff(self):
        old_counter = User.objects.count()
        user = create_staff()

        new_counter = User.objects.count()
        self.assert_equal(new_counter - 1, old_counter)

        self.assert_true(user.is_staff)

    def test_create_superuser(self):
        old_counter = User.objects.count()
        user = create_superuser()

        new_counter = User.objects.count()
        self.assert_equal(new_counter - 1, old_counter)

        self.assert_true(user.is_staff)
        self.assert_true(user.is_superuser)

    def test_create_user(self):
        old_counter = User.objects.count()
        user = create_user()

        new_counter = User.objects.count()
        self.assert_equal(new_counter - 1, old_counter)

        self.assert_equal(user.username, USERNAME)
        self.assert_true(check_password(PASSWORD, user.password))
        self.assert_equal(user.email, EMAIL)
        self.assert_true(user.is_active)
        self.assert_false(user.is_staff)
        self.assert_false(user.is_superuser)

    def test_create_user_raw(self):
        old_counter = User.objects.count()
        user = create_user(raw=True)

        new_counter = User.objects.count()
        self.assert_equal(new_counter - 1, old_counter)

        self.assert_equal(user.username, USERNAME)
        self.assert_equal(user.password, PASSWORD)
        self.assert_equal(user.email, EMAIL)
        self.assert_true(user.is_active)
        self.assert_false(user.is_staff)
        self.assert_false(user.is_superuser)
