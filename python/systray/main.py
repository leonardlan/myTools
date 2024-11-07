'''My system tray context menu.

Creates a new icon in system tray with convenient developer tools.

Example usage:

from systray import main
reload(main)

app = main.App()
app.run()
'''


import os
import sys

from PyQt5.QtWidgets import QSystemTrayIcon, QApplication
from PyQt5.QtCore import QFile
from PyQt5.QtCore import QMetaType

from python_compatibility import reload

from . import utils
reload(utils)


class App:

    def __init__(self):
        self.app = QApplication(sys.argv)
        self._load_stylesheet()
        self._create_tray_icon()

    def _create_tray_icon(self):
        self.tray = utils.TrayIcon(self.reload)

    def _load_stylesheet(self):
        fil = QFile(os.path.join(utils.MYTOOLS, 'style/stylesheet.qss'))
        fil.open(QFile.ReadOnly)
        self.app.setStyleSheet(str(fil.readAll()))
        fil.close()

    def run(self):
        # Enter Qt application main loop
        self.app.exec_()
        sys.exit()

    def reload(self):
        '''Reloads utils and redraws menu'''
        print('Reloading app')
        try:
            reload(utils)
        except Exception as err:
            self.tray.showMessage(
                'Error',
                'Unable to reload utils module!\n%s' % err,
                QSystemTrayIcon.Critical
            )
        else:
            self._create_tray_icon()
        self._load_stylesheet()


if __name__ == '__main__':
    app = App()
    app.run()
