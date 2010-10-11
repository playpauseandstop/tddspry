import re


__all__ = ('camelcase_to_underscore', 'process_re_flags',
           'underscore_to_camelcase')


RE_FLAGS = {'i': re.I, 'l': re.L, 'm': re.M, 's': re.S, 'u': re.U, 'x': re.X}


def camelcase_to_underscore(name):
    """
    Convert old-style camel-case method names to new-style names with
    underscores.

    ::

        >>> camelcase_to_underscore('assertEqual')
        ... 'assert_equal'
        >>> camelcase_to_underscore('assertNotEqual')
        ... 'assert_not_equal'
        >>> camelcase_to_underscore('assert_equal')
        ... 'assert_equal'
        >>> camelcase_to_underscore('assert_not_equal')
        ... 'assert_not_equal'

    """
    new_name = u''

    for char in name:
        if char.isupper():
            char = char.lower()
            new_name += u'_'

        new_name += char

    return new_name


def process_re_flags(flags=None):
    """
    Specify ``flags`` supported by ``re`` module in text format, like ``'i'``
    or ``'s'`` instead of ``re.I`` or ``re.S``. If multiple ``flags`` specified
    they would connected with ``|`` (unary OR), e.g. ``'iu'`` would be
    processed as ``re.I | re.U``.

    All supported flags are: ``'i', 'l', 'm', 's', 'u', 'x'``.
    """
    if flags:
        old_flags = flags
        flags = None

        for flag in old_flags:
            flag = flag.lower()

            if not flag in RE_FLAGS:
                continue

            flag = RE_FLAGS[flag]

            if flags is None:
                flags = flag
            else:
                flags |= flag

    return flags or 0


def underscore_to_camelcase(name):
    """
    Convert new-style method names with underscores to old style camel-case
    names.

    ::

        >>> underscore_to_camelcase('assert_equal')
        ... 'assertEqual'
        >>> underscore_to_camelcase('assert_not_equal')
        ... 'assertNotEqual'
        >>> underscore_to_camelcase('assertEqual')
        ... 'assertEqual'
        >>> underscore_to_camelcase('assertNotEqual')
        ... 'assertNotEqual'

    """
    return name[0].lower() + \
           name.replace('_', ' ').title().replace(' ', '')[1:]
