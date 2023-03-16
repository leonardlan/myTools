'''Tools for reading/writing to files.'''


WRITE_ONLY_MODE = 'w'
APPEND_ONLY_MODE = 'a'


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


def write_file(file_path, lines, mode=WRITE_ONLY_MODE):
    '''Write lines to file.

    Args:
        file_path (str): File path.
        lines (str or [str]): Line or lines to write to file.
        mode (str): Mode to open file.
    '''
    content = '\n'.join(lines) if isinstance(lines, list) else lines
    with open(file_path, mode) as fil:
        fil.write(content)


def clear_file(file_path):
    '''Clears files.'''
    open(file_path, 'w').close()
