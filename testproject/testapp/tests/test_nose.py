import time

from tddspry import TestCase


TEST_STRING = 'Something'
TEST_UNICODE = u'Something'


class DummyUnicodeAndStr(object):

    def __str__(self):
        return TEST_STRING * 2

    def __unicode__(self):
        return TEST_UNICODE


class DummyUnicode(object):

    def __unicode__(self):
        return TEST_UNICODE


def dummy_setup():
    pass


def dummy_teardown():
    pass


def raise_exception():
    raise TypeError


class TestNose(TestCase):

    def setup(self):
        self.has_setup = True

    def test_find_in(self):
        self.find_in('Text', 'Text in (valid) parentheses')

    def test_find_in_count(self):
        self.find_in('in', 'Text in (invalid) parentheses', count=2)

    @TestCase.raises(AssertionError)
    def test_find_in_count_error(self):
        self.find_in('Text', 'Text in (valid) parentheses', count=2)

    @TestCase.raises(AssertionError)
    def test_find_in_error(self):
        self.find_in('invalid', 'Text in (valid) parentheses')

    def test_find_in_escape(self):
        self.find_in('(valid)', 'Text in (valid) parentheses', escape=True)

    @TestCase.raises(AssertionError)
    def test_find_in_escape_error(self):
        self.find_in('(valid)', 'Test in \(valid\) parentheses', escape=True)

    def test_find_in_found(self):
        self.find_in('in', 'Text in (invalid) parentheses', count=2)
        self.assert_true(hasattr(self, '_found'))
        self.assert_equal(len(self._found), 2)
        self.assert_true(isinstance(self._found[0], object))
        self.assert_equal(self._found[0].group(), 'in')
        self.assert_equal(self._found[0].start(), 5)
        self.assert_equal(self._found[0].end(), 7)
        self.assert_true(isinstance(self._found[1], object))
        self.assert_equal(self._found[1].group(), 'in')
        self.assert_equal(self._found[1].start(), 9)
        self.assert_equal(self._found[1].end(), 11)

        self.find_in('valid', 'Text in (valid) parentheses')
        self.assert_true(hasattr(self, '_found'))
        self.assert_equal(len(self._found), 1)
        self.assert_true(isinstance(self._found[0], object))
        self.assert_equal(self._found[0].group(), 'valid')
        self.assert_equal(self._found[0].start(), 9)
        self.assert_equal(self._found[0].end(), 14)

        self.find_in('(valid)', 'Text in (valid) parentheses', flat=True)
        self.assert_false(hasattr(self, '_found'))

        self.find_in('Text', 'Text in (valid) parentheses')
        self.assert_true(hasattr(self, '_found'))

        self.assert_raises(AssertionError,
                           self.find_in,
                           'text',
                           'Text in (valid) parentheses')
        self.assert_false(hasattr(self, '_found'))

    def test_find_in_flags(self):
        self.find_in('text', 'Text in (valid) parentheses', flags='i')

    @TestCase.raises(AssertionError)
    def test_find_in_flags_error(self):
        self.find_in('text', 'Text in (valid) parentheses', flags='s')

    def test_find_in_flat(self):
        self.find_in('c++', 'c++ is good, but python is better', flat=True)

    @TestCase.raises(AssertionError)
    def test_find_in_flat_error(self):
        self.find_in('c++', 'python is great, but erlang is faster', flat=True)

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

        self.assert_not_unicode(TEST_STRING, TEST_UNICODE[::-1])
        self.assert_not_unicode(DummyUnicode(), TEST_STRING[::-1])
        self.assert_not_unicode(DummyUnicode(), TEST_UNICODE[::-1])
        self.assert_not_unicode(DummyUnicodeAndStr(), TEST_STRING[::-1])
        self.assert_not_unicode(DummyUnicodeAndStr(), TEST_UNICODE[::-1])

        self.assert_unicode(TEST_STRING, TEST_UNICODE)
        self.assert_unicode(DummyUnicode(), TEST_STRING)
        self.assert_unicode(DummyUnicode(), TEST_UNICODE)
        self.assert_unicode(DummyUnicode(), DummyUnicodeAndStr())
        self.assert_unicode(DummyUnicodeAndStr(), TEST_STRING)
        self.assert_unicode(DummyUnicodeAndStr(), TEST_UNICODE)

    def test_notfind_in(self):
        self.notfind_in('invalid', 'Text in (valid) parentheses')

    @TestCase.raises(AssertionError)
    def test_notfind_in_error(self):
        self.notfind_in('valid', 'Text in (valid) parentheses')

    def test_notfind_in_escape(self):
        self.notfind_in('(valid)',
                        'Text in (invalid) parentheses',
                        escape=True)

    @TestCase.raises(AssertionError)
    def test_notfind_in_escape_error(self):
        self.notfind_in('(valid)', 'Test in (valid) parentheses', escape=True)

    def test_notfind_in_flags(self):
        self.notfind_in('text', 'Text in (valid) parentheses', flags='s')

    @TestCase.raises(AssertionError)
    def test_notfind_in_flags_error(self):
        self.notfind_in('text', 'Text in (valid) parentheses', flags='i')

    def test_notfind_in_flat(self):
        self.notfind_in('c#', 'c++ is good, but python is better', flat=True)

    @TestCase.raises(AssertionError)
    def test_notfind_in_flat_error(self):
        self.notfind_in('c++', 'c++ is good, but python is better', flat=True)

    @TestCase.raises(TypeError)
    def test_raises(self):
        raise_exception()

    @TestCase.raises(AssertionError, TypeError, ValueError)
    def test_raises_complex(self):
        self.ok_(False)
        raise_exception()
        raise ValueError

    @TestCase.raises(TypeError)
    @TestCase.raises(ValueError)
    def test_raises_failed(self):
        raise_exception()

    def test_setup(self):
        self.assert_true(hasattr(self, 'has_setup'))

    @TestCase.timed(10)
    def test_timed(self):
        pass

    @TestCase.raises(AssertionError)
    @TestCase.timed(1)
    def test_timed_failed(self):
        time.sleep(2)

    @TestCase.with_setup(dummy_setup, dummy_teardown)
    def test_with_setup_complex(self):
        pass

    @TestCase.with_setup(setup=dummy_setup)
    def test_with_setup_setup(self):
        pass

    @TestCase.with_setup(teardown=dummy_teardown)
    def test_with_setup_teardown(self):
        pass
