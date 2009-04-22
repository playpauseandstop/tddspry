from tddspry import NoseTestCase


def raise_exception():
    raise TypeError


class TestNose(NoseTestCase):

    def test_nose_tools(self):
        self.ok_(True)
        self.eq_(True, True)

        self.assert_almost_equal(1.99999999, 1.9999999, 4)
        self.assert_almost_equals(1.99999999, 1.9999999, 4)
        self.assert_not_almost_equal(1.43578901, 1.43758900)
        self.assert_not_almost_equals(1.43578901, 1.43758900)

        self.assert_equal(1, 1)
        self.assert_equals(1, 1)
        self.assert_not_equal(1, 2)
        self.assert_not_equals(1, 2)

        self.assert_false(False)
        self.assert_raises(TypeError, raise_exception)
        self.assert_true(True)
