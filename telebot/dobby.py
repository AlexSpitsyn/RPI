#!/usr/bin/python
# encoding=utf8
import sys
reload (sys)
sys.setdefaultencoding('utf8')
import subprocess
import csv
import socket
import telebot
from telebot import apihelper, types, util

tor_start = subprocess.call(["service", "tor", "start"])
print('start tor flag' ,tor_start)

rpi_ip = socket.gethostbyname(socket.getfqdn())

print(rpi_ip)
#/etc/tor/torrc
#service tor start
#PROXY = 'socks5://127.0.0.1:9150'
#apihelper.proxy = {'https': PROXY}
#telebot.apihelper.proxy = {'https': 'socks5://192.168.8.105:9100'}
telebot.apihelper.proxy = {'https': 'socks5://'+ rpi_ip + ':9100'}

#telebot.apihelper.proxy = {'https': 'socks5://972228317:rhYF02He@grsst.s5.opennetwork.cc:999'}


TOKEN = '927942451:AAG7HMnzpyLVKcydJiEW0zGjOcnqi7_1EDE'

bot = telebot.TeleBot(TOKEN)

bot.send_message(972228317, "привет")

@bot.message_handler(commands=['help'])
def start(message):    
    #print(message)
    print(message.chat.id)
    bot.reply_to(message, "Howdy, how are you doing?")
    

@bot.message_handler(content_types=['text'])
def send_text(message):
    if message.text.lower().find('добби') == 0:
        bot.send_message(message.chat.id, 'Привет, мой создатель')
    elif message.text.lower() == 'пока':
        bot.send_message(message.chat.id, 'Прощай, создатель')
		
    elif message.text.lower().find('д 1') == 0:
        bot.send_message(message.chat.id, 'Проверяю датчик 1')
	a = subprocess.call(["read_wts_num", "2"])
	print a	
	if a==0:
		#print "OK"
		bot.send_message(message.chat.id, 'OK')
		wts_line = []
		FILENAME = "wts.csv"
		
		with open(FILENAME, "r") as in_file:
			reader = csv.DictReader(in_file, delimiter=';')
			for row in reader:
				print(row["WTSN"], "-" , row["STATE"],"-", row["VAL"])
				wts_line.append(row)
				if row["STATE"]=='0':				
					print ("Датчик"  , "не работает")
				else:
					print ("Температура" , "=", row["VAL"])
					bot.send_message(message.chat.id, "temp= " + row["VAL"])
					
		#fieldnames = [t for i, t in enumerate(wts_line[0])]
		
		#with open(FILENAME, "w", newline='') as out_file:
		#	writer = csv.DictWriter(out_file, delimiter=';', fieldnames=fieldnames)
		#	writer.writeheader()
		#	for row in wts_line:
		#		writer.writerow(row)
	else:
		print "FAIL"
		bot.send_message(message.chat.id, 'FAIL')


bot.polling()
