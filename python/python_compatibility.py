'''Backwards compatible functions for all Python 2-3 versions.'''

import sys


PYTHON_VERSION_MAJOR = sys.version_info.major
PYTHON_VERSION_MINOR = sys.version_info.minor


def is_in_python_2():
    return PYTHON_VERSION_MAJOR == 2


def is_in_python_3():
    return PYTHON_VERSION_MAJOR == 3


def reload(module):
    '''Reload module backwards compatible for all Python versions. Why, Python, why?'''
    if is_in_python_2():
        reload(module)
        return

    # Assume Python 3 here.
    if PYTHON_VERSION_MINOR <= 3:
        # Python 3, up to 3.3, use this:
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
    if is_in_python_2():
        execfile(file_path)
    else:
        exec(open(file_path).read())


def get_input(*args, **kwargs):
    '''Python renamed raw_input() to input().'''
    if is_in_python_2():
        return raw_input(*args, **kwargs)
    else:
        return input(*args, **kwargs)
