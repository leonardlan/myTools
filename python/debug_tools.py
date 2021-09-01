'''Debugging related tools.'''

import glob
import multiprocessing
import re


# Matches Python traceback with named capturing groups: 'exception' and 'message'.
# Example:
# Traceback (most recent call last):
#   File "<stdin>", line 1, in <module>
# NameError: name 'foo' is not defined
TRACEBACK_RE = r'''
    Traceback                                     # Traceback first line.
    [\s\S]+?                                      # Content.
    (?P<exception>[a-zA-Z]\w*):\ (?P<message>.*)  # Exception and message.
    '''
TRACEBACK_PATTERN = re.compile(TRACEBACK_RE, re.M | re.X)


def find_traceback(file_path):
    '''Find Python tracebacks in file.

    Args:
        file_path (str): File path.

    Returns:
        [dicts]: Traceback dicts with 'match', exception' (ie. 'NameError') and 'message'.
    '''
    tracebacks = []

    try:
        fil = open(file_path, 'r')
    except IOError, exception:
        print 'Unable to open {}: {}'.format(file_path, exception.strerror)
        return tracebacks

    with fil:
        content = fil.read()
        count = 0

        # Do preliminary check here to save time if file is too large and regex search takes a long
        # time.
        if 'Traceback' in content:
            # Do regex search.
            for match in TRACEBACK_PATTERN.finditer(content):
                result = {'match': match.group(0)}
                result.update(match.groupdict())
                tracebacks.append(result)
                count += 1

    return tracebacks


def find_traceback_in_files(file_paths, cpus=multiprocessing.cpu_count()):
    '''Find tracebacks in files using multiprocessing for faster results.

    Args:
        file_paths (str or [str]): File paths or str of file path passed to glob.
        cpus (int): Number of CPUs to use. Defaults to system CPUs.

    Returns:
        [[dict]]: List of results from find_traceback().
    '''
    if isinstance(file_paths, str):
        print 'Globbing {}...'.format(file_paths)
        file_paths = glob.glob(file_paths)
        print 'Found {} path(s)'.format(len(file_paths))

    pool = multiprocessing.Pool(cpus)
    return pool.map(find_traceback, file_paths)
