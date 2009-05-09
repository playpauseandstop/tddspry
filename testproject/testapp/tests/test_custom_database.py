import os

from tddspry.django import DatabaseTestCase

from django.conf import settings
from django.contrib.auth.models import Group, User
from django.contrib.flatpages.models import FlatPage

from testproject.testapp.models import UserProfile


TEST_BIO = 'Test bio'
TEST_USERNAME = 'testusername'


class TestCustomDatabase(DatabaseTestCase):

    database_name = os.path.join(settings.DIRNAME, 'test.db')

    def setup(self):
        super(TestCustomDatabase, self).setup()
        self.user = self.helper('create_user')

    def test_create(self):
        self.assert_create(UserProfile, user=self.user)

    def test_delete(self):
        profile = self.assert_create(UserProfile, user=self.user)
        self.assert_delete(profile)

    def test_read(self):
        self.assert_create(UserProfile, user=self.user)
        self.assert_read(UserProfile, user=self.user)

    def test_update(self):
        profile = self.assert_create(UserProfile, user=self.user)
        self.assert_update(profile, bio=TEST_BIO)

    def test_unicode(self):
        profile = self.assert_create(UserProfile, user=self.user)
        self.assert_equal(unicode(profile),
                          u'Profile for "%s" user' % self.user.username)


class TestCustomDatabaseWithFlush(DatabaseTestCase):

    database_name = os.path.join(settings.DIRNAME, 'test.db')
    database_flush = True

    def setup(self):
        super(TestCustomDatabaseWithFlush, self).setup()
        self.user = self.helper('create_user')

    def test_create(self):
        self.assert_create(UserProfile, user=self.user)

    def test_delete(self):
        profile = self.assert_create(UserProfile, user=self.user)
        self.assert_delete(profile)

    def test_read(self):
        self.assert_create(UserProfile, user=self.user)
        self.assert_read(UserProfile, user=self.user)

    def test_update(self):
        profile = self.assert_create(UserProfile, user=self.user)
        self.assert_update(profile, bio=TEST_BIO)

    def test_unicode(self):
        profile = self.assert_create(UserProfile, user=self.user)
        self.assert_equal(unicode(profile),
                          u'Profile for "%s" user' % self.user.username)


class TestCustomDatabaseWithoutFlush(DatabaseTestCase):

    database_name = os.path.join(settings.DIRNAME, 'test.db')
    database_flush = False

    def test_create(self):
        user = self.helper('create_user', username=TEST_USERNAME)
        self.assert_create(UserProfile, user=user)

    def test_delete(self):
        profile = self.assert_read(UserProfile, user__username=TEST_USERNAME)
        self.assert_delete(profile)

    def test_read(self):
        user = self.assert_read(User, username=TEST_USERNAME)
        self.assert_create(UserProfile, user=user)
        self.assert_read(UserProfile, user=user)

    def test_update(self):
        profile = self.assert_read(UserProfile, user__username=TEST_USERNAME)
        self.assert_update(profile, bio=TEST_BIO)

    def test_unicode(self):
        profile = self.assert_read(UserProfile, user__username=TEST_USERNAME)
        self.assert_equal(unicode(profile),
                          u'Profile for "%s" user' % TEST_USERNAME)


class TestCustomDatabaseWithFixtures(DatabaseTestCase):

    database_name = os.path.join(settings.DIRNAME, 'test.db')
    fixtures = ['users.json', 'userprofiles.json', 'groups.json',
                'flatpages.json']

    def test_data(self):
        # Users loaded from ``testapp/fixtures/users.json``
        self.assert_count(User, 10)

        # UserProfiles loaded from ``testapp/fixtures/userprofiles.json``
        self.assert_count(UserProfile, 10)

        # Groups loaded from ``fixtures/groups.json``
        self.assert_count(Group, 3)

        # FlatPages loaded from ``fixtures/flatpages.json``
        self.assert_count(FlatPage, 3)


class TestCustomDatabaseWithoutFixtures(DatabaseTestCase):

    database_name = os.path.join(settings.DIRNAME, 'test.db')

    def test_data(self):
        self.assert_count(User, 0)
        self.assert_count(UserProfile, 0)
        self.assert_count(Group, 0)
        self.assert_count(FlatPage, 0)
