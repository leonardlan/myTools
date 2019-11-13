'''My useful core functions.'''
import time
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
        'Style': ['BRIGHT', 'NORMAL', 'RESET_ALL']
    }
    for typ, codes in type_to_code.iteritems():
        for code in codes:
            globals()[code] = getattr(getattr(colorama, typ), code) if colorama else ''

    # Shortcut color global variables.
    globals()['BRIGHT_BLUE'] = lambda s: BRIGHT + BLUE + s + RESET_ALL
    globals()['INFO'] = BRIGHT_BLUE
    globals()['WARN'] = lambda s: YELLOW + s + RESET
    globals()['ERROR'] = lambda s: BRIGHT + LIGHTRED_EX + s + RESET_ALL
    globals()['CRITICAL'] = lambda s: colorama.Back.RED + BRIGHT + s + RESET_ALL


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
    '''Prints how long function execution took.'''
    start = time.time()
    res = func(*args, **kwargs)
    end = time.time()
    args_str = [str(arg) for arg in args]
    params = ', '.join(args_str + ['%s=%s' % (key, str(val)) for key, val in kwargs.iteritems()])
    print '%s(%s) took %s' % (func.__name__, params, human_time(end - start))
    return res
