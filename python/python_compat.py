'''Backwards compatible functions for all Python 2-3 versions.'''

import sys


def reload(module):
    '''Reload module backwards compatible for all Python versions. Why, Python, why?'''
    major_minor_float = float('{}.{}'.format(sys.version_info.major, sys.version_info.minor))
    if major_minor_float <= 2:
        reload(module)
    if major_minor_float <= 3.3:
        import imp
        imp.reload(module)
    else:
        import importlib
        importlib.reload(module)
