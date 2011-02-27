import nose.core

from django_nose.plugin import ResultPlugin
from django_nose.runner import NoseTestSuiteRunner, _get_plugins_from_settings

from tddspry.noseplugins import DjangoPlugin


__all__ = ('TestSuiteRunner', )


class TestSuiteRunner(NoseTestSuiteRunner):
    """
    NoseRunner which works with tddspry.

    Basically the difference is that we remove DjangoSetUpPlugin as tddspry
    does setup itself and add ``--with-django`` option.
    """
    def run_suite(self, nose_argv):
        # Install necessary plugins
        django_plugin = DjangoPlugin(self)
        result_plugin = ResultPlugin()

        plugins_to_add = [django_plugin, result_plugin]

        for plugin in _get_plugins_from_settings():
            plugins_to_add.append(plugin)

        # Enable tddspry
        nose_argv.append('--with-django')

        # Run nosetests
        nose.core.TestProgram(argv=nose_argv,
                              exit=False,
                              addplugins=plugins_to_add)

        return result_plugin.result
