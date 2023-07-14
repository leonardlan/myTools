'''Tools for reading/writing to files.'''


import re


APPEND_ONLY_MODE = 'a'
READ_ONLY_MODE = 'r'
READ_WRITE_MODE = 'r+'
WRITE_ONLY_MODE = 'w'

MAX_LINE_LENGTH = 100

def read_file(
        file_path, print_lines=True, print_line_num=False, max_lines=None, max_line_len=100,
        return_lines=True):
    '''Read and print file with options.

    Args:
        file_path (str): File path.
        print_lines (bool): Print lines if True.
        print_line_num (bool): Print line number if True.
        max_lines (int or None): Max lines to print. No limit if None.
        max_line_len (int or None): Max characters to print per line. Adds ellipsis to end. No limit
            if None.
        return_lines (bool): Return lines if True.

    Raises:
        IOError: File does not exist.

    Returns:
        list or None: File content as lines.
    '''
    lines = []
    with open(file_path, 'r') as fil:
        for index, line in enumerate(fil):
            # Check if reached max_lines.
            if max_lines is not None and index + 1 > max_lines:
                print('...\nReached max lines: {}'.format(max_lines))
                break

            line = line.rstrip()
            lines.append(line)

            # Print line.
            if print_lines:
                # Cut down line if too long.
                if max_line_len is not None and len(line) > max_line_len:
                    line = '{}...'.format(line[0:max_line_len - 1])

                # Add line number.
                if print_line_num:
                    line = '{}: {}'.format(index + 1, line)

                print(line)

    if return_lines:
        return lines
    return None


def find_in_file(file_path, target, regex_match=False, first_only=True):
    '''Find target in file.

   Args:
        file_path (str): File path.
        target (str): Target as normal or regex search string.

   Kwargs:
        regex_match (bool): Use re.match() if True; use 'in' operator otherwise.

   Returns:
        (int, (str/re.Match)) or [(int, (str/re.Match))]: If first_only is True, returns tuple of
            first (zero-based) index that matches target and re.Match object if regex_match is True,
            else line with target. If first_only is False, returns list of above matched lines.
            Empty list if no matches.
    '''
    results = []
    with open(file_path, READ_ONLY_MODE) as fil:
        for index, line in enumerate(fil):
            if regex_match:
                res = re.match(target, line)
                if res:
                    if first_only:
                        return index, res
                    results.append((index, res))
            else:
                if target in line:
                    result = index, line.rstrip()
                    if first_only:
                        return result
                    results.append((result))
    return results


def write_file(file_path, lines, mode=WRITE_ONLY_MODE, encoding=None):
    '''Write lines to file.

    Args:
        file_path (str): File path.
        lines (str or [str]): Line or lines to write to file.
        mode (str): Mode to open file.
    '''
    content = '\n'.join(lines) if isinstance(lines, list) else lines
    with open(file_path, mode, encoding=encoding) as fil:
        fil.write(content)


def clear_file(file_path):
    '''Clears files.'''
    open(file_path, 'w').close()
