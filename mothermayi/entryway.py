import logging
import pkg_resources

LOGGER = logging.getLogger(__name__)
PLUGINS = {}
def load():
    for entry in pkg_resources.iter_entry_points(group='mothermayi'):
        runner = entry.load()
        plugin = runner()
        LOGGER.debug("Loaded plugin %s", plugin['name'])
        if plugin['name'] in PLUGINS:
            raise Exception("Already have a plugin with the name {}, cannot overwrite".format(plugin['name']))

        PLUGINS[plugin['name']] = plugin

def get_plugins(name):
    return {k: v for k, v in PLUGINS.items() if name in v}
