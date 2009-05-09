.. tddspry documentation master file, created by sphinx-quickstart on Fri May 8 00:10:14 2009.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

====================
Testing with tddspry
====================

**tddspry** is collection of testcases and additional helpers for testing
Django applications with nose__ library.

.. __: http://somethingaboutorange.com/mrl/projects/nose/

Requirements
============

- Django_ >= 1.0
- mock_ >= 0.5.0
- nose_ >= 0.10.3
- twill_ >= 0.9

.. _Django: http://www.djangoproject.com/download/
.. _mock: http://pypi.python.org/pypi/mock/
.. _nose: http://pypi.python.org/pypi/nose/
.. _twill: http://pypi.python.org/pypi/twill/

Installation
============

*On most UNIX-like systems, you'll probably need to run these commands as root
or using sudo.*

To install::

    python setup.py install

Or via easy_install_::

    easy_install tddspry

Also, you can retrieve fresh version of **tddspry** from GitHub_::

    git clone git://github.com/playpauseandstop/tddspry.git

.. _easy_install: http://pypi.python.org/pypi/setuptools/
.. _GitHub: http://github.com/

Usage
=====

We create **tddspry** to easing testing Django projects and applications.

.. toctree ::
   :maxdepth: 3

   writing_tests
   running_tests

Bugs, features, contacts
========================

Sending bugs and features
-------------------------

We use ``tddspry`` in all our projects, so we hope that it hasn't any bug,
but if you really find it - send it to `issues tracker`__ on GitHub.

And if ``tddspry`` does not support feature needed to you - tell us too and
we tries to adds it as soon as possible.

.. __: http://github.com/playpauseandstop/tddspry/issues

Contacts
--------

:Authors:
    Igor Davydenko *< playpauseandstop [at] gmail >*,

    Volodymyr Hotsyk *< gotsyk [at] gmail >*

:Idea:
    Andriy Khavryuchenko *< akhavr [at] gmail >*
