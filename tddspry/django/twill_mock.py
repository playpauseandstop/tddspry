# -*- coding: utf-8 -*-
"""
@version: 1.0
@copyright: 2007-2008 KDS Software Group http://www.kds.com.ua/
@license: TBD
@status: production
@summary: Base class for nosetests operating with twill.
"""
from django.db import backend, connection
from django.conf import settings
from django.core import mail
from django.test import utils

from twill.commands import *
from twill import add_wsgi_intercept
from twill.errors import TwillAssertionError
from twill.extensions.check_links import check_links

from warnings import filterwarnings

"""
Default variables for twill tests
"""
IP = '127.0.0.1'
PORT = 8088
SITE = 'http://%s:%s' % (IP, PORT)

try:
    filterwarnings('always', category=backend.Database.Warning)
except AssertionError:
    pass

def show_on_error(func):
    """
    @summary: On error, show last page got by twill
    This is decorator and every twill test should be decorated.
    """
    def test_wrapper(*args, **kwargs):
        'wrapper'
        try:
            func(*args, **kwargs)
        except TwillAssertionError:
            show()
            raise
    test_wrapper.__name__ = func.__name__
    test_wrapper.__doc__ = func.__doc__
    test_wrapper.__dict__.update(func.__dict__)
    return test_wrapper


class TwillMock(object):
    def setup(self):
        """
        @summary:
        - Setup twill virtual web server
        - Copy incoming email,
        - Create test DB
        """
        from django.core.servers.basehttp import AdminMediaHandler
        from django.core.handlers.wsgi import WSGIHandler
        global orig_database_name

        app = AdminMediaHandler(WSGIHandler())
        add_wsgi_intercept(IP, PORT, lambda: app)

        mail.SMTPConnection = utils.TestSMTPConnection
        mail.outbox = []

        orig_database_name = settings.DATABASE_NAME

        try:
            settings.DATABASE_NAME = 'test_' + settings.DATABASE_NAME
            connection.creation.destroy_test_db(orig_database_name)
            settings.DATABASE_NAME = orig_database_name
        except Exception:
            pass

        connection.creation.create_test_db(autoclobber=True)

    def teardown(self):
        """
        @summary: Drop test db
        """
        connection.creation.destroy_test_db(orig_database_name)


#TwillMock = show_on_error(TwillMock)
