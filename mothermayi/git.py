import contextlib
import logging
import re
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
    return stdout, stderr

@contextlib.contextmanager
def stash():
    execute(['git', 'stash', '-u', '--keep-index'])
    try:
       yield
    finally:
        execute(['git', 'reset', '--hard'])
        execute(['git', 'stash', 'pop', '--quiet', '--index'])


IS_MODIFIED = re.compile(r'^[MA]\s+(?P<filename>.*)$')
def get_staged():
    staged = []
    stdout, stderr = execute(['git', 'status', '--porcelain'])
    output = stdout.decode('utf-8')
    for line in output.splitlines():
        match = IS_MODIFIED.match(line)
        if match:
            staged.append(match.group('filename'))
    return staged
