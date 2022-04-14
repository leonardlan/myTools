'''My Maya userSetup.py.'''
import os
import sys

from maya import utils


def add_to_sys_path(path):
    '''Add path to sys.path if exists.'''
    if os.path.exists(path) and path not in sys.path:
        print('Adding {}'.format(path))
        sys.path.append(path)


def add_my_python_tools():
    '''Add my python tools.'''
    system = os.name
    if system == 'nt':
        home_dir = os.environ['USERPROFILE']
    elif system == 'posix':
        home_dir = os.environ['HOME']
    else:
        print('Unknown OS: {}. Cannot get home directory environment variable.'.format(system))
        return

    mytools_python = os.path.join(home_dir, 'myTools', 'python')
    add_to_sys_path(mytools_python)

    # Add my tools menu later.
    print('Adding my tools menu (execute deferred)')
    from maya_tools import menu_tools
    utils.executeDeferred(menu_tools.create_my_menu)


add_my_python_tools()
