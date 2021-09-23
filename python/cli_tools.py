'''Useful functions in Python CLI (terminal, CMD, or Maya).'''

import datetime
import os
import re
import subprocess
import sys

from lancore import _is_text, var_name, human_int
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
            print 'Displayed first %i results...' % max_results
            break

        # Print path to value and value itself.
        path = ''
        for attr in result:
            if _is_text(attr):
                path += "['%s']" % attr
            else:
                path += '[%s]' % attr
        print '%s%s:' % (var_name(haystack), path),
        print eval('haystack%s' % path)
    num_results = len(results)
    if not first:
        info('Found %s result%s' % (human_int(num_results), 's' if num_results > 1 else ''))


def _find(haystack, needle, first, ignore_case):
    '''Recursive helper for find().'''
    results = []
    if isinstance(haystack, dict):
        iterable = sorted(haystack.iteritems())
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
                if _is_text(item) and _is_text(needle):
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


def print_sys_path(key=''):
    '''Print sys.path. Able to filter by case-insensitive search.'''
    count = 0
    for path in sys.path:
        if not key or key.lower() in path.lower():
            print path
            count += 1
    print '{} path{}'.format(count, 's' if count != 1 else '')


def ns(title='Hello!', msg=''):
    '''Sends a desktop notification.'''
    msg = msg or 'Have a good {}!'.format(datetime.datetime.now().strftime('%A'))
    if os.name == 'nt':
        # Attemp to use ToastNotifier (if installed) on Windows.
        try:
            from win10toast import ToastNotifier
        except ImportError:
            print 'No ToastNotifier module installed for notifications'
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
        clip.SetClipboardText(content, clip.CF_UNICODETEXT)
        clip.CloseClipboard()
    else:
        if content is None:
            return clipboard.paste()
        clipboard.copy(str(content))


def cb(content=None, as_int=False, as_ints=False):
    '''Copies content to clipboard. If no content, returns clipboard content as string.
    Supports Windows and Linux.

    Args:
        content (str): Content to copy to clipboard.
        as_int (bool): Returns first integer in clipboard as int if True. Raises ValueError if
            no integers.
        as_ints (bool): Returns list of integers in clipboard if True. Raises ValueError if no
            integers.
    '''
    res = _cb(content=content)

    if content is None:
        if as_int or as_ints:
            ints = re.findall(r'\d+', res)  # Find all integers.
            if ints:
                if as_int:
                    return int(ints[0])
                return [int(num) for num in ints]
            raise ValueError('No integer found in clipboard')

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
