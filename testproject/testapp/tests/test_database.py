import os

from tddspry.django import DatabaseTestCase

from django.conf import settings
from django.contrib.auth.models import Group, User
from django.contrib.flatpages.models import FlatPage

from testproject.testapp.models import UserProfile


TEST_BIO = u'Something text'
TEST_NEW_BIO = u'Another something text'


class TestCustomDatabase(DatabaseTestCase):

    database_name = os.path.join(settings.DIRNAME, 'test.db')

    def setup(self):
        super(TestCustomDatabase, self).setup()
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


class TestCustomDatabaseWithFlush(DatabaseTestCase):

    database_name = os.path.join(settings.DIRNAME, 'test.db')
    database_flush = True

    def setup(self):
        super(TestCustomDatabaseWithFlush, self).setup()

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


class TestCustomDatabaseWithoutFlush(DatabaseTestCase):

    database_name = os.path.join(settings.DIRNAME, 'test.db')
    database_flush = False

    def setup(self):
        super(TestCustomDatabaseWithoutFlush, self).setup()

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


class TestDatabaseWithFixtures(DatabaseTestCase):

    fixtures = ['users.json', 'userprofiles.json', 'groups.json',
                'flatpages.json']

    def test_data(self):
        # Users loaded from ``testapp/fixtures/users.json``
        self.assert_equal(User.objects.count(), 10)

        # UserProfiles loaded from ``testapp/fixtures/userprofiles.json``
        self.assert_equal(UserProfile.objects.count(), 10)

        # Groups loaded from ``fixtures/groups.json``
        self.assert_equal(Group.objects.count(), 3)

        # FlatPages loaded from ``fixtures/flatpages.json``
        self.assert_equal(FlatPage.objects.count(), 3)


class TestDatabaseWithoutFixtures(DatabaseTestCase):

    def test_data(self):
        self.assert_equal(User.objects.count(), 0)
        self.assert_equal(UserProfile.objects.count(), 0)
        self.assert_equal(Group.objects.count(), 0)
        self.assert_equal(FlatPage.objects.count(), 0)


class TestMemoryDatabase(DatabaseTestCase):

    def setup(self):
        super(TestMemoryDatabase, self).setup()
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


class TestOriginalDatabase(DatabaseTestCase):

    database_name = ':original:'

    def setup(self):
        super(TestOriginalDatabase, self).setup()

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
