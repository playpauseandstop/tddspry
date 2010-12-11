from settings import *


# MySQL database engine settings for tddspry test project
DATABASE_ENGINE = 'sqlite3'
DATABASE_NAME = DATABASES['default']['NAME']

# Remove new-style database settings
del DATABASES


# Try to loading settings from ``settings_legacy_local.py`` file
try:
    from settings_legacy_local import *
except ImportError, e:
    sys.stderr.write('settings_legacy_local.py not found. Using legacy ' \
                     'default settings\n')
    sys.stderr.write('%s: %s\n\n' % (e.__class__.__name__, e))
