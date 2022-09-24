'''Get folder/file path structure as Python object.'''

import os
import re


class Path(dict):
    '''Path object with results from regex match .groupdict() as keys.'''
    path = None

    def is_dir(self):
        return os.path.isdir(self.path)

    def is_file(self):
        return os.path.isfile(self.path)

    def exists(self):
        return os.path.exists(self.path)

    def __repr__(self):
        return 'Path({})'.format(self.path)


def get_paths(root, regexes=None, ignore_case=True):
    '''Recursively list folders/files with regex matching. Also supports regex group naming.

    Args:
        root (str): Root directory.
        regexes ([str]): Regexes to match starting from current directory.

    Returns:
        [dict]: List of dicts with groupdict() and path.
    '''
    if not regexes:
        return []

    regex = regexes[0]
    all_paths = []
    for content in os.listdir(root):
        content_path = os.path.join(root, content)

        # Skip if there's more regexes and current one is not a folder.
        is_last = len(regexes) == 1
        if not is_last and not os.path.isdir(content_path):
            continue

        # Match by regex.
        kwargs = {'flags': re.IGNORECASE} if ignore_case else {}
        res = re.match(regex, content, **kwargs)

        if res:
            if is_last:
                path = Path()
                path.update(res.groupdict())
                path.path = content_path
                all_paths.append(path)
            else:
                paths = get_paths(content_path, regexes[1:])
                for path in paths:
                    path.update(res.groupdict())
                    all_paths.append(path)
    return all_paths
