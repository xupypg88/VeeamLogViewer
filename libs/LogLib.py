import os,sys
import datetime
from time import mktime


class LogLine:

    def __init__(self, textline):
        text = textline[:-1].split(' ')
        if textline[0] == '[':
            self.timecode = self.time2int(text[0].strip('[]'), text[1].strip('[]'))
            self.pid = int(text[2].strip('<>')),  # pid
            self.infotype = str(text[3]),  # type
            message = ''
            for word in text[4:]:
                message += ' ' + word
            self.message = message
        else:
            self.timecode = 0
            self.pid = 0
            self.infotype = 'comment'
            message = ''
            for word in text:
                message += ' ' + word
            self.message = message

    def findinpar(self, chars):
        if chars[0] == chars[1]:
            beg = self.message.split(chars[0])
            return [str(beg[i]) for i in range(1, len(beg), 2)]
        else:
            beg = self.message.split(chars[0])
            return [(i.split(chars[1])[0]) for i in beg[1:]]

    def __repr__(self):
        return str(datetime.datetime.utcfromtimestamp(self.timecode)).strip(' ,') + ' | ' + str(self.infotype) + ' | ' + self.message

    @staticmethod
    def time2int(date, time):
        logdate = datetime.datetime(int(date.split('.')[2])
                                    , int(date.split('.')[1])
                                    , int(date.split('.')[0])
                                    , int(time.split(':')[0])
                                    , int(time.split(':')[1])
                                    , int(time.split(':')[2]))
        return int(mktime(logdate.timetuple()))

class Log:

    def __init__(self, lines, entry):
        self.importLines(lines)
        self.type = 'job'
        self.entry = entry
        return

    def importLines(self, lines):
        self.Lines = self.parse_lines(lines)
        # findpharse looks for entries and returns array of LogLines from Log.Lines
        # findquadpar looks for data in paranties [] and returns array of the data items
        #self.getstat()

        return

    def getstat(self):
        return 'Job name: \t\t' + str(self.findphrase('Job Name:')[0].findinpar('[]')[0]) \
         + '\nStart time: \t' + str(self.findphrase('Process start time:')[0].findinpar('[]')[0]) \
         + '\nEnd time: \t\t' + str(datetime.datetime.fromtimestamp(self.Lines[-1].timecode).strftime('%d/%m/%Y %H:%M:%S')) \
         + '\nResult stat: \t' + str(self.findphrases(['Job session', 'has been completed'], self.Lines)[0].findinpar('\'\'')[1]) \
         + '\nLoaded lines: \t' + str(len(self.Lines))

    def parse_lines(self, lines):
        logLines = []
        for line in lines:
           logLines.append(LogLine(line))
        return logLines

    def findphrases(self, phrases, lines):
        if len(phrases) == 0:
            return lines
        else:
            arr = []
            for line in lines:
                if phrases[0] in line.message:
                    arr.append(line)
            return self.findphrases(phrases[1:], arr)

    def findphrase(self, phrase):
        lines = []
        for line in self.Lines:
            if phrase in line.message:
                lines.append(line)
        return lines

    def finderrors(self):
        lines = []
        for line in self.Lines:
            if tuple(line.infotype) == ('Warning',) or tuple(line.infotype) == ('Error',):
                lines.append(line)
        return lines

class LogImporter:

    def __init__(self):
        return

    @staticmethod
    def openfile(path):
        joblogs = []
        if path != '':
            try:
                fd = open(path, 'r')
            except:
                print "Log file error!"

            loglines = []

            lines = fd.readlines()
            begins = []
            for i in range(0, len(lines), 1):
                if 'Starting new log' in lines[i]:
                    begins.append(i)

            for i in range(0, len(begins), 1):
                if i < len(begins) - 1:
                    #debug - start and end lines
                    #print str(begins[i]) + ' ' + str(begins[i + 1] - 2)
                    joblogs.append(Log(lines[begins[i]:begins[i + 1] - 2], [begins[i], begins[i + 1] - 2]))
                else:
                    #print str(begins[i]) + ' ' + str(len(lines))
                    joblogs.append(Log(lines[begins[i]:len(lines)], [begins[i], len(lines)]))


        return joblogs

