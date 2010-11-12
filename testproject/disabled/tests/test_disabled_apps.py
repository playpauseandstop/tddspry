from tddspry.django import TestCase as TestCase

from django.conf import settings


TEST_ATTR_APP = 'testproject.disabled.attr'
TEST_SETTING_APP = 'testproject.disabled.setting'


class TestDisableApps(TestCase):

    disabled_apps = [TEST_ATTR_APP]

    def test_disabled_apps(self):
        self.assert_false(TEST_ATTR_APP in settings.INSTALLED_APPS)


class TestDisableAppsBoth(TestCase):

    disabled_apps = [TEST_ATTR_APP]

    def test_disabled_apps(self):
        self.assert_false(TEST_ATTR_APP in settings.INSTALLED_APPS)
        self.assert_false(TEST_SETTING_APP in settings.INSTALLED_APPS)


class TestDisableAppsSetting(TestCase):

    def test_disabled_apps(self):
        self.assert_true(TEST_ATTR_APP in settings.INSTALLED_APPS)
        self.assert_false(TEST_SETTING_APP in settings.INSTALLED_APPS)
