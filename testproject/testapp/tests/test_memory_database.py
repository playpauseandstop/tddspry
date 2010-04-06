from tddspry.django import DatabaseTestCase

from django.contrib.auth.models import Group, User
from django.contrib.flatpages.models import FlatPage

from testproject.testapp.models import UserProfile


TEST_ADDRESS = '221B Baker Street'
TEST_BIO = 'Test bio'
TEST_CITIES = ('London', 'Edinburg', 'Cardiff', 'Belfast', 'Dublin')
TEST_CITY = TEST_CITIES[0]


class TestMemoryDatabase(DatabaseTestCase):

    def setup(self):
        super(TestMemoryDatabase, self).setup()
        self.user = self.helper('create_user')

    def test_create(self):
        self.assert_create(UserProfile, user=self.user)

    def test_create_manager(self):
        profile = self.assert_create(UserProfile, user=self.user)
        self.assert_create(profile.contacts, city=TEST_CITY)

    def test_delete(self):
        profile = self.assert_create(UserProfile, user=self.user)
        self.assert_delete(profile)

    def test_delete_manager(self):
        profile = self.assert_create(UserProfile, user=self.user)

        for city in TEST_CITIES:
            self.assert_create(profile.contacts, city=city)

        self.assert_count(profile.contacts, len(TEST_CITIES))
        self.assert_delete(profile.contacts)
        self.assert_count(profile.contacts, 0)

    def test_delete_model(self):
        self.assert_create(UserProfile, user=self.user)
        self.assert_delete(UserProfile)
        self.assert_count(UserProfile, 0)

    def test_read(self):
        self.assert_create(UserProfile, user=self.user)
        self.assert_read(UserProfile, user=self.user)

    def test_read_manager(self):
        profile = self.assert_create(UserProfile, user=self.user)

        for city in TEST_CITIES:
            self.assert_create(profile.contacts, city=city)
            self.assert_read(profile.contacts, city=city)

    def test_update(self):
        profile = self.assert_create(UserProfile, user=self.user)
        self.assert_update(profile, bio=TEST_BIO)

    def test_update_manager(self):
        profile = self.assert_create(UserProfile, user=self.user)

        for city in TEST_CITIES:
            self.assert_create(profile.contacts, city=city)

        self.assert_update(profile.contacts, address=TEST_ADDRESS)
        queryset = self.assert_read(profile.contacts, address=TEST_ADDRESS)
        self.assert_count(queryset, len(TEST_CITIES))

    def test_update_model(self):
        self.assert_create(UserProfile, user=self.user)
        self.assert_update(UserProfile, bio=TEST_BIO)
        self.assert_read(UserProfile, bio=TEST_BIO)

    def test_unicode(self):
        profile = self.assert_create(UserProfile, user=self.user)
        self.assert_unicode(profile,
                            u'Profile for "%s" user' % self.user.username)


class TestMemoryDatabaseWithFlush(TestMemoryDatabase):

    database_flush = True


class TestMemoryDatabaseWithoutFlush(TestMemoryDatabase):

    database_flush = False


class TestMemoryDatabaseWithFixtures(DatabaseTestCase):

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


class TestMemoryDatabaseWithoutFixtures(DatabaseTestCase):

    def test_data(self):
        self.assert_count(User, 0)
        self.assert_count(UserProfile, 0)
        self.assert_count(Group, 0)
        self.assert_count(FlatPage, 0)
