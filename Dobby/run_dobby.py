from time import sleep
import subprocess
import os
import zipfile
import shutil

base_folder = '/home/alex/Dobby'
update_file = 'update.zip'
update_folder = 'update'
backup_folder = 'backup'

update_run = 0
if not os.path.exists('log'):
    os.mkdir('log')
if not os.path.exists(update_folder):
    os.mkdir(update_folder)
if not os.path.exists(backup_folder):
    os.mkdir(backup_folder)

if os.path.isfile(update_folder + '/' + update_file):
    update_run = 1
z = zipfile.ZipFile(update_folder + '/' + update_file, 'r')
z.extractall(update_folder)
z.close()
os.remove(update_folder + '/' + update_file)

# ------BACKUP-------
backup_files = os.listdir()
for file_name in backup_files:
    if os.path.isfile(file_name):
        shutil.copy(file_name, backup_folder)

# ------UPDATE
update_files = os.listdir(update_folder)
for file_name in update_files:
    if os.path.isfile(update_folder + '/' + file_name):
        shutil.copy(update_folder + '/' + file_name, os.getcwd())
        os.remove(update_folder + '/' + file_name)

sleep(30)

f_log = open('log/log.txt', 'a')
f_err = open('log/log_err.txt', 'a')

res = subprocess.call(["python3", 'dobby.py'], stdout=f_log, stderr=f_err)

if res != '0' and update_run == 1:
    backup_files = os.listdir(backup_folder)
    for file_name in backup_files:
        if os.path.isfile(file_name):
            shutil.copy(backup_folder + '/' + file_name, os.getcwd())
    fail_update = open(update_folder + '/' + 'FAIL', 'a')
    fail_update.close()

    subprocess.call(["python3", 'dobby.py'], stdout=f_log, stderr=f_err)

f_log.close()
f_err.close()
