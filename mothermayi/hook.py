import logging
import os

LOGGER = logging.getLogger(__name__)

def find_git_repo():
    location = os.path.abspath('.')
    while location != '/':
        check = os.path.join(location, '.git')
        if os.path.exists(check) and os.path.isdir(check):
            return check
        location = os.path.dirname(location)

def install():
    repo = find_git_repo()
    LOGGER.debug("Found git repo at %s", repo)
