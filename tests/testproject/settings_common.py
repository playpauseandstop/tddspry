import os
import sys
import time

from django import VERSION


rel = lambda *x: os.path.abspath(os.path.join(os.path.dirname(__file__), *x))


# Authentication settings
AUTH_PROFILE_MODULE = 'testapp.UserProfile'
LOGIN_URL = '/login/'
LOGIN_REDIRECT_URL = '/'
LOGOUT_URL = '/logout/'

# Debug settings
DEBUG = True
TEMPLATE_DEBUG = DEBUG

# Date and time settings
TIME_ZONE = time.tzname[0]

# Installed applications
INSTALLED_APPS = (
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.flatpages',
    'django.contrib.sessions',
    'django.contrib.sites',

    'registration',

    'testproject.disabled.attr',
    'testproject.disabled.setting',

    'testproject.testapp',
)

# Fixture directories
FIXTURE_DIRS = (
    rel('fixtures'),
)

# Media files settings
if VERSION > (1, 2):
    STATIC_ROOT = rel('static')
    STATIC_URL = '/static/'
else:
    MEDIA_ROOT = rel('static')
    MEDIA_URL = '/static/'

# Middleware settings
MIDDLEWARE_CLASSES = [
    'django.middleware.common.CommonMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.middleware.locale.LocaleMiddleware',
]

# Session settings
SESSION_COOKIE_NAME = 'testproject_sid'

# Template settings
TEMPLATE_CONTEXT_PROCESSORS = (
    'django.core.context_processors.auth',
    'django.core.context_processors.i18n',
    'django.core.context_processors.media',
)
TEMPLATE_DIRS = (
    rel('templates'),
)

# Test settings
TEST_DISABLED_APPS = ('testproject.disabled.setting', )

# Other **Django** settings
ROOT_URLCONF = 'testproject.urls'
SECRET_KEY = 'set proper value in ``settings_local.py`` file'
SITE_ID = 1

# ``django-registration`` settings
ACCOUNT_ACTIVATION_DAYS = 30
