from settings_common import *


# Database settings
if VERSION >= (1, 2):
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.sqlite3',
            'NAME': rel('testproject.db'),
        },
    }
else:
    DATABASE_ENGINE = 'sqlite3'
    DATABASE_NAME = rel('testproject.db')

# Email settings
EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'

# Logging settings (disable annoying ``django.db.backends`` logs)
LOGGING['loggers'].update({
    'django.db.backends': {
        'handlers': ['null'],
        'level': 'DEBUG',
        'propagate': False,
    },
})


try:
    from settings_local import *
except ImportError:
    pass
