import mothermayi.hook
import os
import pytest

def test_find_git_repo():
    assert mothermayi.hook.find_git_repo()

def test_find_git_repo_non_existent():
    os.chdir('/tmp')
    with pytest.raises(mothermayi.hook.NoRepoFoundError):
        mothermayi.hook.find_git_repo()
