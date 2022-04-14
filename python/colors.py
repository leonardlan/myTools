'''Global colored text variables and functions for console/terminal.'''
import sys


# Make CLI beautiful with color-printing to terminal using colorama.
try:
    import colorama
except ImportError:
    print('Module colorama not available.')
    colorama = None
else:
    # Need to call init() on Windows.
    if sys.platform.startswith('win'):
        colorama.init()


# Adds color codes to global variables
TYPE_TO_CODE = {
    'Fore': ['BLUE', 'CYAN', 'GREEN', 'MAGENTA', 'RED', 'LIGHTGREEN_EX', 'YELLOW', 'RESET',
             'LIGHTRED_EX', 'WHITE'],
    'Style': ['BRIGHT', 'NORMAL', 'DIM', 'RESET_ALL']
}
for typ, codes in TYPE_TO_CODE.items():
    for code in codes:
        globals()[code] = getattr(getattr(colorama, typ), code) if colorama else ''
del TYPE_TO_CODE


BACK_RED = colorama.Back.RED if colorama else ''


def demo_colorama(line='', case='upper'):
    '''Print every style and color possible with colorama.

    Args:
        line (str): Text to print.
        case (str): One of 'upper', 'title', or 'lower'.
    '''
    if not colorama:
        print('Cannot demonstrate colorama because module not imported')
        return
    for color in dir(colorama.Fore):
        if color.isupper() and color != 'RESET':
            print(getattr(colorama.Fore, color), end='')
            for style in dir(colorama.Style):
                if style.isupper() and style != 'RESET_ALL':
                    if line:
                        text = '{} ({} {})'.format(line, style, color)
                    else:
                        text = '"{} {}"'.format(style, color)

                    if case == 'title':
                        text = text.title()
                    elif case == 'lower':
                        text = text.lower()
                    print(getattr(colorama.Style, style), text, end='')
            print()
    sys.stdout.write(RESET_ALL)


def brighten_it_up(func):
    '''Wrapper that brightens up the output.'''
    def wrapper(*args, **kwargs):
        '''Wrapper func.'''
        sys.stdout.write(BRIGHT)
        res = func(*args, **kwargs)
        sys.stdout.write(RESET_ALL)
        return res
    return wrapper


# Shortcut color global functions.
def blue(str_):
    return BLUE + str(str_) + RESET


def bright_blue(str_):
    return BRIGHT + BLUE + str(str_) + RESET_ALL


def cyan(str_):
    return CYAN + str(str_) + RESET


def bright_cyan(str_):
    return BRIGHT + CYAN + str(str_) + RESET_ALL


def green(str_):
    return GREEN + str(str_) + RESET


def bright_green(str_):
    return BRIGHT + GREEN + str(str_) + RESET_ALL


def magenta(str_):
    return MAGENTA + str(str_) + RESET


def bright_magenta(str_):
    return BRIGHT + MAGENTA + str(str_) + RESET_ALL


def red(str_):
    return RED + str(str_) + RESET


def bright_red(str_):
    return BRIGHT + RED + str(str_) + RESET_ALL


def white(str_):
    return WHITE + str(str_) + RESET


def bright_white(str_):
    return BRIGHT + WHITE + str(str_) + RESET_ALL


def yellow(str_):
    return YELLOW + str(str_) + RESET


def bright_yellow(str_):
    return BRIGHT + YELLOW + str(str_) + RESET_ALL
