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

#Add route via huawei
os.system(f"ip route add 149.154.167.220 via 192.168.8.1")  

if not os.path.exists('log'):
    os.mkdir('log')
if not os.path.exists(update_folder):
    os.mkdir(update_folder)
if not os.path.exists(backup_folder):
    os.mkdir(backup_folder)

if os.path.isfile('log/clear'):
    f_log = open('log/log.txt', 'w')
    os.remove('log/clear')
else:
    f_log = open('log/log.txt', 'a')


now = datetime.datetime.now()
f_log.write(now.strftime("\n\t\t\t\t%d/%m/%Y %H:%M:%S\n"))
f_log.flush()


# ----------------------------------------------------------------
#                            RECOVERY
# ----------------------------------------------------------------


if os.path.isfile(update_folder + '/' + 'idle'):
    f_log.write('\n\t\t\t\tRECOVERY START \n' )
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

    f_log.write('\n\t\t\t\tUPDATE START\n')
    f_log.flush()
    try:
        z = zipfile.ZipFile(update_folder + '/' + update_file, 'r')
        z.extractall(update_folder)
        z.close()
        extrating_pass = 'OK'
        f_log.write('unpacking done\n')
        f_log.flush()
    except (IOError, zipfile.BadZipfile):
        f_log.write('unpacking fail\n')
        f_log.flush()


    os.remove(update_folder + '/' + update_file)

    if extrating_pass == 'OK':
        # backup
        f_log.write('Backup file:\n')
        f_log.flush()
        backup_files = os.listdir()
        for file_name in backup_files:
            if os.path.isfile(file_name):
                shutil.copy(file_name, backup_folder)
                f_log.write(file_name + '\n')
        f_log.flush()

        # update
        f_log.write('Replace file:\n')
        f_log.flush()
        update_files = os.listdir(update_folder)
        for file_name in update_files:
            if os.path.isfile(update_folder + '/' + file_name):
                shutil.copy(update_folder + '/' + file_name, current_dir)
                os.remove(update_folder + '/' + file_name)
                f_log.write(file_name + '\n')
        f_log.flush()

    update_state = open(update_folder + '/' + 'update_state', 'a')
    update_state.write(extrating_pass)
    update_state.close()
# ----------------------------------------------------------------
wl_update()
while True:

    f_log.write("\n\t\t\t\tSTARTING DOBBY\n")
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
        f_log.write('\n\t\t\t\tEXCEPTION\n')
        f_log.flush()

# f_log.close()

