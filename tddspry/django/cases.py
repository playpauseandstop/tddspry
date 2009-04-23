from django.conf import settings
from django.contrib.auth.models import Permission
from django.core import mail
from django.core.handlers.wsgi import WSGIHandler
from django.core.management import call_command
from django.core.servers.basehttp import AdminMediaHandler
from django.db import connection
from django.test.utils import TestSMTPConnection

from tddspry.cases import NoseTestCase, NoseTestCaseMetaclass
from tddspry.django.decorators import show_on_error

from twill import add_wsgi_intercept, commands
from twill.errors import TwillAssertionError
from twill.extensions.check_links import check_links


__all__ = ('DatabaseTestCase', 'HttpTestCase')


class BaseDatabaseTestCase(NoseTestCase):

    def setup(self, database_name=None, database_flush=None):
        """
        Creates or sets up test database name and mocks ``SMTPConnection``
        class from ``django.core.mail``.

        Additional arguments
        --------------------

        database_name
          Use ``None`` or ``':memory'`` to creates sqlite3 database in
          memory. (Default case of Django TestCases).

          Use ``':original:'`` to test in your current projects
          ``settings.DATABASE_NAME``.

          Use custom name to creates test database with current
          ``settings.DATABASE_ENGINE``.

        database_flush
          Flush database if it exists while ``True``, any changes to database
          on ``False`` and recreates it while ``None``.

          **Note:** Please, do not use ``database_flush=True``, on
          ``database_name=':original:'``, it's flushes all data in your
          original (that exists in ``settings.DATABASE_NAME``) database.

        """
        # Creates test database
        self._OLD_DATABASE_NAME = settings.DATABASE_NAME

        if database_name == ':original:':
            database_name = settings.DATABASE_NAME

            if database_flush is None:
                database_flush = False

        self._database_name = database_name or ':memory:'
        self._database_flush = database_flush

        if database_flush is not None:
            settings.DATABASE_NAME = database_name
            tables = connection.introspection.table_names()

            if not tables:
                settings.TEST_DATABASE_NAME = database_name
                self._database_name = \
                    connection.creation.create_test_db(autoclobber=True)

            if database_flush and tables:
                call_command('flush', interactive=False)
        else:
            settings.TEST_DATABASE_NAME = database_name
            self._database_name = \
                connection.creation.create_test_db(autoclobber=True)

        # Mock original SMTPConnection
        mail.original_SMTPConnection = mail.SMTPConnection
        mail.SMTPConnection = TestSMTPConnection

        mail.outbox = []

    def teardown(self):
        # Destroys test database
        if self._database_flush is None:
            connection.creation.destroy_test_db(self._database_name)

        settings.DATABASE_NAME = self._OLD_DATABASE_NAME

        # Unmock original SMTPConnection
        mail.SMTPConnection = mail.original_SMTPConnection
        del mail.original_SMTPConnection

        del mail.outbox


class BaseHttpTestCase(BaseDatabaseTestCase):

    IP = '127.0.0.1'
    PORT = 8088

    def __init__(self, *args, **kwargs):
        self.SITE = 'http://%s:%s' % (self.IP, self.PORT)
        super(BaseHttpTestCase, self).__init__(*args, **kwargs)

        for attr in commands.__all__:
            if attr in ('find', 'go', 'url'):
                name = '_' + attr
            else:
                name = attr

            setattr(self, name, getattr(commands, attr))

        setattr(self, 'check_links', check_links)

    def setup(self, *args, **kwargs):
        super(BaseHttpTestCase, self).setup(*args, **kwargs)

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
        for name, value in attrs.items():
            if 'test' in name and callable(value):
                attrs[name] = show_on_error(value)

        super_new = super(HttpTestCaseMetaclass, cls).__new__
        return super_new(cls, name, bases, attrs)


class HttpTestCase(BaseHttpTestCase):

    __metaclass__ = HttpTestCaseMetaclass

    def find(self, what, flags='', flat=False):
        """
        Twill used regexp for searching content on web-page. Use ``flat=True``
        to search content on web-page by standart Python ``what in html``
        expression.

        If this expression was not found on page it's raises
        ``TwillAssertionError`` as in ``twill.commands.find`` method.
        """
        if not flat:
            return self._find(what, flags)

        html = self.get_browser().get_html()
        if not what in html:
            raise TwillAssertionError, 'No match to %r' % what

        return True

    def go(self, url):
        """
        Twill needs to set full URL of web-page to loading. This helper
        auto-prepends ``SITE`` value if needed.
        """
        if not url.startswith(self.SITE):
            url = self.SITE + '/' + url.lstrip('/')
        return self._go(url)

    def url(self, should_be):
        """
        Helper auto-prepernds ``SITE`` value to ``should_be`` url value if
        needed.
        """
        if not should_be.startswith(self.SITE):
            should_be = self.SITE + '/' + should_be.lstrip('/')
        return self._url(should_be)
