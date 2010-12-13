from settings import *


# MySQL database engine settings for tddspry test project
if VERSION >= (1, 2):
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.mysql',
            'HOST': '127.0.0.1',
            'PORT': 3306,
            'USER': 'root',
            'PASSWORD': '',
            'NAME': 'tddspry',
        },
    }
else:
    DATABASE_ENGINE = 'mysql'
    DATABASE_HOST = '127.0.0.1'
    DATABASE_PORT = 3306
    DATABASE_USER = 'root'
    DATABASE_PASSWORD = ''
    DATABASE_NAME = 'tddspry'


try:
    from settings_mysql_local import *
except ImportError, e:
    pass
