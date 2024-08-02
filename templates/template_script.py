'''Script title.

Details about this script.

Created: [Thu 2024-08-01 05:00 PM]

Example usage:

import template_script
reload(template_script)
results = template_script.run_on_multiple(template_script.ITEMS, dry_run=True, return_results=True)
'''

# Basic Python modules.
import os
import re
import time

# My tools.
from colors import bright_blue, green, red, yellow


# Global variables.
FOO = 'fee'


# Settings.
ITEMS = ['Corgi', 'Samoyed', 'Shiba Inu', 'Maltese', 'Shih Tzu']


# Cached variables that aren't reloaded on module reload.
if '_CACHED_VAR' not in globals():
    _CACHED_VAR = None


def run_on_one(item, dry_run=True):
    '''Run something on one item.'''
    print('Item: {}'.format(item))

    # Handle dry run.
    if dry_run:
        print(yellow('Not running in dry run'))
        return

    print('Doing something on item')


def run_on_multiple(items, dry_run=True, return_results=True):
    '''Run something on multiple items.'''
    total = len(items)
    results = []
    for ind, item in enumerate(items, start=1):
        print(bright_blue('\n[{}/{}] Item: {}'.format(ind, total, item)))
        res = run_on_one(item, dry_run=dry_run)
        results.append(res)

    if return_results:
        return results


# If running as a script.
if __name__ == '__main__':
    # Start timer.
    start_time = time.time()

    results = run_on_multiple(ITEMS)

    # End timer.
    duration = time.time() - start_time
    print('Finished running in {:.2f} seconds'.format(duration))
