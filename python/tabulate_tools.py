'''Tools extending tabulate module.'''

from collections import OrderedDict

from tabulate import tabulate

from my_settings import MAX_LINES


def print_tabulate(
        input_, keys=None, sorted_key=None, reverse=False, limit=MAX_LINES, headers='keys'):
    '''Wrapper around tabulate() to print table from dicts or dict of dicts with keys as headers.

    Args:
        input_ ([dict] or dict): Dict(s) to print.
        keys (list): Print only these keys as columns in this order. Print all keys if None.
            Supports char-delimited string for nested dicts.
        sorted_key (list of keys or whatever keys are): Key to sort rows by.
        reverse (bool): Reverse row sort order if True. Passed to sorted().
        limit (int): Limit number of results. Show all if negative.
        headers (str): Passed to tabulate(). Show keys as headers by difficult.
    '''
    if isinstance(input_, dict) and all(isinstance(val, dict) for val in input_.values()):
        # Convert dict of dicts to list of dicts with new 'key' value as key of original dict.
        # {
        #     'fruits': {'apple': 'red', 'banana': 'yellow'},
        #     'vegetables': {'kale': 'green'}
        # } =>
        # [
        #     {'key': 'fruits', 'apple': 'red', 'banana': 'yellow'},
        #     {'key': 'vegetables', 'kale': 'green'}
        # ]
        new_dicts = []
        for key, val in input_.iteritems():
            new_dict = OrderedDict()
            new_dict['key'] = key
            if isinstance(val, dict):
                for key_1, val_1 in val.iteritems():
                    new_dict[key_1] = val_1
            new_dicts.append(new_dict)
        dicts = new_dicts
    else:
        dicts = input_

    # Sort by specified key(s.
    if sorted_key:
        if isinstance(sorted_key, list):
            # List of keys to sort by.
            sorted_key_func = lambda x: tuple(get(x, key) for key in sorted_key)
        else:
            sorted_key_func = lambda x: x.get(sorted_key)
        dicts = sorted(dicts, key=sorted_key_func, reverse=reverse)

    # Filter to only specified keys in order.
    if keys:
        new_dicts = []
        for dict_ in dicts:
            new_dict = OrderedDict()
            for key in keys:
                new_dict[key] = get(dict_, key)
            new_dicts.append(new_dict)
    else:
        new_dicts = dicts

    # Limit rows to show.
    is_limited = False
    len_before_limit = -1
    if len(new_dicts) > limit >= 0:
        is_limited = True
        len_before_limit = len(new_dicts)
        new_dicts = new_dicts[:limit]

    # Print table.
    print(tabulate(new_dicts, headers))

    # Print results are limited.
    if is_limited:
        print('...')
        print('Only showing %i/%i results' % (limit, len_before_limit))
