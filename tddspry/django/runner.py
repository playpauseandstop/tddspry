import nose.core

from django_nose.plugin import ResultPlugin
from django_nose.runner import _get_plugins_from_settings, NoseTestSuiteRunner


class TddspryTestSuiteRunner(NoseTestSuiteRunner):
    """
    NoseRunner which works with tddspry. Basically the difference is that we
    remove DjangoSetUpPlugin as tddspry does setup itself and add
    --with-django option.
    """

    def run_suite(self, nose_argv):
        #tddspry option
        nose_argv.append('--with-django')

        result_plugin = ResultPlugin()
        plugins_to_add = [result_plugin]

        for plugin in _get_plugins_from_settings():
            plugins_to_add.append(plugin)

        nose.core.TestProgram(argv=nose_argv, exit=False,
                              addplugins=plugins_to_add)
        return result_plugin.result
