'''Test tools.'''

import random
import time


def sleep_random(seconds):
    '''Sleeps for anywhere between 0 and input seconds.'''
    nap_time = random.uniform(0, seconds)
    time.sleep(nap_time)
    return 'Napped for {:.2f}/{} seconds'.format(nap_time, seconds)


def randomly_error(percentage=50):
    '''Randomly raises an exception given percentage of the time.

    Args:
        percentage (float): Percentage between 0 and 100.
    '''
    if random.random() < 0.01 * percentage:
        raise Exception('Randomly errored')
    return percentage


def infinite_loop():
    '''Hangs current process.'''
    while True:
        pass
