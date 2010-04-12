import tddspry

from tddspry import TestCase
from tddspry.utils import camelcase_to_underscore, underscore_to_camelcase


TEST_METHOD_NAMES = (
    ('assert_create', 'assertCreate'),
    ('assert_contains', 'assertContains'),
    ('assert_count', 'assertCount'),
    ('assert_delete', 'assertDelete'),
    ('assert_equal', 'assertEqual'),
    ('assert_form_error', 'assertFormError'),
    ('assert_not_contains', 'assertNotContains'),
    ('assert_not_equal', 'assertNotEqual'),
    ('assert_raises', 'assertRaises'),
    ('assert_read', 'assertRead'),
    ('assert_redirects', 'assertRedirects'),
    ('assert_template_not_used', 'assertTemplateNotUsed'),
    ('assert_template_used', 'assertTemplateUsed'),
    ('assert_unicode', 'assertUnicode'),
    ('assert_update', 'assertUpdate'),
)

TEST_VERSIONS = (
    ((0, 1), '0.1'),
    ((0, 1, None), '0.1'),
    ((0, 1, 'alpha'), '0.1-alpha'),
    ((0, 1, 1), '0.1.1'),
    ((0, 1, 1, 'beta'), '0.1.1-beta'),
    ((0, 1, 1, 1), '0.1.1.1'),
    ((0, 1, 1, 1, 'rc1'), '0.1.1.1-rc1'),
)


class TestUtils(tddspry.TestCase):

    def test_camelcase_to_underscore(self):
        for underscore, camelcase in TEST_METHOD_NAMES:
            self.assert_equal(camelcase_to_underscore(camelcase), underscore)

    def test_underscore_to_camelcase(self):
        for underscore, camelcase in TEST_METHOD_NAMES:
            self.assert_equal(underscore_to_camelcase(underscore), camelcase)


class TestVersion(tddspry.TestCase):

    def setup(self):
        self.OLD_VERSION = tddspry.VERSION

    def teardown(self):
        tddspry.VERSION = self.OLD_VERSION

    def test_get_version(self):
        for version, result in TEST_VERSIONS:
            tddspry.VERSION = version
            self.assert_equal(tddspry.get_version(), result)
