"""
Plugin that make able to test Django projects or applications with nose
library.
"""

import logging
import os
import re
import sys

from nose.plugins.base import Plugin
from nose.util import ispackage, resolve_name, skip_pattern


__all__ = ('DjangoPlugin', )


log = logging.getLogger(__name__)
skip_pattern_re = re.compile(skip_pattern)


class DjangoPlugin(Plugin):
    """
    Run nosetests for Django projects or apps. You need to specify settings of
    your project or plugin tries to auto-load from current or child
    directories.
    """
    error_dir = None
    name = 'django'
    settings = None
    verbosity = 1

    def begin(self):
        from django.conf import settings
        from django.core.handlers.wsgi import WSGIHandler
        from django.core.servers.basehttp import AdminMediaHandler
        from django.test.simple import TEST_MODULE

        from tddspry.django.settings import IP, PORT

        from twill import add_wsgi_intercept

        log.debug('DjangoPlugin start')

        # Find to Django models in tests modules for each of ``INSTALLED_APPS``
        for label in settings.INSTALLED_APPS:
            tests = label + '.' + TEST_MODULE

            try:
                self.load_tests(tests)
            except (AttributeError, ImportError):
                pass

        # Setup Django test environment and test database
        self.setup_django()

        # Setup Twill for testing with Django
        app = AdminMediaHandler(WSGIHandler())
        add_wsgi_intercept(IP, PORT, lambda: app)

    def configure(self, options, config):
        Plugin.configure(self, options, config)

        # Do nothing if plugin not enabled
        if not self.enabled:
            return

        # Check that Django and twill libraries available in this system
        if self.enabled:
            for lib in ('Django', 'twill'):
                try:
                    __import__(lib.lower())
                except ImportError, e:
                    log.error('%s not available: %s' % (lib, e))
                    self.enabled = False
                    return

        # Get user defined options
        self.error_dir = options.error_dir
        self.settings = options.settings
        self.verbosity = options.verbosity
        self.test_match_re = config.testMatch

        # Try to load Django project settings
        self.load_settings(self.settings)

        # Make sure that ``TWILL_ERROR_DIR`` set to ``os.environ`` if needed
        if self.error_dir:
            os.environ['TWILL_ERROR_DIR'] = self.error_dir

    def error(self, settings, dirname=None, subdirs=None):
        if settings is not None:
            sys.stderr.write(
                "Error: Can't find the module %r in ``sys.path``.\n(If " \
                "the file settings.py does indeed exist, it's causing an " \
                "ImportError somehow.)\n" % settings)
        else:
            sys.stderr.write(
                "Error: Can't find the file 'settings.py' in the current " \
                "work directory %r and all subdirectories %r. It appears " \
                "you've customized things.\nYou'll have to run `nosetests " \
                "--with-django` passing it your settings module.\n(If the " \
                "file settings.py does indeed exist, it's causing an " \
                "ImportError somehow.)\n" % (dirname, subdirs))
        sys.exit(1)

    def ismodule(self, obj):
        return hasattr(obj, '__file__')

    def ispackage(self, module):
        return module.__file__.rstrip('co').endswith('__init__.py')

    @property
    def legacy_django(self):
        from django import VERSION
        return not (VERSION[0] == 1 and VERSION[1] >= 2)

    def load_settings(self, settings):
        # If settings module was set try to load or die with error
        if settings is not None:
            try:
                resolve_name(settings)
            except (AttributeError, ImportError):
                return self.error(settings)
        else:
            settings = 'settings'

            try:
                resolve_name(settings)
            except (AttributeError, ImportError):
                dirname = os.getcwd()
                loaded = False

                subdirs = \
                    filter(lambda name: os.path.isdir(os.path.join(dirname,
                                                                   name)),
                           os.listdir(dirname))
                subdirs.sort()

                for name in subdirs:
                    settings = name + '.settings'

                    try:
                        resolve_name(settings)
                    except (AttributeError, ImportError, ValueError):
                        pass
                    else:
                        loaded = True
                        break

                if not loaded:
                    self.error(None, dirname, subdirs)

        os.environ['DJANGO_SETTINGS_MODULE'] = settings

    def load_tests(self, basename):
        obj = resolve_name(basename)

        if not self.ismodule(obj) or not self.ispackage(obj):
            return

        dirname = os.path.dirname(obj.__file__)

        childs = os.listdir(dirname)
        childs.sort()
        childs = map(lambda name: (name, os.path.join(dirname, name)), childs)

        for name, fullname in childs:
            if os.path.isdir(fullname) and ispackage(fullname):
                self.load_tests(basename + '.' + name)

            if not os.path.isfile(fullname) or skip_pattern_re.match(name) or \
               not name.endswith('.py') or name == '__init__.py':
                continue

            if self.test_match_re.match(name):
                self.load_tests(basename + '.' + name[:-3])

    def options(self, parser, env=None):
        env = env or os.environ
        Plugin.options(self, parser, env)

        parser.add_option('--django-settings', action='store',
                          default=env.get('DJANGO_SETTINGS_MODULE'),
                          dest='settings', help='Settings module of your ' \
                          'Django project to test. [DJANGO_SETTINGS_MODULE]')
        parser.add_option('--django-verbosity', action='store',
                          default=1, dest='verbosity', type='int',
                          help='Django verbosity level.')
        parser.add_option('--twill-error-dir', action='store',
                          default=env.get('TWILL_ERROR_DIR'), dest='error_dir',
                          help='If `TwillAssertionError` raised store all ' \
                          'output in this directory. [TWILL_ERROR_DIR]')

    def report(self, stream):
        log.debug('DjangoPlugin report')

        # Destroy Django test database and teardown Django test environment
        self.teardown_django()

    def setup_django(self):
        from django.conf import settings

        # If Django < 1.2
        if self.legacy_django:
            from django.db import connection
            from django.test.utils import setup_test_environment

            # Setup Django test environment
            setup_test_environment()

            # Create Django test database
            self.old_database_name = settings.DATABASE_NAME
            connection.creation.create_test_db(self.verbosity, autoclobber=True)
        # If Django >= 1.2
        else:
            from django.test.simple import DjangoTestSuiteRunner

            # Initialize Django tests runner
            runner = DjangoTestSuiteRunner(verbosity=self.verbosity)

            # New Django tests runner set ``DEBUG`` to False on setup test
            # environment, so we need to store real ``DEBUG`` value
            DEBUG = settings.DEBUG

            # Setup test environment
            runner.setup_test_environment()

            # And restore it to real value if needed
            if settings.DEBUG != DEBUG:
                settings.DEBUG = DEBUG

            # Setup test databases
            self.old_config = runner.setup_databases()
            self.runner = runner

    def teardown_django(self):
        # If Django < 1.2
        if self.legacy_django:
            from django.db import connection
            from django.test.utils import teardown_test_environment

            # Destroy test database
            connection.creation.destroy_test_db(self.old_database_name,
                                                self.verbosity)

            # Teardown Django test environment
            teardown_test_environment()
        # If Django >= 1.2
        else:
            # Destroy test databases
            self.runner.teardown_databases(self.old_config)

            # Teardown Django test environment
            self.runner.teardown_test_environment()
