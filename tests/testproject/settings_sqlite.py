from settings import *


# SQLite database doesn't properly work with standart django TestCase class
TDDSPRY_TEST_CASE = 'django.test.TransactionTestCase'

# SQLite database engine configuration for tddspry test project set in original
# settings, here set test database name
if VERSION > (1, 2):
    DATABASES['default'].update({
        'TEST_NAME': rel('test_testproject.db'),
    })
else:
    TEST_DATABASE_NAME = rel('test_testproject.db')


try:
    from settings_sqlite_local import *
except ImportError, e:
    pass
