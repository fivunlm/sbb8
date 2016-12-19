import re
from feed import get_builds


def _filter_old_builds(builds):
    to_remove = []

    for build in builds:
        for b in builds:
            if b['artifact'] == build['artifact']:
                partial_b_version = b['version'][:b['version'].rfind('.')]
                partial_build_version = build['version'][:build['version'].rfind('.')]
                if partial_b_version == partial_build_version and b['timestamp'] > build['timestamp']:
                    to_remove.append(build)
                    break

    return [b for b in builds if b not in to_remove]


def command_check_builds(reg_ex, command):
    builds = get_builds()
    response = ''
    clean_builds = _filter_old_builds(builds)
    clean_builds.sort(key=lambda b: b['version'])
    for build in clean_builds:
        response += '%s %s *#%s* _%s_\n' % (
            ':heavy_check_mark:' if 'successful' in build['status'] else ':bangbang:', build['artifact'],
            build['version'], 'successful' if 'successful' in build['status'] else 'failed')
    return response


def command_check_specific_build(reg_ex, command):

    build_name = reg_ex.match(command).group(1)

    builds = get_builds()
    response = ''
    clean_builds = _filter_old_builds(builds)
    clean_builds.sort(key=lambda b: b['version'])
    clean_builds = filter(lambda b: build_name in b['version'], clean_builds)

    for build in clean_builds:
        response += '%s %s *#%s* _%s_\n' % (
            ':heavy_check_mark:' if 'successful' in build['status'] else ':bangbang:', build['artifact'],
            build['version'], 'successful' if 'successful' in build['status'] else 'failed')
    return response


COMMANDS = [
    {
        'regex': re.compile(r'\.do check builds(\s*)'),
        'command': command_check_builds
    },
    {
        'regex': re.compile(r'\.do check build ([\w.-]+)'),
        'command': command_check_specific_build
    }
]
