import time

from tddspry import NoseTestCase


def dummy_setup():
    pass


def dummy_teardown():
    pass


def raise_exception():
    raise TypeError


class TestNose(NoseTestCase):

    def test_methods(self):
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

    @NoseTestCase.raises(TypeError)
    def test_raises(self):
        raise_exception()

    @NoseTestCase.raises(AssertionError, TypeError, ValueError)
    def test_raises_complex(self):
        self.ok_(False)
        raise_exception()
        raise ValueError

    @NoseTestCase.raises(TypeError)
    @NoseTestCase.raises(ValueError)
    def test_raises_failed(self):
        raise_exception()

    @NoseTestCase.timed(10)
    def test_timed(self):
        pass

    @NoseTestCase.raises(AssertionError)
    @NoseTestCase.timed(1)
    def test_timed_failed(self):
        time.sleep(2)

    @NoseTestCase.with_setup(dummy_setup, dummy_teardown)
    def test_with_setup_complex(self):
        pass

    @NoseTestCase.with_setup(setup=dummy_setup)
    def test_with_setup_setup(self):
        pass

    @NoseTestCase.with_setup(teardown=dummy_teardown)
    def test_with_setup_teardown(self):
        pass
