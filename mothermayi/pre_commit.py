import mothermayi.entryway
import mothermayi.git

def handle_plugins(config, entries, staged):
    for entry in entries:
        result = entry(config, staged)

def run(config):
    with mothermayi.git.stash():
        staged = mothermayi.git.get_staged()
        entries = mothermayi.entryway.get_entries('pre-commit')
        handle_plugins(config, entries, staged)
