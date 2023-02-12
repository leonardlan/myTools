'''Useful functions for lists.'''


from collections import Counter


def print_duplicates(my_list, ignore_case=False):
    '''Print duplicates in list.

    Args:
        my_list (list): List of items to find duplicates in.
        ignore_case (bool): If True, case-insensitive when finding duplicates.

    Returns:
        None

    Example:
    >>> print_duplicates([1, 2, 3, 3, 3, 'a', 'a', 'b', 'B', 'b', 'c'], ignore_case=True)
    3 appears 3 times
    b appears 3 times
    a appears 2 times
    '''
    # Handle ignore_case.
    if ignore_case:
        my_list = [item.lower() if hasattr(item, 'lower') else item for item in my_list]

    counter = Counter(my_list)
    duplicated_count = 0
    for item, count in counter.most_common():
        if count == 1:
            break
        print('{} appears {} times'.format(item, count))
        duplicated_count += 1

    print('Found {} duplicate(s)'.format(duplicated_count))
