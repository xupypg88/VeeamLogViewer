import sublime
import sublime_plugin


class TextgetCommand(sublime_plugin.TextCommand):
    def run(self):
        currvw = self.view
        return currvw.substr(currvw.sel()[0])


class TestexecCommand(sublime_plugin.TextCommand):
    def run(self, edit, lines):
        texta = ''
        for line in lines:
            texta += line
        self.view.insert(edit, self.view.size(), texta)


class ShowpopCommand(sublime_plugin.TextCommand):
    def run(self, edit, lines):
        texta = ''
        for line in lines:
            texta += line
        self.view.insert(edit, 0, texta)
        return


class NewwinCommand(sublime_plugin.WindowCommand):
    def run(self):
        v = self.window.active_view()
        regs = []
        for pattern in v.sel():
            for ln in v.find_all(v.substr(pattern), sublime.LITERAL):
                if v.full_line(ln) not in regs:
                    regs.append(v.full_line(ln))
        regs.sort()

        buffa = []
        for ln in regs:
            buffa.append(v.substr(ln))
        self.window.new_file()
        viewv = self.window.active_view()
        viewv.set_name('Found to Tab')
        viewv.run_command('testexec', {"lines": buffa})
        viewv.set_syntax_file('Packages/VeeamLogViewer/veeam-logs.tmLanguage')


class PutnewwinCommand(sublime_plugin.WindowCommand):
    def run(self):
        """
        Pycharm says view should be added to avoid to be invoked before definition
        but in this case I cannot make it to be not in locals
        """
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
        viewv.run_command('testexec', {"lines": lines})
        viewv.set_syntax_file('Packages/VeeamLogViewer/veeam-logs.tmLanguage')
