import os
import subprocess
from time import sleep
from pprint import pprint
from huaweisms.api import monitoring, user, sms
from huaweisms.api.common import ApiCtx
import configparser

config = configparser.ConfigParser()
config.read('dobby_login')
USER = config['Huawei']['admin']
PASSWORD = config['Huawei']['pwd']
ADMIN_PHONE = config['Huawei']['admin_phone']
INBOX = 1

def get_session():
    return user.quick_login(USER, PASSWORD)
ctx = get_session()

while True:
    sms_cnt = int(sms.sms_count(ctx)['response']['LocalInbox'])
    for sms_num in range(0,sms_cnt):
        message = sms.get_sms(ctx, INBOX, sms_num,1)
        phone=message['response']['Messages']['Message'][0]['Phone']
        text=message['response']['Messages']['Message'][0]['Content']
        index = message['response']['Messages']['Message'][0]['Index']
        if (phone == ADMIN_PHONE) and (text.strip().lower() == 'reboot'):
            sms.delete_sms(ctx, index)
            os.system("sudo reboot")
    sleep(60)
