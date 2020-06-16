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
finally:
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

    BACK_RED = colorama.Back.RED

    # Shortcut color global variables.
    bright_blue = lambda s: BRIGHT + BLUE + str(s) + RESET_ALL


def demo_colorama(case='upper'):
    '''Print every style and color possible with colorama.

    Args:
        case (str): One of 'upper', 'title', or 'lower'.
    '''
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
