'''Functions used in Maya environment.'''

from PySide2.QtWidgets import QApplication
import maya.mel


def cb(content=None):
    '''Copies content to clipboard. If no content, returns clipboard content.'''
    clipboard = QApplication.clipboard()
    if content is None:
        return str(clipboard.text())
    clipboard.setText(str(content))


def print_to_status(text):
    '''Print to status line in bottom of Maya UI. Replaces newlines with pipe '|'.'''
    maya.mel.eval('print "{}"'.format(text.replace('"', '\\"').replace('\n', '|')))
