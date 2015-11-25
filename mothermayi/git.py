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

COMMIT_PATTERN = re.compile((
    r'commit (?P<commit>\w+)\n'
    r'Author:\s+(?P<Author>.*)\n'
    r'AuthorDate:\s+(?P<AuthorDate>.*)\n'
    r'Commit:\s+(?P<Commit>.*)\n'
    r'CommitDate:\s+(?P<CommitDate>.*)\n'
    r'\s*\n'
    r'\s*(?P<Title>.*)\n'
    r'\s*(?P<Message>.*)'
))
def parse_commit(text):
    match = COMMIT_PATTERN.match(text)
    if match:
        return match.groupdict()

def get_latest_commit():
    stdout, stderr = mothermayi.process.execute(['git', 'log', '-1', 'HEAD', '--format=fuller'])
    return parse_commit(stdout.decode('utf-8'))
