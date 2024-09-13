"""Insert current timestamp at cursor location(s).

Example: [2024-09-13 11:53:59 AM]

Install:
1. Copy this file to "Sublime Text 3/Packages/User" folder.
2. Setup a key binding under Preferences > Key Bindings. I use Ctrl+T, then S for "TimeStamp" here:
{ "keys": ["ctrl+t", "s"], "command": "timestamp"}
"""


import datetime
import sublime, sublime_plugin


DATETIME_STR = "%Y-%m-%d %I:%M:%S %p"


class TimestampCommand(sublime_plugin.TextCommand):
    def run(self, edit):
        timestamp = "[%s]" % (datetime.datetime.now().strftime(DATETIME_STR))
        for sel in self.view.sel():
                self.view.insert(edit, sel.begin(), timestamp)
