import mothermayi.entryway
import mothermayi.git

def handle_plugins(config, entries, staged):
    for entry in entries:
        result = entry(config, staged)

def run(config):
    with mothermayi.git.stash():
        staged = mothermayi.git.get_staged()
        if not staged:
            return
        plugins = mothermayi.entryway.get_plugins('pre-commit')
        handle_plugins(config, plugins, staged)
