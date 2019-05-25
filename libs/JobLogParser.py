import os,sys
import datetime
from time import mktime


class Log:


    def __init__(self, path):
        # Open file and read contents
        textdata = self.openfile(path)

        # Import job runs
        self.runs = self.define_runs(textdata)

        return


    """
    Open job log and provide plain text as lines
    """
    def openfile(self, filepath):
        if filepath != '':
            try:
                fd = open(filepath, 'r')
            except:
                print(   "Log file error!")

        return fd.readlines()


    """
    returns list of the job runs as list of text lines
    """
    def define_runs(self, lines):

        # creates list of every run entry point
        start_points = [ n for n in range(1, len(lines)) if "Starting new log" in lines[n] and "=====================" in lines[n-1]]

        # returns list of lines[x:y] where x and y are entry points (beginings for one and endings for others runs)
        # range is used to iterate start_points putting them as pairs one-by-one
        return [ [lines[start_points[i]:start_points[i+1]-1]] for i in range(0, len(start_points)-1) ]
