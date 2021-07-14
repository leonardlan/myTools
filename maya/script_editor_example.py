from pprint import pprint

# My tools.
from wai import wai
from maya_tools import debugger_tools


# Print attributes.
debugger_tools.print_attrs()
debugger_tools.print_attrs(val_filter=False)
debugger_tools.print_attrs('defaultRenderGlobals')
debugger_tools.print_attrs('defaultArnoldDriver', val_filter='zip')


# Diff nodes.
debugger_tools.diff()
