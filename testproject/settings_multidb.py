from settings import *


# MySQL database engine settings for tddspry test project
DATABASES.update({
    'legacy': {
        'ENGINE': DATABASES['default']['ENGINE'],
        'NAME': DATABASES['default']['NAME'].replace('.db', '_legacy.db'),
    },
})

# Add application that testing multidb purposes to tddspry
INSTALLED_APPS += (
    'testproject.olddata',
)


# Try to loading settings from ``settings_mysql_local.py`` file
try:
    from settings_mysql_local import *
except ImportError, e:
    sys.stderr.write('settings_mysql_local.py not found. Using MySQL ' \
                     'default settings\n')
    sys.stderr.write('%s: %s\n\n' % (e.__class__.__name__, e))
