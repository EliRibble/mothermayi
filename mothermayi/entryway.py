import pkg_resources

def get_entries(name):
    entries = []
    for entry in pkg_resources.iter_entry_points(group='mothermayi'):
        if entry.name != name:
            continue
        runner = entry.load()
        entries.append(runner)
    return entries
