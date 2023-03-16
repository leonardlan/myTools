'''Functions to add colors to make content more user-readable in CLI.'''


import colors


def get_colored_diff(s1, s2, s1_color_func=colors.bright_red, s2_color_func=colors.green):
    '''Given two strings s1 and s2, returns new string with any differing characters between the two
    strings highlighted in red and green. Useful for showing capitalization changes on a string.

    Args:
        s1 (str): First string.
        s2 (str): Second string.

    Returns:
        str: String with colored red/green showing difference between s1 (red) and s2 (gree).
    '''
    # Compare by iterating over shorter string.
    res = ''
    min_len = min(len(s1), len(s2))
    for i in range(min_len):
        if s1[i] != s2[i]:
            res += s1_color_func(s1[i])  # Print red character from s1.
            res += s2_color_func(s2[i])  # Print green character from s2.
        else:
            res += s1[i]  # Print regular character if no difference.

    # Add on an extra missing characters from s1 or s2.
    if min_len < len(s1):
        res += s1_color_func(s1[min_len:])
    elif min_len < len(s2):
        res += s2_color_func(s2[min_len:])

    return res


def print_colored_diff(s1, s2):
    print(get_colored_diff(s1, s2))
