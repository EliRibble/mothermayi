import pytest
import mothermayi.files

@pytest.mark.parametrize('header, matches', [
    ('#!/usr/bin/env python',       True),
    ('#!/usr/bin/env python2',      True),
    ('#!/usr/bin/env python3',      True),
    ('#!/usr/bin/env python3.4',    True),
    ('#!python',                    True),
    ('#!python2.7',                 True),
    ('#!/bin/bash',                 False),
])
def test_python_shebangs(header, matches, mocker):
    mocker.patch('mothermayi.files.read_header', return_value=header)
    result = mothermayi.files.has_python_shebang('fakefile')
    assert result == matches

@pytest.mark.parametrize('inputs, expected', [
    (['a.py', 'b.py', 'c.txt'], {'a.py', 'b.py'}),
    (['a/a.py', 'b.py'],        {'a/a.py', 'b.py'}),
])
def test_python_source(expected, inputs, mocker):
    mocker.patch('mothermayi.files.has_python_shebang', return_value=False)
    outputs = mothermayi.files.python_source(inputs)
    assert outputs == expected
