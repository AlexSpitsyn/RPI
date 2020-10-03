#!/usr/bin/python
# encoding=utf8

import os
import sys
import csv

#reload (sys)
#sys.setdefaultencoding('utf8')

FILENAME_WL_SEND_RET = "retpack.txt"
FILENAME_WTS_CONF = "wts_conf.txt"
FILENAME_BOILER_CONF = "boiler_conf.txt"
FILENAME_WF_CONF = "wf_conf.txt"
FILENAME_CIRC_CONF = "circ_conf.txt"


wts_addr=[0x53545701,0x54545701,0x55545701,0x56545701,0x57545701,0x58545701,0x59545701,0x5A545701,0x5B545701,0x5C545701,0x5D545701,0x5E545701,0x5F545701,0x60545701,0x61545701,0x62545701]
wfcr_addr = 0x52434657
boiler_addr = 0x524C4F42



wts_fieldnames =  ['WTSN' , 'STATE' , 'TEMP' , 'NAME', 'CHECK']
wf_blr_fieldnames =  ['STATE' ,'T_CTRL' , 'TEMP' , 'TEMP_SET']# numeration must be like in wl.py WF_VAR
circ_fieldnames =  ['CIRC1_1' , 'CIRC1_2' , 'CIRC2_1' , 'CIRC2_2']# numeration must be like in wl.py BOILER_VAR

wts = []
wf = dict.fromkeys(wf_blr_fieldnames)
boiler = dict.fromkeys(wf_blr_fieldnames)
circ = dict.fromkeys(circ_fieldnames)

temp = {'BOILER_MIN':30,'BOILER_MAX':70, 'WF_MIN':5,'WF_MAX':50}



def init():	
	read_wts()	
	read_wf()
	read_boiler()	
	read_circ()
		
	

#=====================  WTS =============================
#--------------CONFIG------------	
#WTSN / STATE / TEMP / NAME / CHECK
#--------------------------------
	
def read_wts():

	#wts_line = []
	try:
		with open(FILENAME_WTS_CONF, "r") as in_file:
			reader = csv.DictReader(in_file, delimiter=';')
			for row in reader:			
				wts.append(row)
	except IOError:
		print("Read file"+FILENAME_WTS_CONF + 'FAIL')
		
	#return wts_line

def write_wts():		
		
	with open(FILENAME_WTS_CONF, 'w') as out_file:
		writer = csv.DictWriter(out_file, delimiter=';', fieldnames=wts_fieldnames)
		writer.writeheader()
		for row in wts:
			writer.writerow(row)

def wts_checking_toggle(wts_num):	

	if wts[wts_num][wts_fieldnames[4]]=='0':
		wts[wts_num][wts_fieldnames[4]]='1'
	else:
		wts[wts_num][wts_fieldnames[4]]='0'
	
	write_wts()
	
def wts_checking_onoff(wts_num, onoff):	

	if onoff=='on':
		wts[wts_num][wts_fieldnames[4]]='1'
	elif onoff=='off':
		wts[wts_num][wts_fieldnames[4]]='0'
	else:
		print('wrong wts_check_onoff arg')
	write_wts()		
		
		
#=====================  WF =============================
#------CONFIG-----------
#STATE / T_CTRL / TEMP / TEMP_SET
#-----------------------
def read_wf():

	read_file_to_dict(FILENAME_WF_CONF, wf)
		
def write_wf():	
	
	write_dict_to_file(FILENAME_WF_CONF, wf)
	
#=====================  BOILER =============================
#------CONFIG-----------
#STATE / T_CTRL / TEMP / TEMP_SET
#-----------------------
		
def read_boiler():

	read_file_to_dict(FILENAME_BOILER_CONF, boiler)
			
		
def write_boiler():	
	
	write_dict_to_file(FILENAME_BOILER_CONF, boiler)
	
		
	
#=====================  CIRC =============================	
#-----------------CONFIG--------------------------------------
#CIRC1_1_STATE / CIRC1_2_STATE / CIRC2_1_STATE / CIRC2_2_STATE 
#-------------------------------------------------------------
def read_circ():

	read_file_to_dict(FILENAME_CIRC_CONF, circ)
	
		
def write_circ():	
	write_dict_to_file(FILENAME_CIRC_CONF, circ)
	
	
def read_file_to_dict(filename, dct):

	try:	
		fieldnames = list(dct.keys())
		file_handler = open(filename, 'r')
		file_handler.readline() # read fielnames
		data= file_handler.readline() # read config
		
		parts=data.rstrip().split(';')
		
		for i in range(len(dct.keys())):
			dct[fieldnames[i]]=parts[i]
		
		file_handler.close()
		return 0
		
	except IOError:
		print("read file error: "+filename)		
		return 1
		
def write_dict_to_file(filename, dct):	

	try:	
		file_handler = open(filename, 'w')	
		
		file_handler.write(merg_str(list(dct.keys()))+'\n')
		file_handler.write(merg_str(list(dct.values())))
		
		file_handler.close()
		return 0
		
	except IOError:
		print("write file error: "+filename)		
		return 1
	

def merg_str(list_var):
	s=''
	for fn in list_var:	
		s=s+str(fn) +';'
	
	return s[0:-1]





