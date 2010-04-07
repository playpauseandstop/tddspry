def camelcase(name):
    """
    Convert new-style method names with underscores to old style camel-case
    names.

    So this function converts ``'assert_equal'`` string to ``'assertEqual' and
    ``'assert_not_equal'`` to ``'assertNotEqual'``.
    """
    return name[0].lower() + \
           name.replace('_', ' ').title().replace(' ', '')[1:]
