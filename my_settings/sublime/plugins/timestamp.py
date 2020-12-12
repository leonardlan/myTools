""" Inserts timestamp at cursor location(s) """
import datetime
import sublime, sublime_plugin


class TimestampCommand(sublime_plugin.TextCommand):
  def run(self, edit):
    timestamp = "[%s]" % (datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
    for sel in self.view.sel():
        self.view.insert(edit, sel.begin(), timestamp)
