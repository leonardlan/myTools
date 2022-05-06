'''Useful functions in Python CLI (terminal, CMD, or Maya).'''

from __future__ import print_function

import datetime
import os
import re
import subprocess
import sys

from lancore import var_name, human_int
from my_logging import info


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
            if isinstance(attr, str):
                path += "['%s']" % attr
            else:
                path += '[%s]' % attr
        print('%s%s:' % (var_name(haystack), path), end='')
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
                if isinstance(item, str) and isinstance(needle, str):
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
    if len(keys) == 1 and keys[0] not in data and isinstance(keys[0], str):
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


def cb(content=None, type='string'):
    '''Copies content to clipboard. If no content, returns clipboard content as string.
    Supports Windows and Linux.

    Args:
        content (str): Content to copy to clipboard.
        type (str): Type of content. One of "string", "strings", "int", "ints".
            string: String as is.
            strings: String split by newline.
            int: First integer as int.
            ints: Integers.
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
            # Strings split by newline. Filter out empty strings.
            strings = []
            for line in res.split('\n'):
                line = line.strip()
                if line:
                    strings.append(str(line))
            return strings
        return str(res)


def confirm(question):
    '''True if user confirms yes/no question. False otherwise. Will keep asking if not y/n.'''
    reply = str(raw_input('{} (y/n): '.format(question))).lower().strip()
    if reply:
        if reply[0] == 'y':
            return True
        if reply[0] == 'n':
            return False
    return confirm('Please enter')


def diff(apple, orange):
    '''Print difference between two dicts (apple vs. orange).

    Example:
    >>> diff(
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
