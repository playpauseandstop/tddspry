#!/usr/bin/env python
"""
Custom ``nosetests`` runner that make possible to run ``nosetests`` for your
Django projects without installed ``setuptools``.
"""

import os
import sys

import nose
from nose.plugins.manager import EntryPointPluginManager

from tddspry.noseplugins import DjangoPlugin


def main():
    # First of all add current work directory to ``sys.path`` if it not there
    cwd = os.getcwd()

    if not cwd in sys.path or not cwd.strip(os.sep) in sys.path:
        sys.path.append(cwd)

    # Try to find that DjangoPlugin loaded from entry_points or not
    found, kwargs = False, {}

    manager = EntryPointPluginManager()
    manager.loadPlugins()

    for plugin in manager.plugins:
        if isinstance(plugin, DjangoPlugin):
            found = True
            break

    # If not manually add
    if not found:
        kwargs = {'addplugins': [DjangoPlugin()]}

    # Enable DjangoPlugin
    os.environ['NOSE_WITH_DJANGO'] = '1'

    # Run ``nosetests``
    nose.main(**kwargs)


if __name__ == '__main__':
    main()
