import os
import time

from functools import wraps

from twill.commands import save_html, show
from twill.errors import TwillAssertionError


__all__ = ('show_on_error', )


def show_on_error(func, clsname=None):
    """
    On ``TwillAssertionError``, show last page got by twill.

    By sets up ``TWILL_ERROR_DIR`` environment var all error pages would be
    saved on it.
    """
    @wraps(func)
    def wrapper(*args, **kwargs):
        try:
            func(*args, **kwargs)
        except TwillAssertionError:
            saved, showed = False, False

            if 'TWILL_ERROR_DIR' in os.environ:
                dirname = os.environ['TWILL_ERROR_DIR']

                if not os.path.isdir(dirname):
                    try:
                        os.mkdir(dirname)
                    except:
                        print 'Cannot create directory at %r.' % dirname
                        show()

                        showed = True

                if not showed:
                    timestamp = int(time.time())

                    if clsname is None:
                        filename = '%s.%s' % (func.__module__, func.__name__)
                    else:
                        filename = '%s.%s.%s' % (func.__module__,
                                                 clsname,
                                                 func.__name__)

                    filename = '%s-%d.html' % (filename, timestamp)
                    filename = os.path.join(dirname, filename)

                    try:
                        save_html(filename)
                    except:
                        print 'Cannot write to file at %r.' % filename
                        show()

                        showed = True
                    else:
                        print 'Output saved to %r.' % filename
                        saved = True

            if not saved and not showed:
                show()

            raise

    return wrapper
