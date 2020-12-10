#!/usr/bin/python
# encoding=utf8

# reload (sys)
# sys.setdefaultencoding('utf8')

import json
import os
import dbg

CONFIG_PATH = "config/"
FILENAME_WTS_CONF = CONFIG_PATH + "wts.cfg"
FILENAME_BOILER_CONF = CONFIG_PATH + "boiler.cfg"
FILENAME_WF_CONF = CONFIG_PATH + "wf.cfg"
FILENAME_CIRC_CONF = CONFIG_PATH + "circ.cfg"
FILENAME_DOBBY_CONF = CONFIG_PATH + "dobby.cfg"

wts_addr = [0x53545701,0x53545702,0x53545703,0x53545704,0x53545705,0x53545706,0x53545707,0x53545708,0x53545709,0x5354570A,0x5354570B,0x5354570C,0x5354570D,0x5354570E,0x5354570F,0x53545710]
wfcr_addr = 0x52434657
boiler_addr = 0x524C4F42

wts_fieldnames = ['WTSN', 'STATE', 'TEMP', 'NAME', 'CHECK']
wf_blr_fieldnames = ['STATE', 'T_CTRL', 'TEMP', 'TEMP_SET']
circ_fieldnames = ['CIRC1_1', 'CIRC1_2', 'CIRC2_1', 'CIRC2_2']  # numeration must be like in wl.py BOILER_VAR
dobby_fieldnames = ['DBG', 'LOG', 'EMULATION', 'UPDATE_TIME']

wts = []
wf = {}
boiler = {}
circ = {}
dobby = {}

def create_cfg_files(filename):
    if filename==FILENAME_WTS_CONF:
        wtsx = dict.fromkeys(wts_fieldnames)
        wtsx[wts_fieldnames[1]] = 'OFFLINE'
        wtsx[wts_fieldnames[2]] = '0'
        wtsx[wts_fieldnames[3]] = 'NoName'
        wtsx[wts_fieldnames[4]] = '0'
        for i in range(16):
            wts.append(wtsx.copy())
            wts[i][wts_fieldnames[0]] = str(i)

        with open(filename, 'w') as outfile:
            json.dump(wts, outfile)

    if filename == FILENAME_WF_CONF:
        wf = dict.fromkeys(wf_blr_fieldnames)
        wf[wf_blr_fieldnames[0]] = '0'
        wf[wf_blr_fieldnames[1]] = '0'
        wf[wf_blr_fieldnames[2]] = '0'
        wf[wf_blr_fieldnames[3]] = '0'
        with open(filename, 'w') as outfile:
            json.dump(wf, outfile)

    if filename==FILENAME_BOILER_CONF:
        boiler = dict.fromkeys(wf_blr_fieldnames)
        boiler[wf_blr_fieldnames[0]] = '0'
        boiler[wf_blr_fieldnames[1]] = '0'
        boiler[wf_blr_fieldnames[2]] = '0'
        boiler[wf_blr_fieldnames[3]] = '0'
        with open(filename, 'w') as outfile:
            json.dump(boiler, outfile)

    if filename==FILENAME_CIRC_CONF:
        circ = dict.fromkeys(circ_fieldnames)
        circ[circ_fieldnames[0]]='0'
        circ[circ_fieldnames[1]] = '0'
        circ[circ_fieldnames[2]] = '0'
        circ[circ_fieldnames[3]] = '0'
        with open(filename, 'w') as outfile:
            json.dump(circ, outfile)


def init():
    if os.path.isfile(FILENAME_DOBBY_CONF):
        read_dobby()
    else:
        dobby = dict.fromkeys(dobby_fieldnames)
        dobby[dobby_fieldnames[0]]='OFF'
        dobby[dobby_fieldnames[1]] = 'OFF'
        dobby[dobby_fieldnames[2]] = 'OFF'
        dobby[dobby_fieldnames[3]] = '1000'


    if os.path.isfile(FILENAME_WTS_CONF):
        read_wts()
    else:
        create_cfg_files(FILENAME_WTS_CONF)

    if os.path.isfile(FILENAME_WF_CONF):
        read_wf()
    else:
        create_cfg_files(FILENAME_WF_CONF)

    if os.path.isfile(FILENAME_BOILER_CONF):
        read_boiler()
    else:
        create_cfg_files(FILENAME_BOILER_CONF)

    if os.path.isfile(FILENAME_CIRC_CONF):
        read_circ()
    else:
        create_cfg_files(FILENAME_CIRC_CONF)

# =====================  DOBBY =============================

def read_dobby():
    dobby.update(read_config(FILENAME_DOBBY_CONF))

# =====================  WTS =============================
# --------------CONFIG------------
# WTSN / STATE / TEMP / NAME / CHECK
# --------------------------------

def read_wts():
    wts.extend(read_config(FILENAME_WTS_CONF))


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


# =====================  CIRC =============================
# -----------------CONFIG--------------------------------------
# CIRC1_1_STATE / CIRC1_2_STATE / CIRC2_1_STATE / CIRC2_2_STATE
# -------------------------------------------------------------
def read_circ():
    circ.update(read_config(FILENAME_CIRC_CONF))


def write_circ():
    write_config(FILENAME_CIRC_CONF, circ)


def read_config(filename):
    try:
        with open(filename, "r") as read_file:
            dct = json.load(read_file)
        return dct

    except IOError:
        dbg.prints("read file error: " + filename)


def write_config(filename, dct):
    try:
        with open(filename, 'w') as outfile:
            json.dump(dct, outfile)

    except IOError:
        dbg.prints("write config file error: " + filename)
