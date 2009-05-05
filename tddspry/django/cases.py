import os

from django.conf import settings
from django.contrib.auth.models import Permission
from django.core import mail
from django.core.handlers.wsgi import WSGIHandler
from django.core.management import call_command
from django.core.servers.basehttp import AdminMediaHandler
from django.core.urlresolvers import NoReverseMatch, reverse
from django.db import connection, models
from django.test.utils import TestSMTPConnection

from tddspry.cases import NoseTestCase, NoseTestCaseMetaclass
from tddspry.django.decorators import show_on_error

from twill import add_wsgi_intercept, commands
from twill.errors import TwillAssertionError
from twill.extensions.check_links import check_links


__all__ = ('DatabaseTestCase', 'HttpTestCase')


class BaseDatabaseTestCase(NoseTestCase):

    """
    Additional arguments
    --------------------

    database_name
      Use ``None`` or ``':memory'`` to creates sqlite3 database in memory.
      (Default case of Django TestCases).

      Use ``':original:'`` to test in your current projects
      ``settings.DATABASE_NAME``.

      Use custom name to creates test database with current
      ``settings.DATABASE_ENGINE``.

    database_flush
      Flush database if it exists while ``True``, any changes to database on
      ``False`` and recreates it while ``None``.

      **Note:** Please, do not use ``database_flush=True``, on
      ``database_name=':original:'``, it's flushes all data in your
      original (that exists in ``settings.DATABASE_NAME``) database.

    fixtures
      List or tuple with fixtures names to load. See
      ``./manage.py loaddata --help`` in your project to more details.

    """

    database_name = None
    database_flush = None
    fixtures = []

    def setup(self):
        """
        Creates or sets up test database name, loads fixtures and mocks
        ``SMTPConnection`` class from ``django.core.mail``.
        """
        # Creates test database
        is_original_database = False
        settings.original_DATABASE_ENGINE = settings.DATABASE_ENGINE
        settings.original_DATABASE_NAME = settings.DATABASE_NAME

        if self.database_name is None or self.database_name == ':memory:':
            settings.DATABASE_ENGINE = 'sqlite3'
        elif self.database_name == ':original:':
            is_original_database = True
            self.database_name = settings.DATABASE_NAME

            if self.database_flush is None:
                self.database_flush = False

        self.database_name = self.database_name or ':memory:'

        settings.TEST_DATABASE_NAME = self.database_name

        if not is_original_database:
            self.database_name = \
                connection.creation.create_test_db(autoclobber=True)
        tables = connection.introspection.table_names()

        if self.database_flush != False and tables:
            call_command('flush', interactive=False)

        # Load data from fixtures
        if self.fixtures:
            call_command('loaddata', *self.fixtures)

        # Mock original SMTPConnection
        mail.original_SMTPConnection = mail.SMTPConnection
        mail.SMTPConnection = TestSMTPConnection

        mail.outbox = []

    def teardown(self):
        # Destroys test database
        if self.database_flush is None:
            connection.creation.destroy_test_db(self.database_name)

        settings.DATABASE_ENGINE = settings.original_DATABASE_ENGINE
        settings.DATABASE_NAME = settings.original_DATABASE_NAME

        # Unmock original SMTPConnection
        mail.SMTPConnection = mail.original_SMTPConnection
        del mail.original_SMTPConnection

        del mail.outbox


class BaseHttpTestCase(BaseDatabaseTestCase):

    IP = '127.0.0.1'
    PORT = 8088

    def __init__(self, *args, **kwargs):
        super(BaseHttpTestCase, self).__init__(*args, **kwargs)
        self.SITE = 'http://%s:%s' % (self.IP, self.PORT)

    def setup(self):
        super(BaseHttpTestCase, self).setup()

        app = AdminMediaHandler(WSGIHandler())
        add_wsgi_intercept(self.IP, self.PORT, lambda: app)

    def disable_redirect(self):
        """
        Disable auto-redirects in Twill tests.

        To enable use ``HttpTestCase.enable_redirect`` method.
        """
        self.enable_redirect(False)

    def disable_edit_hidden_fields(self):
        """
        Disable editing hidden fields (``<input type="hidden" ... />``) in
        Twill tests (as by default in twill).

        To enable use ``HttpTestCase.enable_edit_hidden_fields`` method.
        """
        self.enable_edit_hidden_fields(False)

    def enable_redirect(self, flag=True):
        """
        Enable auto-redirects in Twill tests (as by default in twill).

        To disable use ``HttpTestCase.disable_redirect`` method.
        """
        self.config('acknowledge_equiv_refresh', int(flag))

    def enable_edit_hidden_fields(self, flag=True):
        """
        Enable editing hidden fields (``<input type="hidden" ... />``) in
        Twill tests.

        To disable use ``HttpTestCase.disable_edit_hidden_fields`` method.
        """
        self.config('readonly_controls_writeable', flag)


class DatabaseTestCase(BaseDatabaseTestCase):

    def check_create(self, model, **kwargs):
        """
        Create Django instance for given model with given kwargs and check
        if it is created correctly.
        """
        old_counter = model.objects.count()

        instance = model.objects.create(**kwargs)
        new_counter = model.objects.count()

        self.assert_equal(new_counter - 1,
                          old_counter,
                          'Could not to create only one new %r instance. ' \
                          'New counter is %d, when old counter is %d.' % (
                              model.__name__,
                              new_counter,
                              old_counter,
                          ))

        return instance

    def check_delete(self, instance):
        """
        Delete Django instance and check if it is deleted correctly.
        """
        model = type(instance)
        pk = instance.pk

        old_counter = model.objects.count()
        instance.delete()
        new_counter = model.objects.count()

        self.assert_equal(old_counter - 1,
                          new_counter,
                          'Could not to delete only one %r instance. ' \
                          'New counter is %d, when old counter is %d.' % (
                              model.__name__,
                              new_counter,
                              old_counter,
                          ))

        try:
            model.objects.get(pk=pk)
        except model.DoesNotExist:
            pass
        else:
            assert False, 'Could not to delete %r instance with %d pk.' % (
                model.__name__, pk
            )

    def check_update(self, instance, **kwargs):
        """
        Update Django instance with given kwargs and check if it is updated
        correctly.
        """
        for name, value in kwargs.items():
            setattr(instance, name, value)
        instance.save()

        upd_instance = type(instance).objects.get(pk=instance.pk)

        for name, value in kwargs.items():
            self.assert_equal(getattr(upd_instance, name),
                              value,
                              'Could not to update %r field.' % name)

        return upd_instance


class HttpTestCaseMetaclass(NoseTestCaseMetaclass):

    def __new__(cls, name, bases, attrs):
        def method(func):
            return lambda _, *args, **kwargs: func(*args, **kwargs)

        for attr_name, attr_value in attrs.items():
            if 'test' in attr_name and callable(attr_value):
                attrs[attr_name] = show_on_error(attr_value, clsname=name)

        for attr in commands.__all__:
            if attr in ('find', 'go', 'notfind', 'url'):
                attr_name = '_' + attr
            else:
                attr_name = attr

            attrs.update({attr_name: method(getattr(commands, attr))})

        attrs.update({'check_links': method(check_links)})

        super_new = super(HttpTestCaseMetaclass, cls).__new__
        return super_new(cls, name, bases, attrs)


class HttpTestCase(BaseHttpTestCase):

    __metaclass__ = HttpTestCaseMetaclass

    def find(self, what, flags='', flat=False):
        """
        Twill used regexp for searching content on web-page. Use ``flat=True``
        to search content on web-page by standart Python ``what in html``
        expression.

        If this expression was not True (was not found on page) it's raises
        ``TwillAssertionError`` as in ``twill.commands.notfind`` method.
        """
        if not flat:
            return self._find(what, flags)

        html = self.get_browser().get_html()
        if not what in html:
            raise TwillAssertionError, 'No match to %r' % what

        return True

    def go(self, url, args=None, kwargs=None):
        """
        Twill needs to set full URL of web-page to loading. This helper
        auto-prepends ``SITE`` value if needed.

        You can also give urlpattern name and function tries to ``reverse``
        it to real URL.
        """
        if not url.startswith(self.SITE):
            if not url.startswith('/'):
                args = args
                kwargs = kwargs

                try:
                    url = reverse(url, args=args, kwargs=kwargs)
                except NoReverseMatch:
                    pass

            url = self.SITE + '/' + url.lstrip('/')
        return self._go(url)

    def go200(self, url, args=None, kwargs=None, check_links=False):
        """
        Go to url and check that response code is 200.
        """
        self.go(url, args, kwargs)
        self.code(200)

        if check_links:
            self.check_links()

    def login(self, username, password, url=None, formid=None):
        """
        Login to Django using ``username`` and ``password``.
        """
        formid = formid or 1
        url = url or 'auth_login'

        self.go200(url)

        self.formvalue(formid, 'username', username)
        self.formvalue(formid, 'password', password)

        self.submit200()

    def login_to_admin(self, username, password):
        """
        Login to Django admin CRUD using ``username`` and ``password``.
        """
        self.go200('/admin/')

        self.formvalue(1, 'username', username)
        self.formvalue(1, 'password', password)

        self.submit200()
        self.notfind('<input type="hidden" name="this_is_the_login_form" ' \
                     'value="1" />')

    def logout(self, url=None):
        """
        Logout from current Django session.
        """
        self.go200(url or 'auth_logout')

    def notfind(self, what, flags='', flat=False):
        """
        Twill used regexp for searching content on web-page. Use ``flat=True``
        to search content on web-page by standart Python ``not what in html``
        expression.

        If this expression was not True (was found on page) it's raises
        ``TwillAssertionError`` as in ``twill.commands.notfind`` method.
        """
        if not flat:
            return self._notfind(what, flags)

        html = self.get_browser().get_html()
        if what in html:
            raise TwillAssertionError, 'Match to %r' % what

        return True

    def submit200(self, submit_button=None, url=None, check_links=False):
        """
        Submit form and checks that response code is 200.
        """
        self.submit(submit_button)
        self.code(200)

        if url is not None:
            self.url(url)

        if check_links:
            self.check_links()

    def url(self, should_be):
        """
        Auto-prepernds ``SITE`` value to ``should_be`` value if needed.
        """
        if not should_be.startswith(self.SITE):
            should_be = self.SITE + '/' + should_be.lstrip('/')
        return self._url(should_be)
