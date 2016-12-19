import re
from feed import get_builds


def command_check_builds():
    builds = get_builds()
    return '\n'.join(builds)

COMMANDS = [
    {
        'regex': re.compile(r'\.do check builds(\s*)'),
        'command': command_check_builds
    }
]
