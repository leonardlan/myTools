'''Tools extending os module.'''

import os

import python_compat


def list_files(path='.', ext=None, print_found=False):
    '''List files in folder recursively using os.walk() with extensions filter.

    Args:
        path (str): Root directory to search. Defaults to current directory.
        ext (str, [str], (str,)): Case-insensitive match file path using endswith().
        print_found (bool): Prints found paths while looping, if True.

    Returns:
        list: File paths.
    '''
    paths = []

    # Convert ext list to tuple.
    ext = tuple(ext) if isinstance(ext, list) else ext

    # Lowercase extension.
    if python_compat.is_string(ext):
        ext = ext.lower()
    elif isinstance(ext, tuple):
        ext = tuple(e.lower() for e in ext)

    for root, _, files in os.walk(path):
        for file in files:
            if ext is None or (ext and file.lower().endswith(ext)):
                full_path = os.path.join(root, file)
                paths.append(full_path)
                if print_found:
                    print(full_path)

    # Print report.
    if print_found:
        if len(paths) > 1:
            print('\nFound {} paths'.format(len(paths)))
        elif not paths:
            print('Did not find any paths')

    return paths


def remove_pyc_files(path='.', print_found=True, dry_run=True):
    '''Remove .pyc files from directory recursively.'''
    paths = list_files(ext='.pyc', path=path, print_found=print_found)
    for path in paths:
        if dry_run:
            print('Not removing in dry run: {}'.format(path))
        else:
            print('Removing {}'.format(path))
            os.remove(path)
