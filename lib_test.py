from libs.LogLib import *

log_file_path = 'LogsExamples/2018-08-06T145142_Copy job/ttd-bck.ttd.local/Backup/Utils/VMC.log'


def find_root_log_path(current_path):
    print('Log root path: %s' % LogImporter.find_root_path(current_path))
    print('Path expected: %s' % current_path[:current_path.find('Backup') + 6])
    if  LogImporter.find_root_path(current_path) == current_path[:current_path.find('Backup') + 6]:
        print("Test passed")
    else:
        print("Test Failed")
    return


def run_all():
    find_root_log_path(log_file_path)
    print('All tests are done!')
    return

run_all()
