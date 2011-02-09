import re
import warnings

# If possible use ``unittest2.TestCase`` as base test class
try:
    from unittest2 import TestCase as BaseTestCase
except ImportError:
    from unittest import TestCase as BaseTestCase

# Try to load ``datadiff`` library to use its ``assert_equal``
try:
    from datadiff.tools import assert_equal as datadiff_assert_equal
except ImportError:
    datadiff_assert_equal = None

# Dirty hack to prevent ``ImportError`` on installing tddspry via pip
try:
    from nose import tools
except ImportError:
    tools = type('FakeNoseToolsModule', (object, ), {'__all__': []})

from tddspry.utils import *


__all__ = ('NoseTestCase', 'TestCase')


class BaseTestCaseMetaclass(type):

    def __new__(cls, name, bases, attrs):
        for base in bases:
            for base_name in dir(base):
                base_value = getattr(base, base_name)

                if not callable(base_value) or \
                   not base_name.startswith('assert'):
                    continue

                if not base_name in attrs:
                    attrs.update({base_name: base_value})

        for attr_name, attr_value in attrs.items():
            if not attr_name.startswith('assert') or attr_name == 'assert_':
                continue

            if attr_name[6] == '_':
                new_name = underscore_to_camelcase(attr_name)
            else:
                new_name = camelcase_to_underscore(attr_name)

            if not new_name in attrs:
                attrs[new_name] = attr_value

        for attr in tools.__all__:
            attrs.update({attr: getattr(tools, attr)})
            attrs[attr] = staticmethod(attrs[attr])

        if datadiff_assert_equal:
            key = attrs.get('use_datadiff', False) and 'assert_equal' \
                                                   or 'datadiff_assert_equal'

            attrs.update({key: datadiff_assert_equal})
            attrs[key] = staticmethod(attrs[key])
        elif attrs.get('use_datadiff', False):
            warnings.warn('You enabled ``datadiff.tools.assert_equal``, but ' \
                          'looks like you have not ``datadiff`` library ' \
                          'installed in your system.')

        return type.__new__(cls, name, bases, attrs)


class TestCaseMetaclass(BaseTestCaseMetaclass):

    def __new__(cls, name, bases, attrs):
        for attr_name, attr_value in attrs.items():
            # Add nose styled names of setup and teardown methods to cls attrs
            if attr_name == 'setup' and not 'setUp' in attrs:
                attrs['setUp'] = attr_value

            if attr_name == 'teardown' and not 'tearDown' in attrs:
                attrs['tearDown'] = attr_value

        return super(TestCaseMetaclass, cls).__new__(cls, name, bases, attrs)


class TestCase(BaseTestCase):
    """
    For convenience this class consist of all functions exists in nose.tools__
    module.

    .. __: http://somethingaboutorange.com/mrl/projects/nose/0.11.0/testing_tools.html

    So, if you have functions, like this::

        def addititon(first, second):
            return first + second

        def division(first, second):
            if not second:
                raise ValueError
            return first / second

        def multiplication(first, second):
            return first * second

        def subtraction(first, second):
            return first - second

    You can write simple ``TestFunctions`` class to test its::

        from tddspry import NoseTestCase


        class TestFunctions(NoseTestCase):

            def test_addition(self):
                self.assert_equal(addititon(1, 2), 3)
                self.assert_not_equal(addititon(1, 2), 2)

            def test_division(self):
                self.assert_equal(division(4, 2), 2)
                self.assert_not_equal(division(5.0, 2), 2)
                self.assert_raises(ValueError, division, 2, 0)

            def test_multiplication(self):
                self.assert_equal(multiplication(1, 2), 2)
                self.assert_not_equal(multiplication(1, 2), 3)

            def test_subtraction(self):
                self.assert_equal(subtraction(2, 1), 1)
                self.assert_equal(subtraction(2, 1), 2)

    """

    __metaclass__ = TestCaseMetaclass

    def assert_not_unicode(self, first, second, message=None):
        """
        Test that ``first`` and ``second`` after converting to ``unicode``
        are not equal.
        """
        return self.assert_not_equal(unicode(first), unicode(second), message)

    def assert_unicode(self, first, second, message=None):
        """
        Test that ``first`` and ``second`` after converting to ``unicode``
        are equal.

        Without ``assert_unicode`` method you may be need to manually convert
        ``first`` and ``second`` values to ``unicode``, when ``assert_unicode``
        make this in place of you.
        """
        return self.assert_equal(unicode(first), unicode(second), message)

    def find_in(self, what, where, flags=None, count=None, escape=False,
                flat=False):
        """
        Try to find ``what`` text in ``where``.

        Method supports both of regular expression matching (with
        ``re.finditer`` function) and ``flat`` string matching (with ``what in
        where`` expression) modes. To enable flat mode call ``find_in`` with
        ``flat=True``.

        If ``what`` string not found, ``AssertionError`` would be raised.

        Specify ``count`` to test that ``what`` occurs ``count`` times in the
        ``where`` text.

        In regular expression mode you can specify ``flags`` supported by
        ``re`` module in text format, like ``'i'`` or ``'s'`` instead of
        ``re.I`` or ``re.S``. If multiple ``flags`` specified they would
        connected with ``|`` (unary OR), e.g. ``flags='iu'`` would be sent to
        ``re.finditer`` as ``flags=re.I | re.U``.

        In reqular expression mode you also can escape ``what`` text with
        ``re.escape`` method. It's useful if your search string contains of
        regular expression metacharacters.

        All non-overlapping matches of ``what`` in ``where`` would be stored
        as list of ``MatchObject`` instances in ``_found`` private var.
        """
        if flat:
            found = None
            real_count = where.count(what)
        else:
            if escape:
                what = re.escape(what)

            regexp = re.compile(what, process_re_flags(flags))
            found = filter(lambda matched: matched, regexp.finditer(where))
            real_count = len(found)

        if found:
            setattr(self, '_found', found)
        elif not found and hasattr(self, '_found'):
            delattr(self, '_found')

        if count is not None:
            assert count == real_count, 'Matched to %r %d times, not %d ' \
                                        'times. Text to search: %r' % \
                                        (what, real_count, count, where)
        else:
            assert real_count, 'No match to %r in %r' % (what, where)

        return True

    def notfind_in(self, what, where, flags=None, escape=False, flat=False):
        """
        Assert that ``what`` not found in ``where``.

        This method is negate version of ``TestCase.find_in`` and supports
        all keywords and modes from it exclude of ``count``. Also in regular
        expression mode ``re.search`` function used instead of ``re.finditer``
        cause we don't need to store matched groups.

        If ``what`` string found, ``AssertionError`` would be raised.
        """
        message = 'Matched %r in %r' % (what, where)

        if not flat:
            if escape:
                what = re.escape(what)

            regexp = re.compile(what, process_re_flags(flags))
            assert not regexp.search(where), message
        else:
            assert not what in where, message

        return True


NoseTestCase = TestCase
