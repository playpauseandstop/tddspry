from nose import tools


__all__ = ('NoseTestCase', )


class NoseTestCase(object):

    def __init__(self, *args, **kwargs):
        super(NoseTestCase, self).__init__(*args, **kwargs)
        for attr in tools.__all__:
            setattr(self, attr, getattr(tools, attr))
