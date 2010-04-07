from tddspry import TestCase


TEST_VERSIONS = (
    ((0, 1), '0.1'),
    ((0, 1, None), '0.1'),
    ((0, 1, 'alpha'), '0.1_alpha'),
    ((0, 1, 1), '0.1.1'),
    ((0, 1, 1, 'rc1'), '0.1.1_rc1'),
    ((0, 1, 1, 1), '0.1.1.1')
)


class TestVersion(TestCase):

    def setup(self):
        self.OLD_VERSION = tddspry.VERSION

    def teardown(self):
        tddspry.VERSION = self.OLD_VERSION

    def test_get_version(self):
        for version, result in TEST_VERSIONS:
            tddspry.VERSION = version
            self.assert_equal(tddspry.get_version(), result)
