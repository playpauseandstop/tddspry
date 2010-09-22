import httplib
import re
import warnings

try:
    from cStringIO import StringIO
except ImportError:
    from StringIO import StringIO

from urllib import addinfourl

from django.core.management import call_command
from django.core.urlresolvers import NoReverseMatch, reverse
try:
    from django.conf import settings
except ImportError:
    pass
from django.db.models import get_model
from django.utils.encoding import force_unicode
from django.utils.html import escape as real_escape

from tddspry.cases import TestCase as NoseTestCase, \
                          TestCaseMetaclass as NoseTestCaseMetaclass
from tddspry.django import helpers
from tddspry.django.decorators import django_request, show_on_error
from tddspry.django.settings import SITE, DjangoTestCase

from twill import commands
from twill.commands import browser, _parseFindFlags
from twill.errors import TwillAssertionError
from twill.extensions.check_links import check_links
from twill.utils import ResultWrapper


__all__ = ('DatabaseTestCase', 'HttpTestCase', 'TestCase')


class LoginContext(object):
    def __init__(self, testcase, username, password, url=None, formid=None):

        self.testcase = testcase
        formid = formid or 1

        self.testcase.go200(url or settings.LOGIN_URL)

        self.testcase.formvalue(formid, 'username', username)
        self.testcase.formvalue(formid, 'password', password)

        self.testcase.submit200()

        self.testcase.client.login(username=username, password=password)

    def __enter__(self):
        pass

    def __exit__(self, *args):
        self.testcase.logout()


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

        # Add ``delete``, ``get``, ``head``, ``options``, ``post``, ``put``
        # methods from Django test client to ``TestCase``
        for attr_name in ('delete', 'get', 'head', 'options', 'post', 'put'):
            attrs.update({attr_name: django_request(attr_name)})
            attrs.update({'%s200' % attr_name: django_request(attr_name, 200)})

        # Dirty hack to convert django testcase camelcase method names to
        # name with underscores
        attr_names = filter(lambda item: item.startswith('assert'),
                            dir(DjangoTestCase))

        for attr_name in attr_names:
            attrs.update({attr_name: getattr(DjangoTestCase, attr_name)})

        super_new = super(TestCaseMetaclass, cls).__new__
        return super_new(cls, name, bases, attrs)


class TestCase(DjangoTestCase, NoseTestCase):

    __metaclass__ = TestCaseMetaclass

    def activate_form(self, formid):
        """
        Set form with ``formid`` as last used by twill. This method useful if
        you got ``TwillException`` with message: ``"more than one form;
        you must select one (use 'fv') before submitting"``.

        Method supports both of numerical and string form ID.
        """
        browser = self.get_browser()
        form = browser.get_form(formid)
        browser._browser.form = form

    def assert_count(self, model_or_manager, mixed, **kwargs):
        """
        Test that number of all ``model_or_manager`` objects equals to given
        ``mixed`` value.

        You can put ``mixed`` argument as ``tuple`` or ``list`` and
        ``assert_count`` checks all of its values.

        Method supports ``using`` keyword, so you can test count objects not
        only in default database.
        """
        manager = self._get_manager(model_or_manager)
        manager, kwargs = self._process_using(manager, kwargs)

        counter = manager.count()

        try:
            manager_from_mixed = self._get_manager(mixed)
            manager_from_mixed, kwargs = \
                self._process_using(manager_from_mixed, kwargs)

            number = manager_from_mixed.count()
        except:
            number = mixed

        if isinstance(number, (list, tuple)):
            equaled = False
            numbers = number

            for number in numbers:
                if number == counter:
                    equaled = True
                    break

            if not equaled:
                assert False, '%r model has %d instance(s), not %s.' % \
                              (manager.model.__name__, counter, numbers)
        else:
            self.assert_equal(counter,
                              number,
                              '%r model has %d instance(s), not %d.' % \
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

        Method supports ``using`` keyword, so you can test create process
        not only in default database.

        .. note:: If your model contains ``using`` field, use::

               self.assert_create(model.objects.using('database'),
                                  ...
                                  using='value')

           instead of given ``using`` as keyword argument, cause::

               self.assert_create(model,
                                  ...
                                  using='value')

           will create new ``model`` object in ``default`` database.

        Method returns created ``instance`` if any.
        """
        manager = self._get_manager(model_or_manager)
        manager, kwargs = self._process_using(manager, kwargs)

        old_counter = manager.count()

        instance = manager.create(**kwargs)
        new_counter = manager.count()

        self.assert_equal(new_counter - 1,
                          old_counter,
                          'Could not create only one new %r instance. ' \
                          'New counter is %d, when old counter is %d.' % \
                          (manager.model.__name__, new_counter, old_counter))

        return instance

    def assert_delete(self, mixed, **kwargs):
        """
        Helper tries to delete ``instance`` directly or all objects from
        ``model`` or ``manager`` and checks that its correctly deleted.
        """
        instance, pk = self._get_instance_and_pk(mixed)
        manager = self._get_manager(mixed)
        manager, kwargs = self._process_using(manager, kwargs)
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

    def assert_not_count(self, model_or_manager, mixed, **kwargs):
        """
        Test that number of all ``model_or_manager`` objects not equals to
        given ``mixed`` value.

        You can put ``mixed`` argument as ``tuple`` or ``list`` and
        ``assert_count`` checks all of its values.

        Method supports ``using`` keyword, so you can test count objects not
        only in default database.
        """
        manager = self._get_manager(model_or_manager)
        manager, kwargs = self._process_using(manager, kwargs)

        counter = manager.count()

        try:
            manager_from_mixed = self._get_manager(mixed)
            manager_from_mixed, kwargs = \
                self._process_using(manager_from_mixed, kwargs)

            number = manager_from_mixed.count()
        except:
            number = mixed

        if isinstance(number, (list, tuple)):
            equaled = False
            numbers = number

            for number in numbers:
                if number == counter:
                    equaled = True
                    break

            if equaled:
                assert False, '%r model has %d instance(s), but should not.' %\
                              (manager.model.__name__, counter)
        else:
            self.assert_not_equal(counter,
                                  number,
                                  '%r model has %d instance(s), but should ' \
                                  'not.' % (manager.model.__name__, number))

    def assert_not_read(self, model_or_manager, query_=None, **kwargs):
        """
        Helper filters ``model_or_manager`` instance by ``query`` or
        ``**kwargs`` lookup and check for empty ``QuerySet``.

        Method support ``using`` keyword so you can test unread models not only
        for default database.
        """
        manager = self._get_manager(model_or_manager)
        manager, kwargs = self._process_using(manager, kwargs)

        if query_:
            queryset = manager.filter(query_)
        else:
            queryset = manager.filter(**kwargs)

        count = queryset.count()

        if count != 0:
            assert False, '%d %s objects exist by %r lookup.' % \
                          (count, manager.model.__name__, query_ or kwargs)

        return True

    def assert_not_unicode(self, first, second, message=None):
        """
        Test that ``first`` and ``second`` after converting with
        ``django.utils.encoding.force_unicode`` function are not equal.
        """
        return self.assert_not_equal(force_unicode(first),
                                     force_unicode(second),
                                     message)

    def assert_read(self, model_or_manager, query_=None, **kwargs):
        """
        Helper filters ``model_or_manager`` instance by ``query`` or
        ``**kwargs`` lookup and checks for valid ``QuerySet``.

        Method returns ``QuerySet`` with filtered instances or simple model
        instance if resulted ``QuerySet`` is only one.

        Method supports ``using`` keyword so you can test read models not only
        from default database.
        """
        manager = self._get_manager(model_or_manager)
        manager, kwargs = self._process_using(manager, kwargs)

        if query_:
            queryset = manager.filter(query_)
        else:
            queryset = manager.filter(**kwargs)

        count = queryset.count()

        if count == 0:
            assert False, 'Could not filter %r objects by %s lookup.' % \
                          (manager.model.__name__, query_ or kwargs)

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

        Method supports ``using`` keyword so you can test update models not
        only for default database.
        """
        instance, pk = self._get_instance_and_pk(mixed)
        manager = self._get_manager(mixed)
        manager, kwargs = self._process_using(manager, kwargs)

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

    def deactivate_form(self):
        """
        Reset last selected form by Twill.
        """
        self.get_browser()._browser.form = None

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

    def find(self, what, flags='', flat=False, count=None, escape=False):
        """
        Twill used regexp for searching content on web-page. Use ``flat=True``
        to search content on web-page by standart Python ``what in html``
        expression.

        If this expression was not True (was not found on page) it's raises
        ``TwillAssertionError`` as in ``twill.commands.find`` method.

        Specify ``count`` to test that ``what`` occurs ``count`` times in the
        content of the web-page.

        You could escape ``what`` text by standart ``django.utils.html.escape``
        function if call method with ``escape=True``, like::

            self.find('Text with "quotes"', escape=True)

        """
        if escape:
            what = real_escape(what)

        if not flat and not count:
            return self._find(what, flags)

        html = self.get_browser().get_html()
        real_count = html.count(what)

        if count is not None and count != real_count:
            raise TwillAssertionError('Matched to %r %d times, not %d ' \
                                      'times.' % (what, real_count, count))
        elif real_count == 0:
            raise TwillAssertionError('No match to %r' % what)

        return True

    def find_in(self, what, where, flags='', flat=False, count=None,
                escape=False):
        """
        Alternate version of ``find`` method that allow to find text in another
        text, not only in current loaded page.

        ``find_in`` supports all keywords from original ``find`` method.

        If ``what`` not found in ``where``, ``find_in`` raises
        ``TwillAssertionError``.
        """
        if escape:
            what = real_escape(what)

        if not flat and not count:
            regexp = re.compile(what, _parseFindFlags(flags))

            if not regexp.search(where):
                self.text_to_twill(where)
                raise TwillAssertionError('No match to %r' % what)

            return True

        real_count = where.count(what)

        if count is not None and count != real_count:
            self.text_to_twill(where)
            raise TwillAssertionError('Matched to %r %d times, not %d ' \
                                      'times.' % (what, real_count, count))
        elif real_count == 0:
            self.text_to_twill(where)
            raise TwillAssertionError('No match to %r' % what)

        return True

    def find_url(self, url, args=None, kwargs=None, prepend=False, flags='',
                 flat=False, count=None, escape=False):
        """
        Helper method to build url and find it on current web-page.

        ::

            self.find_url('index')

        equals to::

            self.find(self.build_url('index'))

        You should use all of ``build_url`` and ``find`` keyword arguments,
        like ``args`` for ``build_url`` or ``count`` for ``find``.
        """
        return self.find(self.build_url(url, args, kwargs, prepend),
                         flags=flags,
                         flat=flat,
                         count=count,
                         escape=escape)

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

        Also login to Django test client.
        """
        return LoginContext(self, username, password, url, formid)

    def login_to_admin(self, username, password):
        """
        Login to Django admin CRUD using ``username`` and ``password``.

        Also login to Django test client.
        """
        self.go200('/admin/')

        self.formvalue(1, 'username', username)
        self.formvalue(1, 'password', password)

        self.submit200()
        self.notfind('<input type="hidden" name="this_is_the_login_form" ' \
                     'value="1" />')

        self.client.login(username=username, password=password)

    def logout(self, url=None):
        """
        Logout from current Django session.

        Also logout from Django test client.
        """
        self.go200(url or 'auth_logout')
        self.client.logout()

    def notfind(self, what, flags='', flat=False, escape=False):
        """
        Twill used regexp for searching content on web-page. Use ``flat=True``
        to search content on web-page by standart Python ``not what in html``
        expression.

        If this expression was not True (was found on page) it's raises
        ``TwillAssertionError`` as in ``twill.commands.notfind`` method.

        You could escape ``what`` text by standart ``django.utils.html.escape``
        function if call method with ``escape=True``, like::

            self.notfind('Text with "quotes"', escape=True)

        """
        if escape:
            what = real_escape(what)

        if not flat:
            return self._notfind(what, flags)

        html = self.get_browser().get_html()
        if what in html:
            raise TwillAssertionError('Match to %r' % what)

        return True

    def notfind_in(self, what, where, flags='', flat=False, escape=False):
        """
        Alternate version of ``notfind`` method that allow to check that text
        not found in another text, not only in current loaded page.

        ``notfind_in`` supports all keywords from original ``notfind`` method.

        If ``what`` found in ``where``, ``notfind_in`` raises
        ``TwillAssertionError``.
        """
        found = False

        if escape:
            what = real_escape(what)

        if flat and what in where:
            found = True
        elif not flat:
            regexp = re.compile(what, _parseFindFlags(flags))
            if regexp.search(where):
                found = True

        if found:
            self.text_to_twill(where)
            raise TwillAssertionError('Match to %r' % what)

        return True

    def notfind_url(self, url, args=None, kwargs=None, prepend=False, flags='',
                    flat=False, escape=False):
        """
        Helper method to build url and not find it on current web-page.

        ::

            self.notfind_url('index')

        equals to::

            self.notfind(self.build_url('index'))

        You should use all of ``build_url`` and ``notfind`` keyword arguments,
        like ``args`` for ``build_url`` or ``flat`` for ``notfind``.
        """
        return self.notfind(self.build_url(url, args, kwargs, prepend),
                            flags=flags,
                            flat=flat,
                            escape=escape)

    def response_to_twill(self, response):
        """
        Wrap Django response to work with Twill.
        """
        path = response.request.get('PATH_INFO')
        url = path and SITE + path.lstrip('/') or path

        headers_msg = '\n'.join('%s: %s' % (k, v) for k, v in response.items())
        headers_msg = StringIO(headers_msg)
        headers = httplib.HTTPMessage(headers_msg)

        io_response = StringIO(response.content)
        urllib_response = addinfourl(io_response,
                                     headers,
                                     url,
                                     response.status_code)
        urllib_response._headers = headers
        urllib_response._url = url
        urllib_response.msg = u'OK'
        urllib_response.seek = urllib_response.fp.seek

        browser._browser._factory.set_response(urllib_response)
        browser.result = ResultWrapper(response.status_code,
                                       url,
                                       response.content)

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

    def text_to_twill(self, text):
        """
        Wrap text to work with Twill.
        """
        headers_msg = 'Content: text-plain; encoding=utf-8\n'
        headers_msg = StringIO(headers_msg)
        headers = httplib.HTTPMessage(headers_msg)

        status_code = 200
        url = 'text://'

        io_response = StringIO(text)
        urllib_response = addinfourl(io_response,
                                     headers,
                                     url,
                                     status_code)
        urllib_response._headers = headers
        urllib_response._url = url
        urllib_response.msg = u'OK'
        urllib_response.seek = urllib_response.fp.seek

        browser._browser._factory.set_response(urllib_response)
        browser.result = ResultWrapper(status_code, url, text)

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

    def _process_using(self, manager, kwargs):
        """
        Utility function to check if model of manager has ``using`` field and
        if not use it as arg for ``manager.using`` function.
        """
        if 'using' in kwargs:
            model = manager.model

            all_fields = model._meta.fields + model._meta.many_to_many
            found = False

            for field in all_fields:
                if field.name == 'using':
                    found = True
                    break

            if not found:
                using = kwargs.pop('using')
                return (manager.using(using), kwargs)

        return (manager, kwargs)


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
