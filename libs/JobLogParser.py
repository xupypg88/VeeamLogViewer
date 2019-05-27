import os,sys
import datetime
from time import mktime

""" Class for the job session """
class JobSession:

    def __init__(self, data, start, end):
        self.data = data
        self.end = end
        self.start = start
        return

    def getJobType(self):
        for line in self.data[0:4]:
            print(line)
            if 'START' in line:
                print(line)
        jbtype =0
        return jbtype

    def getJobStats(self):
        stats = { 'jbtype' : self.getJobType()}

        return stats

class Log:

    def __init__(self, textdata, curpos = 3):
        # Open file and read contents
        self.textdata = textdata
        self.cursor = curpos
        # Import job runs
        self.currsession = self.define_session(textdata)


    def getGlobalLine(self, session, linenum):

        return session.start + linenum

    def define_session(self, lines):
        for n in range(self.cursor, 0):
            if "Starting new log" in lines[n] and "=====================" in lines[n - 1]:
                start_point = n

    """
    returns list of the job runs (lists of text lines)
    """
    def define_sessions(self, lines):

        # creates list of every run entry point
        start_points = [ n for n in range(1, len(lines)) if "Starting new log" in lines[n] and "=====================" in lines[n-1]]

        # returns list of lines[x:y] where x and y are entry points (beginnings for one and endings for others runs)
        # range is used to iterate start_points putting them as pairs one-by-one
        return [ JobSession([lines[start_points[i]:start_points[i+1]-1]],
                            start_points[i],
                            start_points[i+1-1])
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
