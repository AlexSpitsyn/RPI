#!/usr/bin/python
# encoding=utf8
import sys
reload (sys)
sys.setdefaultencoding('utf8')

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
	
