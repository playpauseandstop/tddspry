from nose import tools


__all__ = ('NoseTestCase', )


class BaseTestCase(object):

    pass


class NoseTestCaseMetaclass(type):

    def __new__(cls, name, bases, attrs):
        def func(attr):
            return lambda _, *args, **kwargs: \
                       getattr(tools, attr)(*args, **kwargs)

        decorators = ('make_decorator', 'raises', 'timed', 'with_setup')

        for attr in tools.__all__:
            if attr in decorators:
                setattr(cls, attr, func(attr))
            else:
                attrs.update({attr: func(attr)})

        return type.__new__(cls, name, bases, attrs)


class NoseTestCase(BaseTestCase):
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

    __metaclass__ = NoseTestCaseMetaclass
