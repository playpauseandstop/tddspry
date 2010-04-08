from settings import *


# SQLite database doesn't properly work with standart django TestCase class
TDDSPRY_TEST_CASE = 'django.test.TransactionTestCase'

# SQLite database engine configuration for tddspry test project set in original
# settings, here set test database name
TEST_DATABASE_NAME = os.path.join(DIRNAME, 'test.db')


# Try to loading settings from ``settings_mysql_local.py`` file
try:
    from settings_sqlite_local import *
except ImportError, e:
    sys.stderr.write('settings_sqlite_local.py not found. Using SQLite ' \
                     'default settings\n')
    sys.stderr.write('%s: %s\n\n' % (e.__class__.__name__, e))
