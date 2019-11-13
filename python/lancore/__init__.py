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


def human_time(seconds, decimals=3):
    '''Human-readable time from seconds (ie. 5 days and 2 hours).

    Args:
        seconds (int or float): Duration in seconds.
        decimals (int): Number of decimals.

    Returns:
        str: Human-readable time.
    '''
    if seconds == 0:
        return '0 seconds'
    elif seconds < 1:
        return str(round(seconds, decimals)) + ' seconds'

    res = []
    for name, count in INTERVALS.iteritems():
        value = seconds // count
        if value:
            seconds -= value * count
            if value != 1:
                # Plurals.
                if name == 'millennium':
                    name = 'millennia'
                elif name == 'century':
                    name = 'centuries'
                else:
                    name += 's'
            res.append((int(value), name))

    # Purge zeros starting from seconds.
    while res and res[-1][0] == 0:
        res.pop()

    res = ['%i %s' % (val, interval) for val, interval in res]
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
