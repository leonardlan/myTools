'''My useful core functions.'''
import datetime
import os
import sys
import time
import traceback
from functools import wraps

from collections import OrderedDict, defaultdict, Counter

from my_logging import debug, info, warning, error, critical, demo_logging


INTERVALS = OrderedDict([
    ('millennium', 31536000000),  # 60 * 60 * 24 * 365 * 1000
    ('century', 3153600000),      # 60 * 60 * 24 * 365 * 100
    ('year', 31536000),           # 60 * 60 * 24 * 365
    ('month', 2627424),           # 60 * 60 * 24 * 30.41 (assuming 30.41 days in a month)
    ('week', 604800),             # 60 * 60 * 24 * 7
    ('day', 86400),               # 60 * 60 * 24
    ('hour', 3600),               # 60 * 60
    ('minute', 60),
    ('second', 1)
])
HOME = os.environ['HOME'] if sys.platform.startswith('linux') else os.environ['USERPROFILE']
MYTOOLS = os.path.join(HOME, 'myTools')
LESS_THAN_A_SECOND = [
    'millisecond',
    'microsecond',
]


def human_time(seconds, decimals=1):
    '''Human-readable time from seconds (ie. 3600 -> '1 hour').

    Examples:
        >>> human_time(15)
        '15 seconds'
        >>> human_time(60)
        '1 minute'
        >>> human_time(3600)
        '1 hour'
        >>> human_time(3720)
        '1 hour and 2 minutes'
        >>> human_time(266400)
        '3 days and 2 hours'
        >>> human_time(12345678890)
        '39 years and 1 month'

        >>> human_time(-1.5)
        '-1.5 seconds'
        >>> human_time(0)
        '0 seconds'

        Less than a second.
        >>> human_time(0.1)
        '100 milliseconds'
        >>> human_time(1.1e-6)
        '1.1 microseconds'

        >>> human_time(1)
        '1 second'
        >>> human_time(1.234, 2)
        '1.23 seconds'

    Args:
        seconds (int or float): Duration in seconds.
        decimals (int): Number of decimals. Only applies 0 < seconds < 60.

    Returns:
        str: Human-readable time.
    '''
    is_int = isinstance(seconds, int)
    if seconds < 0:
        # Negative time.
        return str(seconds if is_int else round(seconds, decimals)) + ' seconds'
    elif seconds == 0:
        # Zero time.
        return '0 seconds'
    elif 0 < seconds < 1:
        # Less than a second.
        for interval in LESS_THAN_A_SECOND:
            seconds *= 1000
            quotient, remainder = divmod(seconds, 1)
            if quotient > 0:
                if remainder == 0:
                    res = int(quotient)
                else:
                    res = round(seconds, decimals)
                return '%s %s%s' % (str(res), interval, 's' if res != 1 else '')
        # Less than a microsecond.
        return '0 seconds'
    elif 1 < seconds < INTERVALS['minute']:
        # A second to a minute.
        return str(seconds if is_int else round(seconds, decimals)) + ' seconds'

    res = []
    for interval, count in INTERVALS.iteritems():
        quotient, remainder = divmod(seconds, count)
        if quotient >= 1:
            seconds = remainder
            if quotient > 1:
                # Plurals.
                if interval == 'millennium':
                    interval = 'millennia'
                elif interval == 'century':
                    interval = 'centuries'
                else:
                    interval += 's'
            res.append('%i %s' % (int(quotient), interval))
        if remainder == 0:
            break

    if len(res) >= 2:
        # Only shows 2 most important intervals.
        return '{} and {}'.format(res[0], res[1])
    return res[0]


def time_me(func, *args, **kwargs):
    '''Prints how long function execution took.

    >>> time_me(time.sleep, 5)
    Running sleep(5)
    1/1 [2019-11-26 09:45:33.276782]: 5.0 seconds

    Run multiple times
    >>> time_me(time.sleep, 1, n=5)
    Running sleep(1)
    1/5 [2020-03-11 00:03:48.178749]: 1.0 seconds
    2/5 [2020-03-11 00:03:49.179930]: 1.0 seconds
    3/5 [2020-03-11 00:03:50.181081]: 1.0 seconds
    4/5 [2020-03-11 00:03:51.182234]: 1.0 seconds
    5/5 [2020-03-11 00:03:52.182661]: 1.0 seconds
    Total time: 5.0 seconds
    Average time: 1.0 seconds
    Fastest time: 1.0 seconds
    Slowest time: 1.0 seconds
    Standard deviation: 0.00

    Args:
        func (function): Function to call.
        args (list): Args to pass to function.
        kwargs (dict): Kwargs to pass to function. Contains these special ones for time_me():
            n (int): Number of times to run func. Default to 1. If multiple, prints out simple stats
                (ie. average time, total time).
            return_time (bool): If True, returns a tuple with result and time in seconds.

    Returns:
        Anything: Whatever function call returns. None if call failed on first try.
    '''
    if not func:
        error('Invalid function: %s' % func)
        return
    n = kwargs.pop('n', 1)
    return_time = kwargs.pop('return_time', False)

    # Print nice function call.
    args_str = [str(arg) for arg in args]
    params = ', '.join(args_str + ['%s=%s' % (key, str(val)) for key, val in kwargs.iteritems()])
    print 'Running %s(%s)' % (func.__name__, params)

    # Run function n times.
    run_times = []
    res = None
    for count in range(n):
        sys.stdout.write('%i/%i [%s]: ' % (count + 1, n, str(datetime.datetime.now())))
        sys.stdout.flush()
        start = time.time()

        # Execute function call.
        try:
            res = func(*args, **kwargs)
        except Exception, e:
            # Function call errored.
            end = time.time()
            duration = end - start
            print  # Newline before warning.
            warning('Function errored after %s: %s' % (human_time(duration), e))
            print traceback.format_exc().strip()
            return res

        # Print how long did function call took
        end = time.time()
        duration = end - start
        run_times.append(duration)
        print human_time(duration)

    if n >= 2:
        # Print total time and average time.
        total = sum(run_times)
        print 'Total time: %s' % human_time(total)
        print 'Average time: %s' % human_time(total / n)

    if n >= 3:
        # Print simple stats.
        import numpy
        print 'Fastest time: %s' % human_time(min(run_times))
        print 'Slowest time: %s' % human_time(max(run_times))
        print 'Standard deviation: %.2f' % numpy.std(run_times)

    if return_time:
        if n == 1:
            return res, duration
        elif n > 1:
            return res, run_times
    else:
        return res


def time_me_wrapper(func):
    '''Decorator for time_me().'''
    @wraps(func)
    def wrapper(*args, **kwargs):
        time_me(func, *args, **kwargs)
    return wrapper


def _is_text(s):
    return type(s) in [str, unicode]


def var_name(var, locals=locals()):
    '''Hacky way of getting variable name from variable. Empty string if not found.

    >>> foo = 5
    >>> var_name(foo)
    'foo'
    '''
    for name, val in locals.iteritems():
        if val == var:
            return name
    return ''


def human_int(int_):
    '''Add commas to int every 3 digits (ie. 1,234,567,890)'''
    return '{:,}'.format(int_)


BASE_10 = 1000  # How many bytes in 1 kilobyte.
BASE_10_SUFFIXES = ['B', 'kB', 'MB', 'GB', 'TB', 'PB', 'EB', 'ZB', 'YB']
BASE_2 = 1024   # How many bytes in 1 kibibyte.
BASE_2_SUFFIXES = ['B', 'KiB', 'MiB', 'GiB', 'TiB', 'PiB', 'EiB', 'ZiB', 'YiB']


def human_size(nbytes, base=BASE_10):
    '''Human-readable file size (ex. 10.02 GB). Traditional base 2 (1024 bytes) AKA binary unit.
    SI unit using base 10 (1000 bytes).

    Args:
        nbytes (int): Number of bytes.
        base (int): How many bytes in 1 kilobyte/kibibyte? 1000 or 1024.
    '''
    i = 0
    while nbytes >= base and i < len(BASE_2_SUFFIXES) - 1:
        nbytes /= base
        i += 1
    f = ('%.2f' % nbytes).rstrip('0').rstrip('.')
    return '%s %s' % (f, BASE_2_SUFFIXES[i])


'''Nested dict/list related functions.'''
MAX_NUM_SIMILARITIES_TO_PRINT = 3


def _get_iterable(input_):
    '''Key-value iterable of dict/list.'''
    if isinstance(input_, dict):
        return sorted(input_.iteritems())
    elif isinstance(input_, list):
        return enumerate(input_)
    else:
        raise TypeError('Not list or dict')


def similarities(input_):
    '''Dict shared in common among all dicts.

    Args:
        input_ (list or dict): List/dict to find similarities in.

    Raises:
        TypeError: Input not list or dict.
    '''
    from pprint import pprint
    dd = defaultdict(list)

    for _, dict_ in _get_iterable(input_):
        for key, val in dict_.iteritems():
            # Skip unhashable.
            if not val.__hash__:
                continue

            dd[key].append(val)
    for key, vals in sorted(dd.iteritems()):
        counter = Counter(vals)
        if len(counter) > MAX_NUM_SIMILARITIES_TO_PRINT:
            continue
        print '%s (%i): ' % (key, len(counter)),
        pprint(dict(counter))


'''YAML.'''
def load_yaml(file_path):
    from ruamel.yaml import YAML
    yaml = YAML()
    with open(file_path, 'r') as fil:
        return yaml.load(fil)



'''Data structures.'''
class SimpleNamespace:
    '''Ported from Python 3. https://docs.python.org/3.3/library/types.html'''

    def __init__(self, **kwargs):
        self.__dict__.update(kwargs)

    def __repr__(self):
        keys = sorted(self.__dict__)
        items = ('{}={!r}'.format(k, self.__dict__[k]) for k in keys)
        return 'SimpleNamespace({})'.format(', '.join(items))

    def __eq__(self, other):
        return self.__dict__ == other.__dict__
