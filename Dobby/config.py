#!/usr/bin/python
# encoding=utf8

import json
import os
import dbg

# private information
users_ID = []
admin_ID = 0
DOBBY_TOKEN = ''
tapo_user = ''
tapo_pass = ''

CONFIG_PATH = "config/"
FILENAME_WTS_CONF = CONFIG_PATH + "wts-#.cfg"
FILENAME_BOILER_CONF = CONFIG_PATH + "boiler.cfg"
FILENAME_WF_CONF = CONFIG_PATH + "wf.cfg"
FILENAME_PUMP_CONF = CONFIG_PATH + "pump.cfg"
FILENAME_DOBBY_CONF = CONFIG_PATH + "dobby.cfg"
FILENAME_USERS_LIST = CONFIG_PATH + "users_list.txt"

wts_addr = 0x53545700
wfcr_addr = 0x52434657
boiler_addr = 0x524C4F42

wts_fieldnames = ['WTSN', 'STATE', 'TEMP', 'NAME', 'CHECK', 'GPIO']
wf_blr_fieldnames = ['STATE', 'T_CTRL', 'TEMP', 'TEMP_SET']
pump_fieldnames = ['STATE', 'PUMP_1_1_SW', 'PUMP_1_2_SW', 'PUMP_2_1_SW', 'PUMP_2_2_SW', 'PUMP_1_1_ST', 'PUMP_1_2_ST',
                   'PUMP_2_1_ST', 'PUMP_2_2_ST']  # numeration must be like in wl.py BOILER_VAR
dobby_fieldnames = ['OS', 'DBG', 'LOG', 'EMULATION', 'UPDATE_TIME']

temp = {'WF_MIN': 20, 'WF_MAX': 50, 'BOILER_MIN': 10, 'BOILER_MAX': 65}

wts = []
wf = {}
boiler = {}
pump = {}
dobby = {}


def create_cfg_files(filename):
    if 'wts-' in filename:
        wtsx = dict.fromkeys(wts_fieldnames)
        wtsx[wts_fieldnames[0]] = filename.split('wts-')[1].split('.')[0]  # WTSN
        wtsx[wts_fieldnames[1]] = 'OFFLINE'  # STATE
        wtsx[wts_fieldnames[2]] = '0'  # TEMP
        wtsx[wts_fieldnames[3]] = 'NoName'  # NAME
        wtsx[wts_fieldnames[4]] = '0'  # CHECK
        wtsx[wts_fieldnames[5]] = '0'  # GPIO

        wts.append(wtsx.copy())

        with open(filename, 'w') as outfile:
            json.dump(wtsx, outfile)

    if filename == FILENAME_WF_CONF:
        wf = dict.fromkeys(wf_blr_fieldnames, '0')

        with open(filename, 'w') as outfile:
            json.dump(wf, outfile)

    if filename == FILENAME_BOILER_CONF:
        boiler = dict.fromkeys(wf_blr_fieldnames, '0')

        with open(filename, 'w') as outfile:
            json.dump(boiler, outfile)

    if filename == FILENAME_PUMP_CONF:
        pump = dict.fromkeys(pump_fieldnames, '0')
        pump['STATE'] = 'OFFLINE'

        with open(filename, 'w') as outfile:
            json.dump(pump, outfile)

    outfile.close()


def init_dobby():
    global DOBBY_TOKEN, dobby, admin_ID, tapo_pass, tapo_user, users_ID
    if os.path.isfile('dobby_login'):
        with open('dobby_login', "r") as readfile:
            for line in readfile:
                line = line.strip()
                if "tocken" in line:
                    DOBBY_TOKEN = line.split('=')[1]
                if "admin_ID" in line:
                    admin_ID = int(line.split('=')[1])
                if "tapo_user" in line:
                    tapo_user = line.split('=')[1]
                if "tapo_pass" in line:
                    tapo_pass = line.split('=')[1]
            readfile.close()
    else:
        return 'login not found'

    if os.path.isfile(FILENAME_DOBBY_CONF):
        read_dobby()
    else:
        dbg.prints('WARNING! No such file:' + FILENAME_DOBBY_CONF)
        dobby = dict.fromkeys(dobby_fieldnames)
        dobby[dobby_fieldnames[0]] = 'LIN'
        dobby[dobby_fieldnames[1]] = 'OFF'
        dobby[dobby_fieldnames[2]] = 'OFF'
        dobby[dobby_fieldnames[3]] = 'OFF'
        dobby[dobby_fieldnames[4]] = '1000'
        with open(FILENAME_DOBBY_CONF, 'w') as outfile:
            json.dump(dobby, outfile)

    return 'OK'


def init():
    if os.path.isfile(FILENAME_USERS_LIST):
        with open(FILENAME_USERS_LIST, 'r') as readfile:
            lines = readfile.readlines()
            for uid in lines:
                users_ID.append(int(uid))
            readfile.close()
    else:
        dbg.prints('WARNING! No such file:' + FILENAME_USERS_LIST)
        dbg.prints('Creating file...')
        idfile = open(FILENAME_USERS_LIST, 'w')
        idfile.writelines(str(admin_ID) + '\n')
        users_ID.append(admin_ID)
        idfile.close()

    for num in range(16):
        if os.path.isfile(FILENAME_WTS_CONF.replace('#', str(num))):
            wts.append(read_config(FILENAME_WTS_CONF.replace('#', str(num))))

    if os.path.isfile(FILENAME_WF_CONF):
        read_wf()
    else:
        dbg.prints('WARNING! No such file:' + FILENAME_WF_CONF)
        dbg.prints('Creating file...')
        create_cfg_files(FILENAME_WF_CONF)

    if os.path.isfile(FILENAME_BOILER_CONF):
        read_boiler()
    else:
        dbg.prints('WARNING! No such file:' + FILENAME_BOILER_CONF)
        dbg.prints('Creating file...')
        create_cfg_files(FILENAME_BOILER_CONF)

    if os.path.isfile(FILENAME_PUMP_CONF):
        read_pump()
    else:
        dbg.prints('WARNING! No such file:' + FILENAME_PUMP_CONF)
        dbg.prints('Creating file...')
        create_cfg_files(FILENAME_PUMP_CONF)


# =====================  PASS ID =============================

def write_pass_list(lst):
    with open(FILENAME_USERS_LIST, 'w') as wfile:
        for uid in lst:
            wfile.writelines(str(uid) + '\n')


# =====================  DOBBY =============================
def read_dobby():
    dobby.update(read_config(FILENAME_DOBBY_CONF))


# =====================  WTS =============================
# --------------CONFIG------------
# STATE / TEMP / NAME / CHECK
# --------------------------------

def read_wts(wts_num):
    global wts
    wts[wts_num].update(read_config(FILENAME_WTS_CONF.replace('#', wts[wts_num]['WTSN'])))


def write_wts(wts_num):
    write_config(FILENAME_WTS_CONF.replace('#', wts[wts_num]['WTSN']), wts[wts_num])


def wts_checking_toggle(wts_num):
    if wts[wts_num][wts_fieldnames[4]] == '0':
        wts[wts_num][wts_fieldnames[4]] = '1'
    else:
        wts[wts_num][wts_fieldnames[4]] = '0'

    write_wts(wts_num)


def wts_checking_onoff(wts_num, onoff):
    if onoff == 'on':
        wts[wts_num][wts_fieldnames[4]] = '1'
    elif onoff == 'off':
        wts[wts_num][wts_fieldnames[4]] = '0'
    else:
        dbg.dbg.printss('wrong wts_check_onoff arg')
    write_wts(wts_num)


def get_wtsidx(wts_num):
    for wtsn in wts:
        if wtsn['WTSN'] == wts_num:
            return wts.index(wtsn)


# =====================  WF =============================
# ------CONFIG-----------
# STATE / T_CTRL / TEMP / TEMP_SET
# -----------------------
def read_wf():
    wf.update(read_config(FILENAME_WF_CONF))


def write_wf():
    write_config(FILENAME_WF_CONF, wf)


# =====================  BOILER =============================
# ------CONFIG-----------
# STATE / T_CTRL / TEMP / TEMP_SET
# -----------------------
def read_boiler():
    boiler.update(read_config(FILENAME_BOILER_CONF))


def write_boiler():
    write_config(FILENAME_BOILER_CONF, boiler)


# =====================  PUMP =============================
# -----------------CONFIG--------------------------------------
# PUMP1_1_STATE / PUMP1_2_STATE / PUMP2_1_STATE / PUMP2_2_STATE
# -------------------------------------------------------------
def read_pump():
    pump.update(read_config(FILENAME_PUMP_CONF))


def write_pump():
    write_config(FILENAME_PUMP_CONF, pump)


def read_config(filename):
    try:
        with open(filename, "r") as read_file:
            dct = json.load(read_file)
            read_file.close()
        return dct

    except IOError:
        dbg.prints("read file error: " + filename)


def write_config(filename, dct):
    try:
        with open(filename, 'w') as outfile:
            json.dump(dct, outfile)
            outfile.close()

    except IOError:
        dbg.prints("write config file error: " + filename)
