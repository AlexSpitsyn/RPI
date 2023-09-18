#!/usr/bin/python
# encoding=utf8

from time import sleep
import subprocess 
import config
import dbg
import os
import serial_port


#reload (sys)
#sys.setdefaultencoding('utf8')


EMULATION = False
DEBUG_SX1278 = False
LOG_SX1278 = False



CMD = {'CMD_PRESENT':'0',
	'GET':'1', 
	'SET':'2', 
	'EEPROM_WR':'3',
	'ERR_CLR':'4',
	'RESET':'5'
	}
	
WL_CMD_STATE = {
	0:'DONE',
	1:'CMD_NOT_SUPPORTED',
	2:'VAR_NOT_SUPPORTED',
	3:'VAL_NOT_SUPPORTED',
	4:'ERROR'

};


WL_STATE={
  0:'OK',
  1:'ADDRESS_FAIL',  
  2:'CRC_BAD',
  3:'ERROR',
  4:'OFFLINE',
  5:'BUSY'
};



def wl_rw(addr, cmd, var, val):
	wl_send_code = 0
	d=''
	l=''
	#addr = 0
	cmd_state = 1
	#cmd = 2
	#var = 3
	#val = 4
	desc = 5
	dev_error_code = 6
	
	dbg.prints ('\r\nSend Packet to:',hex(addr))
	dbg.prints ('CMD:', cmd)
	dbg.prints ('VAR:', var)
	dbg.prints ('VAL:', val)
	

	if EMULATION:
		dbg.prints ('Warning!!! Emulation mode')
		dbg.prints ("wl_send_cmd", hex(addr), cmd,var, val)
		# ADDR;STATE;CMD;VAR;VAL;DESC;ERROR_CODE
		# wl_send_ret_str= str(addr)+';'+'0'+';'+cmd+';'+var+';'+str(val)+';'+'test;0'
		return 'OK', 'DONE', '0', '0'
	else:
		if config.dobby['OS'] == 'WIN':
			wl_send_code,addr,cmd_state,cmd,var,val,desc,dev_error_code = serial_port.send_sPort(str(hex(addr)) + ' ' + str(cmd) + ' ' + str(var) + ' ' + str(val))
		else:
			if DEBUG_SX1278:
				d='-d'
			if LOG_SX1278:
				l='-l'
			dbg.prints ('Sending...')
			#--------------------------------------
			#check if another treed use wl_send_cmd
			# --------------------------------------

			wl_busy=1
			if os.path.isfile('wl_idle'):
				dbg.prints('wl busy\r\n')
				cnt = 10
				while (cnt):
					sleep(1)
					if os.path.isfile('wl_idle'):
						cnt = cnt - 1
					else:
						cnt=0
						wl_busy = 0

				#f_wl_idle_data=f_wl_idle.read()
				#idle=1
			else:
				wl_busy = 0
				dbg.prints('wl free\r\n')

			if (wl_busy):
				return WL_STATE[5], '', '0', '0'

			res = subprocess.run(["wl_send_cmd", str(hex(addr)), cmd, var, str(val), d, l],stdout=subprocess.PIPE, encoding='utf-8')
			wl_send_code=res.returncode
			#========  return code from wl_send_cmd	=========
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
			#================================================
			wl_send_ret_str=res.stdout
	
			if wl_send_code==0:#WL_OK
				dbg.prints ("=====PACKET RECIEVED=====")
				dbg.prints ("WL PACK STATE: ",wl_send_code, ' / '+ WL_STATE[wl_send_code])

				# ADDR;STATE;CMD;VAR;VAL;DESC;ERROR_CODE
				parts=wl_send_ret_str.split(';')
				addr = hex(int(parts[0]))
				cmd_state = int(parts[1])
				cmd = parts[2]
				var = parts[3]
				val = parts[4]
				desc = parts[5]
				dev_error_code = parts[6]
			#END LIN
		
		dbg.prints('ADDR: ', addr)
		dbg.prints('CMD STATE: ', WL_CMD_STATE[cmd_state])
		dbg.prints('CMD: ', cmd)
		dbg.prints('VAR: ', var)
		dbg.prints('VAL: ', val)
		dbg.prints('DESC: ', desc)
		dbg.prints('DEV ERRROR CODE: ', dev_error_code)		

		
		return WL_STATE[wl_send_code], WL_CMD_STATE[cmd_state], dev_error_code, val
	




	
	
#=====================  WTS =============================	
	
WTS_VAR = {
	'TEMP':'0',
	't_updt_time':'2',
	'GPIO': '1'
}

def send_to_wts(wtsn, cmd, var, val):
	config.read_wts()
	wl_send_state, cmd_state, dev_error_code, retval = wl_rw(config.wts_addr[wtsn], CMD[cmd], WTS_VAR[var], val)

	config.wts[wtsn]["STATE"] = wl_send_state

	if wl_send_state==WL_STATE[0]:#OK
		if dev_error_code != '0':
			dbg.prints('WARNING! DevERC: ' + str(dev_error_code))
			config.wts[wtsn]["STATE"] = wl_send_state + '- DevERC:' + str(dev_error_code)

		if cmd_state=='DONE':
			if var in config.wts[wtsn]:
				if var == 'TEMP':#convert to signet
					t = int(retval)
					t = (t + 2**7) % 2**8 - 2**7
					retval = str(t)
				config.wts[wtsn][var] = retval
				dbg.prints('Write wts config! ', config.wts[wtsn])
		else:
			dbg.prints('WARNING! ', cmd_state)
			config.wts[wtsn]['STATE'] =	 wl_send_state + '- cmd: ' + cmd_state
	# else:
	# 	if var in config.wts[wtsn]:
	# 		config.wts[wtsn][var] = '0'

	config.write_wts()
	dbg.prints('WTS' + str(wtsn) + ':' + cmd_state)
	return cmd_state, str(retval)

def read_wts(wts_num):
	send_to_wts(wts_num, 'GET', 'TEMP', 0)
	send_to_wts(wts_num, 'GET', 'GPIO', 0)

def update_wts():
	config.read_wts()
	for wts_conf in config.wts:
		if wts_conf["CHECK"] =='1':			
			read_wts(int(wts_conf["WTSN"]))
			read_wts(int(wts_conf["WTSN"]))


def set_gpio_wts(wtsn, GPIO_VAL):
	return send_to_wts(wtsn, 'SET', 'GPIO', GPIO_VAL)[0]

def toggle_gpio_wts(wtsn):
	config.read_wts()
	if config.wts[wtsn]['GPIO'] == '0':
		return set_gpio_wts(wtsn, '1')

	elif config.wts[wtsn]['GPIO'] == '1':
		return set_gpio_wts(wtsn, '0')

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
	config.read_wf()
	wl_send_state, cmd_state, dev_error_code, retval = wl_rw(config.wfcr_addr, CMD[cmd], WF_VAR[var], val)

	config.wf["STATE"] = wl_send_state

	if wl_send_state==WL_STATE[0]:#OK
		if dev_error_code != '0':
			dbg.prints('WARNING! DevERC: ' + str(dev_error_code))
			config.wf["STATE"] = wl_send_state + ' DevERC:' + str(dev_error_code)

		if cmd_state=='DONE':
			if var in config.wf:
				config.wf[var] = retval
				dbg.prints('Write wf config! ', config.wf)
		else:
			dbg.prints('WARNING! ', cmd_state)
			config.wf['STATE'] = wl_send_state + ' cmd: ' + cmd_state
	else:
		if var in config.wf:
			config.wf[var] = 'X'

	config.write_wf()

	return cmd_state, str(retval)
	
	
def get_wf(var):
	return send_to_wf('GET', var, 0)

def set_wf(var, val):	
	return send_to_wf('SET', var, val)
	
def update_wf():
	
	if get_wf('T_CTRL')[0] == 'DONE' and get_wf('TEMP')[0] == 'DONE' and get_wf('TEMP_SET')[0] == 'DONE':
		return 'OK'
	else:
		return 'FAIL'

	
def toggle_wf():
	config.read_wf()
	if config.wf['T_CTRL'] == '0':
		return set_wf('T_CTRL', 1)

	elif config.wf['T_CTRL'] == '1':
		return set_wf('T_CTRL', 0)
			

	
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
	config.read_boiler()
	
	wl_send_state, cmd_state, dev_error_code, retval = wl_rw(config.boiler_addr, CMD[cmd], BOILER_VAR[var], val)
	config.boiler["STATE"] = wl_send_state

	if wl_send_state == WL_STATE[0]:  # OK
		if dev_error_code != '0':
			dbg.prints('WARNING! DevERC: ' + str(dev_error_code))
			config.boiler["STATE"] = wl_send_state + ' DevERC:' + str(dev_error_code)

		if cmd_state == 'DONE':
			if var in config.boiler:
				config.boiler[var] = retval
				dbg.prints('Write boiler config! ', config.boiler)
		else:
			dbg.prints('WARNING! ', cmd_state)
			config.boiler['STATE'] = wl_send_state + ' cmd: ' + cmd_state
	else:

		if var in config.boiler:
			config.boiler[var] = 'X'

	config.write_boiler()
	return cmd_state, str(retval)
	


def get_boiler(var):	
	return send_to_boiler('GET', var, 0)
	

def set_boiler(var, val):	
	return send_to_boiler('SET', var, val)


def update_boiler():

	if get_boiler('T_CTRL')[0] == 'DONE' and get_boiler('TEMP')[0] == 'DONE' and  get_boiler('TEMP_SET')[0] == 'DONE':
		return 'OK'
	else:
		return 'FAIL'
	

def toggle_boiler():
	config.read_boiler()
	if config.boiler['T_CTRL'] == '0':
		return set_boiler('T_CTRL', 1)
			
	elif config.boiler['T_CTRL']  == '1':
		return set_boiler('T_CTRL', 0)

	
#=====================  PUMP ===================== ========
#PUMP_1_1_SW / PUMP_1_2_SW / PUMP_2_1_SW / PUMP_2_2_SW / PUMP_1_1_ST / PUMP_1_2_ST / PUMP_2_1_ST / PUMP_2_2_ST
def get_pump():
	config.read_pump()
	wl_send_state, cmd_state, dev_error_code, retval = wl_rw(config.wfcr_addr, CMD['GET'], WF_VAR['pump'], 0)


	config.pump = dict.fromkeys(config.pump_fieldnames, '0')
	config.pump["STATE"] = wl_send_state

	if wl_send_state == WL_STATE[0]:  # OK
		if dev_error_code != '0':
			dbg.prints('WARNING! DevERC: ' + str(dev_error_code))
			config.pump["STATE"] = wl_send_state + ' DevERC:' + str(dev_error_code)

		if cmd_state == 'DONE':
			bit_str = format(int(retval), '08b')
			l = len(bit_str)
			dbg.prints('PUMP RETURN VAL: ' + bit_str)
			config.pump[config.pump_fieldnames[1]] = bit_str[l - 1]
			config.pump[config.pump_fieldnames[2]] = bit_str[l - 2]
			config.pump[config.pump_fieldnames[3]] = bit_str[l - 3]
			config.pump[config.pump_fieldnames[4]] = bit_str[l - 4]
			config.pump[config.pump_fieldnames[5]] = bit_str[l - 5]
			config.pump[config.pump_fieldnames[6]] = bit_str[l - 6]
			config.pump[config.pump_fieldnames[7]] = bit_str[l - 7]
			config.pump[config.pump_fieldnames[8]] = bit_str[l - 8]

		else:
			dbg.prints('WARNING! ', cmd_state)
			config.pump['STATE'] = wl_send_state + ' cmd: ' + cmd_state

	config.write_pump()
	return cmd_state
	
	

def pump_onoff(pump_name, onoff):
	config.read_pump()
	config.pump[pump_name]=str(onoff)
	bit_str='000100000000'+ config.pump[config.pump_fieldnames[4]] + config.pump[config.pump_fieldnames[3]]+ config.pump[config.pump_fieldnames[2]] + config.pump[config.pump_fieldnames[1]]
	
	val=int(bit_str,2)	
	
	wl_send_state, cmd_state, dev_error_code, retval = wl_rw(config.wfcr_addr, CMD['SET'], WF_VAR['pump'], val)

	if wl_send_state == WL_STATE[5]:  # BUSY
		return WL_STATE[5]
	else:
		#config.pump = dict.fromkeys(config.pump_fieldnames, 'X')
		config.pump["STATE"] = wl_send_state

	if wl_send_state == WL_STATE[0]:  # OK
		if dev_error_code != '0':
			dbg.prints('WARNING! DevERC: ' + str(dev_error_code))
			config.pump["STATE"] = wl_send_state + ' DevERC:' + str(dev_error_code)

		if cmd_state != 'DONE':
			config.pump[pump_name] = '0'
			dbg.prints('WARNING! ', cmd_state)
			config.pump['STATE'] = wl_send_state + ' cmd: ' + cmd_state

	config.write_pump()
	return cmd_state
	
	
def toggle_pump(pump_name):
	config.read_pump()
	if config.pump[pump_name]=='0':
		return pump_onoff(pump_name, 1)
	else:
		return pump_onoff(pump_name, 0)


