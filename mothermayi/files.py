import re

PYTHON_SHEBANG_PATTERN = re.compile(r'#![\w /]*python')

def read_header(filename):
    with open(filename, 'r') as f:
        return f.read(100)

def has_python_shebang(filename):
    header = read_header(filename)
    return bool(PYTHON_SHEBANG_PATTERN.match(header))

def matches_any_pattern(filenames, patterns):
    matches = set()
    # I specifically loop patterns first so that we can put
    # cheaper checks in the front of the list and do those first
    for pattern in patterns:
        for filename in filenames:
            if filename in matches:
                continue
            if pattern(filename):
                matches.add(filename)
                continue
    return matches

def python_source(filenames):
    patterns = [
        lambda filename: filename.endswith('.py'),
        has_python_shebang,
    ]
    return matches_any_pattern(filenames, patterns)
