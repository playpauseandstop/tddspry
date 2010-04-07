from settings import *


# MySQL database engine settings for tddspry test project
DATABASE_ENGINE = 'mysql'
DATABASE_NAME = 'tddspry'
DATABASE_USER = 'root'
DATABASE_PASSWORD = ''
DATABASE_HOST = '127.0.0.1'
DATABASE_PORT = 3306


# Try to loading settings from ``settings_mysql_local.py`` file
try:
    from settings_mysql_local import *
except ImportError, e:
    sys.stderr.write('settings_mysql_local.py not found. Using MySQL ' \
                     'default settings\n')
    sys.stderr.write('%s: %s\n\n' % (e.__class__.__name__, e))
