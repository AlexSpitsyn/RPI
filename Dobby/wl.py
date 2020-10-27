#!/usr/bin/python
# encoding=utf8


import subprocess 
import config

#reload (sys)
#sys.setdefaultencoding('utf8')

DEBUG = False
EMULATION = False
DEBUG_SX1278 = False
LOG_SX1278 = False

def dbg_print(*args, **kwargs):
   if DEBUG:
      print(*args, **kwargs)
	  
	  

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



def wl_rw(addr, cmd, var, val):

	d=''
	l=''
	
	dbg_print ('Send Packet to:',hex(addr))
	dbg_print ('CMD:', cmd)
	dbg_print ('VAR:', var)
	dbg_print ('VAL:', val)
	

	if EMULATION:
		dbg_print ('Warning!!! Emulation mode')
		dbg_print ("wl_send_cmd", hex(addr), cmd,var, val)
		wl_send_code=0#WL_OK
		# ADDR;STATE;CMD;VAR;VAL;DESC;ERROR_CODE
		wl_send_ret_str= str(addr)+';'+'0'+';'+cmd+';'+var+';'+str(val)+';'+'test;0'
	else:
		if DEBUG_SX1278:
			d='-d'
		
		if LOG_SX1278:
			l='-l'
		dbg_print ('Sending...')	
		res = subprocess.run(["wl_send_cmd", str(hex(addr)), cmd,var, str(val), d, l],stdout=subprocess.PIPE, encoding='utf-8')	
		wl_send_code=res.returncode
		#========  return code 	=========	
		# 0	ok
		# 1	address fail
		# 2	bad crc
		# 3	error
		# 4	offline	
		# 101 addr not specified	
		# 102 wrong TX ADDR
		# 103 cmd not specified
		# 104 wrong TX CMD
		# 105 wrong TX VAR
		# 106 wrong TX VAL
		#=================================

		wl_send_ret_str=res.stdout
		
	
	if wl_send_code==0:#WL_OK
		dbg_print ("=====PACKET RECIEVED=====")
		dbg_print ("WL PACK STATE: ",wl_send_code, ' / '+ WL_STATE[wl_send_code])

		# ADDR;STATE;CMD;VAR;VAL;DESC;ERROR_CODE
		parts=wl_send_ret_str.split(';')
		addr = parts[0]	
		cmd_state = int(parts[1])
		#cmd = parts[2]	
		var = parts[3]
		val = parts[4]	
		desc = parts[5]	
		dev_error_code = parts[6]
		
		
		dbg_print('ADDR: ', hex(int(addr)))
		dbg_print('CMD STATE: ', WL_CMD_STATE[cmd_state])
		dbg_print('CMD: ', cmd)
		dbg_print('VAR: ', var)
		dbg_print('VAL: ', val)
		dbg_print('DESC: ', desc)
		dbg_print('DEV ERRROR CODE: ', dev_error_code)		

		
		return WL_STATE[wl_send_code], WL_CMD_STATE[cmd_state], dev_error_code, val
	
	else:
		
		return WL_STATE[wl_send_code],wl_send_ret_str,'0','0'


	
	
#=====================  WTS =============================	
	
WTS_VAR = {
	'temp':'0',	
	't_updt_time':'1'
}

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

	
	wl_send_state, cmd_state, dev_error_code, retval = wl_rw(config.wts_addr[wtsn], CMD['GET'], WTS_VAR['temp'], 0)
	
	if dev_error_code != '0':
		dbg_print('WARNING! DevERC: ' + str(dev_error_code))		
		config.wts[wtsn]["STATE"] = str(dev_error_code)	
	else:
		config.wts[wtsn]["STATE"] = wl_send_state
	
	
	if wl_send_state==WL_STATE[0]:#OK
		if cmd_state=='DONE':		
			config.wts[wtsn]["TEMP"] = retval
			dbg_print('Write wts config! ', config.wts[wtsn])
		else:
			dbg_print('WARNING! ', cmd_state)
			config.wts[wtsn]["TEMP"] = 'X'
	else:
		config.wts[wtsn]["TEMP"] = 'X'
	
	config.write_wts()	
	
	return cmd_state

def update_wts():
	for wts_conf in config.wts:
		if wts_conf["CHECK"] =='1':			
			res = read_wts(int(wts_conf["WTSN"]))
			dbg_print('Read WTS' + wts_conf["WTSN"]+':'+ res)

#=====================  WF ===============================
#STATE / T_CTRL / TEMP / TEMP_SET
WF_VAR = {
	'TEMP':'0',
	'T_CTRL':'1',
	'TEMP_SET':'2',
	't_ctrl_time':'3',
	't_updt_time':'4',
	't_hyst':'5',
	'pump':'6',
	'drv_pos':'7',
	'drv_pos_max':'8',
	'drv_pos_dest':'9',
	'drv_steps':'10'
}
def send_to_wf(cmd, var, val):
	
	wl_send_state, cmd_state, dev_error_code, retval = wl_rw(config.wfcr_addr, cmd, var, val)
	if dev_error_code != '0':
		dbg_print('WARNING! DevERC: ' + str(dev_error_code))		
		config.wf["STATE"] = str(dev_error_code)	
	else:
		config.wf["STATE"] = wl_send_state
			
	if wl_send_state==WL_STATE[0]:#OK			 
		if cmd_state=='DONE':
			config.wf[list(WF_VAR.keys())[int(var)]]=str(retval)
		else:
			dbg_print(cmd_state)
			config.wf[list(WF_VAR.keys())[int(var)]] = 'X'
	else:
		dbg_print(wl_send_state)
		config.wf[list(WF_VAR.keys())[int(var)]] = 'X'
	
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
BOILER_VAR = {
	'TEMP':'0',
	'T_CTRL':'1',
	'TEMP_SET':'2',
	't_ctrl_time':'3',
	't_updt_time':'4',
	't_hyst':'5',
	'pump':'6',
	'burner':'7',
	't_th':'8',
}

def send_to_boiler(cmd, var, val):
	
	wl_send_state, cmd_state, dev_error_code, retval = wl_rw(config.boiler_addr, cmd, var, val)
	if dev_error_code != '0':
		dbg_print('WARNING! DevERC: ' + str(dev_error_code))		
		config.boiler["STATE"] = str(dev_error_code)	
	else:
		config.boiler["STATE"] = wl_send_state
			
	if wl_send_state==WL_STATE[0]:#OK			 
		if cmd_state=='DONE':
			config.boiler[list(BOILER_VAR.keys())[int(var)]]=str(retval)
		else:
			dbg_print(cmd_state)
			config.boiler[list(BOILER_VAR.keys())[int(var)]] = 'X'
	else:
		dbg_print(wl_send_state)
		config.boiler[list(BOILER_VAR.keys())[int(var)]] = 'X'
	
	config.write_boiler()
	
	return cmd_state
	


def get_boiler(var):	
	return send_to_boiler(CMD['GET'], var, 0)	
	

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
	
	
	config.write_circ()
		
		
	return cmd_state
	
	

def circ_onoff(circ_name, onoff):
		
	config.circ[circ_name]=str(onoff)
	bit_str='000000010000'+ config.circ[config.circ_fieldnames[0]] + config.circ[config.circ_fieldnames[1]]+ config.circ[config.circ_fieldnames[2]] + config.circ[config.circ_fieldnames[3]] 
	
	val=int(bit_str,2)	
	
	wl_send_state, cmd_state, dev_error_code, retval = wl_rw(config.wfcr_addr, CMD['SET'], WF_VAR['pump'], val)
	
	if dev_error_code != '0':
		dbg_print('WARNING! DevERC: ' + str(dev_error_code))		

			
	if wl_send_state==WL_STATE[0]:#OK			 
		if cmd_state=='DONE':					
			dbg_print('CIRC RETURN VAL: ' + str(hex(int(retval))))
		else:
			dbg_print('WARNING! ', cmd_state)
			config.circ[circ_name]='X'

	else:
		dbg_print('WARNING! ', wl_send_state)
		config.circ[circ_name]='X'	
	
	config.write_circ()				
		
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
