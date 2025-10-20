'''Tools for simulating long processes, randomly erroring, infinite-loop hangs, memory leaks,
overloading CPU and disk writing situations. Run with caution.
'''

import multiprocessing
import os
import random
import sys
import time


# Most Python errors.
# Note, Exception does not catch these exceptions: GeneratorExit, KeyboardInterrupt, SystemExit.
# BaseException will catch them all.
PYTHON_ERRORS = [AssertionError, AttributeError, EOFError, FloatingPointError, GeneratorExit,
    ImportError, IndexError, KeyError, KeyboardInterrupt, MemoryError, NameError,
    NotImplementedError, OSError, OverflowError, ReferenceError, RuntimeError, StopIteration,
    SyntaxError, IndentationError, TabError, SystemError, SystemExit, TypeError, UnboundLocalError,
    UnicodeEncodeError, UnicodeDecodeError, UnicodeTranslateError, ValueError, ZeroDivisionError]


def sleep_random(seconds=5):
    '''Sleeps for anywhere between 0 and input seconds. Returns seconds slept.'''
    if seconds <= 0:
        return 0
    nap_time = random.uniform(0, seconds)
    print('Sleeping for {:.2f}/{} seconds...'.format(nap_time, seconds))
    time.sleep(nap_time)
    return seconds


def randomly_error(percentage=50):
    '''Randomly raises a random Python exception, given percentage of the time.

    Args:
        percentage (float): Percentage between 0 and 100.
    '''
    if random.random() < 0.01 * percentage:
        exception = random.choice(PYTHON_ERRORS)
        raise exception('Randomly raising {}'.format(exception.__name__))
    return percentage


def infinite_loop():
    '''Hangs current process. Session will have high power usage.'''
    print('Hanging in infinite loop...')
    while True:
        pass


def memory_leak():
    '''Infinite loop with memory leak.

    Run this and watch machine memory increase. Once maxed, it'll start writing to disk. Will also
    slow down all other apps. To go back to normal, force quit the terminal.

    Creates list where every value is the previous value times two. Can quit with Ctrl+C but will
    have to close session to clear memory.
    '''
    print('Starting memory leak...')
    print('Force quit terminal to stop.')
    items = [2]
    while True:
        items.append(items[-1] * 2)


def memory_leak_2():
    '''Infinite loop with memory leak. Memory rises slower than memory_leak().'''
    print('Starting memory leak...')
    print('Ctrl+C to stop.')
    while True:
        def func(): pass
        func.__doc__ = func


def overload_cpu():
    '''Maximize usage on all CPUs. Creates a pool and runs infinite loop of calcuations.'''
    cpus = multiprocessing.cpu_count()
    pool = multiprocessing.Pool(processes=cpus)
    print('Overloading {} CPUs. Quit with Ctrl+C...'.format(cpus))
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
    print('Crashing using recursion...')
    func()


def overload_write(num_chars=10000, char='a', file_path='test.txt'):
    '''Overload disk write by writing an increasing line of characters to a file. The disk graph in
    Task Manager should start rising with fluctuations, until it maxes out. Quit with Ctrl+C.

    Kwargs:
        num_chars (int): Positive integer of number of characters to start and increment with. Can
            use 1 for slowest rise in disk write.
        char (str): Character to write with.
        file_path (str): Path to file to write to.
    '''
    increment = char * num_chars
    line = increment
    print('Writing temp file to {} ...'.format(os.path.abspath(file_path)))
    with open(file_path, 'w') as f:
        while True:
            f.write('{}\n'.format(line))
            line += increment
