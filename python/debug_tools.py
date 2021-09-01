'''Debugging related tools.'''

import glob
import multiprocessing
import random
import re
import time


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
        return (tracebacks, 'Unable to open {}: {}'.format(file_path, exception.strerror))

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

    return (tracebacks, '')


def find_traceback_in_files(file_paths, cpus=multiprocessing.cpu_count()):
    '''Find tracebacks in files using multiprocessing for faster results.

    Args:
        file_paths (str or [str]): File paths or str of file path passed to glob.
        cpus (int): Number of CPUs to use. Defaults to system CPUs.

    Returns:
        [[dict]]: List of results from find_traceback().
    '''
    return call_function(find_traceback, file_paths, cpus=cpus)


def call_function(func, args, cpus=multiprocessing.cpu_count()):
    '''Call function on list of single arguments using multiprocessing.

    Uses imap_unordered() to print progress after each call, instead of having to wait for all calls
    to finish.

    Args:
        func (func(arg)): Function to call that takes a single argument. If string, will assume it's
            a path and glob for list of paths.
            Returns a tuple of two. First one is the result. Second one is a string to print after
            function call. Makes it easier to see progress.
        args (str or [str]): File paths or str of file path to glob.
        cpus (int): Number of CPUs to use. Defaults to system CPUs.

    Returns:
        list: List of results from function call. None if failed.
    '''
    if isinstance(args, str):
        print 'Globbing "{}"...'.format(args)
        args = glob.glob(args)
        print 'Found {} path(s)'.format(len(args))

    # Launch multiprocessing pool.
    pool = multiprocessing.Pool(processes=cpus)
    results = []
    num_files = len(args)
    for ind, result in enumerate(pool.imap_unordered(func, args)):
        # Print progress.
        to_print = ''
        if isinstance(result, tuple) and len(result) == 2:
            result, to_print = result
        print '{}/{}: {}'.format(ind + 1, num_files, to_print)

        results.append(result)
    return results


def sleep_random(seconds):
    '''Sleeps random seconds between 0 and input seconds.'''
    nap_time = random.uniform(0, seconds)
    time.sleep(nap_time)
    return nap_time, 'Napped for {:.2f} seconds'.format(nap_time)
