from tddspry.django import TestCase
from tddspry.django.helpers import EMAIL, PASSWORD, USERNAME

from django.contrib.auth.models import User


class TestModels(TestCase):

    multidb = True

    def setup(self):
        self.model = User
        self.manager = self.model.objects.using('legacy')

        self.kwargs = {'username': USERNAME,
                       'password': PASSWORD,
                       'email': EMAIL}
        self.sgrawk = {'username': USERNAME[::-1],
                       'password': PASSWORD[::-1],
                       'email': EMAIL[::-1]}

    def test_using_keyword(self):
        self.assert_count(self.model, 0)
        self.assert_count(self.model, 0, using='legacy')

        self.assert_create(self.model, using='legacy', **self.kwargs)

        self.assert_count(self.model, 0)
        self.assert_not_count(self.model, 0, using='legacy')
        self.assert_count(self.model, 1, using='legacy')

        for key, value in self.kwargs.items():
            self.assert_not_read(self.model, **{key: value})

        for key, value in self.kwargs.items():
            self.assert_read(self.model, using='legacy', **{key: value})

        try:
            self.assert_update(self.model, **self.sgrawk)
        except AssertionError:
            pass
        else:
            assert False, 'Any %r model should be exist in default ' \
                          'database.' % self.model

        self.assert_update(self.model, using='legacy', **self.sgrawk)

        self.assert_not_read(self.model, **self.kwargs)
        self.assert_not_read(self.model, using='legacy', **self.kwargs)

        self.assert_delete(self.model)
        self.assert_delete(self.model, using='legacy')

        self.assert_count(self.model, 0)
        self.assert_count(self.model, 0, using='legacy')

    def test_using_manager(self):
        self.assert_count(self.manager, 0)
        self.assert_create(self.manager, **self.kwargs)
        self.assert_not_count(self.manager, 0)
        self.assert_count(self.manager, 1)

        for key, value in self.kwargs.items():
            self.assert_read(self.manager, **{key: value})

        self.assert_update(self.manager, **self.sgrawk)
        self.assert_not_read(self.manager, **self.kwargs)
        self.assert_delete(self.manager)
        self.assert_count(self.manager, 0)
