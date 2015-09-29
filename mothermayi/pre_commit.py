import mothermayi.entryway
import mothermayi.git

def handle_plugins(entries):
    for entry in entries:
        result = entry()

def run():
    with mothermayi.git.stash():
        entries = mothermayi.entryway.get_entries('pre-commit')
        handle_plugins(entries)
