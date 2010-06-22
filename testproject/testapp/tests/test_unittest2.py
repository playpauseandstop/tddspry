import copy
import re

from random import randint, shuffle

from tddspry import TestCase
from tddspry.django import TestCase as DjangoTestCase


TEST_DICT = {
    'key': 'value',
    'some': 'thing',
}
TEST_ITEM = randint(1, 10)
TEST_LIST = range(1, 11)
TEST_NONE = None
TEST_NOT_REGEXP = re.compile('\d+')
TEST_NOT_ITEM = -TEST_ITEM
TEST_REGEXP = re.compile('\w+')
TEST_SUBSET = {'key': 'value'}
TEST_TEXT = 'Something'


class TestUnitTest2CamelCaseMethods(TestCase):

    def testAssertMethods(self):
        self.assertGreater(2, 1)
        self.assertGreaterEqual(2, 1)
        self.assertGreaterEqual(2, 2)

        self.assertLess(1, 2)
        self.assertLessEqual(1, 2)
        self.assertLessEqual(2, 2)

        self.assertRegexpMatches(TEST_TEXT, TEST_REGEXP)
        self.assertNotRegexpMatches(TEST_TEXT, TEST_NOT_REGEXP)

        self.assertIn(TEST_ITEM, TEST_LIST)
        self.assertNotIn(TEST_NOT_ITEM, TEST_LIST)

        self.assertIs(TEST_NONE, None)
        self.assertIsNot(1, None)

        self.assertIsNone(TEST_NONE)
        self.assertIsNotNone(1)

        self.assertIsInstance(TEST_ITEM, int)
        self.assertNotIsInstance(TEST_ITEM, float)

        self.assertDictContainsSubset(TEST_SUBSET, TEST_DICT)
        self.assertSequenceEqual(tuple(TEST_LIST), TEST_LIST)

        sequence = copy.copy(TEST_LIST)
        shuffle(sequence)

        self.assertItemsEqual(TEST_LIST, sequence)


class TestUnitTest2CamelCaseMethodsDjango(DjangoTestCase):

    def testAssertMethods(self):
        self.assertGreater(2, 1)
        self.assertGreaterEqual(2, 1)
        self.assertGreaterEqual(2, 2)

        self.assertLess(1, 2)
        self.assertLessEqual(1, 2)
        self.assertLessEqual(2, 2)

        self.assertRegexpMatches(TEST_TEXT, TEST_REGEXP)
        self.assertNotRegexpMatches(TEST_TEXT, TEST_NOT_REGEXP)

        self.assertIn(TEST_ITEM, TEST_LIST)
        self.assertNotIn(TEST_NOT_ITEM, TEST_LIST)

        self.assertIs(TEST_NONE, None)
        self.assertIsNot(1, None)

        self.assertIsNone(TEST_NONE)
        self.assertIsNotNone(1)

        self.assertIsInstance(TEST_ITEM, int)
        self.assertNotIsInstance(TEST_ITEM, float)

        self.assertDictContainsSubset(TEST_SUBSET, TEST_DICT)
        self.assertSequenceEqual(tuple(TEST_LIST), TEST_LIST)

        sequence = copy.copy(TEST_LIST)
        shuffle(sequence)

        self.assertItemsEqual(TEST_LIST, sequence)


class TestUnitTest2UnderscoreMethods(TestCase):

    def test_assert_methods(self):
        self.assert_greater(2, 1)
        self.assert_greater_equal(2, 1)
        self.assert_greater_equal(2, 2)

        self.assert_less(1, 2)
        self.assert_less_equal(1, 2)
        self.assert_less_equal(2, 2)

        self.assert_regexp_matches(TEST_TEXT, TEST_REGEXP)
        self.assert_not_regexp_matches(TEST_TEXT, TEST_NOT_REGEXP)

        self.assert_in(TEST_ITEM, TEST_LIST)
        self.assert_not_in(TEST_NOT_ITEM, TEST_LIST)

        self.assert_is(TEST_NONE, None)
        self.assert_is_not(1, None)

        self.assert_is_none(TEST_NONE)
        self.assert_is_not_none(1)

        self.assert_is_instance(TEST_ITEM, int)
        self.assert_not_is_instance(TEST_ITEM, float)

        self.assert_dict_contains_subset(TEST_SUBSET, TEST_DICT)
        self.assert_sequence_equal(tuple(TEST_LIST), TEST_LIST)

        sequence = copy.copy(TEST_LIST)
        shuffle(sequence)

        self.assert_items_equal(TEST_LIST, sequence)


class TestUnitTest2UnderscoreMethodsDjango(DjangoTestCase):

    def test_assert_methods(self):
        self.assert_greater(2, 1)
        self.assert_greater_equal(2, 1)
        self.assert_greater_equal(2, 2)

        self.assert_less(1, 2)
        self.assert_less_equal(1, 2)
        self.assert_less_equal(2, 2)

        self.assert_regexp_matches(TEST_TEXT, TEST_REGEXP)
        self.assert_not_regexp_matches(TEST_TEXT, TEST_NOT_REGEXP)

        self.assert_in(TEST_ITEM, TEST_LIST)
        self.assert_not_in(TEST_NOT_ITEM, TEST_LIST)

        self.assert_is(TEST_NONE, None)
        self.assert_is_not(1, None)

        self.assert_is_none(TEST_NONE)
        self.assert_is_not_none(1)

        self.assert_is_instance(TEST_ITEM, int)
        self.assert_not_is_instance(TEST_ITEM, float)

        self.assert_dict_contains_subset(TEST_SUBSET, TEST_DICT)
        self.assert_sequence_equal(tuple(TEST_LIST), TEST_LIST)

        sequence = copy.copy(TEST_LIST)
        shuffle(sequence)

        self.assert_items_equal(TEST_LIST, sequence)
