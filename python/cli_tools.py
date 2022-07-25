'''Useful functions in Python CLI (terminal, CMD, or Maya).'''

from __future__ import print_function

import datetime
import os
import re
import subprocess
import sys
import time

from lancore import var_name, human_int, human_time, my_timestamp
from my_logging import info
from python_compat import is_string


def find(haystack, needle, all=False, first=False, ignore_case=True, max_results=50):
    '''Prints path to needle in iterable haystack (can be nested list or dict).

    Example:
        >>> haystack = {
            'fruits': [
                {'color': 'yellow', 'name': 'banana'},
                {'color': 'red', 'name': 'strawberry'},
                {'color': 'yellow', 'name': 'lemon'}],
            'vegetables': [
                {'color': 'green', 'name': 'green pepper'}
        ]}

        >>> find(haystack, 'pepper')
        INFO: Searching...
        haystack['vegetables'][0]['name']: green pepper
        INFO: Found 1 result

        >>> haystack['vegetables'][0]['name']
        'green pepper'

        >>> find(haystack, 'cucumber')
        INFO: Searching...
        INFO: Not found

        >>> find(haystack, 'yellow')
        INFO: Searching...
        haystack['fruits'][0]['color']: yellow
        haystack['fruits'][2]['color']: yellow
        INFO: Found 2 results

        # Case-sensitive
        >>> find(haystack, 'YeLLow', ignore_case=False)
        INFO: Searching...
        INFO: Not found

    Args:
        haystack (dict or list): Nested dict or list.
        needle (anything): Target to find.
        all (bool): Shows all results if True. Up to max_results otherwise.
        first (bool): Returns first result if True. All results otherwise.
        ignore_case (bool): Case-insensitive if True.
        max_results (int): Max number of results to return. Unlimited if negative or zero.
    '''
    info('Searching...')
    all_ = all
    results = _find(haystack, needle, first, ignore_case)
    if not results:
        info('Not found')
        return
    for index, result in enumerate(results):
        if not all_ and index >= max_results > 0:
            # Max number of results reached.
            print('Displayed first %i results...' % max_results)
            break

        # Print path to value and value itself.
        path = ''
        for attr in result:
            if is_string(attr):
                path += "['%s']" % attr
            else:
                path += '[%s]' % attr
        print('%s%s:' % (var_name(haystack), path), end=' ')
        print(eval('haystack%s' % path))
    num_results = len(results)
    if not first:
        info('Found %s result%s' % (human_int(num_results), 's' if num_results > 1 else ''))


def _find(haystack, needle, first, ignore_case):
    '''Recursive helper for find().'''
    results = []
    if isinstance(haystack, dict):
        iterable = sorted(haystack.items())
    elif isinstance(haystack, list):
        iterable = enumerate(haystack)
    else:
        # Not sure how to iterate or if iterable.
        return results

    for key, val in iterable:
        # Check both key and val.
        for item in [key, val]:
            if isinstance(item, (dict, list)):
                # It's a dict/list. Check recursively.
                recursive_results = _find(item, needle, first, ignore_case)
                if recursive_results:
                    results.extend([[key] + res for res in recursive_results])
                    if first:
                        return results
                    if item == key:
                        break
            elif item == needle:
                # Found exact match.
                results.append([key])
                if first:
                    return results
                if item == key:
                    break
            elif item:
                # Check if in text.
                if is_string(item) and is_string(needle):
                    if ignore_case:
                        if needle.lower() in item.lower():
                            # Is text and in item, case-insensitive.
                            results.append([key])
                            if first:
                                return results
                            if item == key:
                                break
                    else:
                        if needle in item:
                            # Is text and in item, case-sensitive.
                            results.append([key])
                            if first:
                                return results
                            if item == key:
                                break

    return results


DEFAULT_DELIMITER = ' '


def get(data, *keys, **kwargs):
    '''Get value in nested dict/list. keys can be path to value or space-delimited string.
    Returns None if not found.

    >>> data = {
        'fruits': [
            {'color': 'yellow', 'name': 'banana'},
            {'color': 'red', 'name': 'strawberry'},
            {'color': 'yellow', 'name': 'lemon'}
        ],
        'vegetables': [
            {'color': 'green', 'name': 'green pepper'}
        ]}
    >>> get(data, 'fruits', 0, 'color')
    'yellow'

    Can also pass string with any delimiter
    >>> get(data, 'vegetables 0 name')
    'green pepper'

    Args:
        keys (list or str): Keys of path to value. Can also be string of keys separated by space
            delimiter.
        delimiter (str): Delimiter for when keys is string. Defaults to space.

    Returns:
        any: Value found or None. Returns original data if no keys provided.
    '''
    delimiter = kwargs.get('delimiter', DEFAULT_DELIMITER)

    # Split keys up if keys is 1 string of delimited keys.
    if len(keys) == 1 and keys[0] not in data and is_string(keys[0], str):
        keys = keys[0].split(delimiter)

    # Iterate keys to find value.
    for key in keys:
        # Convert key to int if data is list.
        if isinstance(data, list):
            try:
                key = int(key)
            except ValueError:
                return

        try:
            data = data[key]
        except (KeyError, TypeError):
            return
    return data


def print_env_vars(filter_=''):
    '''Print os.environ. Able to filter by case-insensitive search.'''
    count = 0
    for key in sorted(os.environ):
        filter_lower = filter_.lower()
        val = os.environ[key]
        if not filter_ or filter_lower in key.lower() or filter_lower in val.lower():
            if ';' in val:
                # Split paths by semi-colon. Probably list of paths.
                paths = val.split(';')
                print('{} ({}):\n\t{}'.format(key, len(paths), '\n\t'.join(paths)))
            else:
                print('{}: {}'.format(key, val))
            count += 1
    print('{} env var{}'.format(count, 's' if count != 1 else ''))


def print_sys_path(key=''):
    '''Print sys.path. Able to filter by case-insensitive search.'''
    count = 0
    for path in sys.path:
        if not key or key.lower() in path.lower():
            print(path)
            count += 1
    print('{} path{}'.format(count, 's' if count != 1 else ''))


def ns(title='Hello!', msg=''):
    '''Sends a desktop notification.'''
    msg = msg or 'Have a good {}!'.format(datetime.datetime.now().strftime('%A'))
    if os.name == 'nt':
        # Attemp to use ToastNotifier (if installed) on Windows.
        try:
            from win10toast import ToastNotifier
        except ImportError:
            print('No ToastNotifier module installed for notifications')
        else:
            toaster = ToastNotifier()
            toaster.show_toast(title=title, msg=msg, threaded=True)
    else:
        subprocess.call("ns '%s'" % msg, shell=True)


def _cb(content=None):
    '''Helper for cb().'''
    try:
        import clipboard, pyperclip
    except ImportError:
        # Try win32clipboard.
        import win32clipboard as clip
        clip.OpenClipboard()

        if content is None:
            # Return clipboard content.
            data = clip.GetClipboardData()
            clip.CloseClipboard()
            return data

        # Copy content to clipboard.
        clip.EmptyClipboard()
        clip.SetClipboardText(str(content), clip.CF_UNICODETEXT)
        clip.CloseClipboard()
    else:
        if content is None:
            return clipboard.paste()
        clipboard.copy(str(content))


def cb(content=None, type='string', delimiter='\n'):
    '''Copies content to clipboard. If no content, returns clipboard content as string.
    Supports Windows and Linux.

    Args:
        content (str): Content to copy to clipboard.
        type (str): Type of content. One of "string", "strings", "int", "ints".
            string: String as is.
            strings: String split by delimiter, defaults to newline.
            int: First integer as int.
            ints: Integers.
        delimiter (str): Delimiter to separate clipboard text. Defaults to newline.
    '''
    res = _cb(content=content)

    type = type.lower()
    if type not in ['string', 'strings', 'int', 'ints']:
        raise ValueError('Unrecognized type: {}'.format(type))

    if content is None:
        if type in ['int', 'ints']:
            ints = re.findall(r'\d+', res)  # Find all integers.
            if ints:
                if type == 'int':
                    return int(ints[0])
                return [int(num) for num in ints]
            raise ValueError('No integer found in clipboard')
        elif type == 'strings':
            # Strings split by delimiter. Filter out empty strings.
            strings = []
            for line in res.split(delimiter):
                line = line.strip()
                if line:
                    strings.append(str(line))
            return strings
        return str(res)


def cb_strings(delimiter='\n'):
    return cb(type='strings', delimiter=delimiter)


def confirm(question):
    '''True if user confirms yes/no question. False otherwise. Will keep asking if not y/n.'''
    reply = str(raw_input('{} (y/n): '.format(question))).lower().strip()
    if reply:
        if reply[0] == 'y':
            return True
        if reply[0] == 'n':
            return False
    return confirm('Please enter')


def diff_lists(apples, oranges):
    '''Print difference between two dicts (apples vs. oranges).

    Example:
    >>> diff_lists(['BMW', 'Toyota'], ['Mercedes', 'Toyota', 'Tesla'])
    Apple only (1):
        BMW
    Orange only (2):
        Mercedes
        Tesla
    '''
    oranges_set = set(oranges)
    apple_only = [x for x in apples if x not in oranges_set]
    if apple_only:
        print('Apple only ({}):'.format(len(apple_only)))
        for item in apple_only:
            print('\t{}'.format(item))

    apples_set = set(apples)
    orange_only = [x for x in oranges if x not in apples_set]
    if orange_only:
        print('Orange only ({}):'.format(len(orange_only)))
        for item in orange_only:
            print('\t{}'.format(item))


def diff_dicts(apple, orange):
    '''Print difference between two dicts (apple vs. orange).

    Example:
    >>> diff_dicts(
        {'a': 1, 'c': 3, 'name': 'Andrew', 'age': 20},
        {'a': 1, 'b': 2, 'name': 'Mark', 'age': 25})
    Key age: 20 | 25
    Key name: Andrew | Mark
    Apple only keys (1)
            c: 3
    Orange only keys (1)
            b: 2
    '''
    apple_only_keys = []
    for key in apple:
        if key not in orange:
            apple_only_keys.append(key)
        else:
            apple_val = apple[key]
            orange_val = orange[key]
            if apple_val != orange_val:
                # Print different values.
                print('Key {}: {} | {}'.format(key, apple_val, orange_val))

    # Print mutually exclusive keys.
    if apple_only_keys:
        print('Apple only keys ({}):'.format(len(apple_only_keys)))
        for key in apple_only_keys:
            print('\t{}: {}'.format(key, apple[key]))
    orange_only_keys = set(orange.keys()) - set(apple.keys())
    if orange_only_keys:
        print('Orange only keys ({}):'.format(len(orange_only_keys)))
        for key in orange_only_keys:
            print('\t{}: {}'.format(key, orange[key]))


def diff(apple, orange):
    '''Print difference between two dicts/lists (apple vs. orange). Non-recursive.'''
    if isinstance(apple, list) and isinstance(orange, list):
        diff_lists(apple, orange)
    elif isinstance(apple, dict) and isinstance(orange, dict):
        diff_dicts(apple, orange)
    else:
        print('Cannot diff type {} and type {}'.format(type(apple), type(orange)))


class Timer(object):
    '''Run function call every sleep_seconds seconds. Can cancel with Ctrl+C.

    Simple print time every 10 seconds example:
    >>> def print_time():
            msg = 'Hello! The time is {}'.format(datetime.datetime.now())
            print(msg)
            return msg
    >>> timer = Timer(print_time, 10)
    >>> timer
    Timer(func=print_time, sleep_seconds=10)
    >>> timer.run()
    -------------------- 1 --------------------
    Hello! The time is 2022-05-26 23:17:33.236474
    [2022-05-26 23:17:33] Function call finished in 0 seconds
    Sleeping for 10 seconds...
    -------------------- 2 --------------------
    Hello! The time is 2022-05-26 23:17:43.242285
    [2022-05-26 23:17:43] Function call finished in 0 seconds
    Sleeping for 10 seconds...

    Stop at a specific return value.
    >>> def rand_int():
            val = random.randint(1, 4)
            print(val)
            return val
    >>> timer = Timer(rand_int, 2, stop_on_result=True, final_result=2)
    >>> timer.run()
    -------------------- 1 --------------------
    1
    [2022-05-26 23:14:52] Function call finished in 6.0 milliseconds
    Sleeping for 2 seconds...
    -------------------- 2 --------------------
    1
    [2022-05-26 23:14:54] Function call finished in 0 seconds
    Sleeping for 2 seconds...
    -------------------- 3 --------------------
    4
    [2022-05-26 23:14:56] Function call finished in 0 seconds
    Sleeping for 2 seconds...
    -------------------- 4 --------------------
    2
    [2022-05-26 23:14:58] Function call finished in 0 seconds
    Stopping on result 2
    '''

    def __init__(
            self, func, sleep_seconds, keep_results=True, stop_on_result=False, final_result=None,
            *args, **kwargs):
        self.func = func
        self.sleep_seconds = sleep_seconds
        self.keep_results = keep_results
        self.stop_on_result = stop_on_result
        self.final_result = final_result
        self.args = args
        self.kwargs = kwargs
        self.results = []
        self.run_times = []

    def __repr__(self):
        return 'Timer(func={}, sleep_seconds={})'.format(
            self.func.__name__, self.sleep_seconds)

    @property
    def times_ran(self):
        '''Number of times function was called.'''
        return len(self.run_times)

    def run(self):
        count = 1
        while True:
            print('{} {} {}'.format('-' * 20, count, '-' * 20))

            start = time.time()
            res = self.func(*self.args, **self.kwargs)
            run_time = time.time() - start

            print('[{}] Function call finished in {}'.format(my_timestamp(), human_time(run_time)))
            if self.keep_results:
                self.results.append(res)
            self.run_times.append(run_time)

            if self.stop_on_result and res == self.final_result:
                print('Stopping on result :{}'.format(self.final_result))
                break

            # Sleep for some time.
            print('Sleeping for {}...'.format(human_time(self.sleep_seconds)))
            time.sleep(self.sleep_seconds)

            count += 1
