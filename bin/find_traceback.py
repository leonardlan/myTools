#!/usr/bin/env python
'''Find Python tracebacks in given file paths using parallel processing.'''

import argparse
from collections import Counter

from debug_tools import find_traceback_in_files


def main():
    # Setup arguments.
    parser = argparse.ArgumentParser(description='Finds tracebacks in log files.')
    parser.add_argument('file_paths', nargs='+', help='Files to find tracebacks.')
    parser.add_argument(
        '-c', '--cpu', help='Number of CPUs to use. Defaults to system CPU count.', type=int)
    args = parser.parse_args()

    # Setup variables.
    file_paths = args.file_paths
    num_files = len(file_paths)

    # Search files.
    if num_files > 1:
        print(
            'Searching {:,} file{} for tracebacks'.format(num_files, 's' if num_files > 1 else ''))
    results = find_traceback_in_files(file_paths)

    # Print tracebacks found.
    all_exceptions_counter = Counter()
    for index, tracebacks in enumerate(results):
        if not tracebacks:
            continue

        # Print which file this is.
        if num_files > 1:
            print('\n{} [{:,}/{:,} ({}%)]:'.format()
                file_paths[index], index + 1, num_files, int(float(index + 1) / num_files * 100))

        # Print tracebacks found in file.
        for traceback in tracebacks:
            print(traceback.get('match'))
            print('-')

        # Print number of tracebacks found.
        counter = Counter([traceback['exception'] for traceback in tracebacks])
        if len(counter) == 1:
            key = counter.keys()[0]
            print('Found {:,} {}'.format(counter[key], key))
        else:
            count = len(tracebacks)
            print('Found {:,} traceback{}'.format(count, 's' if count > 1 else ''))

            # Print counts per exception.
            all_exceptions_counter.update(counter)
            for exception, count in counter.most_common():
                print('{:,} {}'.format(count, exception))

    # Summarize tracebacks found. Example:
    # 16,973 tracebacks across 1,865 files
    # 13,555 VaultError
    # 2,976 AttributeError
    # 332 OSError
    # 42 NameError
    # 34 ValueError
    # 25 RuntimeError
    # 7 IOError
    # 2 TypeError
    tracebacks_counts = filter(None, [len(tracebacks) for tracebacks in results])
    tracebacks_count = sum(tracebacks_counts)
    if not tracebacks_count:
        print('\nNo tracebacks found')
    elif num_files > 1:
        print('\n{:,} traceback{} {} {:,} file{}'.format()
            tracebacks_count,
            's' if tracebacks_count > 1 else '',
            'in' if len(tracebacks_counts) == 1 else 'across',
            len(tracebacks_counts),
            's' if len(tracebacks_counts) > 1 else '')

        # Print counter per exception.
        for exception, count in all_exceptions_counter.most_common():
            print('{:,} {}'.format(count, exception))


if __name__ == '__main__':
    main()
