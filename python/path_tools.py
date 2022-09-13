'''Path tools with folders and directories.'''

import os

from cli_tools import cb
from colors import bright_blue, bright_red, bright_yellow


def get_colored_path(path=None, replace=None):
    '''Return path as colored string to print. Blue up to where path exists. Red for the rest.
    Uses clipboard text if no path supplied.

    Args:
        path (str): File path.
        replace (dict): Replace keys with their values to expand variables.

    Returns:
        str: Colored string of path to print.
    '''
    path = path or cb()

    # Replace any variables.
    if replace:
        for key, val in replace.items():
            path = path.replace(key, val)

    dirname = path
    while not os.path.exists(dirname):
        os.path.dirname(path)
        prev_dirname = dirname
        dirname = os.path.dirname(dirname)

        # Already reached root and still doesn't exist. So entire path doesn't exist.
        if dirname == prev_dirname:
            return bright_red(path)

    # Print existing and non-existing parts of path.
    non_existing = path.replace(dirname, '')
    if non_existing:
        return '{}{}'.format(bright_blue(dirname), bright_red(non_existing))
    return bright_blue(path)


def print_path(*args, **kwargs):
    '''See get_colored_path docstring.

    Try in terminal:
    >>> print_path('/')
    >>> print_path('\\')
    >>> print_path('C:')
    >>> print_path('C:/Users/does_not_exist')
    >>> print_path('C:/Users/does_not_exist/subdir1/subdir2')
    >>> print_path('Z:')
    '''
    print get_colored_path(*args, **kwargs)


def open_path(path):
    '''Open file or directory.'''
    if not os.path.exists(path):
        print bright_yellow('Path does not exist:'),
        print get_colored_path(path)
        return

    if os.path.isdir(path):
        os.startfile(path.replace('/', '\\'))

    print bright_red('Not sure how to open'),
    print get_colored_path(path)
