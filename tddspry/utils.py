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
