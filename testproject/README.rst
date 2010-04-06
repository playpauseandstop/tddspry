============
Test project
============

Django test project for testing tddspry library.

Genral information
==================

This project bootstraped with virtualenv_ and pip_ by::

    $ ./bootstrap.py

You need to have virtualenv_ and pip_ both installed on your system.

.. note:: All project requirements, such as nose_ or twill_ would be
   downloaded on project bootstrap, tddspry would be installed from temporary
   archive ``sdist``'ed before bootstrap from actual repo.

.. important:: To disable downloading requirements from Internet and use
   packages installed in system just create ``bootstrap.cfg`` file with::

       [pip]
       requirements = False

       [virtualenv]
       site_packages = True

.. _virtualenv: http://virtualenv.openplans.org/
.. _pip: http://pip.openplans.org/
.. _nose: http://somethingaboutorange.com/mrl/projects/nose/
.. _twill: http://twill.idyll.org/
.. _Django: http://djangoproject.com/

Testing
=======

To test ``tddspry`` you need firstly bootstrap test project and then execute::

    $ source env/bin/activate
    (env)$ make test

or run full tests with coverage support, by::

    (env)$ make fulltest
