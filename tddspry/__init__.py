"""
``tddspry`` provides ``NoseTestCase`` class to base functional testing.

.. autoclass :: tddspry.NoseTestCase
   :members:

"""

from tddspry.cases import *


VERSION = (0, 4, 'beta')


def get_version():
    """
    Returns human-readable version of your **tddspry** installation.
    """
    intjoin = lambda data, sep=None: (sep or '.').join(map(str, data))

    if VERSION[-1] is not None:
        if isinstance(VERSION[-1], int):
            version = intjoin(VERSION)
        else:
            version = '%s-%s' % (intjoin(VERSION[:-1]), VERSION[-1])
    else:
        version = intjoin(VERSION[:-1])

    return version
