'''Functions to add colors to make content more user-readable in CLI.'''


import colors


def get_colored_diff(s1, s2, s1_color_func=colors.bright_red, s2_color_func=colors.green):
    '''Given two strings s1 and s2, returns new string with any differing characters between the two
    strings highlighted in red (s1) and green (s2). Useful for showing capitalization changes on a
    string. If both strings are not similar at all, print in "red(s1)" -> "green(s2)".

    Args:
        s1 (str): First string.
        s2 (str): Second string.

    Returns:
        str: String with colored red/green showing difference between s1 (red) and s2 (gree).
    '''
    # Handle both equal.
    if s1 == s2:
        return '"{}"'.format(s1)

    # Handle either string empty.
    if not s1:
        return '"" -> "{}"'.format(s2_color_func(s2))
    if not s2:
        return '"{}" -> ""'.format(s1_color_func(s1))

    s1, s2 = str(s1), str(s2)

    # Compare by iterating over shorter string.
    res = ''
    diff_count = 0
    min_len = min(len(s1), len(s2))
    for i in range(min_len):
        if s1[i] != s2[i]:
            res += s1_color_func(s1[i])  # Print red character from s1.
            res += s2_color_func(s2[i])  # Print green character from s2.
            diff_count += 1
        else:
            res += s1[i]  # Print regular character if no difference.

    # If both strings are too different (over 50%), print in different format.
    if float(diff_count) / min_len > 0.5:
        return '"{}" -> "{}"'.format(s1_color_func(s1), s2_color_func(s2))

    # Add on an extra missing characters from s1 or s2.
    if min_len < len(s1):
        res += s1_color_func(s1[min_len:])
    elif min_len < len(s2):
        res += s2_color_func(s2[min_len:])

    return res


def print_colored_diff(s1, s2):
    print(get_colored_diff(s1, s2))
