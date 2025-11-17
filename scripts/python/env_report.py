'''Print OS, global and local variables, environment variables, sys.path.

Standalone script. No depedency on any custom module.
'''


import platform
import os
import sys


# General info.
ENV_INFO = {
    'OS Version': '{} {}'.format(platform.system(), platform.release()),
    'Python Version': sys.version.split(' ')[0],
    'Interpreter': sys.executable,
    'Architecture': platform.architecture(),
    'OS Name': os.name,
    'Current Dir': os.getcwd(),
    'dir()': dir(),
}


def _is_string(data):
    '''Check if input is string. Python 2 uses basestring. Python 3 uses str.'''
    try:
        basestring
    except NameError:
        return isinstance(data, str)
    return isinstance(data, basestring)


def print_dict(dict_, title, delimiter=';'):
    '''Print dictionary.'''
    line = '{} ({})'.format(title, len(dict_))

    print()
    print('{}:'.format(line))

    count = 0
    for key in sorted(dict_):
        val = dict_[key]
        if _is_string(val) and delimiter in val:
            # Split paths by semi-colon. Probably list of paths.
            paths = val.split(delimiter)
            print('\t{} ({}):\n\t\t{}'.format(key, len(paths), '\n\t\t'.join(paths)))
        else:
            print('\t{}: {}'.format(key, val))
        count += 1

    print(line)


def print_env_vars():
    '''Print os.environ.'''
    print_dict(os.environ, 'Environment Variables')


def print_sys_path():
    '''Print sys.path. Able to filter by case-insensitive search.'''
    line = 'sys.path ({})'.format(len(sys.path))

    print()
    print('{}:'.format(line))

    count = 0
    for path in sys.path:
        print('\t{}'.format(path))
        count += 1

    print(line)


def main():
    print('GENERAL INFO:')

    # Print ENV_INFO.
    for k,v in ENV_INFO.items():
        print('{}: {}'.format(k, v))

    # Print globals() and locals().
    print_dict(globals(), 'globals()')
    print_dict(locals(), 'locals()')

    # Print environment variables.
    print_env_vars()

    # Print sys.path.
    print_sys_path()


if __name__ == "__main__":
    main()
