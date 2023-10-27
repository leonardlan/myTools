'''Contains single get_python_architecture function for current Python install.'''


import struct


def get_python_architecture():
    '''Returns bit as int of current Python interpreter's architecture (ie. 32 or 64).'''
    return 8 * struct.calcsize('P')
