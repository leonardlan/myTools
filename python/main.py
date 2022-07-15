#!/usr/bin/python

import os
import sys

from PyQt4.QtGui import QSystemTrayIcon, QApplication
from PyQt4.QtCore import QFile, QString

import utils


class App:

    def __init__(self):
        self.app = QApplication(sys.argv)
        self._load_stylesheet()
        self._create_tray_icon()

    def _create_tray_icon(self):
        self.tray = utils.TrayIcon(self.reload)

    def _load_stylesheet(self):
        fil = QFile(os.path.join(utils.MYTOOLS, 'python/stylesheet.qss'))
        fil.open(QFile.ReadOnly)
        self.app.setStyleSheet(QString(fil.readAll()))
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
