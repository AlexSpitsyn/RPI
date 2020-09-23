#!/usr/bin/python
# encoding=utf8


import subprocess 
import config
import os

#reload (sys)
#sys.setdefaultencoding('utf8')

DEBUG = False
EMULATION = False


def dbg_print(*args, **kwargs):
   if DEBUG:
      print(*args, **kwargs)
	  
	  
WTS_VAR = {
	'TEMP':'0',	
	'T_UPDT_TIME':'1'
}


WF_VAR = {
	'temp':'0',
	't_ctrl':'1',
	't_set':'2',
	't_ctrl_time':'3',
	't_updt_time':'4',
	't_hyst':'5',
	'pump':'6',
	'drv_pos':'7',
	'drv_pos_max':'8',
	'drv_pos_dest':'9',
	'drv_steps':'10'
}

BOILER_VAR = {
	'temp':'0',
	't_ctrl':'1',
	't_set':'2',
	't_ctrl_time':'3',
	't_updt_time':'4',
	't_hyst':'5',
	'pump':'6',
	'burner':'7',
	't_th':'8',
}



CMD = {'CMD_PRESENT':'0',
	'GET':'1', 
	'SET':'2', 
	'EEPROM_WR':'3',
	'ERR_CLR':'4' }
	
WL_CMD_STATE = {
	0:'DONE',
	1:'CMD_NOT_SUPPORTED',
	2:'VAR_NOT_SUPPORTED',
	3:'VAL_NOT_SUPPORTED',
	4:'ERROR',

};


WL_STATE={
  0:'OK',
  1:'ADDRESS_FAIL',  
  2:'CRC_BAD',
  3:'ERROR',
  4:'OFFLINE',

};


last_pack_state = 0


# def wl_send_data(addr, cmd, var, val):
	# if EMULATION:
		# dbg_print ('Warning!!! Emulation mode')
		# dbg_print ("wl_send_cmd", hex(addr), cmd,var, val)
		# wl_state=0#WL_OK
	# else:
		# wl_state = subprocess.call(["wl_send_cmd", hex(addr), cmd,var, val]) 
	
		
	# last_pack_state = wl_state
	# dbg_print ("WL PACK STATE: " + WL_STATE[wl_state])
	# return wl_state



def wl_rw(addr, cmd, var, val):

	dbg_print ('wl_send addr:',addr, 'cmd:', cmd, 'var:', var, 'val:', val)
	
	

	if EMULATION:
		dbg_print ('Warning!!! Emulation mode')
		dbg_print ("wl_send_cmd", hex(addr), cmd,var, val)
		wl_send_state=0#WL_OK
	else:
		wl_send_state = subprocess.call(["wl_send_cmd", hex(addr), cmd,var, val]) 
	
		
	#last_pack_state = wl_state
	dbg_print ("WL PACK STATE: " + WL_STATE[wl_send_state])

	if wl_send_state==0:#WL_OK
	
		try:
			# ADDR;STATE;CMD;VAR;VAL;DESC:ERROR_CODE
			file_handler = open(config.FILENAME_WL_SEND_RET)
			data= file_handler.readline() # read just one line
			parts=data.split(';')
			addr = parts[0]	
			cmd_state = int(parts[1])
			#cmd = parts[2]	
			var = parts[3]
			val = parts[4]	
			desc = parts[5]	
			dev_error_code = parts[6]
			dbg_print('ADDR: ', addr)
			dbg_print('CMD STATE: ', WL_CMD_STATE[cmd_state])
			dbg_print('CMD: ', cmd)
			dbg_print('VAR: ', var)
			dbg_print('VAL: ', val)
			dbg_print('DESC: ', desc)
			dbg_print('DEV ERRROR CODE: ', dev_error_code)
			file_handler.close()
			
			#REMOVE FILE AFTER READING
		
			if EMULATION:
				dbg_print ('Warning!!! Emulation mode. File retpack.txt not removed')				
			else:
				os.remove(config.FILENAME_WL_SEND_RET)	
			
			return WL_STATE[wl_send_state], WL_CMD_STATE[cmd_state], dev_error_code, val

			
		except IOError:
			print("An IO Error has occurred!")		
			return 'FAIL','File read error','0','0'
		
	else:		
		return WL_STATE[wl_send_state],WL_STATE[wl_send_state],'0','0'


	
	
#=====================  WTS =============================	
def read_wts(wtsn):
	#wl_rw retval WL_STATE, WL_CMD_STATE, DEV ERRROR CODE, VALUE
	# WL_STATE:		'OK',
	#				'ADDRESS_FAIL'  
	#				'CRC_BAD'
	#				'ERROR'
	#				'OFFLINE'
	#				'FAIL' File read error
	
	# WL_CMD_STATE:	'DONE'	
	#				'CMD NOT SUPPORTED'
	#				'VAR NOT SUPPORTED'
	#				'VAL NOT SUPPORTED'	
	#				'ERROR'
	
	
	
	wl_send_state, cmd_state, dev_error_code, retval = wl_rw(config.wts_addr[wtsn], CMD['GET'], WTS_VAR['TEMP'], 0)
	
	if dev_error_code != '0':
		dbg_print('WARNING! DevERC: ' + str(dev_error_code))		
		config.wts[wtsn]["STATE"] = str(dev_error_code)	
	else:
		config.wts[wtsn]["STATE"] = wl_send_state
	
	
	if wl_send_state==WL_STATE[0]:#OK
		if cmd_state=='DONE':		
			config.wts[wtsn]["TEMP"] = retval			
		else:
			dbg_print('WARNING! ', cmd_state)
			config.wts[wtsn]["TEMP"] = 'X'
	else:
		config.wts[wtsn]["TEMP"] = 'X'
	
	config.write_wts()	
	
	return cmd_state



#=====================  WF ================ ====== =======
#STATE / T_CTRL / TEMP / TEMP_SET

def send_to_wf(cmd, var, val):
	
	wl_send_state, cmd_state, dev_error_code, retval = wl_rw(config.wfcr_addr, cmd, var, val)
	if dev_error_code != '0':
		dbg_print('WARNING! DevERC: ' + str(dev_error_code))		
		config.wf["STATE"] = str(dev_error_code)	
	else:
		config.wf["STATE"] = wl_send_state
			
	if wl_send_state==WL_STATE[0]:#OK			 
		if cmd_state=='DONE':
			config.wf[list(VAR.keys())[int(var)]]=str(retval)
		else:
			dbg_print('WARNING! ', cmd_state)
			config.wf[list(VAR.keys())[int(var)]] = 'X'
	else:
		dbg_print('WARNING! ', wl_send_state)
		config.wf[list(VAR.keys())[int(var)]] = 'X'
	
	config.write_wf()
	
	return cmd_state
	
	
def get_wf(var):
	return send_to_wf(CMD['GET'], var, 0)

def set_wf(var, val):	
	return send_to_wf(CMD['SET'], var, val)	
	
def update_wf():
	if get_wf(WF_VAR['T_CTRL']) == 'DONE' and get_wf(WF_VAR['TEMP']) == 'DONE' and get_wf(WF_VAR['TEMP_SET']) == 'DONE':
		return 'OK'
	else:
		return 'FAIL'

	
def toggle_wf():
	if config.wf['T_CTRL'] == '0':
		return set_wf(WF_VAR['T_CTRL'], 1)

	elif config.wf['T_CTRL'] == '1':
		return set_wf(WF_VAR['T_CTRL'], 0)
			

	
#=====================  BOILER =================== ==========
#------CONFIG-----------
#STATE / T_CTRL / TEMP / TEMP_SET
#-----------------------

def send_to_boiler(cmd, var, val):
	
	wl_send_state, cmd_state, dev_error_code, retval = wl_rw(config.boiler_addr, cmd, var, val)
	if dev_error_code != '0':
		dbg_print('WARNING! DevERC: ' + str(dev_error_code))		
		config.boiler["STATE"] = str(dev_error_code)	
	else:
		config.boiler["STATE"] = wl_send_state
			
	if wl_send_state==WL_STATE[0]:#OK			 
		if cmd_state=='DONE':
			config.boiler[list(VAR.keys())[int(var)]]=str(retval)
		else:
			dbg_print('WARNING! ', cmd_state)
			config.boiler[list(VAR.keys())[int(var)]] = 'X'
	else:
		dbg_print('WARNING! ', wl_send_state)
		config.boiler[list(VAR.keys())[int(var)]] = 'X'
	
	config.write_boiler()
	
	return cmd_state
	


def get_boiler(var):	
	return send_to_boiler(CMD['SET'], var, 0)	
	

def set_boiler(var, val):	
	return send_to_boiler(CMD['SET'], var, val)	


def update_boiler():
	if get_boiler(BOILER_VAR['T_CTRL']) == 'DONE' and get_boiler(BOILER_VAR['TEMP']) == 'DONE' and  get_boiler(BOILER_VAR['TEMP_SET']) == 'DONE':
		return 'OK'
	else:
		return 'FAIL'
	

def toggle_boiler():

	if config.boiler['T_CTRL'] == '0':
		return set_boiler(BOILER_VAR['T_CTRL'], 1) 
			
	elif config.boiler['T_CTRL']  == '1':
		return set_boiler(BOILER_VAR['T_CTRL'], 0)

	
#=====================  CIRC ===================== ========	
#CIRC1_1 / CIRC1_2 / CIRC2_1 / CIRC2_2 
def get_circ():	
	wl_send_state, cmd_state, dev_error_code, retval = wl_rw(config.wfcr_addr, CMD['GET'], var, 0)
	
	
		
	if dev_error_code != '0':
		dbg_print('WARNING! DevERC: ' + str(dev_error_code))		

			
	if wl_send_state==WL_STATE[0]:#OK			 
		if cmd_state=='DONE':
			bit_str=str(bin(int(retval)))		
			dbg_print('CIRC RETURN VAL: ' + bit_str)
			config.circ[circ_fieldnames[3]]=bit_str[-5]
			config.circ[circ_fieldnames[2]]=bit_str[-6]
			config.circ[circ_fieldnames[1]]=bit_str[-7]
			config.circ[circ_fieldnames[0]]=bit_str[-8]	
		else:
			dbg_print('WARNING! ', cmd_state)
			config.circ[circ_fieldnames[3]]='X'
			config.circ[circ_fieldnames[2]]='X'
			config.circ[circ_fieldnames[1]]='X'
			config.circ[circ_fieldnames[0]]='X'
	else:
		dbg_print('WARNING! ', wl_send_state)
		config.circ[circ_fieldnames[3]]='X'
		config.circ[circ_fieldnames[2]]='X'
		config.circ[circ_fieldnames[1]]='X'
		config.circ[circ_fieldnames[0]]='X'
	
	
	config.write_boiler()		
		
		
	return cmd_state
	
	

def circ_onoff(circ_name, onoff):
		
	config.circ[circ_name]=str(onoff)
	bit_str='0000'+ config.circ[config.circ_fieldnames[0]] + config.circ[config.circ_fieldnames[1]]+ config.circ[config.circ_fieldnames[2]] + config.circ[config.circ_fieldnames[3]] + '00000000'
	
	val=int(bit_str,2)	
	
	wl_send_state, cmd_state, dev_error_code, retval = wl_rw(config.wfcr_addr, CMD['SET'], WF_VAR['pump'], val)
	
	if dev_error_code != '0':
		dbg_print('WARNING! DevERC: ' + str(dev_error_code))		

			
	if wl_send_state==WL_STATE[0]:#OK			 
		if cmd_state=='DONE':					
			dbg_print('CIRC RETURN VAL: ' + bit_str)
		else:
			dbg_print('WARNING! ', cmd_state)
			config.circ[circ_name]='X'

	else:
		dbg_print('WARNING! ', wl_send_state)
		config.circ[circ_name]='X'	
	
	config.write_boiler()				
		
	return cmd_state
	
	
	
def toggle_circ(circ_name):	
	bit_str = ''	

	if config.circ[circ_name]=='0':
		return circ_onoff(circ_name, 1)
	else:
		return circ_onoff(circ_name, 0)

	
def get_key(dct, value):
    for k, v in dct.items():
        if v == value:
            return k	
