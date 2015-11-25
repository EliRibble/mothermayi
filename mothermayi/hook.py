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

HOOKS = {
    'pre-commit'    : "mothermayi pre-commit",
    'post-commit'   : "mothermayi post-commit",
}

def write_hooks(hooks):
    for name, content in HOOKS.items():
        path = os.path.join(hooks, name)
        if os.path.exists(path):
            with open(path, 'r') as f:
                if f.read() == content:
                    LOGGER.debug("Not writing the hook for %s - it's already installed", name)
                else:
                    raise PreCommitExists("A git hook already exists at {}. Refusing to overwrite. Please remove it manually".format(path))
        else:
            with open(path, 'w') as f:
                f.write(content)
        original = os.stat(path)
        os.chmod(path, original.st_mode | stat.S_IXUSR | stat.S_IXGRP | stat.S_IXOTH)
        LOGGER.debug("Set %s to executable", path)
        LOGGER.info("Installed %s", path)

def install(config):
    repo = find_git_repo()
    LOGGER.debug("Found git repo at %s", repo)
    hooks = os.path.join(repo, 'hooks')
    write_hooks(hooks)
