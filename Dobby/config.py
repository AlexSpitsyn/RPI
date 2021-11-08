#!/usr/bin/python
# encoding=utf8

# reload (sys)
# sys.setdefaultencoding('utf8')

import json
import os
from typing import List, Any

import dbg

CONFIG_PATH = "config/"
FILENAME_WTS_CONF = CONFIG_PATH + "wts.cfg"
FILENAME_BOILER_CONF = CONFIG_PATH + "boiler.cfg"
FILENAME_WF_CONF = CONFIG_PATH + "wf.cfg"
FILENAME_PUMP_CONF = CONFIG_PATH + "pump.cfg"
FILENAME_DOBBY_CONF = CONFIG_PATH + "dobby.cfg"

wts_addr = [0x53545701,0x53545702,0x53545703,0x53545704,0x53545705,0x53545706,0x53545707,0x53545708,0x53545709,0x5354570A,0x5354570B,0x5354570C,0x5354570D,0x5354570E,0x5354570F,0x53545710]
wfcr_addr = 0x52434657
boiler_addr = 0x524C4F42
DOBBY_TOKEN = '927942451:AAG7HMnzpyLVKcydJiEW0zGjOcnqi7_1EDE'
DOBBY_DBG_TOKEN = '1576222883:AAEtQ6GWeNWI64NLB3w7jEb1-pXcUu4I0AM'

wts_fieldnames = ['WTSN', 'STATE', 'TEMP', 'NAME', 'CHECK', 'GPIO']
wf_blr_fieldnames = ['STATE', 'T_CTRL', 'TEMP', 'TEMP_SET']
pump_fieldnames = ['STATE','PUMP_1_1_SW', 'PUMP_1_2_SW', 'PUMP_2_1_SW', 'PUMP_2_2_SW','PUMP_1_1_ST', 'PUMP_1_2_ST', 'PUMP_2_1_ST', 'PUMP_2_2_ST']  # numeration must be like in wl.py BOILER_VAR
dobby_fieldnames = ['OS','DBG', 'LOG', 'EMULATION', 'UPDATE_TIME', 'TOKEN']

temp= {'WF_MIN':20, 'WF_MAX': 50, 'BOILER_MIN': 10, 'BOILER_MAX': 65}

wts = []
wf = {}
boiler = {}
pump = {}
dobby = {}

def create_cfg_files(filename):
    if filename==FILENAME_WTS_CONF:
        wtsx = dict.fromkeys(wts_fieldnames)
        wtsx[wts_fieldnames[1]] = 'OFFLINE' #STATE
        wtsx[wts_fieldnames[2]] = '0'       #TEMP
        wtsx[wts_fieldnames[3]] = 'NoName'  #NAME
        wtsx[wts_fieldnames[4]] = '0'       #CHECK
        wtsx[wts_fieldnames[5]] = '0'       #GPIO
        for i in range(16):
            wts.append(wtsx.copy())
            wts[i][wts_fieldnames[0]] = str(i)

        with open(filename, 'w') as outfile:
            json.dump(wts, outfile)

    if filename == FILENAME_WF_CONF:
        wf = dict.fromkeys(wf_blr_fieldnames, '0')

        with open(filename, 'w') as outfile:
            json.dump(wf, outfile)

    if filename==FILENAME_BOILER_CONF:
        boiler = dict.fromkeys(wf_blr_fieldnames, '0')

        with open(filename, 'w') as outfile:
            json.dump(boiler, outfile)

    if filename==FILENAME_PUMP_CONF:
        pump = dict.fromkeys(pump_fieldnames, 'X')

        with open(filename, 'w') as outfile:
            json.dump(pump, outfile)

    outfile.close()

def init_dobby():
    if os.path.isfile(FILENAME_DOBBY_CONF):
        read_dobby()
    else:
        dbg.prints('WARNING! No such file:'+ FILENAME_DOBBY_CONF)
        dobby = dict.fromkeys(dobby_fieldnames)
        dobby[dobby_fieldnames[0]]='WIN'
        dobby[dobby_fieldnames[1]]='OFF'
        dobby[dobby_fieldnames[2]] = 'OFF'
        dobby[dobby_fieldnames[3]] = 'OFF'
        dobby[dobby_fieldnames[4]] = '1000'
        dobby[dobby_fieldnames[5]] = DOBBY_TOKEN

def init():

    if os.path.isfile(FILENAME_WTS_CONF):
        read_wts()
    else:
        dbg.prints('WARNING! No such file:' + FILENAME_WTS_CONF)
        dbg.prints('Creating file...')
        create_cfg_files(FILENAME_WTS_CONF)

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

# =====================  DOBBY =============================

def read_dobby():
    dobby.update(read_config(FILENAME_DOBBY_CONF))

# =====================  WTS =============================
# --------------CONFIG------------
# WTSN / STATE / TEMP / NAME / CHECK
# --------------------------------

def read_wts():
    global wts
    wts = read_config(FILENAME_WTS_CONF)


def write_wts():
    write_config(FILENAME_WTS_CONF, wts)


def wts_checking_toggle(wts_num):
    if wts[wts_num][wts_fieldnames[4]] == '0':
        wts[wts_num][wts_fieldnames[4]] = '1'
    else:
        wts[wts_num][wts_fieldnames[4]] = '0'

    write_wts()


def wts_checking_onoff(wts_num, onoff):
    if onoff == 'on':
        wts[wts_num][wts_fieldnames[4]] = '1'
    elif onoff == 'off':
        wts[wts_num][wts_fieldnames[4]] = '0'
    else:
        dbg.dbg.printss('wrong wts_check_onoff arg')
    write_wts()


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
