'''My logging configurations/functions.'''

import logging

from colors import GREEN, BLUE, YELLOW, RED, BACK_RED, BRIGHT, RESET_ALL


LOGGING_LEVEL_TO_COLOR = {
    logging.DEBUG: GREEN,
    logging.INFO: BLUE,
    logging.WARNING: YELLOW,
    logging.ERROR: RED,
    logging.CRITICAL: BACK_RED,
}


# Add color to log levels.
for level, color in LOGGING_LEVEL_TO_COLOR.items():
    logging.addLevelName(level, BRIGHT + color + logging.getLevelName(level) + RESET_ALL)

# Basic config.
logging.basicConfig(
    level=logging.DEBUG,
    format='%(asctime)s [%(levelname)-8s] %(message)s',
    datefmt='%Y-%m-%d %I:%M:%S')

# Shortcut functions for easier access.
debug = logging.debug
info = logging.info
warning = logging.warning
error = logging.error
critical = logging.critical


def demo_logging():
    '''Prints all log levels.'''
    debug('Just ignore me :/')
    info('Just wanted to let you know this is working.')
    warning('You might want to take a look at this.')
    error("Uh, Houston, we've had a problem.")
    critical("I'll just put this over here with the rest of the fire.")
