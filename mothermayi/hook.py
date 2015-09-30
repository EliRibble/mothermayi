import logging
import os
import stat

LOGGER = logging.getLogger(__name__)

class NoRepoFoundError(Exception):
    pass

class PreCommitExists(Exception):
    pass

def find_git_repo():
    location = os.path.abspath('.')
    while location != '/':
        check = os.path.join(location, '.git')
        if os.path.exists(check) and os.path.isdir(check):
            return check
        location = os.path.dirname(location)
    raise NoRepoFoundError("Could not find a git repository (.git) in {}".format(os.path.abspath('.')))

HOOK_CONTENT = """
mothermayi pre-commit
"""

def write_hook(pre_commit):
    if os.path.exists(pre_commit):
        with open(pre_commit, 'r') as f:
            if f.read() == HOOK_CONTENT:
                LOGGER.debug("Not writing the hook - it's already set")
            else:
                raise PreCommitExists("A git hook already exists at {}. Refusing to overwrite. Please remove it manually".format(pre_commit))
    else:
        with open(pre_commit, 'w') as f:
            f.write(HOOK_CONTENT)
    original = os.stat(pre_commit)
    os.chmod(pre_commit, original.st_mode | stat.S_IXUSR | stat.S_IXGRP | stat.S_IXOTH)
    LOGGER.debug("Set %s to executable", pre_commit)

def install(config):
    repo = find_git_repo()
    LOGGER.debug("Found git repo at %s", repo)
    hooks = os.path.join(repo, 'hooks')
    pre_commit = os.path.join(hooks, 'pre-commit')
    write_hook(pre_commit)
