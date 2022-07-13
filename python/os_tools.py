'''Tools extending os module.'''

import os

import python_compat


def list_files(path='.', ext=None, print_found=False):
    '''List files in folder recursively using os.walk().

    Args:
        path (str): Root directory to search. Defaults to current directory.
        ext (str, [str], (str,)): Case-insensitive match file path using endswith().
        print_found (bool): Prints found paths while looping, if True.

    Returns:
        list: File paths.
    '''
    full_paths = []

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
                full_paths.append(full_path)
                if print_found:
                    print(full_path)
    return full_paths
