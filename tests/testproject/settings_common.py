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
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.flatpages',
    'django.contrib.sessions',
    'django.contrib.sites',

    'django_nose',
    'registration',

    'testproject.disabled.attr',
    'testproject.disabled.setting',

    'testproject.testapp',
]

# Remove ``django_nose`` for Django < 1.2
if VERSION < (1, 2):
    INSTALLED_APPS.remove('django_nose')

# Fixture directories
FIXTURE_DIRS = (
    rel('fixtures'),
)

# Logging settings
LOGGING = {
    'disable_existing_loggers': True,
    'formatters': {
        'simple': {
            'format': '%(asctime)s %(levelname)s %(message)s',
        },
    },
    'handlers': {
        'console': {
            'class': 'logging.StreamHandler',
            'formatter': 'simple',
            'level': 'DEBUG',
        },
        'null': {
            'class': 'django.utils.log.NullHandler',
            'level': 'DEBUG',
        }
    },
    'loggers': {
    },
    'version': 1,
}

# Media files settings
if VERSION >= (1, 3):
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
TEMPLATE_CONTEXT_PROCESSORS = [
    'django.core.context_processors.i18n',
]

if VERSION >= (1, 2):
    TEMPLATE_CONTEXT_PROCESSORS.extend([
        'django.contrib.auth.context_processors.auth',
        'django.contrib.messages.context_processors.messages',
    ])

    if VERSION >= (1, 3):
        TEMPLATE_CONTEXT_PROCESSORS.extend([
            'django.core.context_processors.static',
        ])
    else:
        TEMPLATE_CONTEXT_PROCESSORS.extend([
            'django.core.context_processors.media',
        ])
else:
    TEMPLATE_CONTEXT_PROCESSORS.extend([
        'django.core.context_processors.auth',
        'django.core.context_processors.media',
    ])

TEMPLATE_DIRS = (
    rel('templates'),
)

# Test settings
NOSE_ARGS = ('-e', 'datadiff', '-e', 'multidb')
TDDSPRY_DISABLED_APPS = ('testproject.disabled.setting', )
TEST_RUNNER = 'tddspry.django.TestSuiteRunner'

# Other **Django** settings
ROOT_URLCONF = 'testproject.urls'
SECRET_KEY = 'set proper value in ``settings_local.py`` file'
SITE_ID = 1

# ``django-registration`` settings
ACCOUNT_ACTIVATION_DAYS = 30
