# -*- coding: utf-8 -*-
"""
@version: 1.0
@copyright: 2007-2008 KDS Software Group http://www.kds.com.ua/
@license: TBD
@status: production
@summary: Base class for nosetests operating with DB.
Creates temporary sqlite DB in memory for every test and delete it after
test run.

"""
from django.db import backend, connection
from django.db.backends import util
from django.core.management import call_command

import copy
import django.conf
import django.db.backends.sqlite3.base as django_sqlite
import django.db.backends.sqlite3.creation as django_sqlite_creation

try:
    from sqlite3 import dbapi2 as sqlite
except ImportError:
    from pysqlite2 import dbapi2 as sqlite

def syncdb():
    """
    @summary: Initializes Django DB
    """
    call_command('syncdb')

def temp_django_db_conn():
    """
    @summary: Create temporary Django DB connection
    @return: temporary connection
    """
    sqlite_conn = django_sqlite.DatabaseWrapper()
    sqlite_conn.connection = sqlite.connect(
        database=':memory:',
        detect_types=sqlite.PARSE_DECLTYPES | sqlite.PARSE_COLNAMES)
    # define some functions that are missing from sqlite
    sqlite_conn.connection.create_function('concat', 2,
                                           lambda *args: ''.join(args))
    return sqlite_conn

def subst_django_db_conn(new_conn):
    """
    @summary: Substitute Django DB connection by <new_conn>
    warning: Black magic involved
    @param new_conn: connection to be used instead of the standart Django DB
    connection
    @raise TypeError: if new_conn is not supported type
    @return: original connection
    """
    # black magic ;)
    klass = connection.__class__
    orig_conn = klass.__new__(klass)
    orig_conn.__dict__.update(connection.__dict__)

    try:
        connection.__class__ = new_conn.__class__
    except TypeError:
        print connection.__class__, new_conn.__class__
        raise
    connection.__dict__.update(new_conn.__dict__)
    return orig_conn

class DbMock(object):
    """
    @summary: Base class for nosetests which operate with DB. Creates temporary
    sqlite DB in memory for every test and delete it after test run.
    """
    def setup(self):
        """
        @summary: setup of the class
        @raise AttributeError:
        """
        self.orig_db_engine = django.conf.settings.DATABASE_ENGINE
        django.conf.settings.DATABASE_ENGINE = 'sqlite3'

        self.orig_db_name = django.conf.settings.DATABASE_NAME
        django.conf.settings.DATABASE_NAME = ':memory:'

        try:
            self.supports_constraints = backend.supports_constraints
        except AttributeError:
            pass
        backend.supports_constraints = False

        self.orig_DATA_TYPES = copy.deepcopy(connection.creation.data_types)
        data_types = django_sqlite_creation.DatabaseCreation.data_types
        connection.creation.data_types = data_types
        self.operator_mapping = copy.deepcopy(backend.DatabaseWrapper.operators)
        backend.DatabaseWrapper.operators.update(
            django_sqlite.DatabaseWrapper.operators)

        self.orig_integrityerror = django.db.IntegrityError
        django.db.IntegrityError = sqlite.IntegrityError

        # this should be done latest
        self.sqlite_conn = temp_django_db_conn()
        self.orig_conn = subst_django_db_conn(self.sqlite_conn)
        syncdb()
        return

    def teardown(self):
        """
        @summary: db mockup teardown
        @raise AttributeError:
        """
        subst_django_db_conn(self.orig_conn)
        django.conf.settings.DATABASE_ENGINE = self.orig_db_engine
        django.conf.settings.DATABASE_NAME = self.orig_db_name
        try:
            backend.supports_constraints = self.supports_constraints
        except AttributeError:
            pass
        backend.DatabaseWrapper.operators = self.operator_mapping
        connection.creation.data_types = self.orig_DATA_TYPES
        django.db.IntegrityError = self.orig_integrityerror
        return
