"""
=======
tddspry
=======

Utilities to test Django applications with nosetests and twill.

TestCases
=========

NoseTestCase
------------

Base ``TestCase`` in ``tddspry``. The main advantages with standart Python's
``unittest.TestCase`` are that it depends ``object`` and all functions from
`nose.tools`_ existed as ``NoseTestCase``'s methods.

.. _`nose.tools`: http://code.google.com/p/python-nose/wiki/TestingTools

"""

from tddspry.cases import *


VERSION = (0, 2, 3)
