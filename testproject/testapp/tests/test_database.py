import os

from tddspry.django import DatabaseTestCase

from django.conf import settings
from django.contrib.auth.models import User

from testproject.testapp.models import UserProfile


TEST_BIO = u'Something text'
TEST_NEW_BIO = u'Another something text'


class TestModelsCustomDatabase(DatabaseTestCase):

    database_name = os.path.join(settings.DIRNAME, 'test.db')

    def setup(self):
        super(TestModelsCustomDatabase, self).setup()
        self.user = User.objects.create_user(username='username',
                                             password='password',
                                             email='email@domain.com')

    def test_create(self):
        profile = self.check_create(UserProfile,
                                    user=self.user,
                                    bio=TEST_BIO)

        self.assert_equal(profile.bio, TEST_BIO)

    def test_delete(self):
        profile = self.check_create(UserProfile,
                                    user=self.user)
        self.check_delete(profile)

    def test_unicode(self):
        profile = self.check_create(UserProfile,
                                    user=self.user)
        self.assert_equal(profile.__unicode__(),
                          u'Profile for "%s" user' % self.user.username)

    def test_update(self):
        profile = self.check_create(UserProfile,
                                    user=self.user)
        profile = self.check_update(profile, bio=TEST_BIO)
        self.check_update(profile, bio=TEST_NEW_BIO)


class TestModelsCustomDatabaseWithFlush(DatabaseTestCase):

    database_name = os.path.join(settings.DIRNAME, 'test.db')
    database_flush = True

    def setup(self):
        super(TestModelsCustomDatabaseWithFlush, self).setup()

        try:
            self.user = User.objects.get(username='username')
        except User.DoesNotExist:
            self.user = User.objects.create_user(username='username',
                                                 password='password',
                                                 email='email@domain.com')

        print UserProfile.objects.all()

    def test_create(self):
        profile = self.check_create(UserProfile,
                                    user=self.user,
                                    bio=TEST_BIO)

        self.assert_equal(profile.bio, TEST_BIO)

    def test_delete(self):
        profile = self.check_create(UserProfile,
                                    user=self.user)
        self.check_delete(profile)

    def test_unicode(self):
        profile = self.check_create(UserProfile,
                                    user=self.user)
        self.assert_equal(profile.__unicode__(),
                          u'Profile for "%s" user' % self.user.username)

    def test_update(self):
        profile = self.check_create(UserProfile,
                                    user=self.user)
        profile = self.check_update(profile, bio=TEST_BIO)
        self.check_update(profile, bio=TEST_NEW_BIO)


class TestModelsCustomDatabaseWithoutFlush(DatabaseTestCase):

    database_name = os.path.join(settings.DIRNAME, 'test.db')
    database_flush = False

    def setup(self):
        super(TestModelsCustomDatabaseWithoutFlush, self).setup()

        try:
            self.user = User.objects.create_user(username='username',
                                                 password='password',
                                                 email='email@domain.com')
        except:
            self.user = User.objects.get(username='username')

        try:
            profile = UserProfile.objects.get(user=self.user)
        except UserProfile.DoesNotExist:
            pass
        else:
            profile.delete()

    def test_create(self):
        profile = self.check_create(UserProfile,
                                    user=self.user,
                                    bio=TEST_BIO)

        self.assert_equal(profile.bio, TEST_BIO)

    def test_delete(self):
        profile = self.check_create(UserProfile,
                                    user=self.user)
        self.check_delete(profile)

    def test_unicode(self):
        profile = self.check_create(UserProfile,
                                    user=self.user)
        self.assert_equal(profile.__unicode__(),
                          u'Profile for "%s" user' % self.user.username)

    def test_update(self):
        profile = self.check_create(UserProfile,
                                    user=self.user)
        profile = self.check_update(profile, bio=TEST_BIO)
        self.check_update(profile, bio=TEST_NEW_BIO)


class TestModelsMemoryDatabase(DatabaseTestCase):

    def setup(self):
        super(TestModelsMemoryDatabase, self).setup()
        self.user = User.objects.create_user(username='username',
                                             password='password',
                                             email='email@domain.com')

    def test_create(self):
        profile = self.check_create(UserProfile,
                                    user=self.user,
                                    bio=TEST_BIO)

        self.assert_equal(profile.bio, TEST_BIO)

    def test_delete(self):
        profile = self.check_create(UserProfile,
                                    user=self.user)
        self.check_delete(profile)

    def test_unicode(self):
        profile = self.check_create(UserProfile,
                                    user=self.user)
        self.assert_equal(profile.__unicode__(),
                          u'Profile for "%s" user' % self.user.username)

    def test_update(self):
        profile = self.check_create(UserProfile,
                                    user=self.user)
        profile = self.check_update(profile, bio=TEST_BIO)
        self.check_update(profile, bio=TEST_NEW_BIO)


class TestModelsOriginalDatabase(DatabaseTestCase):

    database_name = ':original:'

    def setup(self):
        super(TestModelsOriginalDatabase, self).setup()

        try:
            self.user = User.objects.create_user(username='username',
                                                 password='password',
                                                 email='email@domain.com')
        except:
            self.user = User.objects.get(username='username')

        try:
            profile = UserProfile.objects.get(user=self.user)
        except UserProfile.DoesNotExist:
            pass
        else:
            profile.delete()

    def test_create(self):
        profile = self.check_create(UserProfile,
                                    user=self.user,
                                    bio=TEST_BIO)

        self.assert_equal(profile.bio, TEST_BIO)

    def test_delete(self):
        profile = self.check_create(UserProfile,
                                    user=self.user)
        self.check_delete(profile)

    def test_unicode(self):
        profile = self.check_create(UserProfile,
                                    user=self.user)
        self.assert_equal(profile.__unicode__(),
                          u'Profile for "%s" user' % self.user.username)

    def test_update(self):
        profile = self.check_create(UserProfile,
                                    user=self.user)
        profile = self.check_update(profile, bio=TEST_BIO)
        self.check_update(profile, bio=TEST_NEW_BIO)
