try:
    from unittest2 import TestCase as BaseTestCase
except ImportError:
    from unittest import TestCase as BaseTestCase

# Dirty hack to prevent ``ImportError`` on installing tddspry via pip
try:
    from nose import tools
except ImportError:
    tools = type('FakeNoseToolsModule', (object, ), {'__all__': []})

from tddspry.utils import camelcase_to_underscore, underscore_to_camelcase


__all__ = ('NoseTestCase', 'TestCase')


class TestCaseMetaclass(type):

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

        return type.__new__(cls, name, bases, attrs)


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


NoseTestCase = TestCase
