#!/usr/bin/env python
"""
Custom ``nosetests`` runner that make possible to run ``nosetests`` for your
Django projects.
"""

import nose

from tddspry.noseplugins import DjangoPlugin


if __name__ == '__main__':
    nose.main(addplugins=[DjangoPlugin()])
