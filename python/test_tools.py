'''Tools for simulating long processes, randomly erroring, infinite-loop hangs, memory leaks, and
CPU-overload situations. Run with caution.
'''

import multiprocessing
import random
import sys
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
    print 'Hanging in infinite loop...'
    while True:
        pass


def memory_leak():
    '''Infinite loop with memory leak.

    Run this and watch machine memory increase. Once maxed, it'll start writing to disk. Will also
    slow down all other apps. To go back to normal, force quit the terminal.

    Creates list where every value is the previous value times two. Can quit with Ctrl+C but will
    have to close session to clear memory.
    '''
    print 'Starting memory leak...'
    items = [2]
    while True:
        items.append(items[-1] * 2)


def memory_leak_2():
    print 'Starting memory leak...'
    '''Infinite loop with memory leak. Memory rises slower than memory_leak().'''
    while True:
        def func(): pass
        func.__doc__ = func


def overload_cpu():
    '''Maximize usage on all CPUs. Creates a pool and runs infinite loop of calcuations.'''
    cpus = multiprocessing.cpu_count()
    pool = multiprocessing.Pool(processes=cpus)
    print 'Overloading {} CPUs. Quit with Ctrl+C...'.format(cpus)
    res = pool.map(_overload_cpu, [2] * cpus)


def _overload_cpu(x):
    '''Infinite loop with calculation.'''
    while True:
        x * x


def crash():
    '''Crashes current Python session using recursion.

    Popup error will say "python.exe has stopped working."
    '''
    sys.setrecursionlimit(999999999)
    def func():
        func()
    print 'Crashing using recursion...'
    func()
