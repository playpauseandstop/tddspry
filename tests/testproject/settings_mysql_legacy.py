from settings_mysql import *


# MySQL database engine settings for tddspry test project
DATABASE_ENGINE = 'mysql'
DATABASE_NAME = DATABASES['default']['NAME']
DATABASE_USER = DATABASES['default']['USER']
DATABASE_PASSWORD = DATABASES['default']['PASSWORD']
DATABASE_HOST = DATABASES['default']['HOST']
DATABASE_PORT = DATABASES['default']['PORT']

# Remove new-style database settings
del DATABASES


# Try to loading settings from ``settings_mysql_local.py`` file
try:
    from settings_mysql_legacy_local import *
except ImportError, e:
    sys.stderr.write('settings_mysql_legacy_local.py not found. Using MySQL ' \
                     'legacy default settings\n')
    sys.stderr.write('%s: %s\n\n' % (e.__class__.__name__, e))
