import os

from cli_tools import cb
from colors import bright_blue, bright_red


def print_path(path=None):
    '''Print blue up to where path exists. Red for the rest.

    Try in terminal:
    >>> print_path('/')
    >>> print_path('\\')
    >>> print_path('C:')
    >>> print_path('C:/Users/does_not_exist')
    >>> print_path('C:/Users/does_not_exist/subdir1/subdir2')
    >>> print_path('Z:')
    >>> print_path('')
    '''
    path = path or cb()
    dirname = path
    while not os.path.exists(dirname):
        os.path.dirname(path)
        prev_dirname = dirname
        dirname = os.path.dirname(dirname)

        # Already reached root and still doesn't exist. So entire path doesn't exist.
        if dirname == prev_dirname:
            print(bright_red(path))
            return

    # Print existing and non-existing parts of path.
    non_existing = path.replace(dirname, '')
    if non_existing:
        print('{}{}'.format(bright_blue(dirname), bright_red(non_existing)))
    else:
        print(bright_blue(path))
