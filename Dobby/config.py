
import os
import sys
import csv

#reload (sys)
#sys.setdefaultencoding('utf8')

FILENAME_WL_SEND_RET = "retpack.txt"
FILENAME_WTS_CONG = "wts_conf.txt"
FILENAME_BOILER_CONF = "boiler_conf.txt"
FILENAME_WF_CONF = "wf_conf.txt"
FILENAME_CIRC_CONF = "circ_conf.txt"


wts_addr=[22238295,39015511,55792727,72569943,89347159,106124375,122901591,139678807,156456023,173233239,190010455,206787671,223564887,240342103,257119319,273896535]
wfcr_addr = 1380140631
boiler_addr = 1380732738

wts_base=16777216

wts_fieldnames =  ['WTSN' , 'STATE' , 'TEMP' , 'NAME', 'CHECK']
wf_blr_fieldnames =  ['T_CTRL' , 'TEMP' , 'TEMP_SET']
circ_fieldnames =  ['CIRC_MAIN' ,'CIRC_HB' , 'CIRC1_1' , 'CIRC1_2' , 'CIRC2_1' , 'CIRC2_2']

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
		with open(FILENAME_WTS_CONG, "r") as in_file:
			reader = csv.DictReader(in_file, delimiter=';')
			for row in reader:			
				wts.append(row)
	except IOError:
		print("Read file"+FILENAME_WTS_CONG + 'FAIL')
		
	#return wts_line

def write_wts():		
		
	with open(FILENAME_WTS_CONG, 'w') as out_file:
		writer = csv.DictWriter(out_file, delimiter=';', fieldnames=wts_fieldnames)
		writer.writeheader()
		for row in wts:
			writer.writerow(row)

def wts_toggle_check(wts_num):	

	if wts[wts_num][wts_fieldnames[4]]=='0':
		wts[wts_num][wts_fieldnames[4]]='1'
	else:
		wts[wts_num][wts_fieldnames[4]]='0'
	
	write_wts()
	
		
		
		
#=====================  WF =============================
#------CONFIG-----------
#STATE / TEMP / TEMP_SET
#-----------------------
def read_wf():

	read_file_to_dict(FILENAME_WF_CONF, wf)
		
def write_wf():	
	
	write_dict_to_file(FILENAME_WF_CONF, wf)
	
#=====================  BOILER =============================
#------CONFIG-----------
#STATE / TEMP / TEMP_SET
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





