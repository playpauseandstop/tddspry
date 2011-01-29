from settings import *


# Add application with datadiff tests to list of installed apps
INSTALLED_APPS += (
    'testproject.datadiff',
)


# Enable ``datadiff.tools.assert_equal`` function
TDDSPRY_USE_DATADIFF = True


try:
    from settings_datadiff_local import *
except ImportError:
    pass
