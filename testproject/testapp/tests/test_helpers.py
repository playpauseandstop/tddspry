from tddspry.django import TestCase

from django.contrib.auth.models import User, check_password

from testproject.testapp.models import UserProfile


TEST_BIO = u'Some bio text'


class TestBaseHelpers(TestCase):

    def test_create_profile(self):
        old_counter = UserProfile.objects.count()

        user = self.helper('create_user')
        profile = self.helper('create_profile',
                              user, UserProfile, bio=TEST_BIO)

        new_counter = UserProfile.objects.count()
        self.assert_equal(new_counter - 1, old_counter)

        self.assert_equal(profile.user, user)
        self.assert_equal(profile.bio, TEST_BIO)

    def test_create_staff(self):
        old_counter = User.objects.count()
        user = self.helper('create_staff')

        new_counter = User.objects.count()
        self.assert_equal(new_counter - 1, old_counter)

        self.assert_true(user.is_staff)

    def test_create_superuser(self):
        old_counter = User.objects.count()
        user = self.helper('create_superuser')

        new_counter = User.objects.count()
        self.assert_equal(new_counter - 1, old_counter)

        self.assert_true(user.is_staff)
        self.assert_true(user.is_superuser)

    def test_create_user(self):
        old_counter = User.objects.count()
        user = self.helper('create_user')

        new_counter = User.objects.count()
        self.assert_equal(new_counter - 1, old_counter)

        self.assert_equal(user.username, self.helpers.USERNAME)
        self.assert_true(check_password(self.helpers.PASSWORD, user.password))
        self.assert_equal(user.email, self.helpers.EMAIL)
        self.assert_true(user.is_active)
        self.assert_false(user.is_staff)
        self.assert_false(user.is_superuser)

    def test_create_user_raw(self):
        old_counter = User.objects.count()
        user = self.helper('create_user', raw=True)

        new_counter = User.objects.count()
        self.assert_equal(new_counter - 1, old_counter)

        self.assert_equal(user.username, self.helpers.USERNAME)
        self.assert_equal(user.password, self.helpers.PASSWORD)
        self.assert_equal(user.email, self.helpers.EMAIL)
        self.assert_true(user.is_active)
        self.assert_false(user.is_staff)
        self.assert_false(user.is_superuser)


class TestRegistrationHelpers(TestCase):

    def test_registration(self):
        self.helper('registration')
