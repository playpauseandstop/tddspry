"""
``tddspry`` provides ``NoseTestCase`` class to base functional testing.

.. autoclass :: tddspry.NoseTestCase
   :members:

"""

from tddspry.cases import *


VERSION = (0, 3, 2, 'alpha')


def get_version():
    """
    Returns human-readable version of your **tddspry** installation.
    """
    def intjoin(data, sep):
        return sep.join(str(i) for i in data)

    if VERSION[-1] is not None:
        if isinstance(VERSION[-1], int):
            version = intjoin(VERSION, '.')
        else:
            version = '%s_%s' % (intjoin(VERSION[:-1], '.'), VERSION[-1])
    else:
        version = intjoin(VERSION[:-1], '.')

    return version
