from django.conf import settings
from django.core import mail
from django.core.handlers.wsgi import WSGIHandler
from django.core.management import call_command
from django.core.servers.basehttp import AdminMediaHandler
from django.core.urlresolvers import NoReverseMatch, reverse
from django.db import connection
from django.test import Client
from django.test.utils import TestSMTPConnection

from tddspry.cases import NoseTestCase, NoseTestCaseMetaclass
from tddspry.django import helpers
from tddspry.django.decorators import show_on_error
from tddspry.django.utils import db_exists, flush

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
      Flush database if it exists while ``True`` and any changes to database on
      ``False``.

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
        create_test_db = True

        settings.original_DATABASE_ENGINE = settings.DATABASE_ENGINE
        settings.original_DATABASE_NAME = settings.DATABASE_NAME

        if self.database_name is None or self.database_name == ':memory:':
            # Closes current database connection and changes
            # ``DATABASE_ENGINE`` to ``'sqlite3'``
            connection.close()
            settings.DATABASE_ENGINE = 'sqlite3'

            settings.TEST_DATABASE_NAME = ':memory:'

            # Flushes in-memory database if it exists
            if db_exists(settings.TEST_DATABASE_NAME):
                flush()
        elif self.database_name == ':original:':
            # Disable database flush by default
            if self.database_flush is None:
                self.database_flush = False

            self.database_name = settings.DATABASE_NAME
            settings.TEST_DATABASE_NAME = settings.DATABASE_NAME

            # If original database not exist - tries to create it
            if db_exists(self.database_name):
                create_test_db = False
        else:
            settings.TEST_DATABASE_NAME = self.database_name

            # Do not re-creates tests database if it exists on
            # ``database_flush == False``
            if self.database_flush == False and \
               db_exists(self.database_name):
                create_test_db = False

        if create_test_db:
            self.database_name = \
                connection.creation.create_test_db(autoclobber=True)

        tables = connection.introspection.table_names()

        if self.database_flush and tables:
            call_command('flush', interactive=False)

        # Load data from fixtures
        if self.fixtures:
            call_command('loaddata', *self.fixtures)

        # Mock original SMTPConnection
        mail.original_SMTPConnection = mail.SMTPConnection
        mail.SMTPConnection = TestSMTPConnection

        mail.outbox = []

    def helper(self, name, *args, **kwargs):
        return getattr(helpers, name)(self, *args, **kwargs)

    def _get_helpers(self):
        return helpers
    helpers = property(_get_helpers)

    def teardown(self):
        # Destroys test database
        if self.database_name == ':memory:' and self.database_flush != False:
            flush()

        if self.database_name != settings.original_DATABASE_NAME and \
           self.database_flush != False:
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

    def __init__(self):
        super(BaseHttpTestCase, self).__init__()
        self.SITE = 'http://%s:%s/' % (self.IP, self.PORT)

    def setup(self):
        super(BaseHttpTestCase, self).setup()

        app = AdminMediaHandler(WSGIHandler())
        add_wsgi_intercept(self.IP, self.PORT, lambda: app)

    def build_url(self, url, args=None, kwargs=None, prepend=False):
        """
        Helper reverses ``url`` if possible and auto-prepends ``SITE`` to
        it if ``prepend=True``.
        """
        if url.startswith(self.SITE):
            return url

        try:
            url = reverse(url, args=args or [], kwargs=kwargs or {})
        except NoReverseMatch:
            pass

        if not prepend:
            return url

        return self.SITE + url.lstrip('/')

    def disable_edit_hidden_fields(self):
        """
        Disable editing hidden fields (``<input type="hidden" ... />``) by
        Twill browser (as by default in twill).

        To enable use ``HttpTestCase.enable_edit_hidden_fields`` method.
        """
        self.enable_edit_hidden_fields(False)

    def disable_redirect(self):
        """
        Disable auto-redirects in Twill tests.

        To enable use ``HttpTestCase.enable_redirect`` method.
        """
        self.enable_redirect(False)

    def enable_edit_hidden_fields(self, flag=True):
        """
        Enable editing hidden fields (``<input type="hidden" ... />``) by
        Twill browser.

        To disable use ``HttpTestCase.disable_edit_hidden_fields`` method.
        """
        self.config('readonly_controls_writeable', flag)

    def enable_redirect(self, flag=True):
        """
        Enable auto-redirects in Twill tests (as by default in twill).

        To disable use ``HttpTestCase.disable_redirect`` method.
        """
        self.config('acknowledge_equiv_refresh', int(flag))


class DatabaseTestCase(BaseDatabaseTestCase):

    def assert_count(self, model, number):
        """
        Helper counts all ``model`` objects and ``assert_equals`` it with given
        ``number``.

        Also you can to put ``number`` argument as ``tuple`` and ``list`` and
        ``assert_count`` checks all of its values.
        """
        counter = model.objects.count()

        if isinstance(number, (list, tuple)):
            equaled = False
            numbers = number

            for number in numbers:
                if number == counter:
                    equaled = True
                    break

            if not equaled:
                assert False, '%r model has %d instance(s), not %s' % (
                                  model.__name__, counter, numbers,
                              )
        else:
            self.assert_equal(counter,
                              number,
                              '%r model has %d instance(s), not %d' % (
                                  model.__name__, counter, number,
                              ))

    def assert_create(self, model, **kwargs):
        """
        Helper tries to create new ``instance`` of ``model`` class with given
        ``**kwargs`` and checks that ``instance`` really created.

        ``assert_create`` returns created ``instance``.
        """
        old_counter = model.objects.count()

        instance = model.objects.create(**kwargs)
        new_counter = model.objects.count()

        self.assert_equal(new_counter - 1,
                          old_counter,
                          'Could not to create only one new %r instance. ' \
                          'New counter is %d, when old counter is %d.' % (
                              model.__name__, new_counter, old_counter,
                          ))

        return instance

    def assert_delete(self, instance):
        """
        Helper tries to delete ``instance`` and checks that it correctly
        deleted.
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
                              model.__name__, new_counter, old_counter,
                          ))

        try:
            model.objects.get(pk=pk)
        except model.DoesNotExist:
            pass
        else:
            assert False, 'Could not to delete %r instance with %d pk.' % (
                model.__name__, pk,
            )

    def assert_read(self, model, **kwargs):
        """
        Helper tries to filter ``model`` instances by ``**kwargs`` lookup.

        ``assert_read`` returns QuerySet with filtered instances or simple
        instance if resulted QuerySet count is ``1``.
        """
        queryset = model.objects.filter(**kwargs)
        count = queryset.count()

        if count == 0:
            assert False, 'Could not to filter %r objects by %s lookup.' % (
                              model.__name__, kwargs,
                          )

        if count == 1:
            return queryset[0]

        return queryset

    def assert_update(self, instance, **kwargs):
        """
        Helper tries to update given ``instance`` with ``**kwargs`` and checks
        that all of ``**kwargs`` values was correctly saved to ``instance``.

        ``assert_update`` returns updated ``instance``.
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
        for attr_name, attr_value in attrs.items():
            if 'test' in attr_name and callable(attr_value):
                attrs[attr_name] = show_on_error(attr_value, clsname=name)

        for attr in commands.__all__:
            if attr in ('find', 'go', 'notfind', 'url'):
                attr_name = '_' + attr
            else:
                attr_name = attr

            attrs.update({attr_name: staticmethod(getattr(commands, attr))})

        attrs.update({'check_links': staticmethod(check_links)})

        super_new = super(HttpTestCaseMetaclass, cls).__new__
        return super_new(cls, name, bases, attrs)


class HttpTestCase(BaseHttpTestCase):

    __metaclass__ = HttpTestCaseMetaclass

    def _get_client(self):
        if not hasattr(self, '__client'):
            setattr(self, '__client', Client())
        return getattr(self, '__client')
    client = property(_get_client)

    def find(self, what, flags='', flat=False):
        """
        Twill used regexp for searching content on web-page. Use ``flat=True``
        to search content on web-page by standart Python ``what in html``
        expression.

        If this expression was not True (was not found on page) it's raises
        ``TwillAssertionError`` as in ``twill.commands.find`` method.
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
        url = self.build_url(url, args, kwargs, True)
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

        self.go200(url or 'auth_login')

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

    def url(self, url, args=None, kwargs=None):
        """
        Assert that current URL matches the given regexp.
        """
        should_be = self.build_url(url, args, kwargs, True)
        return self._url(should_be)
