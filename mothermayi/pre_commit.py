import logging
import mothermayi.entryway
import mothermayi.errors
import mothermayi.git
import mothermayi.colors

LOGGER = logging.getLogger(__name__)

def handle_plugins(config, plugins, staged):
    for name, plugin in plugins.items():
        try:
            result = plugin['pre-commit'](config, staged)
            status = mothermayi.colors.green("PASSED")
        except mothermayi.errors.FailHook as e:
            result = str(e)
            status = mothermayi.colors.red("FAILED")
        message = "{0:<10}...[{1:<7}]".format(name, status)
        print(message)
        if result:
            print(result)

def run(config):
    with mothermayi.git.stash():
        staged = mothermayi.git.get_staged()
        if not staged:
            return
        plugins = mothermayi.entryway.get_plugins('pre-commit')
        handle_plugins(config, plugins, staged)
