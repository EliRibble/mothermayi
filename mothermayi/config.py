import os
import yaml

class ConfigNotFoundError(Exception):
    pass

def find_config_file():
    location = os.path.abspath('.')
    while location != '/':
        config = os.path.join(location, '.mothermayi')
        if os.path.exists(config):
            return config
        location = os.path.dirname(location)
    raise ConfigNotFoundError("Could not find .mothermayi")

def parse():
    try:
        configfile = find_config_file()
    except ConfigNotFoundError:
        return {}

    with open(configfile, 'r') as f:
        config = yaml.load(f)
    return config
