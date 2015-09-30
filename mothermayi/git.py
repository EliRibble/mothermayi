import contextlib
import logging
import re
import mothermayi.process

LOGGER = logging.getLogger(__name__)

@contextlib.contextmanager
def stash():
    mothermayi.process.execute(['git', 'stash', '-u', '--keep-index'])
    try:
       yield
    finally:
        mothermayi.process.execute(['git', 'reset', '--hard'])
        mothermayi.process.execute(['git', 'stash', 'pop', '--quiet', '--index'])


IS_MODIFIED = re.compile(r'^[MA]\s+(?P<filename>.*)$')
def get_staged():
    staged = []
    stdout, stderr = mothermayi.process.execute(['git', 'status', '--porcelain'])
    output = stdout.decode('utf-8')
    for line in output.splitlines():
        match = IS_MODIFIED.match(line)
        if match:
            staged.append(match.group('filename'))
    return staged
