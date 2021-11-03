#pip install huawei-modem-api-client
import os
import subprocess
from time import sleep
from pprint import pprint
from huaweisms.api import monitoring, user, sms
from huaweisms.api.common import ApiCtx


USER = "admin"
PASSWORD = "ghjdjlf"
ADMIN_PHONE = "+79104034489"
SELF_NUMBER = "+79958819278"
INBOX = 1
OUTBOX = 2

# BEFORE running, do MAKE SURE heaweisms.api.config has the CORRECT VALUES for your MODEM


def get_session():
    return user.quick_login(USER, PASSWORD)


def valid_context(ctx):
    # type: (ApiCtx) -> bool
    sl = user.state_login(ctx)
    if sl['type'] == 'response' and sl['response']['State'] != -1:
        return True
    return False
	
	
output = subprocess.check_output(['iwgetid'])
SSID=str(output).split('"')[1]
#print("Connected Wifi SSID: " + SSID)
if SSID == "HWMR":
	ctx = get_session()
	status = monitoring.status(ctx)

	#sent = sms.send_sms(ctx, PHONE_NUMBER, "This is a test")
	#pprint(sent)
	#pprint(status)


	#get_sms(ctx, box_type=1, page=1, qty=1, unread_preferred=True):
	while True:
		#print('check sms')
		sms_cnt = int(sms.sms_count(ctx)['response']['LocalInbox'])

		for sms_num in range(0,sms_cnt):
			message = sms.get_sms(ctx, INBOX, sms_num,1)
			#pprint(message)
			phone=message['response']['Messages']['Message'][0]['Phone']
			text=message['response']['Messages']['Message'][0]['Content']
			index = message['response']['Messages']['Message'][0]['Index']
			#print(phone)
			#print(text)
			#print(index)
			if (phone == ADMIN_PHONE) and (text.strip().lower() == 'reboot'):
				sms.delete_sms(ctx, index)
				#subprocess.call(["reboot"])
				os.system("sudo reboot")
				#print('reboot')
		sleep(60)
	