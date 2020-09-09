#!/usr/bin/python
# encoding=utf8


import subprocess 
import config

#reload (sys)
#sys.setdefaultencoding('utf8')

VAR = {
	'TEMP':'0',
	'T_CTRL':'1',
	'TEMP_SET':'2',
	'T_CTRL_TIME':'3',
	'T_UPDT_TIME':'4',
	'T_HYST':'5',
	'DRV_POS':'6',
	'DRV_POS_MAX':'7',
	'DRV_POS_DEST':'8',
	'DRV_STEPS':'9',
	'STATE':'10'
}

CMD = {'CMD_PRESENT':'0',
	'GET':'1', 
	'SET':'2', 
	'EEPROM_WR':'3',
	'ERR_CLR':'4' }
	
PACK_STATE = {
	'0':'NEW',
	'1':'DONE',
	'2':'SEND_OK',
	'3':'ADDR_MATCH',
	'4':'ADDR_MISMATCH',
	'5':'CMD_NOT_SUPPORTED',
	'6':'VAR_NOT_SUPPORTED',
	'7':'VAL_NOT_SUPPORTED',
	'8':'CRC_BAD',
	'9':'CRC_OK',
	'10':'TIMEOUT',
	'11':'ERROR'
};

WL_STATE={
  0:'WL_OK',
  1:'WL_OFFLINE',  
  2:'WL_CMD_NOT_SUPPORTED',
  3:'WL_VAR_NOT_SUPPORTED',
  4:'WL_VAL_NOT_SUPPORTED',
  5:'WL_CRC_BAD',
  6:'WL_ADDRESS_FAIL',
  7:'WL_ERROR'
};
last_pack_state = 0


def wl_send_data(addr, cmd, var, val):
	#return WL_STATE
	#wl_state = subprocess.call(["wl_send_cmd", str(addr), cmd,var, val]) 
	
	print ('Warning!!! Enable run wl_send_cmd')
	wl_state=0#WL_OK
	
	last_pack_state = wl_state
	print ("WL PACK STATE: " + WL_STATE[wl_state])
	return wl_state



def wl_rw(addr, cmd, var, val):

	print ('wl_rw addr cmd var val',addr ,cmd ,var ,val)
	
	wl_send_state=wl_send_data(addr, cmd, var, val)


	if wl_send_state==0:
	
		try:
			# ADDR STATE CMD VAR VAL
			file_handler = open(config.FILENAME_WL_SEND_RET)
			data= file_handler.readline() # read just one line
			parts=data.split(';')
			addr = parts[0]	
			state = parts[1]
			#cmd = parts[2]	
			var = parts[3]
			val = parts[4]	
			print('ADDR: ', addr)
			print('STATE: ', PACK_STATE[state])
			print('CMD: ', cmd)
			print('VAR: ', var)
			print('VAL: ', val)
			file_handler.close()
			#REMOVE FILE AFTER READING
			print ('Warning!!! retpack not removed')
			#os.remove(config.FILENAME_WL_SEND_RET)			
			
			if cmd == CMD['GET']:
				print ('wl_rw return val', cmd, CMD['GET'])
				return val
			else:
				print ('wl_rw return pack_state')
				return PACK_STATE[state]
			
		except IOError:
			print("An IO Error has occurred!")		
			return 'FAIL'
		
	else:		
		return 'FAIL'


	
	
#=====================  WTS =============================	
def read_wts(wtsn):
	
	wl_send_state=wl_send_data(config.wts_addr[wtsn], CMD['GET'], VAR['TEMP'], 0)

	if wl_send_state==0:
	
		try:
			# ADDR STATE CMD VAR VAL
			file_handler = open(config.FILENAME_WL_SEND_RET)
			data= file_handler.readline() # read just one line
			parts=data.split(';')
					 
			config.wts[wts_num]["VAL"] = parts[4]
			config.wts[wts_num]["STATE"] = parts[1]
			
			
			
			file_handler.close()
			os.remove(config.FILENAME_WL_SEND_RET)	
			return 'OK'
			
		except IOError:
			print("An IO Error has occurred!")		
			return 'FAIL'
		
	else:		
		return 'FAIL'



#=====================  WF ================ ====== =======
#T_CTRL / TEMP / TEMP_SET

def get_wf(var):
	
	val = wl_rw(config.wfcr_addr, CMD['GET'], var, 0)
	if val != 'FAIL':		
		config.wf[list(VAR.keys())[int(var)]]=str(val)
		config.write_wf()
	return val
	
	


def set_wf(var, val):	
	res = wl_rw(config.wfcr_addr, CMD['SET'], var, val)
	if res != 'FAIL':
		if res == 'DONE':
			config.wf[list(VAR.keys())[int(var)]]=str(val)
			config.write_wf()
	return res
	
def update_wf():
	if get_wf(VAR['T_CTRL']) == 'FAIL':
		return 'FAIL'
	if get_wf(VAR['TEMP']) == 'FAIL':
		return 'FAIL'
	if get_wf(VAR['TEMP_SET']) == 'FAIL':
		return 'FAIL'
	return 'OK'
	
def toggle_wf():
	if config.wf['T_CTRL'] == '0':
		if set_wf(VAR['T_CTRL'], 1) == 'FAIL':
			return 'FAIL'
		else:
			return 'OK'
	elif config.wf['T_CTRL'] == '1':
		if set_wf(VAR['T_CTRL'], 0) == 'FAIL':
			return 'FAIL'
		else:
			return 'OK'		

	
#=====================  BOILER =================== ==========
#------CONFIG-----------
#T_CTRL / TEMP / TEMP_SET
#-----------------------
def get_boiler(var):	
	val = wl_rw(config.boiler_addr, CMD['GET'], var, 0)	
	if val != 'FAIL':		
		config.boiler[list(VAR.keys())[var]]=val
		config.write_boiler()
	return val

def set_boiler(var, val):	
	res = wl_rw(config.boiler_addr, CMD['SET'], var, val)
	print ('Set boiler return:', res)
	if res != 'FAIL':
		if res == 'DONE':
			config.boiler[list(VAR.keys())[int(var)]]=str(val)
			config.write_boiler()
	return res

def update_boiler():
	if get_boiler(VAR['T_CTRL']) == 'FAIL':
		return 'FAIL'
	if get_boiler(VAR['TEMP']) == 'FAIL':
		return 'FAIL'
	if get_boiler(VAR['TEMP_SET']) == 'FAIL':
		return 'FAIL'
	return 'OK'

def toggle_boiler():

	if config.boiler['T_CTRL'] == '0':
		if set_boiler(VAR['T_CTRL'], 1) == 'FAIL':
			return 'FAIL'
		else:
			return 'OK'
	elif config.boiler['T_CTRL']  == '1':
		if set_boiler(VAR['T_CTRL'], 0) == 'FAIL':
			return 'FAIL'
		else:
			return 'OK'	
	
#=====================  CIRC ===================== ========	
#CIRC_MAIN / CIRC_HB / CIRC1_1 / CIRC1_2 / CIRC2_1 / CIRC2_2 

def get_circ():	
	res = wl_rw(config.wfcr_addr, CMD['GET'], var, 0)
	#res2 = wl_rw(config.wfcr_addr, CMD['GET'], var, 0)
	
	if res != 'FAIL':
		bit_str=str(bin(int(res)))
		
		config.circ[circ_fieldnames[3]]=bit_str[-5]
		config.circ[circ_fieldnames[2]]=bit_str[-6]
		config.circ[circ_fieldnames[1]]=bit_str[-7]
		config.circ[circ_fieldnames[0]]=bit_str[-8]	
		
#	if res2 != 'FAIL':
#		bit_str=str(bin(int(res2)))
#		config.circ[circ_fieldnames[0]]=bit_str[-3]
#		config.circ[circ_fieldnames[1]]=bit_str[-4]
	
	config.write_boiler()
	
	return res	

def set_circ(all_circ_val):	
	res = wl_rw(config.wfcr_addr, CMD['SET'], VAR['STATE'], all_circ_val)
#	res2 = wl_rw(config.boiler_addr, CMD['SET'], VAR['STATE'], all_circ_val)
	if res != 'FAIL' :		
		if res == 'DONE':
			return 'OK'
		else:
			return 'Warning'
	
	else:
		return 'FAIL'
	
def toggle_circ(circ):	
	bit_str = '00000000'	

	if config.circ[circ]=='0':
		config.circ[circ]='1'
	else:
		config.circ[circ]='0'	
		
	bit_str='0000'+ config.circ[config.circ_fieldnames[0]] + config.circ[config.circ_fieldnames[1]]+ config.circ[config.circ_fieldnames[2]] + config.circ[config.circ_fieldnames[3]] 
	

	val=int(bit_str,2)
	print (val)
	res = set_circ(val)
	 
	if res != 'FAIL':
		config.write_circ()
		
	else:
		if config.circ[config.circ_fieldnames[circ]]=='0':
			config.circ[config.circ_fieldnames[circ]]='1'
		else:
			config.circ[config.circ_fieldnames[circ]]='0'
	 
	return res	
	
def get_key(dct, value):
    for k, v in dct.items():
        if v == value:
            return k	
