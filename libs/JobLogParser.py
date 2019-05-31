import os,sys
import datetime
from time import mktime

""" Class for the job session """
class JobSession:

    def __init__(self, data, start, end):
        self.data = data
        self.end = end
        self.start = start
        self.getJobStats()
        return

    def getJobStats(self):
        for line in self.data[0:25]:
            if 'CmdLineParams' in line:
                self.jbtype, self.job_id, self.session_id = line.split('[')[1].split(']')[0].split()

        return

class Log:

    def __init__(self, textdata, curpos = 3):
        # Open file and read contents
        self.textdata = textdata
        self.cursor = curpos
        # Import job runs
        self.sessions = self.define_sessions(textdata)


    def getGlobalLine(self, session, linenum):

        return session.start + linenum + 1

    #finds job session under cursor position
    def pickSession(self, position):
        for sess in self.sessions:
            if sess.start < position and sess.end > position:
                return sess
        raise Exception("Session is not complete in one file!")


    """
    returns list of the job runs (lists of text lines)
    """
    def define_sessions(self, lines):

        # creates list of every run entry point
        start_points = [ n for n in range(1, len(lines)) if "Starting new log" in lines[n] and "=====================" in lines[n-1]]

        # returns list of lines[x:y] where x and y are entry points (beginnings for one and endings for others runs)
        # range is used to iterate start_points putting them as pairs one-by-one
        return [ JobSession(lines[start_points[i]:start_points[i+1]-1],
                            start_points[i],
                            start_points[i+1]-1)
                 for i in range(0, len(start_points)-1) ]


class ExtHelper:

    @staticmethod
    def openfile(filepath):
        if filepath != '':
            try:
                fd = open(filepath, 'r')
            except:
                print("Log file error!")

        return fd.readlines()
