"""
Hacks Django ``flush`` command to clean up ``:memory:`` database without
installing default fixtures data after flush.

Original code exists in ``django.core.management.commands.flush`` module.
"""

from django import VERSION
from django.core.management.base import CommandError
from django.core.management.color import no_style


__all__ = ('flush', )

ERROR_MESSAGE = """Database %r couldn't be flushed. Possible reasons:
  * The database isn't running or isn't configured correctly.
  * At least one of the expected database tables doesn't exist.
  * The SQL was invalid.
Hint: Look at the output of 'django-admin.py sqlflush'. That's the SQL this
command wasn't able to run.
The full error: %s"""


def get_db_connection(db_name):
    from django.conf import settings
    from django.db import connection

    # Closes exists connection and sets up new connection
    connection.close()
    settings.DATABASE_NAME = db_name

    # Django 1.1 branch has some new abilities in
    # ``django.db.connection.creation.create_test_db`` function.
    if VERSION[0] == 1 and VERSION[1]:
        connection.settings_dict["DATABASE_NAME"] = db_name

        can_rollback = connection.creation._rollback_works()
        settings.DATABASE_SUPPORTS_TRANSACTIONS = can_rollback
        connection.settings_dict["DATABASE_SUPPORTS_TRANSACTIONS"] = \
            can_rollback

    tables = connection.introspection.table_names()
    if tables:
        return connection

    return None


def flush():
    from django.core.management.sql import sql_flush
    from django.db import connection, models, transaction

    sql_list = sql_flush(no_style(), only_django=True)

    try:
        cursor = connection.cursor()

        for sql in sql_list:
            cursor.execute(sql)
    except Exception, e:
        transaction.rollback_unless_managed()
        raise CommandError(ERROR_MESSAGE % (settings.DATABASE_NAME, e))

    transaction.commit_unless_managed()
