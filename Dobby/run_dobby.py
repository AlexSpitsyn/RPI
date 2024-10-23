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

