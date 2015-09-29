import contextlib
import os
import re
import subprocess

from setuptools import setup
from setuptools.command.sdist import sdist

DATA_ROOTS = []
PROJECT = 'mothermayi'
VERSION_FILE = 'mothermayi/__init__.py'

def _get_output_or_none(args):
    try:
        return subprocess.check_output(args).decode('utf-8').strip()
    except subprocess.CalledProcessError:
        return None

def _get_git_description():
    return _get_output_or_none(['git', 'describe'])

def _get_git_branches_for_this_commit():
    branches = _get_output_or_none(['git', 'branch', '-r', '--contains', 'HEAD'])
    split = branches.split('\n') if branches else []
    return [branch.strip() for branch in split]

def _is_on_releasable_branch(branches):
    return any(['origin/master' == branch or branch.startswith('origin/hotfix') for branch in branches])

def _git_to_version(git):
    match = re.match(r'(?P<tag>[\d\.]+)-(?P<offset>[\d]+)-(?P<sha>\w{8})', git)
    if not match:
        version = git
    else:
        version = "{tag}.post0.dev{offset}".format(**match.groupdict())
    return version

def _get_version_from_git():
    git_description = _get_git_description()
    git_branches = _get_git_branches_for_this_commit()
    version = _git_to_version(git_description) if git_description else None
    if git_branches and not _is_on_releasable_branch(git_branches):
        print("Forcing version to 0.0.1 because this commit is on branches {} and not a whitelisted branch".format(git_branches))
        version = '0.0.1'
    return version

VERSION_REGEX = re.compile(r'__version__ = "(?P<version>[\w\.]+)"')
def _get_version_from_file():
    with open(VERSION_FILE, 'r') as f:
        content = f.read()
    match = VERSION_REGEX.match(content)
    if not match:
        raise Exception("Failed to pull version out of '{}'".format(content))
    version = match.group(1)
    return version

@contextlib.contextmanager
def write_version():
    version = _get_version_from_git()
    if version:
        with open(VERSION_FILE, 'r') as version_file:
            old_contents = version_file.read()
        with open(VERSION_FILE, 'w') as version_file:
            new_contents = '__version__ = "{}"\n'.format(version)
            version_file.write(new_contents)
    print("Wrote {} with {}".format(VERSION_FILE, new_contents))
    yield
    if version:
        with open(VERSION_FILE, 'w') as version_file:
            version_file.write(old_contents)
            print("Reverted {} to old contents".format(VERSION_FILE))

def get_version():
    file_version = _get_version_from_file()
    git_version = _get_version_from_git()
    return (file_version == 'development' and git_version) or file_version

def get_data_files():
    data_files = []
    for data_root in DATA_ROOTS:
        for root, _, files in os.walk(data_root):
            data_files.append((os.path.join(PROJECT, root), [os.path.join(root, f) for f in files]))
    return data_files

class CustomSDistCommand(sdist): # pylint: disable=no-init
    def run(self):
        with write_version():
            sdist.run(self)

def main():
    setup(
        name                 = "mothermayi",
        version              = get_version(),
        description          = "A system for installing and managing git commit hooks",
        url                  = "https://github.com/EliRibble/mothermayi",
        long_description     = open("README.md").read(),
        author               = "EliRibble",
        author_email         = "junk@theribbles.org",
        cmdclass             = {
            'sdist'         : CustomSDistCommand,
        },
        install_requires    = [
            'PyYAML==3.11',
        ],
        extras_require={
            'develop': [
                'pytest==2.7.3',
            ]
        },
        packages             = ["mothermayi"],
        package_data         = {
            "mothermayi"     : ["mothermayi/*"],
        },
        data_files           = get_data_files(),
        entry_points = {
        },
        scripts = ['bin/mothermayi'],
        include_package_data = True,
    )

if __name__ == "__main__":
    main()
