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

    __metaclass__ = NoseTestCaseMetaclass
