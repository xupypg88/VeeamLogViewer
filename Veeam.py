import sublime
import sublime_plugin
import sys

#from LogLib import *
#Job.Backup_Job_For_restore.Backup.log Job.Veeam_Backup__SUK__-_Daily.Backup.log



# 
buff=''
class TestexecCommand(sublime_plugin.TextCommand):
	def run(self, edit, lines):
		currvw = self.view
		texta=''
		for line in lines:
			texta += line
		self.view.insert(edit, self.view.size(), texta)

class TextgetCommand(sublime_plugin.TextCommand):
	def run(self, edit):
		currvw = self.view
		return currvw.substr(currvw.sel()[0])


class ShowpopCommand(sublime_plugin.TextCommand):
	def run(self, edit, lines):
		#envs = self.window.extract_variables()

		currvw = self.view
		texta=''
		for line in lines:
			texta += line
		self.view.insert(edit, 0, texta)
		
		return

class JobstatsCommand(sublime_plugin.WindowCommand):
	def run(self):

		v = self.window.active_view()
		envs = self.window.extract_variables()
		str(envs['file_path'] + '\\' + envs['file_name'])

		buffa = ''
		jobs = []
		for job in LogImporter.openfile(str(envs['file_path'] + '\\' + envs['file_name'])):
		    jobs.append(job)

		for job in [(job) for job in LogImporter.openfile(str(envs['file_path'] + '\\' + envs['file_name']))]:
		    #if i < job.entry[1] and i > job.entry[0]:
		    buffa += str(job.getstat()) + '\n\n'

		
		self.window.new_file()
		viewv = self.window.active_view()
		viewv.run_command('testexec', { "lines" : buffa })
		viewv.set_syntax_file('Packages/VeeamLogViewer/veeam-logs.tmLanguage')

class JobstatCommand(sublime_plugin.WindowCommand):
	def run(self):

		v = self.window.active_view()
		envs = self.window.extract_variables()
		str(envs['file_path'] + '\\' + envs['file_name'])

		buffa = ''
		jobs = []
		for job in LogImporter.openfile(str(envs['file_path'] + '\\' + envs['file_name'])):
		    jobs.append(job)

		thisview = self.window.active_view()
		(pos,col) = thisview.rowcol(thisview.sel()[0].begin())


		print("POSITION: " + str(pos))
		for job in [(job) for job in LogImporter.openfile(str(envs['file_path'] + '\\' + envs['file_name']))]:
		    if pos < job.entry[1] and pos > job.entry[0]:
			    buffa += str('\n'.join([str(str(k) + ': ' + str(v)) for k,v in job.getstat().items()])) + '\n\n'

		
		self.window.new_file()
		viewv = self.window.active_view()
		viewv.run_command('testexec', { "lines" : buffa } )
		viewv.set_syntax_file('Packages/VeeamLogViewer/veeam-logs.tmLanguage')

class NewwinCommand(sublime_plugin.WindowCommand):
	def run(self):

		v = self.window.active_view()

		regs=[]
		for pattern in v.sel():
			for ln in v.find_all(v.substr(pattern),sublime.LITERAL):
				if v.full_line(ln) not in regs:
				    regs.append(v.full_line(ln))

		regs.sort()

		buffa=[]		
		for ln in regs:
			buffa.append(v.substr(ln))

		
		self.window.new_file()
		viewv = self.window.active_view()
		viewv.run_command('testexec', { "lines" : buffa })
		viewv.set_syntax_file('Packages/VeeamLogViewer/veeam-logs.tmLanguage')

class PutnewwinCommand(sublime_plugin.WindowCommand):
	def run(self):
		v = self.window.active_view()

		for viewitem in self.window.views():
			if viewitem.name() == 'dumper':
				viewv = viewitem

		if 'viewv' not in locals():
			self.window.new_file()
			viewv = self.window.active_view()

			viewv.set_name('dumper')


		lines = [str(v.substr(line)) for line in v.sel() if line is not ""]
		lines.insert(0, str(v.file_name()) + '\n\n')
		lines.append('\n---   ---   ---\n')

		for l in range(0, len(lines)):
			if '\n' not in lines[l]:
				lines[l] += '\n'

		viewv.run_command('testexec', { "lines" : lines })
		viewv.set_syntax_file('Packages/VeeamLogViewer/veeam-logs.tmLanguage')