from settings_sqlite import *


# SQLite database engine configuration for tddspry test project set in original
# settings, here set test database name
DATABASE_ENGINE = 'sqlite3'
DATABASE_NAME = DATABASES['default']['NAME']
TEST_DATABASE_NAME = DATABASES['default']['TEST_NAME']

# Remove new-style database settings
del DATABASES


# Try to loading settings from ``settings_sqlite_legacy_local.py`` file
try:
    from settings_sqlite_legacy_local import *
except ImportError, e:
    sys.stderr.write('settings_sqlite_legacy_local.py not found. Using ' \
                     'SQLite legacy default settings\n')
    sys.stderr.write('%s: %s\n\n' % (e.__class__.__name__, e))
