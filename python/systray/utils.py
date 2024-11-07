import os
import subprocess
import sys

from functools import partial
from ruamel.yaml import YAML

from PyQt5.QtGui import QIcon, QCursor
from PyQt5.QtWidgets import QMenu, QSystemTrayIcon

from my_settings import MYTOOLS
from subprocess_tools import subl


HOME = os.path.expanduser('~')
ACTIONS_CONFIG_FILE = os.path.join(MYTOOLS, 'config/actions.yaml')


def run(cmd, keep_open=False, title=''):
    '''Run a command in new subprocess terminal.

    Args:
        cmd (str): Command to run.
        keep_open (bool): If True, keeps terminal open after command run.
        title (str): Title of terminal.
    '''
    if keep_open:
        cmd = "mate-terminal -e 'bash -i -c \"%s; bash\"'" % cmd
    if title:
        cmd += " -t '%s'" % title
    print('Running:', cmd)
    subprocess.Popen(cmd, shell=True)


def open_terminal(dir_, title=''):
    '''Open Terminal at directory.'''
    run('mate-terminal --working-directory=' + os.path.expanduser(dir_), title=title)


def icon(name):
    '''Icon from name or file path to icon.'''
    if os.path.exists(name):
        return QIcon(name)
    return QIcon(os.path.join(MYTOOLS, 'img', name + '.png'))


class TrayIcon(QSystemTrayIcon):
    '''My implementation of QSystemTrayIcon.'''

    def __init__(self, reload_func):
        super(TrayIcon, self).__init__(icon('ll'))
        self.reload_func = reload_func
        self.setContextMenu(self.make_menu())
        self.setToolTip("Leonard's Quick Links\nMiddle-mouse click to reload")
        self.activated.connect(self._activated)
        self.show()

    def get_actions(self):
        '''Load actions from config file.'''
        yaml = YAML()
        with open(ACTIONS_CONFIG_FILE, 'r') as fil:
            return yaml.load(fil)

    def _setup_actions(self, menu, actions):
        '''Setup actions.'''
        for text, data in actions.items():
            # Separator.
            if data == 'separator':
                menu.addSeparator()
                continue

            # Menu with sub actions.
            if data.get('actions'):
                new_menu = menu.addMenu(text)

                # Icon.
                if data.get('icon'):
                    new_menu.setIcon(icon(data.get('icon')))

                # Recursively setup sub actions in current menu.
                self._setup_actions(new_menu, data.get('actions'))
                continue

            # Action.
            action = menu.addAction(text)
            if data.get('cmd'):
                action.triggered.connect(partial(run, data.get('cmd'), **data.get('kwargs', {})))
            elif data.get('path'):
                action.triggered.connect(partial(subl, data.get('path')))
            elif data.get('terminal_path'):
                action.triggered.connect(
                    partial(open_terminal, data.get('terminal_path'), **data.get('kwargs', {})))

            # Set icon.
            if data.get('icon'):
                action.setIcon(icon(data.get('icon')))

    def make_menu(self):
        '''Make and return menu.'''
        # Setup menu.
        menu = QMenu()
        menu.setTearOffEnabled(True)

        # Setup actions from config file.
        self._setup_actions(menu, self.get_actions())

        # Reload Me action.
        action = menu.addAction(icon('reload'), '&Reload Me')
        action.triggered.connect(self.reload_func)
        menu.addSeparator()

        # Exit action.
        action = menu.addAction(icon('exit'), '&Exit')
        action.triggered.connect(sys.exit)

        return menu

    def _activated(self, reason):
        '''Show context menu on left-click.'''
        if reason == QSystemTrayIcon.Trigger:
            self.contextMenu().popup(QCursor().pos())
        elif reason == QSystemTrayIcon.MiddleClick:
            self.reload_func()
