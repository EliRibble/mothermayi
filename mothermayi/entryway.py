import logging
import pkg_resources

LOGGER = logging.getLogger(__name__)
PLUGINS = {}
def load():
    for entry in pkg_resources.iter_entry_points(group='mothermayi'):
        runner = entry.load()
        plugin = runner()
        plugin['dist'] = entry.dist
        LOGGER.debug("Loaded plugin %s from %s", plugin['name'], entry.dist)
        existing_plugin = PLUGINS.get(plugin['name'], None)
        if existing_plugin and existing_plugin['dist'] != plugin['dist']:
            LOGGER.warning("Overwriting plugin %s with %s", existing_plugin, plugin)

        PLUGINS[plugin['name']] = plugin

def get_plugins(name):
    return {k: v for k, v in PLUGINS.items() if name in v}
