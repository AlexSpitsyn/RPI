#!/usr/bin/python
# encoding=utf8

# reload (sys)
# sys.setdefaultencoding('utf8')

import json
import os

FILENAME_WTS_CONF = "wts.cfg"
FILENAME_BOILER_CONF = "boiler.cfg"
FILENAME_WF_CONF = "wf.cfg"
FILENAME_CIRC_CONF = "circ.cfg"

wts_addr = [0x53545701, 0x54545701, 0x55545701, 0x56545701, 0x57545701, 0x58545701, 0x59545701, 0x5A545701, 0x5B545701,
            0x5C545701, 0x5D545701, 0x5E545701, 0x5F545701, 0x60545701, 0x61545701, 0x62545701]
wfcr_addr = 0x52434657
boiler_addr = 0x524C4F42

wts_fieldnames = ['WTSN', 'STATE', 'TEMP', 'NAME', 'CHECK']
wf_blr_fieldnames = ['STATE', 'T_CTRL', 'TEMP', 'TEMP_SET']  # numeration must be like in wl.py WF_VAR
circ_fieldnames = ['CIRC1_1', 'CIRC1_2', 'CIRC2_1', 'CIRC2_2']  # numeration must be like in wl.py BOILER_VAR

wts = []
wf = {}
boiler = {}
circ = {}


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

        with open(FILENAME_WTS_CONF, 'w') as outfile:
            json.dump(wts, outfile)

    if filename == FILENAME_WF_CONF:
        wf = dict.fromkeys(wf_blr_fieldnames)
        with open(FILENAME_WF_CONF, 'w') as outfile:
            json.dump(wf, outfile)

    if filename==FILENAME_BOILER_CONF:
        boiler = dict.fromkeys(wf_blr_fieldnames)
        with open(FILENAME_BOILER_CONF, 'w') as outfile:
            json.dump(boiler, outfile)

    if filename==FILENAME_CIRC_CONF:
        circ = dict.fromkeys(circ_fieldnames)
        with open(FILENAME_CIRC_CONF, 'w') as outfile:
            json.dump(circ, outfile)


def init():
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
        print('wrong wts_check_onoff arg')
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
        print("read file error: " + filename)


def write_config(filename, dct):
    try:
        with open(filename, 'w') as outfile:
            json.dump(dct, outfile)

    except IOError:
        print("write config file error: " + filename)
