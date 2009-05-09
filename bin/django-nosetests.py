#!/usr/bin/env python

import copy
import os
import sys
import subprocess

from nose.util import getfilename


def error(settings, dirname, subdirs=None):
    if settings is not None:
        sys.stderr.write(
            "Error: Can't find the module %r in the current work directory " \
            "%r.\n(If the file settings.py does indeed exist, it's causing " \
            "an ImportError somehow.)\n" % (
                settings,
                dirname,
            )
        )
    else:
        sys.stderr.write(
            "Error: Can't find the file 'settings.py' in the current work " \
            "directory %r and all subdirectories %r. It appears you've " \
            "customized things.\nYou'll have to run django-nosetests.py, " \
            "passing it your settings module.\n(If the file settings.py does " \
            "indeed exist, it's causing an ImportError somehow.)\n" % (
                dirname,
                subdirs,
            )
        )
    sys.exit(1)

def fake_import(package):
    filename = getfilename(package)
    if not filename:
        raise ImportError
    return filename


def load_settings(settings=None):
    old_settings = settings

    dirname = os.getcwd()
    sys.path.append(dirname)

    childs = os.listdir(dirname)
    childs.sort()

    subdirs = []

    for name in childs:
        if name[0] == '.':
            continue

        if os.path.isdir(os.path.join(dirname, name)):
            subdirs.append(name)

    try:
        settings = old_settings or 'settings'

        try:
            fake_import(settings)
        except ImportError:
            if old_settings is not None:
                error(old_settings, dirname)

            settings = os.path.basename(dirname) + '.settings'

            try:
                fake_import(settings)
            except ImportError:
                imported = False

                for subdir in subdirs:
                    settings = subdir + '.settings'

                    try:
                        fake_import(settings)
                    except ImportError:
                        pass
                    else:
                        imported = True
                        break

                if not imported:
                    raise ImportError
    except ImportError:
        error(None, dirname, subdirs)

    os.environ['DJANGO_SETTINGS_MODULE'] = settings


def main():
    def build_option(i, part):
        if '=' in part:
            _, value = part.split('=')
        else:
            value = old_parts[i + 1]
            del parts[parts.index(part) + 1]

        del parts[parts.index(part)]
        return value.strip()

    old_parts = sys.argv[1:]
    parts = copy.copy(old_parts)

    settings, error_dir = None, None

    for i, part in enumerate(old_parts):
        if part.startswith('--with-django-settings'):
            settings = build_option(i, part)
        elif part.startswith('--with-error-dir'):
            error_dir = build_option(i, part)

    load_settings(settings)
    if error_dir is not None:
        os.environ['TWILL_ERROR_DIR'] = error_dir

    process = subprocess.Popen('nosetests ' + ' '.join(parts), shell=True)
    status = os.waitpid(process.pid, 0)

if __name__ == '__main__':
    main()
