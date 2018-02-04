import sublime
import sublime_plugin


class TestexecCommand(sublime_plugin.TextCommand):
	def run(self, edit):
		self.view.insert(edit, 0, "Hello, World!")

class NewwinCommand(sublime_plugin.WindowCommand):
	def run(self):
		self.window.new_file()

