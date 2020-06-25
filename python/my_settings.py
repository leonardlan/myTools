'''All my global variables shared across Python files.'''

import os
import sys


HOME = os.environ['HOME'] if sys.platform.startswith('linux') else os.environ['USERPROFILE']
MAX_LINES = 50
MYTOOLS = os.path.join(HOME, 'myTools')
