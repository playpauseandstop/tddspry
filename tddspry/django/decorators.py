import os
import time

from functools import wraps

from twill.commands import browser, save_html, show, showforms
from twill.errors import TwillAssertionError, TwillException
from twill.utils import print_form


__all__ = ('show_on_error', )


def show_on_error(func, clsname=None):
    """
    On ``TwillAssertionError``, show last page got by twill.

    On ``TwillException: no field matches``, call twill ``showforms`` command.

    By default, decorator show output in stdout. To store output somewhere in
    disk - set up ``TWILL_ERROR_DIR`` environment var, e.g. if some error
    cathced in tests ran by::

        TWILL_ERROR_DIR=/tmp/tddspry/ django-nosetests.py

    all output would be stored in ``/tmp/tddspry/`` dir.
    """
    def save_forms(filename):
        forms = browser.get_all_forms()
        stream = open(filename, 'w')

        for i, form in enumerate(forms):
            print_form(i, form, stream)

        stream.close()

    @wraps(func)
    def wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except (TwillAssertionError, TwillException), e:
            field_error = False

            # Ignore all ``TwillException`` errors, but "no field matches"
            if e.__class__ == TwillException:
                message = e.args[0]

                if not message.startswith('no field matches "'):
                    raise

                field_error = True

            cmd = field_error and showforms or show
            saved, showed = False, False

            if 'TWILL_ERROR_DIR' in os.environ:
                dirname = os.environ['TWILL_ERROR_DIR']

                if not os.path.isdir(dirname):
                    try:
                        os.mkdir(dirname)
                    except:
                        print('Cannot create directory at %r.') % dirname
                        cmd()

                        showed = True

                if not showed:
                    timestamp = int(time.time())

                    if clsname:
                        filename = '%s.%s.%s' % (func.__module__,
                                                    clsname,
                                                    func.__name__)
                    else:
                        filename = '%s.%s' % (func.__module__,
                                                func.__name__)

                    format = field_error and 'txt' or 'html'
                    filename = '%s-%d.%s' % (filename, timestamp, format)
                    filename = os.path.join(dirname, filename)

                    try:
                        if field_error:
                            save_forms(filename)
                        else:
                            save_html(filename)
                    except:
                        print('Cannot write to file at %r.') % filename
                        cmd()

                        showed = True
                    else:
                        print('Output saved to %r.') % filename
                        saved = True

            if not saved and not showed:
                cmd()

            raise

    return wrapper
