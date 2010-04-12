from random import choice

from tddspry.django import DatabaseTestCase, TestCase

from django.contrib.auth.models import Group, User
from django.contrib.flatpages.models import FlatPage

from testproject.testapp.models import UserProfile


TEST_ADDRESS = '221B Baker Street'
TEST_BIO = 'Test bio'
TEST_CITIES = ('London', 'Edinburg', 'Cardiff', 'Belfast', 'Dublin')
TEST_CITY = TEST_CITIES[0]


class TestDatabase(TestCase):

    def setup(self):
        self.user = self.helper('create_user')

    def test_create(self):
        self.assert_create(UserProfile, user=self.user)

    def test_create_manager(self):
        profile = self.assert_create(UserProfile, user=self.user)
        self.assert_create(profile.contacts, city=TEST_CITY)

    def test_delete(self):
        profile = self.assert_create(UserProfile, user=self.user)
        self.assert_delete(profile)

        profile = self.assert_create(UserProfile, user=self.user)

        for city in TEST_CITIES:
            self.assert_create(profile.contacts, city=city)

        contact = choice(self.assert_read(profile.contacts))
        self.assert_delete(contact)

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


class TestDatabaseCallCommand(TestCase):

    def test_call_command(self):
        self.call_command('loaddata', 'users.json', 'userprofiles.json',
                                      'groups.json', 'flatpages.json')

        # Users loaded from ``testapp/fixtures/users.json``
        self.assert_count(User, 10)

        # UserProfiles loaded from ``testapp/fixtures/userprofiles.json``
        self.assert_count(UserProfile, 10)

        # Groups loaded from ``fixtures/groups.json``
        self.assert_count(Group, 3)

        # FlatPages loaded from ``fixtures/flatpages.json``
        self.assert_count(FlatPage, 3)

        self.call_command('flush', interactive=False)

        self.assert_count(User, 0)
        self.assert_count(UserProfile, 0)
        self.assert_count(Group, 0)
        self.assert_count(FlatPage, 0)


class TestDatabaseDeprecated(DatabaseTestCase):

    def setup(self):
        super(TestDatabaseDeprecated, self).setup()

    def teardown(self):
        super(TestDatabaseDeprecated, self).teardown()

    def test_message(self):
        """
        Check that old styled setup and teardown methods loaded without
        errors.
        """
        self.message = {'big': 'badda boom'}

class TestDatabaseUnitTestStyleMethods(TestCase):

    def setUp(self):
        self.user = self.helper('create_user')

    def testCreate(self):
        self.assertCreate(UserProfile, user=self.user)

    def testCreateManager(self):
        profile = self.assertCreate(UserProfile, user=self.user)
        self.assertCreate(profile.contacts, city=TEST_CITY)

    def testDelete(self):
        profile = self.assertCreate(UserProfile, user=self.user)
        self.assertDelete(profile)

        profile = self.assertCreate(UserProfile, user=self.user)

        for city in TEST_CITIES:
            self.assertCreate(profile.contacts, city=city)

        contact = choice(self.assertRead(profile.contacts))
        self.assertDelete(contact)

    def testDeleteManager(self):
        profile = self.assertCreate(UserProfile, user=self.user)

        for city in TEST_CITIES:
            self.assertCreate(profile.contacts, city=city)

        self.assertCount(profile.contacts, len(TEST_CITIES))
        self.assertDelete(profile.contacts)
        self.assertCount(profile.contacts, 0)

    def testDeleteModel(self):
        self.assertCreate(UserProfile, user=self.user)
        self.assertDelete(UserProfile)
        self.assertCount(UserProfile, 0)

    def testRead(self):
        self.assertCreate(UserProfile, user=self.user)
        self.assertRead(UserProfile, user=self.user)

    def testReadManager(self):
        profile = self.assertCreate(UserProfile, user=self.user)

        for city in TEST_CITIES:
            self.assertCreate(profile.contacts, city=city)
            self.assertRead(profile.contacts, city=city)

    def testUpdate(self):
        profile = self.assertCreate(UserProfile, user=self.user)
        self.assertUpdate(profile, bio=TEST_BIO)

    def testUpdateManager(self):
        profile = self.assertCreate(UserProfile, user=self.user)

        for city in TEST_CITIES:
            self.assertCreate(profile.contacts, city=city)

        self.assertUpdate(profile.contacts, address=TEST_ADDRESS)
        queryset = self.assertRead(profile.contacts, address=TEST_ADDRESS)
        self.assertCount(queryset, len(TEST_CITIES))

    def testUpdateModel(self):
        self.assertCreate(UserProfile, user=self.user)
        self.assertUpdate(UserProfile, bio=TEST_BIO)
        self.assertRead(UserProfile, bio=TEST_BIO)

    def testUnicode(self):
        profile = self.assertCreate(UserProfile, user=self.user)
        self.assertUnicode(profile,
                           u'Profile for "%s" user' % self.user.username)


class TestDatabaseWithFixtures(TestCase):

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


class TestDatabaseWithoutFixtures(TestCase):

    def test_data(self):
        self.assert_count(User, 0)
        self.assert_count(UserProfile, 0)
        self.assert_count(Group, 0)
        self.assert_count(FlatPage, 0)
