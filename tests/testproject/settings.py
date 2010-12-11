from settings_common import *


# Database settings
# Please, set proper database settings in ``settings_local.py`` file
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


try:
    from settings_local import *
except ImportError:
    pass
