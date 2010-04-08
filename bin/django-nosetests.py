#!/usr/bin/env python
"""
Custom ``nosetests`` runner that make possible to run ``nosetests`` for your
Django projects without installed ``setuptools``.
"""

import nose
from nose.plugins.manager import EntryPointPluginManager

from tddspry.noseplugins import DjangoPlugin


if __name__ == '__main__':
    found, kwargs = False, {}

    manager = EntryPointPluginManager()
    manager.loadPlugins()

    for plugin in manager.plugins:
        if isinstance(plugin, DjangoPlugin):
            found = True
            break

    if not found:
        kwargs = {'addplugins': [DjangoPlugin()]}

    nose.main(**kwargs)
