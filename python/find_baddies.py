'''Contains find_baddies().

Example:
>>> items = [1, 2, 3, 4, 5, 'fail1', 6, 7, 8, 9, 10, 'fail2']
>>> res = find_baddies(squared_list, items, exception=TypeError)
Items: 12
Checking first half...
        Items: 6
        Checking second half...
                Items: 3
                Checking second half...
                        Items: 2
                        Found fail1
Checking second half...
        Items: 6
        Checking second half...
                Items: 3
                Checking second half...
                        Items: 2
                        Found fail2
>>> print(res)
['fail1', 'fail2']
'''


def find_baddies(func, items, exception=Exception, **func_kwargs):
    '''Uses divide-and-conquer algorithm to find all bad items in given list of items, when being
    passed to a black-box func(items, **func_kwargs).

    Space complexity: O(n).
    Time complexity: O(n * log(n)).
    * n is number of items.

    Use this when you're running a function call on a list of items, but it's raising an exception
    without telling you which one(s) failed. You could iterate through items, but that would cost
    O(n) time complexity.

    Args:
        func (func): Function that's failing.
        items (list): Items to pass to func as first argument.

    Kwargs:
        exception (exception): Exception thrown from function call.
        func_kwargs (dict): Keyword arguments to pass to function.

    Returns:
        list: Items that fail the function call.
    '''
    return _find_baddies(func, items, exception, 0, **func_kwargs)


def _find_baddies(func, items, exception, level, **func_kwargs):
    '''Recursive helper for find_baddies().'''
    indent = '\t' * level
    print('{}Items: {}'.format(indent, len(items)))

    baddies = []
    halfway = int(len(items) / 2)

    # Check first half.
    first_half = items[0:halfway]
    res = _check_half(func, first_half, 'first', exception, level, indent, **func_kwargs)
    if res:
        baddies.extend(res)

    # Check second half.
    second_half = items[halfway:]
    res = _check_half(func, second_half, 'second', exception, level, indent, **func_kwargs)
    if res:
        baddies.extend(res)

    return baddies


def _check_half(func, half, first_or_second, exception, level, indent, **func_kwargs):
    '''Run func on this half of arguments.'''
    try:
        func(half, **func_kwargs)
    except exception:
        if len(half) == 1:
            # Found a baddie.
            print('{}Found {}'.format(indent, half[0]))
            return half
        else:
            print('{}Checking {} half...'.format(indent, first_or_second))
            res = _find_baddies(func, half, exception, level + 1)
            return res


# Example func:
def squared_list(ints):
    '''Returns list with every item squared.'''
    return [num * num for num in ints]
