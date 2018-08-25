from libs.LogLib import *

log_file_path = 'LogsExamples/2018-08-06T145142_Copy job/ttd-bck.ttd.local/Backup/Utils/VMC.log'


def run_all():
    job_logs = LogImporter.openfile(log_file_path)
    print('%s' % str(job_logs))
    print('All tests are done!')
    return
