import os
import re
import shutil

from tddspry.django import HttpTestCase, TestCase
from tddspry.django.decorators import show_on_error
from tddspry.django.helpers import PASSWORD, USERNAME

from django.conf import settings
from django.contrib.auth.models import User

from twill.errors import TwillAssertionError, TwillException

from testproject.testapp.forms import LoginForm
from testproject.testapp.models import UserProfile


TEST_BIO = 'Something text %d'
TEST_POST_DATA = {
    'hidden_field_1': 'first hidden value',
    'hidden_field_2': 'second hidden value',
    'some_field_1': 'first some value',
    'some_field_2': 'second some value',
}


@show_on_error
def dummy_error(obj):
    obj.go('/does_not_exist/')
    obj.code(200)


@show_on_error
def dummy_field_error(obj):
    obj.go200('edit_hidden_fields')
    obj.fv(1, 'does_not_exist', 'Something')


class TestHttp(TestCase):

    def test_activate_form(self):
        self.go200('multiply_forms')

        self.notfind('First form was submitted.')
        self.notfind('Second form was submitted.')

        self.activate_form(1)
        self.submit200(url='multiply_forms')

        self.find('First form was submitted.')
        self.notfind('Second form was submitted.')

        self.activate_form(2)
        self.submit200(url='multiply_forms')

        self.notfind('First form was submitted.')
        self.find('Second form was submitted.')

        self.activate_form('first-form')
        self.submit200(url='multiply_forms')

        self.find('First form was submitted.')
        self.notfind('Second form was submitted.')

        self.activate_form('second-form')
        self.submit200(url='multiply_forms')

        self.notfind('First form was submitted.')
        self.find('Second form was submitted.')

    @TestCase.raises(TwillException)
    def test_activate_form_error(self):
        self.go200('multiply_forms')
        self.submit200(url='multiply_forms')

    def test_assert_contains_count(self):
        self.go200('index')

        self.assert_contains_count('Index', 1)
        self.assert_contains_count('python', 2)

        self.find('Index', count=1)
        self.find('python', count=2)

    @TestCase.raises(TwillAssertionError)
    def test_assert_contains_count_error(self):
        self.go200('index')
        self.assert_contains_count('python', 3)

    def test_build_url(self):
        user = self.helper('create_user')
        profile = self.helper('create_profile', user, UserProfile)

        self.assert_equal(self.build_url('index'), '/')
        self.assert_equal(self.build_url('user', args=[user.username]),
                          '/user/' + user.username + '/')
        self.assert_equal(self.build_url('user',
                                         kwargs={'username': user.username}),
                          '/user/' + user.username + '/')
        self.assert_equal(self.build_url(profile),
                          '/user/' + user.username + '/')

    def test_client(self):
        # ``GET`` request
        response = self.client.get('/')
        self.assert_equal(response.status_code, 200)

        # ``POST`` request
        response = self.client.post('/edit-hidden-fields/', TEST_POST_DATA)
        self.assert_equal(response.status_code, 200)

    @TestCase.raises(TwillException)
    def test_deactivate_form(self):
        self.go200('multiply_forms')

        self.activate_form(1)
        self.deactivate_form()

        self.submit200(url='multiply_forms')

    def test_get(self):
        self.get('/')
        self.code(200)
        self.url('/')

        self.find('Index')
        self.find('c++ is good, but python - better ;)', flat=True)

        self.get(settings.MEDIA_URL + 'does_not_exist.exe')
        self.code(404)

    def test_get_and_twill(self):
        self.get('/')
        self.code(200)
        self.url('/')

        self.find('Index')
        self.find('c++ is good, but python - better ;)', flat=True)

        self.go(settings.MEDIA_URL + 'does_not_exist.exe')
        self.code(404)

        self.go200('edit_hidden_fields')
        self.url('edit_hidden_fields')

        self.find('Form contains hidden fields')

    def test_get_and_forms(self):
        self.get('edit_hidden_fields')
        self.code(200)
        self.url('edit_hidden_fields')

        self.notfind(TEST_POST_DATA['some_field_1'])
        self.notfind(TEST_POST_DATA['some_field_2'])

        self.fv(1, 'some_field_1', TEST_POST_DATA['some_field_1'])
        self.fv(1, 'some_field_2', TEST_POST_DATA['some_field_2'])

        self.submit200(url='edit_hidden_fields')

        self.find(TEST_POST_DATA['some_field_1'])
        self.find(TEST_POST_DATA['some_field_2'])

    def test_get200(self):
        self.get200('/')
        self.url('/')

        self.find('Index')
        self.find('c++ is good, but python - better ;)', flat=True)

    @TestCase.raises(TwillAssertionError)
    def test_get200_assertion(self):
        self.get200(settings.MEDIA_URL + 'does_not_exist.exe')

    def test_edit_hidden_fields(self):
        self.enable_edit_hidden_fields()
        url = self.build_url('edit_hidden_fields')

        self.go200(url)

        self.formvalue(1, 'hidden_field_1', 'Value')
        self.formvalue(1, 'hidden_field_2', 'Value')
        self.formvalue(1, 'some_field_1', 'Value')

        self.submit200(url=url + '$')

        self.find("hidden_field_1: 'Value'")
        self.find("hidden_field_2: 'Value'")
        self.find("some_field_1: 'Value'")

        self.disable_edit_hidden_fields()

        self.go200(url)

        self.formvalue(1, 'hidden_field_1', 'Value')
        self.formvalue(1, 'hidden_field_2', 'Value')
        self.formvalue(1, 'some_field_1', 'Value')

        self.submit200(url=url + '$')

        self.find("hidden_field_1: ''")
        self.notfind("hidden_field_1: 'Value'")
        self.find("hidden_field_2: ''")
        self.notfind("hidden_field_2: 'Value'")
        self.find("some_field_1: 'Value'")

    @TestCase.raises(TwillException)
    def test_field_error(self):
        self.go200('edit_hidden_fields')
        self.fv(1, 'does_not_exist', 'does_not_exist')

    @TestCase.raises(TwillAssertionError)
    def test_find_count_error(self):
        self.go200('index')
        self.find('python', count=3)

    def test_find_escape(self):
        self.go200('index')
        self.find('Text in "invalid" quotes.', escape=True)

    @TestCase.raises(TwillAssertionError)
    def test_find_escape_error(self):
        self.go200('index')
        self.find('Text in "valid" quotes.', escape=True)

    @TestCase.raises(TwillAssertionError)
    def test_find_flat_error(self):
        self.go200('index')
        self.find('Impossible', flat=True)

    def test_find_in(self):
        self.find_in('Text', 'Text in "valid" quotes')

    def test_find_in_count(self):
        self.find_in('in', 'Text in "invalid" quotes', count=2)

    @TestCase.raises(TwillAssertionError)
    def test_find_in_count_error(self):
        self.find_in('Text', 'Text in "valid" quotes', count=2)

    @TestCase.raises(TwillAssertionError)
    def test_find_in_error(self):
        self.find_in('invalid', 'Text in "valid" quotes')

    def test_find_in_escape(self):
        self.find_in('"valid"',
                     'Text in &quot;valid&quot; quotes',
                     escape=True)

    @TestCase.raises(TwillAssertionError)
    def test_find_in_escape_error(self):
        self.find_in('"invalid"', 'Text in "invalid" quotes', escape=True)

    def test_find_in_flags(self):
        self.find_in('text', 'Text in "valid" quotes', flags='i')

    @TestCase.raises(TwillAssertionError)
    def test_find_in_flags_error(self):
        self.find_in('text', 'Text in "valid" quotes', flags='s')

    def test_find_in_flat(self):
        self.find_in('c++', 'c++ is good, but python is better', flat=True)

    @TestCase.raises(TwillAssertionError)
    def test_find_in_flat_error(self):
        self.find_in('c++', 'python is great, but erlang is faster', flat=True)

    def test_find_in_with_find(self):
        self.go200('index')
        self.find('c++', flat=True)
        self.find_in('c++', 'c++ is good, but python is better', flat=True)
        self.find('Text in "valid" quotes')
        self.find('Text in "invalid" quotes', escape=True)

    def test_find_url(self):
        self.go200('index')
        self.find_url('edit_hidden_fields')

    def test_find_url_count(self):
        self.go200('index')
        self.find_url('edit_hidden_fields', count=1)

    @TwillAssertionError
    def test_find_url_count_error(self):
        self.go200('index')
        self.find_url('edit_hidden_fields', count=2)

    @TestCase.raises(TwillAssertionError)
    def test_find_url_not_found(self):
        self.go200('index')
        self.find_url('auth_login')

    def test_form_id_for_form_functions(self):
        self.enable_edit_hidden_fields()
        self.go200('edit_hidden_fields')

        for key, value in TEST_POST_DATA.items():
            self.fv('hidden-fields-form', key, value)

        self.submit200(url='edit_hidden_fields')

        for key, value in TEST_POST_DATA.items():
            self.find("%s: '%s'" % (key, value))

        self.disable_edit_hidden_fields()

    @TestCase.raises(TwillAssertionError)
    def test_form_id_for_form_functions_error(self):
        self.go200('edit_hidden_fields')
        self.fv('not-hidden-fields-form',
                'some_field_1',
                TEST_POST_DATA['some_field_1'])

    def test_follow200(self):
        self.go200('/')

        self.follow('Edit hidden fields')
        self.code(200)
        self.url('edit_hidden_fields')

        self.go200('/')
        self.follow200('Edit hidden fields', url='edit_hidden_fields')

    def test_index(self):
        self.go200('/')
        self.url('/')

        self.find('Index')
        self.find('c++ is good, but python - better ;)', flat=True)

        try:
            self.notfind('c++ is good, but python - better ;)')
        except re.error:
            pass

        try:
            self.notfind('c++ is good, but python - better ;)', flat=True)
        except TwillAssertionError:
            pass

    def test_login(self):
        self.go200('/profile/')
        self.url('/login/\?next=/profile/')

        user = self.helper('create_user')
        self.login(USERNAME, PASSWORD)

        self.go200('/profile/')
        self.find(user.username)
        self.find(user.email)

    def test_login_context(self):
        self.go200('/profile/')
        self.url('/login/\?next=/profile/')

        user = self.helper('create_user')
        with self.login(USERNAME, PASSWORD):
            self.go200('/profile/')
            self.find(user.username)
            self.find(user.email)

        self.go200('/profile/')
        self.url('/login/\?next=/profile/')

    def test_login_and_get(self):
        user = self.helper('create_user')
        self.login(USERNAME, PASSWORD)

        self.get200('/profile/')
        self.find(user.username)
        self.find(user.email)

    def test_login_to_admin_staff(self):
        staff = self.helper('create_staff')
        self.login_to_admin(USERNAME, PASSWORD)

    def test_login_to_admin_superuser(self):
        superuser = self.helper('create_superuser')
        self.login_to_admin(USERNAME, PASSWORD)

        self.go200('/admin/testapp/userprofile/')
        self.find('Testapp')
        self.find('User profiles')
        self.find('Add user profile')

    @TestCase.raises(TwillAssertionError)
    def test_login_to_admin_regular_user(self):
        user = self.helper('create_user')
        self.login_to_admin(USERNAME, PASSWORD)

    def test_logout(self):
        user = self.helper('create_user')
        self.login(USERNAME, PASSWORD)

        self.go200('/profile/')
        self.find(user.username)
        self.find(user.email)

        self.logout()

        self.go200('/profile/')
        self.url('/login/\?next=/profile/')

    def test_logout_and_get(self):
        user = self.helper('create_user')
        self.login(USERNAME, PASSWORD)

        self.get200('/profile/')
        self.find(user.username)
        self.find(user.email)

        self.logout()

        self.get('/profile/')
        self.code(302)

        self.get200('/profile/', follow=True)
        self.url('/login/')

    def test_notfind(self):
        self.go200('index')
        self.notfind('Impossible')

    @TestCase.raises(TwillAssertionError)
    def test_notfind_error(self):
        self.go200('index')
        self.notfind('tddspry')

    def test_notfind_escape(self):
        self.go200('index')
        self.notfind('Text in "valid" quotes', escape=True)

    @TestCase.raises(TwillAssertionError)
    def test_notfind_escape_error(self):
        self.go200('index')
        self.notfind('Text in "invalid" quotes', escape=True)

    def test_notfind_flags(self):
        self.go200('index')
        self.notfind('IMPOSSIBLE', flags='i')

    @TestCase.raises(TwillAssertionError)
    def test_notfind_flags_error(self):
        self.go200('index')
        self.notfind('TDDSPRY', flags='i')

    def test_notfind_flat(self):
        self.go200('index')
        self.notfind('c#', flat=True)

    @TestCase.raises(TwillAssertionError)
    def test_notfind_flat_error(self):
        self.go200('index')
        self.notfind('c++', flat=True)

    def test_notfind_in(self):
        self.notfind_in('invalid', 'Text in "valid" quotes')

    @TestCase.raises(TwillAssertionError)
    def test_notfind_in_error(self):
        self.notfind_in('valid', 'Text in "valid" quotes')

    def test_notfind_in_escape(self):
        self.notfind_in('"invalid"',
                        'Text in &quot;valid&quot; quotes',
                        escape=True)

    @TestCase.raises(TwillAssertionError)
    def test_notfind_in_escape_error(self):
        self.notfind_in('"valid"',
                        'Text in &quot;valid&quot; quotes',
                        escape=True)

    def test_notfind_in_flags(self):
        self.notfind_in('text', 'Text in "valid" quotes', flags='s')

    @TestCase.raises(TwillAssertionError)
    def test_notfind_in_flags_error(self):
        self.notfind_in('text', 'Text in "valid" quotes', flags='i')

    def test_notfind_in_flat(self):
        self.notfind_in('c#', 'c++ is good, but python is better', flat=True)

    @TestCase.raises(TwillAssertionError)
    def test_notfind_in_flat_error(self):
        self.notfind_in('c++', 'c++ is good, but python is better', flat=True)

    def test_notfind_in_with_notfind(self):
        self.go200('index')
        self.notfind('Impossible')
        self.notfind_in('text', 'Text in "valid" quotes')
        self.notfind('Impossible again')

    def test_notfind_url(self):
        self.go200('edit_hidden_fields')
        self.notfind_url('multiply_forms')

    @TestCase.raises(TwillAssertionError)
    def test_notfind_url_found(self):
        self.go200('index')
        self.notfind_url('multiply_forms')

    def test_pages(self):
        profiles, users = [], []

        for i in xrange(10):
            user = User.objects.create_user(username='username%d' % i,
                                            password='password%d' % i,
                                            email='email%d@domain.com' % i)
            profile = UserProfile.objects.create(user=user,
                                                 bio=TEST_BIO % i)

            users.append(user)
            profiles.append(profile)

        self.go200('/users/')

        for i, user in enumerate(users):
            profile = profiles[i]
            self.find(user.username)
            self.find(profile.get_absolute_url())

        for i, user in enumerate(users):
            profile = profiles[i]
            self.go(profile.get_absolute_url())
            self.find('Username: %s' % user.username)
            self.find('Email: %s' % user.email)
            self.find('Bio: %s' % profile.bio)

    def test_post(self):
        # POST data for testing
        data = TEST_POST_DATA
        empty_data = dict([(k, '') for k in TEST_POST_DATA.keys()])

        # Make POST request without data
        self.post('edit_hidden_fields', data={})
        self.code(200)
        self.url('edit_hidden_fields')
        for key, value in empty_data.items():
            self.notfind("%s: '%s'" % (key, value))

        # Make POST request with empty data
        self.post('edit_hidden_fields', data=empty_data)
        self.code(200)
        self.url('edit_hidden_fields')
        for key, value in empty_data.items():
            self.find("%s: '%s'" % (key, value))

        # Make POST request with data
        self.post('edit_hidden_fields', data=data)
        self.code(200)
        self.url('edit_hidden_fields')
        for key, value in data.items():
            self.find("%s: '%s'" % (key, value))

    def test_post_and_forms(self):
        self.post('edit_hidden_fields', data=TEST_POST_DATA)
        self.code(200)
        self.url('edit_hidden_fields')

        self.find(TEST_POST_DATA['some_field_1'])
        self.notfind(TEST_POST_DATA['some_field_1'][::-1])
        self.find(TEST_POST_DATA['some_field_2'])
        self.notfind(TEST_POST_DATA['some_field_2'][::-1])

        self.info()
        self.showforms()

        self.fv(1, 'some_field_1', TEST_POST_DATA['some_field_1'][::-1])
        self.fv(1, 'some_field_2', TEST_POST_DATA['some_field_2'][::-1])

        self.submit200(url='edit_hidden_fields')

        self.notfind(TEST_POST_DATA['some_field_1'])
        self.find(TEST_POST_DATA['some_field_1'][::-1])
        self.notfind(TEST_POST_DATA['some_field_2'])
        self.find(TEST_POST_DATA['some_field_2'][::-1])

    def test_post_and_twill(self):
        self.post('edit_hidden_fields', TEST_POST_DATA)
        self.code(200)
        self.url('edit_hidden_fields')
        for key, value in TEST_POST_DATA.items():
            self.find("%s: '%s'" % (key, value))

        self.go(settings.MEDIA_URL + 'does_not_exist.exe')
        self.code(404)

        self.go200('/')
        self.url('/')

        self.find('Index')
        self.find('c++ is good, but python - better ;)', flat=True)

    def test_post_short_syntax(self):
        # POST data for testing
        data = TEST_POST_DATA
        empty_data = dict([(k, '') for k in TEST_POST_DATA.keys()])

        # Make POST request without data
        self.post('edit_hidden_fields', {})
        self.code(200)
        self.url('edit_hidden_fields')
        for key, value in empty_data.items():
            self.notfind("%s: '%s'" % (key, value))

        # Make POST request with empty data
        self.post('edit_hidden_fields', empty_data)
        self.code(200)
        self.url('edit_hidden_fields')
        for key, value in empty_data.items():
            self.find("%s: '%s'" % (key, value))

        # Make POST request with data
        self.post('edit_hidden_fields', data)
        self.code(200)
        self.url('edit_hidden_fields')
        for key, value in data.items():
            self.find("%s: '%s'" % (key, value))

    def test_post200(self):
        self.post200('edit_hidden_fields', TEST_POST_DATA)
        self.url('edit_hidden_fields')
        for key, value in TEST_POST_DATA.items():
            self.find("%s: '%s'" % (key, value))

    @TestCase.raises(TwillAssertionError)
    def test_post200_assertion(self):
        self.post200(settings.MEDIA_URL + 'does_not_exist.exe', data={})

    def test_redirect(self):
        self.disable_redirect()
        self.go200('/redirect/')
        self.url('/redirect/')

        self.enable_redirect()
        self.go200('/redirect/')
        self.url('/')

    def test_reversed_urls(self):
        self.go200('index')
        self.find('Index')

        user = self.helper('create_user')
        profile = self.helper('create_profile', user, UserProfile)

        self.go200('user', args=[user.username])
        self.find(user.username)
        self.find(user.email)

        self.go200('user', kwargs={'username': user.username})
        self.find(user.username)
        self.find(user.email)

    def test_show_on_error_save_output(self):

        def check(func, dirname=None):
            old_dirname = os.environ.get('TWILL_ERROR_DIR', None)

            dirname = dirname or os.path.dirname(os.tempnam())
            os.environ['TWILL_ERROR_DIR'] = dirname

            try:
                func(self)
            except (TwillAssertionError, TwillException):
                pass

            contents = os.listdir(dirname)
            contents.sort()

            filename = '%s.%s-' % (self.__module__, func.__name__)
            found = False

            if old_dirname is not None:
                os.environ['TWILL_ERROR_DIR'] = dirname

            for name in contents:
                if name.startswith(filename):
                    os.unlink(os.path.join(dirname, name))
                    found = True

            assert found, \
                'Cannot found file started with %r in %r dir.\nDir ' \
                'contents:\n%s' % (filename, dirname, contents)

        check(dummy_error)
        check(dummy_field_error)

        dirname = 'errors'
        full_dirname = os.path.abspath(os.path.join(os.getcwd(), dirname))

        # Remove directory if it still exists
        if os.path.isdir(full_dirname):
            shutil.rmtree(full_dirname)

        check(dummy_error, dirname)
        check(dummy_field_error, dirname)

        # Check that errors dir exists on current work directory
        if not os.path.isdir(full_dirname):
            assert False, 'Directory %r does not exists.'

        # Remove directory
        shutil.rmtree(full_dirname)

    def test_static(self):
        self.go(settings.MEDIA_URL)
        self.code(404)

        self.go(settings.MEDIA_URL + 'does_not_exist.exe')
        self.code(404)

        self.go(settings.MEDIA_URL + 'css/screen.css')
        self.code(200)

    def test_url_regexp(self):
        self.go200('/')

        self.follow200('Query string')

        self.assert_raises(TwillAssertionError, self.url, '/')
        self.assert_raises(TwillAssertionError, self.url, '/$')
        self.url('/', regexp=False)
        self.url('/\?query=string')
        self.url('/\?query=string$')

        self.find("request.GET\['query'\] = string")

    def test_info(self):
        response = self.get200('/')
        self.info()
        response = self.post200('/')
        self.info()

class TestHttpDeprecated(HttpTestCase):

    def setup(self):
        super(TestHttpDeprecated, self).setup()

    def teardown(self):
        super(TestHttpDeprecated, self).teardown()

    def test_message(self):
        """
        Check that old styled setup and teardown methods loaded without
        errors.
        """
        self.message = {'big': 'badda boom'}


class TestHttpDjangoAssertMethods(TestCase):

    def testContains(self):
        response = self.client.get('/')
        self.assertContains(response, 'Index')
        self.assertContains(response, 'c++ is good, but python - better ;)')

    def testContainsCount(self):
        response = self.client.get('/')
        self.assertContains(response, 'Index', 1)
        self.assertContains(response, 'python', 2)

    def testFormError(self):
        response = self.client.post('/login/', {'username': USERNAME})
        self.assertFormError(response,
                             'form',
                             'password',
                             'This field is required.')

    def testNotContains(self):
        response = self.client.get('/')
        self.assertNotContains(response, 'Impossible')

    def testRedirects(self):
        response = self.client.get('/fast-redirect/')
        self.assertRedirects(response, '/')

        response = self.client.get('/fast-redirect/?next=/edit-hidden-fields/')
        self.assertRedirects(response, '/edit-hidden-fields/')

        response = self.client.get('/fast-redirect/?permanent=yes')
        self.assertRedirects(response, '/', 301)

        url = settings.MEDIA_URL + 'does_not_exist.exe'
        response = self.client.get('/fast-redirect/?next=%s' % url)
        self.assertRedirects(response, url, 302, 404)

    def testTemplateNotUsed(self):
        response = self.client.get('/')
        self.assertTemplateNotUsed(response, 'testapp/user.html')
        self.assertTemplateNotUsed(response, 'testapp/users.html')

    def testTemplateUsed(self):
        response = self.client.get('/')
        self.assertTemplateUsed(response, 'base.html')
        self.assertTemplateUsed(response, 'testapp/index.html')


class TestHttpDjangoAssertMethodsWithUnderscores(TestCase):

    def test_contains(self):
        response = self.client.get('/')
        self.assert_contains(response, 'Index')
        self.assert_contains(response, 'c++ is good, but python - better ;)')

    def test_contains_count(self):
        response = self.client.get('/')
        self.assert_contains(response, 'Index', 1)
        self.assert_contains(response, 'python', 2)

    def test_form_error(self):
        response = self.client.post('/login/', {'username': USERNAME})
        self.assert_form_error(response,
                               'form',
                               'password',
                               'This field is required.')

    def test_not_contains(self):
        response = self.client.get('/')
        self.assert_not_contains(response, 'Impossible')

    def test_redirects(self):
        response = self.client.get('/fast-redirect/')
        self.assert_redirects(response, '/')

        response = self.client.get('/fast-redirect/?next=/edit-hidden-fields/')
        self.assert_redirects(response, '/edit-hidden-fields/')

        response = self.client.get('/fast-redirect/?permanent=yes')
        self.assert_redirects(response, '/', 301)

        url = settings.MEDIA_URL + 'does_not_exist.exe'
        response = self.client.get('/fast-redirect/?next=%s' % url)
        self.assert_redirects(response, url, 302, 404)

    def test_template_not_used(self):
        response = self.client.get('/')
        self.assert_template_not_used(response, 'testapp/user.html')
        self.assert_template_not_used(response, 'testapp/users.html')

    def test_template_used(self):
        response = self.client.get('/')
        self.assert_template_used(response, 'base.html')
        self.assert_template_used(response, 'testapp/index.html')
