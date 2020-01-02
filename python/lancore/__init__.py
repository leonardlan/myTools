'''My useful core functions.'''
import copy
import datetime
import numpy
import sys
import time
import traceback

from collections import OrderedDict


# Make CLI beautiful with color-printing to terminal using colorama.
try:
    import colorama
except ImportError:
    print 'Module colorama not available.'
    colorama = None
finally:
    # Adds color codes to global variables
    type_to_code = {
        'Fore': ['BLUE', 'CYAN', 'GREEN', 'MAGENTA', 'RED', 'LIGHTGREEN_EX', 'YELLOW', 'RESET',
                 'LIGHTRED_EX'],
        'Style': ['BRIGHT', 'NORMAL', 'DIM', 'RESET_ALL']
    }
    for typ, codes in type_to_code.iteritems():
        for code in codes:
            globals()[code] = getattr(getattr(colorama, typ), code) if colorama else ''

    # Shortcut color global variables.
    globals()['BRIGHT_BLUE'] = lambda s: BRIGHT + BLUE + str(s) + RESET_ALL
    globals()['INFO'] = lambda s: BRIGHT + BLUE + 'INFO:' + RESET_ALL + ' ' + str(s)
    globals()['WARN'] = lambda s: BRIGHT + YELLOW + 'WARNING:' + RESET_ALL + ' ' + str(s)
    globals()['ERROR'] = lambda s: BRIGHT + LIGHTRED_EX + 'ERROR:' + RESET_ALL + ' ' + str(s)
    globals()['CRITICAL'] = lambda s: BRIGHT + colorama.Back.RED + 'CRITICAL:' + RESET_ALL + ' ' + \
        str(s)


INTERVALS = OrderedDict([
    ('millennium', 31536000000),  # 60 * 60 * 24 * 365 * 1000
    ('century', 3153600000),      # 60 * 60 * 24 * 365 * 100
    ('year', 31536000),           # 60 * 60 * 24 * 365
    ('week', 604800),             # 60 * 60 * 24 * 7
    ('day', 86400),               # 60 * 60 * 24
    ('hour', 3600),               # 60 * 60
    ('minute', 60),
    ('second', 1)
])


def human_time(seconds, decimals=1):
    '''Human-readable time from seconds (ie. 5 days and 2 hours).

    Examples:
        >>> human_time(15)
        '15 seconds'
        >>> human_time(3600)
        '1 hour'
        >>> human_time(3720)
        '1 hour and 2 minutes'
        >>> human_time(266400)
        '3 days and 2 hours'
        >>> human_time(-1.5)
        '-1.5 seconds'
        >>> human_time(0)
        '0 seconds'
        >>> human_time(0.1)
        '100 milliseconds'
        >>> human_time(1)
        '1 second'

    Args:
        seconds (int or float): Duration in seconds.
        decimals (int): Number of decimals.

    Returns:
        str: Human-readable time.
    '''
    input_is_int = isinstance(seconds, int)
    if seconds < 0:
        return str(seconds if input_is_int else round(seconds, decimals)) + ' seconds'
    elif seconds == 0:
        return '0 seconds'
    elif 0 < seconds < 1:
        # Return in milliseconds.
        ms = int(seconds * 1000)
        return '%i millisecond%s' % (ms, 's' if ms != 1 else '')
    elif 1 < seconds < INTERVALS['minute']:
        return str(seconds if input_is_int else round(seconds, decimals)) + ' seconds'

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

    Args:
        func (function): Function to call.
        args (list): Args to pass to function.
        kwargs (dict): Kwargs to pass to function.
        n (int): Number of times to run func. Default to 1.

    Returns:
        Anything: Whatever function call returns. None if call failed on first try.
    '''
    n = kwargs.pop('n', 1)
    args_str = [str(arg) for arg in args]
    params = ', '.join(args_str + ['%s=%s' % (key, str(val)) for key, val in kwargs.iteritems()])
    print 'Running %s(%s)' % (func.__name__, params)
    run_times = []
    res = None
    for count in range(n):
        sys.stdout.write('%i/%i [%s]: ' % (count + 1, n, str(datetime.datetime.now())))
        sys.stdout.flush()
        start = time.time()
        try:
            res = func(*args, **kwargs)
        except Exception, e:
            end = time.time()
            duration = end - start
            print WARN('\nFunction errored after %s: %s' % (human_time(duration), e))
            print traceback.format_exc().strip()
            return res
        end = time.time()
        duration = end - start
        run_times.append(duration)
        print human_time(duration)

    if n >= 2:
        total = sum(run_times)
        print 'Total time: %s' % human_time(total)
        print 'Average time: %s' % human_time(total / n)
    if n >= 3:
        print 'Fastest time: %s' % human_time(min(run_times))
        print 'Slowest time: %s' % human_time(max(run_times))
        print 'Standard deviation: %.2f' % numpy.std(run_times)
    return res


def similarities(dicts):
    '''Dict shared in common among all dicts.'''
    if not dicts:
        return {}
    same_dict = copy.deepcopy(dicts[0])
    for dict_ in dicts[1:]:
        for key, val in dict_.iteritems():
            if key in same_dict and same_dict[key] != val:
                same_dict.pop(key)
    return same_dict
