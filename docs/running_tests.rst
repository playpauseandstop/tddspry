=============
Running tests
=============

``tddspry`` provides special command-line utility ``django-nosetests.py`` that
run all tests that found in current work directory.

This utility is wrapper to nosetests_ command that only set
``DJANGO_SETTINGS_MODULE`` environment var by ``--with-django-settings`` option
and ``TWILL_ERROR_DIR`` environment var by ``--with-error-dir`` option.

And to test your project, you need execute::

    django-nosetests.py

from your project's root or parent directory.

**Note:** If you wasn't installed ``tddspry`` to your system and using it
from ``PYTHONPATH`` just link ``django-nosetests.py`` something to your
``PATH``, for example::

    ln -s /path/to/tddspry/bin/django-nosetests.py ~/bin/django-nosetests.py

.. _nosetests: http://somethingaboutorange.com/mrl/projects/nose/0.11.0/usage.html
