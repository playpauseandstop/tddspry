import mock


def inject_dependency(name, module=None, mock_params=None):
    """
    Inject mock dependency <name> into <module> (global by default)
    with <mock_params>
    """
    if module is None:
        module = globals()
    else:
        module = module.__dict__

    if mock_params is None:
        mock_params = {}

    def _dec(func):
        """
        Actual parameterless decorator
        """
        # Wrapper name should start with test_ so nosetest will discover it
        def test_wrapper(*args, **kwargs):
            try:
                orig = module[name]
            except KeyError:
                raise Exception, '%r not found' % name

            try:
                module[name] = mock.Mock(mock_params)
                function(*args, **kwargs)
            finally:
                module[name] = orig

        test_wrapper.__name__ = func.__name__
        test_wrapper.__doc__ = func.__doc__
        test_wrapper.__dict__.update(func.__dict__)

        return test_wrapper
    return _dec
