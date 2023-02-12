'''Backwards compatible functions for all Python 2-3 versions.'''

import sys


MAJOR_MINOR_FLOAT = float('{}.{}'.format(sys.version_info.major, sys.version_info.minor))


def is_in_python_2():
    return int(MAJOR_MINOR_FLOAT) == 2


def is_in_python_3():
    return int(MAJOR_MINOR_FLOAT) == 3


def reload(module):
    '''Reload module backwards compatible for all Python versions. Why, Python, why?'''
    if MAJOR_MINOR_FLOAT <= 2:
        reload(module)
    if MAJOR_MINOR_FLOAT <= 3.3:
        import imp
        imp.reload(module)
    else:
        import importlib
        importlib.reload(module)


def is_string(data):
    '''Check if input is string. Python 2 uses basestring. Python 3 uses str. What gives?'''
    try:
        basestring
    except NameError:
        return isinstance(data, str)
    return isinstance(data, basestring)


def exec_file(file_path):
    '''Replace execfile() in Python 2.'''
    if MAJOR_MINOR_FLOAT <= 2:
        execfile(file_path)
    else:
        exec(open(file_path).read())
