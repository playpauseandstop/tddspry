from tddspry.django import TestCase

from django.db import models


TEST_FIELD = 'Test Field value'


class AnotherDummyModel(models.Model):

    field = models.CharField(max_length=128)

    class Meta:
        app_label = 'testapp'


class TestAnotherDummyModel(TestCase):

    def test_create(self):
        self.assert_create(AnotherDummyModel, field=TEST_FIELD)

    def test_delete(self):
        dummy = self.assert_create(AnotherDummyModel, field=TEST_FIELD)
        self.assert_delete(dummy)

    def test_read(self):
        self.assert_create(AnotherDummyModel, field=TEST_FIELD)
        self.assert_read(AnotherDummyModel, field=TEST_FIELD)

    def test_update(self):
        dummy = self.assert_create(AnotherDummyModel, field=TEST_FIELD)
        self.assert_update(dummy, field=TEST_FIELD[::-1])
