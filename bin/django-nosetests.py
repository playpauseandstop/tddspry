#!/usr/bin/env python
"""
Custom ``nosetests`` runner that make possible to run ``nosetests`` for your
Django projects without installed ``setuptools``.
"""

import nose


if __name__ == '__main__':
    kwargs = {}

    try:
        import setuptools
    except ImportError:
        from tddspry.noseplugins import DjangoPlugin
        kwargs = {'addplugins': [DjangoPlugin()]}

    nose.main(**kwargs)
