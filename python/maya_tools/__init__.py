'''Functions used in Maya environment.'''

import maya.mel


def get_QApplication():
    '''Get QApplication regardless of version. Maya 2023 uses PySide2, meanwhile 2026 Uses PySide6.
    '''
    try:
        from PySide2.QtWidgets import QApplication
    except ModuleNotFoundError as _:
        try:
            from PySide6.QtWidgets import QApplication
        except Exception as e:
            raise e('Unable to import QApplication from PySide2 and PySide6')

    return QApplication


def cb(content=None):
    '''Copies content to clipboard. If no content, returns clipboard content.'''
    q_app = get_QApplication()
    clipboard = q_app.clipboard()
    if content is None:
        return str(clipboard.text())
    clipboard.setText(str(content))


def cb_strings(delimiter='\n'):
    '''Returns list of clipboard content as string separated by newlines.'''
    content = cb()
    return content.split(delimiter)


def print_to_status(text):
    '''Print to status line in bottom of Maya UI. Replaces newlines with pipe '|'.'''
    maya.mel.eval('print "{}"'.format(text.replace('"', '\\"').replace('\n', '|')))
