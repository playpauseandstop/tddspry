import os
import sys


# Calculate current directory path and add it to ``sys.path``
DIRNAME = os.path.abspath(os.path.dirname(__file__))
sys.path.append(DIRNAME)

# Debug settings
DEBUG = True
TEMPLATE_DEBUG = DEBUG

# Test settings
TDDSPRY_TEST_CASE = 'django.test.TestCase'

# Authentication settings
AUTH_PROFILE_MODULE = 'testapp.UserProfile'
LOGIN_URL = '/login/'
LOGIN_REDIRECT_URL = '/'
LOGOUT_URL = '/logout/'

# Database settings
# Please, set proper database settings in ``settings_local.py`` file
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(DIRNAME, 'testproject.db'),
    },
}

# Date and time settings
TIME_ZONE = 'Europe/Kiev'

# Installed applications
INSTALLED_APPS = (
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.flatpages',
    'django.contrib.sessions',
    'django.contrib.sites',

    'registration',

    'testproject.testapp',
)

# Fixture directories
FIXTURE_DIRS = (
    os.path.join(DIRNAME, 'fixtures'),
)

# Media files settings
MEDIA_ROOT = os.path.join(DIRNAME, 'static')
MEDIA_URL = '/static/'

# Middleware settings
MIDDLEWARE_CLASSES = (
    'django.middleware.common.CommonMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.middleware.locale.LocaleMiddleware',
)

# Session settings
SESSION_COOKIE_NAME = 'testproject_sid'

# Template settings
TEMPLATE_CONTEXT_PROCESSORS = (
    'django.core.context_processors.auth',
    'django.core.context_processors.i18n',
    'django.core.context_processors.media',
)
TEMPLATE_DIRS = (
    os.path.join(DIRNAME, 'templates'),
)

# Other **Django** settings
ROOT_URLCONF = 'testproject.urls'
SECRET_KEY = 'set proper value in ``settings_local.py`` file'
SITE_ID = 1

# ``django-registration`` settings
ACCOUNT_ACTIVATION_DAYS = 30

# Try to loading settings from ``settings_local.py`` file
try:
    from settings_local import *
except ImportError, e:
    sys.stderr.write('settings_local.py not found. Using default settings\n')
    sys.stderr.write('%s: %s\n\n' % (e.__class__.__name__, e))
