import logging
import mothermayi.entryway
import mothermayi.errors
import mothermayi.git
import mothermayi.colors

LOGGER = logging.getLogger(__name__)

def handle_plugins(config, plugins, commit):
    successful = True
    for name, plugin in plugins.items():
        try:
            result = plugin['post-commit'](config, commit)
            status = mothermayi.colors.green("PASSED")
        except mothermayi.errors.FailHook as e:
            result = str(e)
            status = mothermayi.colors.red("FAILED")
            successful = False
        message = "{0:<10}...[{1:<7}]".format(name, status)
        print(message)
        if result:
            print(result)
    return successful

def run(config):
    commit = mothermayi.git.get_latest_commit()
    plugins = mothermayi.entryway.get_plugins('post-commit')
    if not handle_plugins(config, plugins, commit):
        return 1
    return 0
