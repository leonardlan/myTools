'''Useful functions for lists.'''


from collections import Counter


def print_duplicates(my_list):
    '''Print duplicates in list.

    Args:
        my_list (list): List of items to find duplicates in.

    Returns:
        None

    Example:
    >>> print_duplicates(['a', 'a', 'b', 'b', 'b', 'c'])
    b appears 3 times
    a appears 2 times
    '''
    counter = Counter(my_list)
    for item, count in counter.most_common():
        if count == 1:
            break
        print('{} appears {} times'.format(item, count))
