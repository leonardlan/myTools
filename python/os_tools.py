'''Tools extending os module.'''

import os
import python_compatibility

from os.path import getsize, join


def walk_dir(path='.', max_depth=None, ignore_dir=None, ignore_case=True, ext=None):
    '''Same as os.walk() but with max depth and ignore director(y/ies).

    Kwargs:
        path (str): Root directory to walk.
        max_depth (int or None): Max depth to walk into. None means no max depth.
        ignore_dir (str, [str], or None): Directories to ignore, match by name.
        ignore_case (bool): If True, will match case-insensitive when ignore_dir is specified.
        ext (str, [str], or None): Extension(s) to ignore. Searches with endswith().

    Returns:
        generator: Same as os.walk()
    '''
    # Get ignore_dirs as set.
    ignore_dir = ignore_dir or []
    ignore_dirs = [ignore_dir] if not isinstance(ignore_dir, list) else ignore_dir
    ignore_dirs = set(ignore_dirs) if not isinstance(ignore_dirs, set) else ignore_dirs
    if ignore_case:
        ignore_dirs = set(dir_.lower() for dir_ in ignore_dirs)

    # Get exts as tuple.
    ext = ext or []
    exts = [ext] if not isinstance(ext, list) else ext
    exts = tuple(ext) if not isinstance(ext, tuple) else ext
    if ignore_case:
        exts = tuple(ext.lower() for ext in exts)

    path = path.rstrip(os.sep)
    num_sep = path.count(os.sep)
    for root, dirs, files in os.walk(path):
        # Remove sub directories if max depth reached.
        num_sep_this = root.count(os.sep)
        if isinstance(max_depth, int) and num_sep + max_depth <= num_sep_this:
            del dirs[:]

        # Ignore specified directories by running dirs.remove() since it's mutable.
        if ignore_dirs:
            for dir_ in dirs:
                new_dir = dir_.lower() if ignore_case else dir_
                if new_dir in ignore_dirs:
                    dirs.remove(dir_)

        # Filter files down to specific extensions, if specified.
        if exts:
            # files = [f for f in files if f.endswith(exts)]
            for f in files:
                if not f.endswith(exts):
                    files.remove(f)

        yield root, dirs, files


def list_files(
        root_dir='.', name_contains='', ext=None, print_found=False, max_depth=None, ignore_dir=None,
        ignore_case=True, return_file_names=False):
    '''List files in folder recursively using os.walk() with extensions filter.

    Args:
        root_dir (str): Root directory to search. Defaults to current directory.
        name_contains (str): Filter files by name contains using "in" operator. Use ignore_case if
            ignoring case.
        ext (str, [str], (str,)): Case-insensitive match file path using endswith().
        print_found (bool): Prints found paths while looping, if True.
        max_depth (int or None): Max depth to walk into. None means no max depth.
        ignore_dir (str, [str], or None): Directories to ignore, match by name.
        ignore_case (bool): Ignore case for name_contains if True.
        return_file_names (bool): Return as file names instead of full path if True. Full path if
            False.

    Returns:
        list: File paths.
    '''
    # Convert ext list to tuple.
    ext = tuple(ext) if isinstance(ext, list) else ext

    # Lowercase extension.
    if python_compatibility.is_string(ext):
        ext = ext.lower()
    elif isinstance(ext, tuple):
        ext = tuple(e.lower() for e in ext)

    # Walk directory.
    paths = []
    name_contains = name_contains.lower() if ignore_case else name_contains
    for root, _, files in walk_dir(path=root_dir, max_depth=max_depth, ignore_dir=ignore_dir):
        for file in files:
            # Filter by name_contains.
            if name_contains:
                if ignore_case and name_contains not in file.lower():
                    continue
                elif not ignore_case and name_contains not in file:
                    continue

            if ext is None or (ext and file.lower().endswith(ext)):
                full_path = join(root, file)
                paths.append(full_path)
                if print_found:
                    print(os.path.relpath(full_path, root_dir))

    # Print report.
    if print_found:
        if len(paths) > 1:
            print('\nFound {} paths'.format(len(paths)))
        elif not paths:
            print('Did not find any paths')

    if return_file_names:
        return [os.path.basename(p) for p in paths]
    return paths


def remove_pyc_files(path='.', print_found=True, dry_run=True):
    '''Remove .pyc files from directory recursively.'''
    paths = list_files(ext='.pyc', path=path, print_found=print_found)
    for path in paths:
        if dry_run:
            print('Not removing since dry_run is True: {}'.format(path))
        else:
            print('Removing {}'.format(path))
            os.remove(path)
    print('Removed {} .pyc files'.format(len(paths)))


def tree(path='.', max_depth=None, ignore_dir=None, ignore_case=True):
    '''Print folder tree from path.

    Kwargs:
        See walk_dir().
    '''
    gen = walk_dir(path=path, max_depth=max_depth, ignore_dir=ignore_dir, ignore_case=ignore_case)
    for root, _, files in gen:
        depth = root.replace(path, '').count(os.sep)
        indent = ' ' * 4 * (depth)
        print('{}{}/'.format(indent, os.path.basename(root)))
        subindent = ' ' * 4 * (depth + 1)
        for f in files:
            print('{}{}'.format(subindent, f))


def print_dir_sizes(path='.', max_depth=None, ignore_dir=None, ignore_case=True):
    gen = walk_dir(path=path, max_depth=max_depth, ignore_dir=ignore_dir, ignore_case=ignore_case)
    for root, _, files in gen:
        size = 0
        for name in files:
            try:
                size += getsize(join(root, name))
            except Exception as err:
                print('Unable to get dir size: {}'.format(err))
        print('{} [{} bytes | {} files]'.format(root, size, len(files)))


def make_dirs(path, print_=True):
    '''Creates directory if not exists.'''
    if not os.path.exists(path):
        if print_:
            print('Creating folder {}'.format(path))
        os.makedirs(path)


def run_command_in_new_session(cmd):
    '''Runs command in new Command Prompt session.'''
    print('Running in new session: {}'.format(cmd))
    os.system('start cmd /k "{}"'.format(cmd))
