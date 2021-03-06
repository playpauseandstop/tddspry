#!/usr/bin/env python
"""
Bootstrap project using virtualenv_ and pip_. This script will create new
virtual environment if needed and will install all requirements there.

.. _virtualenv: http://pypi.python.org/pypi/virtualenv
.. _pip: http://pypi.python.org/pypi/pip

"""

import ConfigParser
import copy
import os
import re
import sys


try:
    import pip
except ImportError, e:
    print('ERROR: %s') % e
    print('ERROR: This script requires pip installed in your system.')
    sys.exit(1)


try:
    import virtualenv
except ImportError, e:
    print('ERROR: %s') % e
    print('ERROR: This script requires virtualenv installed in your system.')
    sys.exit(1)


# Default configuration for bootstrap script. You may override configuration
# in ``bootstrap.cfg`` file.
CONFIG = {
    'pip': {
        'download_cache': '%(DEST_DIR)s/src',
        'quiet': False,
        'upgrade': False,
        'verbose': False,
    },
    'virtualenv': {
        'clear': False,
        'dest_dir': 'env',
        'site_packages': False,
        'quiet': 0,
        'unzip_setuptools': True,
        'verbose': 0,
    },
}

# Default requirements file and pattern to match all requirements files
REQUIREMENTS_FILE = 'requirements.txt'
REQUIREMENTS_REGEXP = re.compile(r'^requirements(?P<suffix>.*).txt$')

# Convert relative path to absolute
DIRNAME = os.path.abspath(os.path.dirname(__file__))
rel = lambda *x: os.path.abspath(os.path.join(DIRNAME, *x))


class Environment(object):
    """
    Cumulative class to create new virtual environment and install all
    requirements there.
    """
    def __init__(self, suffix=None, filename=None):
        # Initialize environment
        self.suffix = suffix is None and self.suffix_from_filename(filename) \
                                     or suffix
        print('Working environment is %r' % os.path.basename(self.dest_dir))

    def create(self):
        # Create new virtual environment
        print('\nStep 1. Create new virtual environment')

        if not os.path.isdir(self.dest_dir) or CONFIG['virtualenv']['clear']:
            kwargs = copy.copy(CONFIG['virtualenv'])
            kwargs['home_dir'] = self.dest_dir

            verbosity = int(kwargs['verbose']) - int(kwargs['quiet'])
            logger = virtualenv.Logger([
                (virtualenv.Logger.level_for_integer(2 - verbosity),
                 sys.stdout),
            ])

            del kwargs['dest_dir'], kwargs['quiet'], kwargs['verbose']

            virtualenv.logger = logger
            virtualenv.create_environment(**kwargs)
        else:
            print('Virtual environment %r already exists.' % self.dest_dir)

    @property
    def dest_dir(self):
        if not hasattr(self, '_dest_dir'):
            dest_dir = CONFIG['virtualenv']['dest_dir']
            if self.suffix:
                dest_dir += self.suffix
            setattr(self, '_dest_dir', rel(dest_dir))
        return getattr(self, '_dest_dir')

    def install_requirements(self):
        print('\nStep 2. Install requirements')

        # Install requirements from necessary requirements file
        if os.path.isfile(self.requirements_file):
            args = ['install',
                    '-E', os.path.basename(self.dest_dir),
                    '-r', os.path.basename(self.requirements_file)]

            if CONFIG['pip']['download_cache']:
                download_cache = \
                    CONFIG['pip']['download_cache'] % self.template_context
                args.extend(['--download-cache', download_cache])

            for name in ('quiet', 'upgrade', 'verbose'):
                if CONFIG['pip'][name]:
                    args.append('--' + name)

            try:
                pip.main(args)
            except SystemExit, e:
                if e.code:
                    raise e
        else:
            print('ERROR: Cannot to find requirements file at %r.' % \
                  self.requirements_file)
            sys.exit(1)

    @property
    def requirements_file(self):
        if not hasattr(self, '_requirements_file'):
            requirements_file, ext = os.path.splitext(REQUIREMENTS_FILE)
            if self.suffix:
                requirements_file += self.suffix
            requirements_file += ext
            setattr(self, '_requirements_file', rel(requirements_file))
        return getattr(self, '_requirements_file')

    def suffix_from_filename(self, filename):
        if filename is None:
            return u''
        try:
            return REQUIREMENTS_REGEXP.findall(filename)[0]
        except IndexError:
            print('Cannot init new environment using %r filename.' % filename)
            sys.exit(1)

    @property
    def template_context(self):
        return {'DEST_DIR': self.dest_dir}


def main():
    """
    Create new virtual environments and install pip requirements there.
    """
    # Change directory to current
    os.chdir(DIRNAME)

    # Read configuration values from ``bootstrap.cfg`` file if possible
    read_config('bootstrap.cfg')

    # Search over current directory files
    filenames = sorted(os.listdir(DIRNAME))
    env = None

    for filename in filenames:
        if not REQUIREMENTS_REGEXP.match(filename):
            continue

        if env is not None:
            print('\n%s\n') % ('-' * 79)

        # Initialize environment
        env = Environment(filename=filename)

        # Try to create new virtual environment
        env.create()

        # Install all requirements to this virtual environment if possible
        env.install_requirements()


def read_config(config_file):
    global CONFIG

    if not config_file.startswith(DIRNAME):
        config_file = rel(config_file)

    if not os.path.isfile(config_file):
        return

    config = ConfigParser.ConfigParser()
    config.read(config_file)

    print('Load bootstrap configuration from %r.' % config_file)

    for section in ('pip', 'virtualenv'):
        try:
            items = config.items(section)
        except ConfigParser.NoSectionError:
            continue

        for key, value in items:
            if key in CONFIG[section]:
                CONFIG[section][key] = value

if __name__ == '__main__':
    main()
