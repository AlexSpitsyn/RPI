from time import sleep
import subprocess
import os
import zipfile
import shutil
import datetime
from threading import Timer
import config
import wl
import dbg

config.init_dobby()
UPDATE_TIME = int(config.dobby['UPDATE_TIME'])
dbg.DEBUG = config.dobby['DBG'] == 'ON'
wl.EMULATION = config.dobby['EMULATION'] == 'ON'
wl.LOG_SX1278 = config.dobby['LOG'] == 'ON'
config.init()

def wl_update():

    t=Timer(UPDATE_TIME, wl_update)
    t.start()
    wl.update_wf()
    wl.update_boiler()
    wl.update_wts()
    wl.get_pump()
    dbg.prints('update wl')
    # if wl_update_f==False:
    #     print('stop wl_upate')
    #     t.cancel()

base_folder = '/home/alex/Dobby'
update_file = 'update.zip'
update_folder = 'update'
backup_folder = 'backup'
current_dir = os.getcwd()


if not os.path.exists('log'):
    os.mkdir('log')
if not os.path.exists(update_folder):
    os.mkdir(update_folder)
if not os.path.exists(backup_folder):
    os.mkdir(backup_folder)

if os.path.isfile('log/clear'):
    f_log = open('log/log.txt', 'w')
    #f_err = open('log/log_err.txt', 'w')
    os.remove('log/clear')
else:
    f_log = open('log/log.txt', 'a')
    #f_err = open('log/log_err.txt', 'a')
# f_update_log = open('log/log_update.txt', 'a')

now = datetime.datetime.now()
f_log.write(now.strftime("\r\n\t\t\t\t%d/%m/%Y %H:%M:%S\r\n"))
#f_err.write(now.strftime("\r\n\t\t\t\t%d/%m/%Y %H:%M:%S"))
f_log.flush()
#f_err.flush()

# ----------------------------------------------------------------
#                            RECOVERY
# ----------------------------------------------------------------


if os.path.isfile(update_folder + '/' + 'idle'):
    f_log.write('RECOVERY START \r\n' )
    f_log.flush()
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
extrating_pass = 'FAIL'
if os.path.isfile(update_folder + '/' + update_file):

    f_log.write('UPDATE START \r\n')
    f_log.flush()
    try:
        z = zipfile.ZipFile(update_folder + '/' + update_file, 'r')
        z.extractall(update_folder)
        z.close()
        extrating_pass = 'OK'
        f_log.write('unpacking done\r\n')
        f_log.flush()
    except (IOError, zipfile.BadZipfile):
        f_log.write('unpacking fail\r\n')
        f_log.flush()


    os.remove(update_folder + '/' + update_file)

    if extrating_pass == 'OK':
        # backup
        f_log.write('Backup file:\r\n')
        f_log.flush()
        backup_files = os.listdir()
        for file_name in backup_files:
            if os.path.isfile(file_name):
                shutil.copy(file_name, backup_folder)
                f_log.write(file_name + '\r\n')
        f_log.flush()

        # update
        f_log.write('Replace file:\r\n')
        f_log.flush()
        update_files = os.listdir(update_folder)
        for file_name in update_files:
            if os.path.isfile(update_folder + '/' + file_name):
                shutil.copy(update_folder + '/' + file_name, current_dir)
                os.remove(update_folder + '/' + file_name)
                f_log.write(file_name + '\r\n')
        f_log.flush()

    update_state = open(update_folder + '/' + 'update_state', 'a')
    update_state.write(extrating_pass)
    update_state.close()
# ----------------------------------------------------------------
wl_update()
while True:

    f_log.write("\r\nSTARTING DOBBY")
    f_log.flush()
    try:
        sleep(10)
        #Warning('In RPI must call subprocess with arg python3')
        if config.dobby['OS'] == 'WIN':
            subprocess.call(['python', 'dobby.py'])
        elif config.dobby['OS'] == 'LIN':
            subprocess.call(['python3', 'dobby.py'], stdout=f_log, stderr=subprocess.STDOUT)
        else:
            f_log.write('ERROR: OS not set')

    except subprocess.CalledProcessError as exception:
        f_log.write('EXCEPTION')
        f_log.flush()

# f_log.close()

