'''Useful Qt functions using PyQt5.'''

import re
import sys

from PyQt5.QtWidgets import QApplication
from PyQt5 import QtCore


# Current QApplication instance. Check globals() so that reloading module won't reset.
if 'APPLICATION_INSTANCE' not in globals():
    APPLICATION_INSTANCE = None


def has_application_status():
    '''True if current session has QApplication instance.'''
    global APPLICATION_INSTANCE
    return bool(APPLICATION_INSTANCE)


def start_application_instance():
    '''Start QApplication, if not already started, and return instance.'''
    global APPLICATION_INSTANCE
    if APPLICATION_INSTANCE:
        return APPLICATION_INSTANCE
    APPLICATION_INSTANCE = QApplication.instance() or QApplication(sys.argv)
    return APPLICATION_INSTANCE


def copy_to_clipboard(content):
    '''Copy to clipboard with HTMl formatting. Can paste into Word with formatting, or as
    unformatted text into text editor.

    Example HTML:
    copy_to_clipboard('<b>Bold</b>, <i>italic</i>, <b><i>bold and italic</i></b>, <a href="https://google.com">Google</a>')
    '''
    start_application_instance()

    clipboard = QApplication.clipboard()
    mime_data = QtCore.QMimeData()
    mime_data.setHtml(content)
    mime_data.setText(_remove_html(content))
    clipboard.setMimeData(mime_data)


def _remove_html(html_string):
    '''Remove HTML tags from string.'''
    return re.sub(r'<[^<]+?>', '', html_string)
