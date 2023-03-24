'''All my global variables shared across Python files.'''

import os
import sys
import tempfile

tempfile.gettempdir()


HOME = os.environ['HOME'] if sys.platform.startswith('linux') else os.environ['USERPROFILE']
MAX_LINES = 50
MYTOOLS = os.path.join(HOME, 'myTools')
MY_TEMP_DIR = os.path.join(tempfile.gettempdir(), 'myTools')

# Datetime string formats.
# Ex: '2022-09-12 17:28:33'.
DATETIME_SORTABLE = '%Y-%m-%d %H:%M:%S'
# Ex: 'Mon Sep 12, 5:27 PM'.
DATETIME_NICE = '%a %b %#d, %#I:%M %p'
