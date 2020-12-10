from time import sleep
import subprocess
import os
import zipfile
import shutil
import datetime

base_folder = '/home/alex/Dobby'
update_file = 'update.zip'
update_folder = 'update'
backup_folder = 'backup'
current_dir = os.getcwd()

update_run = 0
if not os.path.exists('log'):
    os.mkdir('log')
if not os.path.exists(update_folder):
    os.mkdir(update_folder)
if not os.path.exists(backup_folder):
    os.mkdir(backup_folder)

f_log = open('log/log.txt', 'a')
f_err = open('log/log_err.txt', 'a')
# f_update_log = open('log/log_update.txt', 'a')

now = datetime.datetime.now()
f_log.write(now.strftime("\r\n\t\t\t\t%d/%m/%Y %H:%M:%S\r\n\r\n"))
f_err.write(now.strftime("\r\n\t\t\t\t%d/%m/%Y %H:%M:%S\r\n\r\n"))
f_log.flush()
f_err.flush()

# ----------------------------------------------------------------
#                            RESTORE
# ----------------------------------------------------------------


if os.path.isfile(update_folder + '/' + 'idle'):
    # f_update_log.write('updating FAIL \r\n' )
    backup_files = os.listdir(backup_folder)
    for file_name in backup_files:
        if os.path.isfile(file_name):
            shutil.copy(backup_folder + '/' + file_name, os.getcwd())
            # f_update_log.write('restoring  ' + file_name )
    os.remove(update_folder + '/' + 'idle')

# ----------------------------------------------------------------
#                            UPDATE
# ----------------------------------------------------------------

# extrating
if os.path.isfile(update_folder + '/' + update_file):
    update_run = 1
    z = zipfile.ZipFile(update_folder + '/' + update_file, 'r')
    z.extractall(update_folder)
    z.close()
    os.remove(update_folder + '/' + update_file)

    # backup
    backup_files = os.listdir()
    for file_name in backup_files:
        if os.path.isfile(file_name):
            shutil.copy(file_name, backup_folder)
            # f_update_log.write('backup ' + file_name + ' to ' + backup_folder +'\r\n')

    # update
    update_files = os.listdir(update_folder)
    for file_name in update_files:
        if os.path.isfile(update_folder + '/' + file_name):
            shutil.copy(update_folder + '/' + file_name, current_dir)
            os.remove(update_folder + '/' + file_name)
            # f_update_log.write('updating  ' + file_name +'\r\n')

    pass_update = open(update_folder + '/' + 'idle', 'a')
    pass_update.close()
# ----------------------------------------------------------------

sleep(10)

subprocess.call(["python3", 'dobby.py'], stdout=f_log, stderr=f_err)

f_log.close()
f_err.close()

