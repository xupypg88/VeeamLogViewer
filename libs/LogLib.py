import datetime
from time import mktime
import platform


class LogLine:
    """
    LogLine class gets log lines as is and parses it into timestamp + type + message
    """
    def __init__(self, text_line):
        text = text_line[:-1].split(' ')
        if text_line[0] == '[':
            self.time_code = self.time2int(text[0].strip('[]'), text[1].strip('[]'))
            self.pid = int(text[2].strip('<>')),  # pid
            self.info_type = str(text[3]),  # type
            message = ''
            for word in text[4:]:
                message += ' ' + word
            self.message = message
        else:
            self.time_code = 0
            self.pid = 0
            self.info_type = 'comment'
            message = ''
            for word in text:
                message += ' ' + word
            self.message = message

    def find_in_par(self, chars):
        if chars[0] == chars[1]:
            beg = self.message.split(chars[0])
            return [str(beg[i]) for i in range(1, len(beg), 2)]
        else:
            beg = self.message.split(chars[0])
            return [(i.split(chars[1])[0]) for i in beg[1:]]

    def __repr__(self):
        return str(datetime.datetime.utcfromtimestamp(self.time_code)).strip(' ,') + \
               ' | ' + str(self.info_type) + \
               ' | ' + self.message

    @staticmethod
    def time2int(date, time) -> int:
        log_date = datetime.datetime(
                                    int(date.split('.')[2]),
                                    int(date.split('.')[1]),
                                    int(date.split('.')[0]),
                                    int(time.split(':')[0]),
                                    int(time.split(':')[1]),
                                    int(time.split(':')[2])
        )
        return int(mktime(log_date.timetuple()))


"""
Class log defines an instance that reads lines and stores them in Line class format
"""


class Log:

    def __init__(self, lines, entry):
        self.import_lines(lines)
        self.type = 'job'
        self.entry = entry
        self.Lines = None
        return

    def import_lines(self, lines):
        self.Lines = self.parse_lines(lines)
        return

    def get_stat(self):
        return 'Job name: \t\t' + str(self.find_phrase('Job Name:')[0].find_in_par('[]')[0]) \
               + '\nStart time: \t' + str(self.find_phrase('Process start time:')[0].find_in_par('[]')[0]) \
               + '\nEnd time: \t\t' + str(
            datetime.datetime.fromtimestamp(self.Lines[-1].timecode).strftime('%d/%m/%Y %H:%M:%S')) \
               + '\nResult stat: \t' + str(
            self.find_phrases(['Job session', 'has been completed'], self.Lines)[0].find_in_par('\'\'')[1]) \
               + '\nLoaded lines: \t' + str(len(self.Lines))

    @staticmethod
    def parse_lines(lines):
        log_lines = []
        for line in lines:
            log_lines.append(LogLine(line))
        return log_lines

    def find_phrases(self, phrases, lines):
        if len(phrases) == 0:
            return lines
        else:
            arr = []
            for line in lines:
                if phrases[0] in line.message:
                    arr.append(line)
            return self.find_phrases(phrases[1:], arr)

    def find_phrase(self, phrase):
        lines = []
        for line in self.Lines:
            if phrase in line.message:
                lines.append(line)
        return lines

    def find_errors(self):
        lines = []
        for line in self.Lines:
            if tuple(line.infotype) == ('Warning',) or tuple(line.infotype) == ('Error',):
                lines.append(line)
        return lines


class LogImporter:

    @staticmethod
    def get_os_slash() -> str:
        """
        Checks if \ or / should be used for current platform
        :return:Slash char for path of system platform (String)
        """
        slsh = '/'
        if 'Windows' in platform.system():
            slsh = '\\'
        return slsh


    @staticmethod
    def find_root_path(path) -> str:
        """
        Finds Backup folder path to define root folder for bundle
        :param path: current file path (String)
        :return: Backup folder full path without slash at the end (String)
        """
        slsh = LogImporter.get_os_slash()

        offset = path.find(slsh + 'Backup')
        if offset < 0:
            return ''
        offset += len(str(slsh + 'Backup'))
        return path[:offset]

    @staticmethod
    def openfile(path):
        job_logs = []
        if path != '':
            fd = None
            try:
                fd = open(path, 'r')
            except FileNotFoundError:
                print("Log file error!")

            lines = fd.readlines()
            begins = []
            for i in range(0, len(lines), 1):
                if 'Starting new log' in lines[i]:
                    begins.append(i)

            for i in range(0, len(begins), 1):
                if i < len(begins) - 1:
                    # debug - start and end lines
                    # print str(begins[i]) + ' ' + str(begins[i + 1] - 2)
                    job_logs.append(Log(lines[begins[i]:begins[i + 1] - 2], [begins[i], begins[i + 1] - 2]))
                else:
                    # print str(begins[i]) + ' ' + str(len(lines))FileNotFoundError
                    job_logs.append(Log(lines[begins[i]:len(lines)], [begins[i], len(lines)]))

        return job_logs
