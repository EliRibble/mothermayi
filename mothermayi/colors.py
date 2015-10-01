BLUE = '\033[94m'
GREEN = '\033[92m'
YELLOW = '\033[93m'
RED = '\033[91m'
ENDC = '\033[0m'
BOLD = '\033[1m'
UNDERLINE = '\033[4m'

def green(text):
    return GREEN + text + ENDC

def red(text):
    return RED + text + ENDC

def yellow(text):
    return YELLOW + text + ENDC
