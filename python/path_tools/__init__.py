'''Path tools with folders and directories.'''

import os
import re
import shutil

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
    print(get_colored_path(*args, **kwargs))


def open_path(path):
    '''Open file or directory.'''
    if not os.path.exists(path):
        print(bright_yellow('Path does not exist:'),)
        print(get_colored_path(path))
        return

    if os.path.isdir(path):
        os.startfile(path.replace('/', '\\'))
        return

    print(bright_red('Not sure how to open'),)
    print(get_colored_path(path))


def re_sub_in_dir(dir_path, regex_pattern, replacement, dry_run=True):
    '''Replaces filenames in a specified directory that contains a regular expression pattern with a
    replacement string.

    Args:
        dir_path (str): The path to the directory containing the filenames to be replaced.
        regex_pattern (str): The regular expression pattern to search for in the filenames.
        replacement (str): The string to replace the regex pattern with.
        dry_run (bool): Will rename files if True.

    Returns:
        None
    '''
    count = 0
    for filename in os.listdir(dir_path):
        if re.search(regex_pattern, filename):
            new_filename = re.sub(regex_pattern, replacement, filename)
            print('Renaming "{}" -> "{}"'.format(filename, new_filename))
            if dry_run:
                print('Not renaming in dry run')
            else:
                os.rename(os.path.join(dir_path, filename), os.path.join(dir_path, new_filename))
            count += 1

    if not count:
        print('No files to rename')
    elif count > 1:
        print('Replacing {} files'.format(count))


def remove_path(path, remove_empty_directories=False, dry_run=True):
    '''Removes file or folder path. Can also remove upper directory if remove_empty_directories is
    True.

    Args:
        path (str): File or folder path to be removed.
        remove_empty_directories (bool): If True, removes upper director(ies) if it's empty after
            removing current path.
        dry_run (bool): Will remove path if True.

    Returns:
        None
    '''
    if not os.path.exists(path):
        print('Path already does not exist: {}'.format(path))
        return

    # If remove_empty_directories is True, go up folder until not empty.
    if remove_empty_directories:
        while len(os.listdir(os.path.dirname(path))) == 1:
            path = os.path.dirname(path)

    # Remove path.
    print('Removing {}'.format(path))
    if dry_run:
        print('Not removing in dry run')
    else:
        # Remove file/folder.
        if os.path.isfile(path):
            os.remove(path)
        else:
            shutil.rmtree(path)
