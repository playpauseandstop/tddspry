from random import choice

from tddspry.django import DatabaseTestCase, TestCase

from django.contrib.auth.models import Group, User
from django.contrib.flatpages.models import FlatPage
from django.db.models import Q

from testproject.testapp.models import Contact, UserProfile


TEST_ADDRESS = '221B Baker Street'
TEST_BIO = 'Test bio'
TEST_CITIES = ('London', 'Edinburg', 'Cardiff', 'Belfast', 'Dublin')
TEST_CITY = TEST_CITIES[0]


class TestDatabase(TestCase):

    def setup(self):
        self.user = self.helper('create_user')

    @TestCase.raises(AssertionError)
    def test_count_assertion(self):
        self.assert_count(UserProfile, 1)
        self.assert_count(UserProfile, (1, 2))
        self.assert_count(UserProfile, [1, 2])

    def test_count_model(self):
        self.assert_count(UserProfile, 0)
        self.assert_count(UserProfile, (0, 1))
        self.assert_count(UserProfile, [0, 1])

        profile = self.assert_create(UserProfile, user=self.user)

        self.assert_count(UserProfile, 1)
        self.assert_count(UserProfile, (0, 1))
        self.assert_count(UserProfile, [0, 1])

    def test_count_model_model(self):
        profile = self.assert_create(UserProfile, user=self.user)
        self.assert_count(UserProfile, User)

    def test_count_model_manager(self):
        profile = self.assert_create(UserProfile, user=self.user)

        for city in TEST_CITIES:
            self.assert_create(profile.contacts, city=city)

        self.assert_count(Contact, profile.contacts)

    def test_count_model_string(self):
        profile = self.assert_create(UserProfile, user=self.user)
        self.assert_count(UserProfile, 'auth.User')

    def test_count_manager(self):
        profile = self.assert_create(UserProfile, user=self.user)

        self.assert_count(profile.contacts, 0)
        self.assert_count(profile.contacts, (0, len(TEST_CITIES)))
        self.assert_count(profile.contacts, [0, len(TEST_CITIES)])

        for city in TEST_CITIES:
            self.assert_create(profile.contacts, city=city)

        self.assert_count(profile.contacts, len(TEST_CITIES))
        self.assert_count(profile.contacts, (0, len(TEST_CITIES)))
        self.assert_count(profile.contacts, [0, len(TEST_CITIES)])

    def test_count_manager_model(self):
        profile = self.assert_create(UserProfile, user=self.user)

        for city in TEST_CITIES:
            self.assert_create(profile.contacts, city=city)

        self.assert_count(profile.contacts, Contact)

    def test_count_manager_manager(self):
        profile = self.assert_create(UserProfile, user=self.user)
        self.assert_count(profile.contacts, self.user.groups)

    def test_count_manager_string(self):
        profile = self.assert_create(UserProfile, user=self.user)

        for city in TEST_CITIES:
            self.assert_create(profile.contacts, city=city)

        self.assert_count(profile.contacts, 'testapp.Contact')

    def test_count_string(self):
        self.assert_count('testapp.UserProfile', 0)
        self.assert_count('testapp.UserProfile', (0, 1))
        self.assert_count('testapp.UserProfile', [0, 1])

        profile = self.assert_create('testapp.UserProfile', user=self.user)

        self.assert_count('testapp.UserProfile', 1)
        self.assert_count('testapp.UserProfile', (0, 1))
        self.assert_count('testapp.UserProfile', [0, 1])

    def test_count_string_model(self):
        profile = self.assert_create('testapp.UserProfile', user=self.user)
        self.assert_count('testapp.UserProfile', User)

    def test_count_string_manager(self):
        profile = self.assert_create('testapp.UserProfile', user=self.user)

        for city in TEST_CITIES:
            self.assert_create(profile.contacts, city=city)

        self.assert_count('testapp.Contact', profile.contacts)

    def test_count_string_string(self):
        profile = self.assert_create('testapp.UserProfile', user=self.user)
        self.assert_count('testapp.UserProfile', 'auth.User')

    def test_create_model(self):
        self.assert_create(UserProfile, user=self.user)

    def test_create_manager(self):
        profile = self.assert_create(UserProfile, user=self.user)
        self.assert_create(profile.contacts, city=TEST_CITY)

    def test_create_string(self):
        self.assert_create('testapp.UserProfile', user=self.user)

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

    def test_delete_string(self):
        self.assert_create('testapp.UserProfile', user=self.user)
        self.assert_delete('testapp.UserProfile')
        self.assert_count('testapp.UserProfile', 0)

    @TestCase.raises(AssertionError)
    def test_not_count_assertion(self):
        self.assert_not_count(UserProfile, 0)
        self.assert_not_count(UserProfile, (0, 1))
        self.assert_not_count(UserProfile, [0, 1])

    def test_not_count_model(self):
        self.assert_not_count(UserProfile, 1)
        self.assert_not_count(UserProfile, (1, 2))
        self.assert_not_count(UserProfile, [1, 2])

    def test_not_count_model_model(self):
        self.assert_not_count(UserProfile, User)

    def test_not_count_model_manager(self):
        profile = self.assert_create(UserProfile, user=self.user)
        self.assert_not_count(UserProfile, profile.contacts)

    def test_not_count_model_string(self):
        self.assert_not_count(UserProfile, 'auth.User')

    def test_not_count_manager(self):
        profile = self.assert_create(UserProfile, user=self.user)
        self.assert_not_count(profile.contacts, 1)
        self.assert_not_count(profile.contacts, (1, 2))
        self.assert_not_count(profile.contacts, [1, 2])

    def test_not_count_manager_model(self):
        profile = self.assert_create(UserProfile, user=self.user)
        self.assert_not_count(profile.contacts, UserProfile)

    def test_not_count_manager_manager(self):
        profile = self.assert_create(UserProfile, user=self.user)

        for city in TEST_CITIES:
            self.assert_create(profile.contacts, city=city)

        self.assert_not_count(profile.contacts, self.user.groups)

    def test_not_count_manager_string(self):
        profile = self.assert_create(UserProfile, user=self.user)
        self.assert_not_count(profile.contacts, 'testapp.UserProfile')

    def test_not_count_string(self):
        self.assert_not_count('testapp.UserProfile', 1)
        self.assert_not_count('testapp.UserProfile', (1, 2))
        self.assert_not_count('testapp.UserProfile', [1, 2])

    def test_not_count_string_model(self):
        self.assert_not_count('testapp.UserProfile', User)

    def test_not_count_string_manager(self):
        profile = self.assert_create('testapp.UserProfile', user=self.user)

        for city in TEST_CITIES:
            self.assert_create(profile.contacts, city=city)

        self.assert_not_count('testapp.UserProfile', profile.contacts)

    def test_not_count_string_string(self):
        self.assert_not_count('testapp.UserProfile', 'auth.User')

    @TestCase.raises(AssertionError)
    def test_not_read_assertion(self):
        self.assert_create(UserProfile, user=self.user)
        self.assert_not_read(UserProfile, Q(user=self.user))
        self.assert_not_read(UserProfile, user=self.user)

    def test_not_read_model(self):
        self.assert_not_read(UserProfile, Q(user=self.user))
        self.assert_not_read(UserProfile, user=self.user)

    def test_not_read_manager(self):
        profile = self.assert_create(UserProfile, user=self.user)
        self.assert_not_read(profile.contacts, Q(city=TEST_CITY))
        self.assert_not_read(profile.contacts, city=TEST_CITY)

    def test_not_read_string(self):
        self.assert_not_read('testapp.UserProfile', Q(user=self.user))
        self.assert_not_read('testapp.UserProfile', user=self.user)

    def test_not_unicode(self):
        profile = self.assert_create(UserProfile, user=self.user)
        self.assert_not_unicode(profile,
                                u'Profile for "%s"' % self.user.username)

    @TestCase.raises(AssertionError)
    def test_not_unicode_assertion(self):
        profile = self.assert_create(UserProfile, user=self.user)
        self.assert_not_unicode(profile,
                                u'Profile for "%s" user' % self.user.username)

    @TestCase.raises(AssertionError)
    def test_read_assertion(self):
        self.assert_read(UserProfile, user=self.user)

    def test_read_model(self):
        self.assert_create(UserProfile, user=self.user)
        self.assert_read(UserProfile, Q(user=self.user))
        self.assert_read(UserProfile, user=self.user)

    def test_read_manager(self):
        profile = self.assert_create(UserProfile, user=self.user)

        for city in TEST_CITIES:
            self.assert_create(profile.contacts, city=city)
            self.assert_read(profile.contacts, Q(city=city))
            self.assert_read(profile.contacts, city=city)

    def test_read_string(self):
        self.assert_create('testapp.UserProfile', user=self.user)
        self.assert_read('testapp.UserProfile', Q(user=self.user))
        self.assert_read('testapp.UserProfile', user=self.user)

    def test_update_instance(self):
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

    def test_update_string(self):
        self.assert_create('testapp.UserProfile', user=self.user)
        self.assert_update('testapp.UserProfile', bio=TEST_BIO)
        self.assert_read('testapp.UserProfile', bio=TEST_BIO)

    def test_unicode(self):
        profile = self.assert_create(UserProfile, user=self.user)
        self.assert_unicode(profile,
                            u'Profile for "%s" user' % self.user.username)

    @TestCase.raises(AssertionError)
    def test_unicode_assertion(self):
        profile = self.assert_create(UserProfile, user=self.user)
        self.assert_unicode(profile,
                            u'Profile for "%s"' % self.user.username)


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

    @TestCase.raises(AssertionError)
    def testCountAssertion(self):
        self.assertCount(UserProfile, 1)
        self.assertCount(UserProfile, (1, 2))
        self.assertCount(UserProfile, [1, 2])

    def testCountModel(self):
        self.assertCount(UserProfile, 0)
        self.assertCount(UserProfile, (0, 1))
        self.assertCount(UserProfile, [0, 1])

        profile = self.assertCreate(UserProfile, user=self.user)

        self.assertCount(UserProfile, 1)
        self.assertCount(UserProfile, (0, 1))
        self.assertCount(UserProfile, [0, 1])

    def testCountManager(self):
        profile = self.assertCreate(UserProfile, user=self.user)

        self.assertCount(profile.contacts, 0)
        self.assertCount(profile.contacts, (0, len(TEST_CITIES)))
        self.assertCount(profile.contacts, [0, len(TEST_CITIES)])

        for city in TEST_CITIES:
            self.assertCreate(profile.contacts, city=city)

        self.assertCount(profile.contacts, len(TEST_CITIES))
        self.assertCount(profile.contacts, (0, len(TEST_CITIES)))
        self.assertCount(profile.contacts, [0, len(TEST_CITIES)])

    def testCountString(self):
        self.assertCount('testapp.UserProfile', 0)
        self.assertCount('testapp.UserProfile', (0, 1))
        self.assertCount('testapp.UserProfile', [0, 1])

        profile = self.assertCreate('testapp.UserProfile', user=self.user)

        self.assertCount('testapp.UserProfile', 1)
        self.assertCount('testapp.UserProfile', (0, 1))
        self.assertCount('testapp.UserProfile', [0, 1])

    def testCreateModel(self):
        self.assertCreate(UserProfile, user=self.user)

    def testCreateManager(self):
        profile = self.assertCreate(UserProfile, user=self.user)
        self.assertCreate(profile.contacts, city=TEST_CITY)

    def testCreateString(self):
        self.assertCreate('testapp.UserProfile', user=self.user)

    def testDeleteInstance(self):
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

    def testDeleteString(self):
        self.assertCreate('testapp.UserProfile', user=self.user)
        self.assertDelete('testapp.UserProfile')
        self.assertCount('testapp.UserProfile', 0)

    @TestCase.raises(AssertionError)
    def testNotCountAssertion(self):
        self.assertNotCount(UserProfile, 0)
        self.assertNotCount(UserProfile, (0, 1))
        self.assertNotCount(UserProfile, [0, 1])

    def testNotCountModel(self):
        self.assertNotCount(UserProfile, 1)
        self.assertNotCount(UserProfile, (1, 2))
        self.assertNotCount(UserProfile, [1, 2])

    def testNotCountManager(self):
        profile = self.assertCreate(UserProfile, user=self.user)
        self.assertNotCount(profile.contacts, 1)
        self.assertNotCount(profile.contacts, (1, 2))
        self.assertNotCount(profile.contacts, [1, 2])

    def testNotCountString(self):
        self.assertNotCount('testapp.UserProfile', 1)
        self.assertNotCount('testapp.UserProfile', (1, 2))
        self.assertNotCount('testapp.UserProfile', [1, 2])

    @TestCase.raises(AssertionError)
    def testNotReadAssertion(self):
        self.assertCreate(UserProfile, user=self.user)
        self.assertNotRead(UserProfile, user=self.user)

    def testNotReadModel(self):
        self.assertNotRead(UserProfile, user=self.user)

    def testNotReadManager(self):
        profile = self.assertCreate(UserProfile, user=self.user)
        self.assertNotRead(profile.contacts, city=TEST_CITY)

    def testNotReadString(self):
        self.assertNotRead('testapp.UserProfile', user=self.user)

    def testNotUnicode(self):
        profile = self.assertCreate(UserProfile, user=self.user)
        self.assertNotUnicode(profile,
                                u'Profile for "%s"' % self.user.username)

    @TestCase.raises(AssertionError)
    def testNotUnicodeAssertion(self):
        profile = self.assertCreate(UserProfile, user=self.user)
        self.assertNotUnicode(profile,
                                u'Profile for "%s" user' % self.user.username)

    @TestCase.raises(AssertionError)
    def testReadAssertion(self):
        self.assertRead(UserProfile, user=self.user)

    def testReadModel(self):
        self.assertCreate(UserProfile, user=self.user)
        self.assertRead(UserProfile, user=self.user)

    def testReadManager(self):
        profile = self.assertCreate(UserProfile, user=self.user)

        for city in TEST_CITIES:
            self.assertCreate(profile.contacts, city=city)
            self.assertRead(profile.contacts, city=city)

    def testReadString(self):
        self.assertCreate('testapp.UserProfile', user=self.user)
        self.assertRead('testapp.UserProfile', user=self.user)

    def testUpdateInstance(self):
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

    def testUpdateString(self):
        self.assertCreate('testapp.UserProfile', user=self.user)
        self.assertUpdate('testapp.UserProfile', bio=TEST_BIO)
        self.assertRead('testapp.UserProfile', bio=TEST_BIO)

    def testUnicode(self):
        profile = self.assertCreate(UserProfile, user=self.user)
        self.assertUnicode(profile,
                            u'Profile for "%s" user' % self.user.username)

    @TestCase.raises(AssertionError)
    def testUnicodeAssertion(self):
        profile = self.assertCreate(UserProfile, user=self.user)
        self.assertUnicode(profile,
                            u'Profile for "%s"' % self.user.username)


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
