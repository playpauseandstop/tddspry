from settings import *


# MySQL database engine settings for tddspry test project
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'tddspry',
        'USER': 'root',
        'PASSWORD': '',
        'HOST': '127.0.0.1',
        'PORT': 3306,
    },
}


# Try to loading settings from ``settings_mysql_local.py`` file
try:
    from settings_mysql_local import *
except ImportError, e:
    sys.stderr.write('settings_mysql_local.py not found. Using MySQL ' \
                     'default settings\n')
    sys.stderr.write('%s: %s\n\n' % (e.__class__.__name__, e))
