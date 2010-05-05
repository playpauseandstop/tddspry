import warnings

from django.core.management import call_command
from django.core.urlresolvers import NoReverseMatch, reverse
from django.db.models import get_model
from django.utils.encoding import force_unicode

from tddspry.cases import TestCase as NoseTestCase, \
                          TestCaseMetaclass as NoseTestCaseMetaclass
from tddspry.django import helpers
from tddspry.django.decorators import show_on_error
from tddspry.django.settings import SITE, DjangoTestCase

from twill import commands
from twill.errors import TwillAssertionError
from twill.extensions.check_links import check_links


__all__ = ('DatabaseTestCase', 'HttpTestCase', 'TestCase')


class TestCaseMetaclass(NoseTestCaseMetaclass):

    def __new__(cls, name, bases, attrs):
        for attr_name, attr_value in attrs.items():
            if 'test' in attr_name and callable(attr_value):
                attrs[attr_name] = show_on_error(attr_value, clsname=name)

            # Add nose styled names of setup and teardown methods to cls attrs
            if attr_name == 'setup' and not 'setUp' in attrs:
                attrs['setUp'] = attr_value

            if attr_name == 'teardown' and not 'tearDown' in attrs:
                attrs['tearDown'] = attr_value

        # Add twill commands to testcase as staticmethods
        for attr in commands.__all__:
            if attr in ('find', 'go', 'notfind', 'run', 'url'):
                attr_name = '_' + attr
            else:
                attr_name = attr

            attrs.update({attr_name: staticmethod(getattr(commands, attr))})

        attrs.update({'call_command': staticmethod(call_command)})
        attrs.update({'check_links': staticmethod(check_links)})

        # Dirty hack to convert django testcase camelcase method names to
        # name with underscores
        attr_names = filter(lambda item: item.startswith('assert'),
                            dir(DjangoTestCase))

        for attr_name in attr_names:
            attrs.update({attr_name: getattr(DjangoTestCase, attr_name)})

        super_new = super(TestCaseMetaclass, cls).__new__
        return super_new(cls, name, bases, attrs)


class TestCase(NoseTestCase, DjangoTestCase):

    __metaclass__ = TestCaseMetaclass

    def assert_count(self, model_or_manager, number):
        """
        Helper counts all ``model_or_manager`` objects and ``assert_equal`` it
        with given ``number``.

        Also you can to put ``number`` argument as ``tuple`` and ``list`` and
        ``assert_count`` checks all of its values.
        """
        manager = self._get_manager(model_or_manager)
        counter = manager.count()

        if isinstance(number, (list, tuple)):
            equaled = False
            numbers = number

            for number in numbers:
                if number == counter:
                    equaled = True
                    break

            if not equaled:
                assert False, '%r model has %d instance(s), not %s' % \
                              (manager.model.__name__, counter, numbers)
        else:
            self.assert_equal(counter,
                              number,
                              '%r model has %d instance(s), not %d' % \
                              (manager.model.__name__, counter, number))

    def assert_contains_count(self, text, count):
        """
        Asserts that ``text`` occuts on current Twill page ``count`` times.

        Else ``TwillAssertionError`` raises.
        """
        return self.find(text, count=count)

    def assert_create(self, model_or_manager, **kwargs):
        """
        Helper tries to create new ``instance`` for ``model_or_manager`` class
        with given ``**kwargs`` and checks that ``instance`` really created.

        Method returns created ``instance`` if any.
        """
        manager = self._get_manager(model_or_manager)
        old_counter = manager.count()

        instance = manager.create(**kwargs)
        new_counter = manager.count()

        self.assert_equal(new_counter - 1,
                          old_counter,
                          'Could not create only one new %r instance. ' \
                          'New counter is %d, when old counter is %d.' % \
                          (manager.model.__name__, new_counter, old_counter))

        return instance

    def assert_delete(self, mixed):
        """
        Helper tries to delete ``instance`` directly or all objects from
        ``model`` or ``manager`` and checks that its correctly deleted.
        """
        instance, pk = self._get_instance_and_pk(mixed)
        manager = self._get_manager(mixed)
        old_counter = manager.count()

        if pk:
            diff = 1
            instance.delete()
            message = 'Could not delete only one %r instance. New counter is '\
                      '%d, when old counter is %d.'
        else:
            diff = manager.count()
            manager.all().delete()
            message = 'Could not delete all instances of %r model. New ' \
                      'counter is %d, when old counter is %d.'

        new_counter = manager.count()
        message = message % (manager.model.__name__, new_counter, old_counter)

        self.assert_equal(new_counter + diff, old_counter, message)

        if pk:
            try:
                manager.get(pk=pk)
            except manager.model.DoesNotExist:
                pass
            else:
                assert False, 'Could not delete %r instance with %d pk.' % \
                               (manager.model.__name__, pk)

    def assert_read(self, model_or_manager, **kwargs):
        """
        Helper tries to filter ``model_or_manager`` instance by ``**kwargs``
        lookup.

        ``assert_read`` returns QuerySet with filtered instances or simple
        instance if resulted QuerySet count is ``1``.
        """
        manager = self._get_manager(model_or_manager)

        queryset = manager.filter(**kwargs)
        count = queryset.count()

        if count == 0:
            assert False, 'Could not filter %r objects by %s lookup.' % \
                          (manager.model.__name__, kwargs)

        if count == 1:
            return queryset[0]

        return queryset

    def assert_unicode(self, first, second, message=None):
        """
        Use ``django.utils.encoding.force_unicode`` to ``first`` and ``second``
        function args.
        """
        return self.assert_equal(force_unicode(first),
                                 force_unicode(second),
                                 message)

    def assert_update(self, mixed, **kwargs):
        """
        Helper tries to update given model instance with ``**kwargs`` and
        checks that all of ``**kwargs`` values was correctly saved to given
        instance. In this case ``assert_update`` returns update instance.

        Also you can update all model class or manager instances with
        QuerySet's ``update`` method and check for these updates.
        """
        instance, pk = self._get_instance_and_pk(mixed)
        manager = self._get_manager(mixed)

        if pk:
            for name, value in kwargs.items():
                setattr(instance, name, value)
            instance.save()

            instance = manager.get(pk=pk)

            for name, value in kwargs.items():
                self.assert_equal(getattr(instance, name),
                                  value,
                                  'Could not update %r field.' % name)

            return instance

        manager.update(**kwargs)
        return self.assert_read(manager, **kwargs)

    def build_url(self, url, args=None, kwargs=None, prepend=False):
        """
        Helper reverses ``url`` if possible and auto-prepends ``SITE`` to
        it if ``prepend=True``.
        """
        if hasattr(url, 'get_absolute_url'):
            url = url.get_absolute_url()

        if url.startswith(SITE):
            return url

        try:
            url = reverse(url, args=args or [], kwargs=kwargs or {})
        except NoReverseMatch:
            pass

        if not prepend:
            return url

        return SITE + url.lstrip('/')

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

    def find(self, what, flags='', flat=False, count=None):
        """
        Twill used regexp for searching content on web-page. Use ``flat=True``
        to search content on web-page by standart Python ``what in html``
        expression.

        If this expression was not True (was not found on page) it's raises
        ``TwillAssertionError`` as in ``twill.commands.find`` method.
        """
        if not flat and not count:
            return self._find(what, flags)

        html = self.get_browser().get_html()
        real_count = html.count(what)

        if count is not None and count != real_count:
            raise TwillAssertionError('Matched to %r %d times, not %d ' \
                                      'times.' % (what, real_count, count))
        elif real_count == 0:
            raise TwillAssertionError, 'No match to %r' % what

        return True

    def follow200(self, what, url=None, args=None, kwargs=None,
                  check_links=False):
        """
        Find the first matching link on the page, visit it and check that
        response code is 200.

        If ``url`` is set function checks to make sure that the current URL
        matches the given regexp or urlpattern.

        If ``check_links`` is set function checks links on current page.
        """
        self.follow(what)
        self.code(200)

        if url:
            self.url(url, args, kwargs)

        if check_links:
            self.check_links()

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

    def helper(self, name, *args, **kwargs):
        return getattr(helpers, name)(self, *args, **kwargs)

    def _get_helpers(self):
        return helpers
    helpers = property(_get_helpers)

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

    def url(self, url, args=None, kwargs=None, regexp=True):
        """
        Assert that current URL matches the given regexp.

        If ``regexp`` is set function appends '$' to the regexp end if needed.
        """
        should_be = self.build_url(url, args, kwargs, True)

        if regexp and should_be[-1] != '$':
            should_be += '$'

        return self._url(should_be)

    def _get_instance_and_pk(self, mixed):
        """
        Utility function to return tuple contains of models instance and its pk
        if possible.
        """
        instance, pk = None, None

        if hasattr(mixed, 'pk') and not isinstance(mixed.pk, property):
            instance, pk = mixed, mixed.pk

        return (instance, pk)

    def _get_manager(self, model_or_manager):
        """
        Utility function to return default manager from model or instance
        object or given manager.
        """
        if isinstance(model_or_manager, basestring):
            app, model = model_or_manager.split('.')
            model_or_manager = get_model(app, model)

        if hasattr(model_or_manager, '_default_manager'):
            return model_or_manager._default_manager

        return model_or_manager


class DatabaseTestCase(TestCase):

    def __init__(self, *args, **kwargs):
        super(DatabaseTestCase, self).__init__(*args, **kwargs)
        self._warning_message = \
            'Calling super for ``%s()`` method is deprecated. ' \
            '``tddspry.django.TestCase`` class does not need this anymore.'

    def setup(self):
        warnings.warn(self._warning_message % 'setup', DeprecationWarning)

    def teardown(self):
        warnings.warn(self._warning_message % 'teardown', DeprecationWarning)


HttpTestCase = DatabaseTestCase
