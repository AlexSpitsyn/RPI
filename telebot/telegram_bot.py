#!/usr/bin/env python
# coding: utf-8

# In[ ]:


import telebot

bot = telebot.TeleBot("927942451:AAG7HMnzpyLVKcydJiEW0zGjOcnqi7_1EDE")
@bot.message_handler(commands=['help'])
def start(message):
    
    #print(message)
    print(message.chat.id)
    bot.reply_to(message, "Howdy, how are you doing?")
    bot.send_message(972228317, "привет")
    
@bot.message_handler(content_types=['text'])
def send_text(message):
    if message.text.lower == 'привет':
        bot.send_message(message.chat.id, 'Привет, мой создатель')
    elif message.text.lower == 'пока':
        bot.send_message(message.chat.id, 'Прощай, создатель')

bot.polling()


# In[59]:


import csv

wts_line = []
FILENAME = "D:\Python\wts.csv"
 

 
with open(FILENAME, "r", newline="") as in_file:
    reader = csv.DictReader(in_file, delimiter=';')
    
    for row in reader:
        #print(row["WTSN"], "-" , row["STATE"],"-", row["VAL"],"-", row["NAME"])
        wts_line.append(row)
        if row["STATE"]=='0':
             print ()
            #print ("Датчик" , row["NAME"] , "не работает")
        else:
            print ("Температура" , row["NAME"] , "=", row["VAL"])
        
fieldnames = [t for i, t in enumerate(wts_line[0])]
with open(FILENAME, "w", newline='') as out_file:
    writer = csv.DictWriter(out_file, delimiter=';', fieldnames=fieldnames)
    writer.writeheader()
    for row in wts_line:
        writer.writerow(row)
    
    
