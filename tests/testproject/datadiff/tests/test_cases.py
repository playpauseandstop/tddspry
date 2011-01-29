from django.conf import settings
from django.utils.encoding import smart_str

from tddspry import TestCase as BaseTestCase
from tddspry.django import TestCase as DjangoTestCase


try:
    import datadiff
except ImportError:
    datadiff = None


TDDSPRY_USE_DATADIFF = getattr(settings, 'TDDSPRY_USE_DATADIFF', False)

TEST_BAR = {'a': 1, 'b': 2, 'c': 3, 'x': [1, 2, 3]}
TEST_FOO = {'a': 1, 'b': 2, 'c': 3, 'd': 4, 'x': [1, 2]}


class TestDataDiff(BaseTestCase):

    def test_datadiff_assert_equal(self):
        if not datadiff:
            self.assert_false(hasattr(self, 'datadiff_assert_equal'))
        else:
            self.datadiff_assert_equal(TEST_BAR, TEST_BAR)

            try:
                self.datadiff_assert_equal(TEST_BAR, TEST_FOO)
            except AssertionError, e:
                diff = datadiff.diff(TEST_BAR, TEST_FOO)
                self.assert_unicode(e, '\n' + smart_str(diff))


class TestDataDiffWithDjango(DjangoTestCase):

    def test_equal(self):
        self.assert_equal(TEST_BAR, TEST_BAR)

    def test_when_disabled(self, force=False):
        if not TDDSPRY_USE_DATADIFF or force:
            try:
                self.assert_equal(TEST_BAR, TEST_FOO)
            except AssertionError, e:
                self.assert_unicode(e, '%r != %r' % (TEST_BAR, TEST_FOO))

    def test_when_enabled(self):
        if TDDSPRY_USE_DATADIFF:
            if not datadiff:
                self.test_when_disabled(True)
            else:
                try:
                    self.assert_equal(TEST_BAR, TEST_FOO)
                except AssertionError, e:
                    diff = datadiff.diff(TEST_BAR, TEST_FOO)
                    self.assert_unicode(e, '\n' + smart_str(diff))
