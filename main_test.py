from libs.JobLogParser import *


def test_opening():
    FILE_NAME='Job.SureBackup_Job_SERVX.log'
    DIRECTORY='/home/grizzly/Development/Veeam/VeeamLogViewer/example_logs/srvveem01.olf.sys/Backup/SureBackup_Job_SERVX/'

    log_instance = Log(ExtHelper.openfile(DIRECTORY+FILE_NAME))

    return log_instance

def test_reading():

    log = Log(test_opening())
    log.finderrors()
    return 0

def test_frames(pos):
    print(test_opening().sessions[1].data[pos])
    return 0

test_opening()




