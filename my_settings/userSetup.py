'''My Maya userSetup.py.'''
import os
import sys


def add_my_python_tools():
    system = os.name
    if system == 'nt':
        home_dir = os.environ['USERPROFILE']
    elif system == 'posix':
        home_dir = os.environ['HOME']
    else:
        print 'Unknown OS: {}. Cannot get home directory environment variable.'.format(system)
        return

    mytools_python = os.path.join(home_dir, 'myTools', 'python')
    if os.path.exists(mytools_python) and mytools_python not in sys.path:
        print 'Adding my python tools'
        sys.path.append(mytools_python)


add_my_python_tools()
