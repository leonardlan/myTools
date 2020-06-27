'''Global colored text variables and functions for console/terminal.'''
import sys


# Make CLI beautiful with color-printing to terminal using colorama.
try:
    import colorama
except ImportError:
    print 'Module colorama not available.'
    colorama = None
else:
    # Need to call init() on Windows.
    if sys.platform.startswith('win'):
        colorama.init()


# Adds color codes to global variables
TYPE_TO_CODE = {
    'Fore': ['BLUE', 'CYAN', 'GREEN', 'MAGENTA', 'RED', 'LIGHTGREEN_EX', 'YELLOW', 'RESET',
             'LIGHTRED_EX'],
    'Style': ['BRIGHT', 'NORMAL', 'DIM', 'RESET_ALL']
}
for typ, codes in TYPE_TO_CODE.iteritems():
    for code in codes:
        globals()[code] = getattr(getattr(colorama, typ), code) if colorama else ''
del TYPE_TO_CODE


BACK_RED = colorama.Back.RED if colorama else ''


# Shortcut color global variables.
def bright_blue(str_):
    return BRIGHT + BLUE + str(str_) + RESET_ALL


def demo_colorama(case='upper'):
    '''Print every style and color possible with colorama.

    Args:
        case (str): One of 'upper', 'title', or 'lower'.
    '''
    if not colorama:
        print 'Cannot demonstrate colorama because module not imported'
        return
    for color in dir(colorama.Fore):
        if color.isupper() and color != 'RESET':
            print getattr(colorama.Fore, color),
            for style in dir(colorama.Style):
                if style.isupper() and style != 'RESET_ALL':
                    text = '"%s %s"' % (style, color)
                    if case == 'title':
                        text = text.title()
                    elif case == 'lower':
                        text = text.lower()
                    print getattr(colorama.Style, style), text,
            print
    sys.stdout.write(RESET_ALL)


def brighten_it_up(func):
    '''Brighten up the output.'''
    def wrapper(*args, **kwargs):
        '''Wrapper func.'''
        sys.stdout.write(BRIGHT)
        res = func(*args, **kwargs)
        sys.stdout.write(RESET_ALL)
        return res
    return wrapper
