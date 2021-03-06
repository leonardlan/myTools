'''My Maya userSetup.py.'''
import os
import sys


def add_to_sys_path(path):
    '''Add path to sys.path if exists.'''
    if os.path.exists(path) and path not in sys.path:
        print 'Adding {}'.format(path)
        sys.path.append(path)


def add_my_python_tools():
    '''Add my python tools.'''
    system = os.name
    if system == 'nt':
        home_dir = os.environ['USERPROFILE']
    elif system == 'posix':
        home_dir = os.environ['HOME']
    else:
        print 'Unknown OS: {}. Cannot get home directory environment variable.'.format(system)
        return

    mytools_python = os.path.join(home_dir, 'myTools', 'python')
    add_to_sys_path(mytools_python)

    add_to_sys_path(r'C:\Python27\lib\site-packages')
    add_to_sys_path(r'C:\Python27\lib\site-packages\win32')


add_my_python_tools()
