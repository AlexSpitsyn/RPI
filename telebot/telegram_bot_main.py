#!/usr/bin/env python
# coding: utf-8

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


