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
    'testproject.multidb',
)


try:
    from settings_multidb_local import *
except ImportError, e:
    pass
