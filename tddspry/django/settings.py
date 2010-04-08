from django.conf import settings
from django.test import TransactionTestCase

from nose.util import resolve_name


__all__ = ('IP', 'PORT', 'SITE', 'DjangoTestCase')


IP = getattr(settings, 'TDDSPRY_IP', '127.0.0.1')
PORT = getattr(settings, 'TDDSPRY_PORT', 8080)
SITE = 'http://%s:%s/' % (IP, PORT)

DjangoTestCase = getattr(settings, 'TDDSPRY_TEST_CASE', TransactionTestCase)

if isinstance(DjangoTestCase, basestring):
    DjangoTestCase = resolve_name(DjangoTestCase)
