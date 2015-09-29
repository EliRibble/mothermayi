import contextlib
import logging
import subprocess

LOGGER = logging.getLogger(__name__)

def execute(command):
    LOGGER.debug("Executing %s", ' '.join(command))
    proc = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    stdout, stderr = proc.communicate(input=None)
    if proc.returncode != 0:
        raise Exception("Failed to execute command {}".format(' '.join(command)))
    LOGGER.debug("stdout %s", stdout)
    LOGGER.debug("stderr %s", stderr)

@contextlib.contextmanager
def stash():
    execute(['git', 'stash', '-u', '--keep-index'])
    yield
    execute(['git', 'reset', '--hard'])
    execute(['git', 'stash', 'pop', '--quiet', '--index'])
