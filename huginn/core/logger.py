import sys

_BLUE = "\033[34m"
_GREEN = "\033[32m"
_YELLOW = "\033[33m"
_RED = "\033[31m"
_RESET = "\033[0m"


def info(msg):
    print(f"{_BLUE}[*]{_RESET} {msg}")


def ok(msg):
    print(f"{_GREEN}[+]{_RESET} {msg}")


def warn(msg):
    print(f"{_YELLOW}[!]{_RESET} {msg}")


def err(msg):
    print(f"{_RED}[-]{_RESET} {msg}", file=sys.stderr)
