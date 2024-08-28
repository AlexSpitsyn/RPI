#!/usr/bin/env python
# coding: utf-8

import telebot
from telebot import types
import wl
import config
import dbg
import os
import time
import ds18b20
import subprocess

# ======================================================================================================
#
#                                       FUNCTION DEF
#
# ======================================================================================================
def drow_main_menu():
    mainmenu = types.InlineKeyboardMarkup()
    key1 = types.InlineKeyboardButton(text='Отопление', callback_data='heat_select')
    key2 = types.InlineKeyboardButton(text='Температура', callback_data='temp')
    mainmenu.row(key2, key1)
    return '\t ГЛАВНОЕ МЕНЮ', mainmenu

def drow_wts_select_menu():
    wts_select_menu = types.InlineKeyboardMarkup()
    keys = []

    for i in range(len(config.wts)):
        keys.append(types.InlineKeyboardButton(text=f'Д{config.wts[i]["WTSN"]}',
                                               callback_data=f'wts_options@{i}'))

    add_wts = types.InlineKeyboardButton(text='добавить', callback_data='wts_add')
    key_back.callback_data = 'temp'

    p = 0
    for i in range(len(config.wts) // 4):
        wts_select_menu.row(*keys[i * p:p + 4])
        p += 4
    if len(config.wts) - p:
        wts_select_menu.row(*keys[p:])

    wts_select_menu.row(add_wts)
    wts_select_menu.row(key_back, key_home)
    return 'Настройки датчиков', wts_select_menu

def drow_wts_menu(wts_num, idle=' '):
    config.read_wts(wts_num)
    wts_name = config.wts[wts_num]['NAME']
    wts_temp = config.wts[wts_num]['TEMP']
    wts_state = config.wts[wts_num]['STATE']
    wts_gpio = config.wts[wts_num]['GPIO']

    if wts_state == wl.WL_STATE[0]:  # 'OK'
        header_str = f'Д{config.wts[wts_num]["WTSN"]} {wts_name} {wts_temp}°C{idle}'
        if wts_gpio == '1':
            button_gpio_text = 'ON'
        else:
            button_gpio_text = 'OFF'

    elif wts_state == wl.WL_STATE[4]:  # 'OFFLINE'
        header_str = f'Д{config.wts[wts_num]["WTSN"]} {wts_name} OFFLINE{idle}'
        button_gpio_text = '⚠'

    else:
        header_str = f'Д{config.wts[wts_num]["WTSN"]} {wts_state} {idle}'
        button_gpio_text = '⚠'

    wts_options_menu = types.InlineKeyboardMarkup()
    key1 = types.InlineKeyboardButton(text='Имя', callback_data=f'set_wts_name@{wts_num}')
    key2 = types.InlineKeyboardButton(text='❌', callback_data=f'wts_delete@{wts_num}')
    key3 = types.InlineKeyboardButton(text=button_gpio_text, callback_data=f'wts_gpio_toggle@{wts_num}')
    key4 = types.InlineKeyboardButton(text='🔄', callback_data=f'wts_update@{wts_num}')

    key_back.callback_data = 'wts_select'
    wts_options_menu.add(key1, key2, key3, key4)
    wts_options_menu.row(key_back, key_home)

    return header_str, wts_options_menu

def drow_boiler_menu(idle=' '):
    config.read_boiler()
    state = config.boiler[config.wf_blr_fieldnames[0]]
    temp_ctrl = config.boiler[config.wf_blr_fieldnames[1]]
    temp = config.boiler[config.wf_blr_fieldnames[2]]
    set_temp = config.boiler[config.wf_blr_fieldnames[3]]

    if state == wl.WL_STATE[0]:  # 'OK'
        if temp_ctrl == '1':
            button_onoff_text = '✅'
            header_str = f'Котёл {temp}\t\t[ {set_temp}°C ]{idle}'
        elif temp_ctrl == '0':
            button_onoff_text = '⏹'
            header_str = f'Котёл {temp}\t\t[ {set_temp}°C ]{idle}'
        else:
            button_onoff_text = '⚠️'
            header_str = f'Котёл [ {set_temp}°C ]{idle}'
    elif state == wl.WL_STATE[4]:  # 'OFFLINE'
        button_onoff_text = '🛑'  # offline
        header_str = f'Котёл - нет связи{idle}'
    else:
        button_onoff_text = '⚠️'
        header_str = f'Котёл {state}{idle}'

    boiler_options_menu = types.InlineKeyboardMarkup()
    key1 = types.InlineKeyboardButton(text=button_onoff_text, callback_data='boiler_onoff')
    key2 = types.InlineKeyboardButton(text='Уст.темп', callback_data='set_temp@boiler')
    key3 = types.InlineKeyboardButton(text='🔄', callback_data='boiler_update')
    key_back.callback_data = 'heat_select'

    boiler_options_menu.add(key1, key2, key3)
    boiler_options_menu.row(key_back, key_home)
    return header_str, boiler_options_menu

def drow_wf_menu(idle=' '):
    config.read_wf()
    state = config.wf[config.wf_blr_fieldnames[0]]
    temp_ctrl = config.wf[config.wf_blr_fieldnames[1]]
    temp = config.wf[config.wf_blr_fieldnames[2]]
    set_temp = config.wf[config.wf_blr_fieldnames[3]]

    if state == wl.WL_STATE[0]:  # 'OK'
        if temp_ctrl == '1':
            button_onoff_text = '✅'
            header_str = f'ТП {temp} [ {set_temp}°C ]{idle}'
        elif temp_ctrl == '0':
            button_onoff_text = '⏹'
            header_str = f'ТП {temp} [ {set_temp}°C ]{idle}'
        else:
            button_onoff_text = '⚠️'
            header_str = f'ТП [ {set_temp}°C ]'
    elif state == wl.WL_STATE[4]:  # 'OFFLINE'
        button_onoff_text = '🛑'  # offline
        header_str = f'ТП - нет связи{idle}'
    else:
        button_onoff_text = '⚠️'
        header_str = f'ТП {state}{idle}'

    wf_options_menu = types.InlineKeyboardMarkup()
    key1 = types.InlineKeyboardButton(text=button_onoff_text, callback_data='wf_onoff')
    key2 = types.InlineKeyboardButton(text='Уст.темп', callback_data='set_temp@wf')
    key3 = types.InlineKeyboardButton(text='🔄', callback_data='wf_update')
    key_back.callback_data = 'heat_select'

    wf_options_menu.add(key1, key2, key3)
    wf_options_menu.row(key_back, key_home)
    return header_str, wf_options_menu

def drow_pump_menu(idle=' '):
    config.read_pump()
    state = config.pump['STATE']
    button_pump = ['00', '00', '00', '00']
    button_pump_char = {'10': '🛑', '00': 'Ⓜ', '11': '⚠', '01': '✅'}
    for x in range(4):
        button_pump[x] = config.pump[config.pump_fieldnames[x + 5]] + config.pump[config.pump_fieldnames[x + 1]]
        # PUMP_X_X_ST + PUMP_X_X_SW

    if state == wl.WL_STATE[0]:  # 'OK'
        header_str = f'Насосы {idle}'
    elif state == wl.WL_STATE[4]:  # 'OFFLINE'
        header_str = f'Насосы нет связи {idle}'
    else:
        header_str = f'Насосы {state}{idle}'

    pumps_menu = types.InlineKeyboardMarkup()

    key1 = types.InlineKeyboardButton(text=button_pump_char[button_pump[0]] + '  Кухня-гост',
                                      callback_data=f'pump_toggle@{config.pump_fieldnames[1]}')
    key2 = types.InlineKeyboardButton(text=button_pump_char[button_pump[1]] + '  Прихожая-сп.гост',
                                      callback_data=f'pump_toggle@{config.pump_fieldnames[2]}')
    key3 = types.InlineKeyboardButton(text=button_pump_char[button_pump[2]] + '  Спальная 2.1 -2.2.',
                                      callback_data=f'pump_toggle@{config.pump_fieldnames[3]}')
    key4 = types.InlineKeyboardButton(text=button_pump_char[button_pump[3]] + '  Спальная 2.3 -2.4.',
                                      callback_data=f'pump_toggle@{config.pump_fieldnames[4]}')
    key5 = types.InlineKeyboardButton(text='🔄', callback_data='pump_update')

    key_back.callback_data = 'heat_select'

    pumps_menu.row(key1)
    pumps_menu.row(key2)
    pumps_menu.row(key3)
    pumps_menu.row(key4)
    pumps_menu.row(key5)
    pumps_menu.row(key_back, key_home)

    return header_str, pumps_menu

def get_temp():
    for i in range(len(config.wts)):
        config.read_wts(i)
    config.read_wf()
    config.read_boiler()

    tempinfo = 'Котёл: '
    if config.boiler['STATE'] == 'OK':
        if config.boiler['T_CTRL'] == '1':
            tempinfo = tempinfo + 'ON '
        else:
            tempinfo = tempinfo + 'OFF '
        tempinfo = tempinfo + config.boiler['TEMP'] + '\r\n'
    else:
        tempinfo = tempinfo + config.boiler['STATE'] + '\r\n'

    tempinfo = tempinfo + 'ТП: '
    if config.wf['STATE'] == 'OK':
        if config.wf['T_CTRL'] == '1':
            tempinfo = tempinfo + 'ON '
        else:
            tempinfo = tempinfo + 'OFF '
        tempinfo = tempinfo + config.wf['TEMP'] + '\r\n'
    else:
        tempinfo = tempinfo + config.wf['STATE'] + '\r\n'

    t_base = str(ds18b20.get_temp())
    tempinfo = tempinfo + f'Темп база: {t_base}\r\n'
    tempinfo = tempinfo + 'Данные датчиков:\r\n'
    for wts_conf in config.wts:
        if wts_conf['STATE'] == 'OK':
            tempinfo = tempinfo + f'Д{wts_conf["WTSN"]} - {wts_conf["NAME"]}: {wts_conf["TEMP"]}\r\n'
        else:
            tempinfo = tempinfo + f'Д{wts_conf["WTSN"]} - {wts_conf["NAME"]}: {wts_conf["STATE"]}\r\n'
    return tempinfo

def get_answer(answer):
    if not hasattr(get_answer, "waiting"):
        get_answer.waiting = False
    #get_answer.waiting = False
    #get_answer.param = ''
    ret = ''
    if 'отмена' in get_answer.param:
        get_answer.waiting = False

    if 'set_wts_name' in get_answer.param:
        wts_num = int(get_answer.param.split('@')[1])
        config.wts[wts_num]["NAME"] = answer
        config.write_wts(wts_num)
        get_answer.waiting = False
        ret = 'Датчик добавлен'

    if 'wts_add' in get_answer.param:
        if answer.isdigit():
            wtsn = int(answer)
            if wtsn > 0 and wtsn < 17:
                for wts_conf in config.wts:
                    if wts_conf['WTSN'] == str(wtsn):
                        return 'Такой датчий уже подключен'
                config.add_wts(wtsn)
                get_answer.param = f'set_wts_name@{len(config.wts) - 1}'
                ret = 'Введите имя датчика'
            else:
                ret = 'WTS: неверное значение.\n Укажите значение от 1 до 16'

    if 'set_temp' in get_answer.param:
        if 'boiler' in get_answer.param:
            if answer.isdigit():
                v = int(answer)
                if v >= config.temp['BOILER_MIN'] and v <= config.temp['BOILER_MAX']:
                        cmd_state, v =  wl.set_boiler('TEMP_SET', v)
                        if cmd_state != wl.WL_CMD_STATE[0]: #DONE
                            ret = f'CMD_STATE: {cmd_state}\nDevice: {config.boiler["STATE"]}'
                        else:
                            ret = 'Ok'
                        get_answer.waiting = False
                else:
                    ret = f'Значение должно быть в интервале\nMin: {config.temp["BOILER_MIN"]}\nMax:{config.temp["BOILER_MAX"]}'
            else:
                ret = 'Введите число'

        if 'wf' in get_answer.param:
            if answer.isdigit():
                v = int(answer)
                if v >= config.temp['WF_MIN'] and v <= config.temp['WF_MAX']:
                        cmd_state, v = wl.set_boiler('TEMP_SET', v)
                        if cmd_state != wl.WL_CMD_STATE[0]: #DONE
                            ret = f'CMD_STATE: {cmd_state}\nDevice: {config.wf["STATE"]}'
                        else:
                            ret = 'Ok'
                        get_answer.waiting = False
                else:
                    ret = f'Значение должно быть в интервале\nMin: {config.temp["WF_MIN"]}\nMax:{config.temp["WF_MAX"]}'
            else:
                ret = 'Введите число'

    return ret

# ======================================================================================================
#
#                                           MAIN
#
# ======================================================================================================
config.init_dobby()
config.init()

bot = telebot.TeleBot(config.DOBBY_TOKEN)
UPDATE_TIME = int(config.dobby['UPDATE_TIME'])
dbg.DEBUG = config.dobby['DBG'] == 'ON'
wl.EMULATION = config.dobby['EMULATION'] == 'ON'
wl.LOG_SX1278 = config.dobby['LOG'] == 'ON'

key_home = types.InlineKeyboardButton(text='🏠', callback_data='mainmenu')
key_back = types.InlineKeyboardButton(text='↩️', callback_data='back')

@bot.message_handler(content_types=['document'])
def upload_file(message):
    file_name = message.document.file_name
    file_id = message.document.file_name
    file_id_info = bot.get_file(message.document.file_id)
    downloaded_file = bot.download_file(file_id_info.file_path)
    with open('update/update.zip', 'wb') as new_file:
        new_file.write(downloaded_file)
        new_file.close()

# dobby commands
# menu - start menu
# temp - temperature info
# boiler - boiler settings
# wf - wf settings
# pumps - pumps settings
# help - help
@bot.message_handler(commands=['menu'])
def menu_command_handler(msg: types.Message):
    if msg.from_user.id not in config.users_ID:
        bot.send_message(config.admin_ID, f'New User: {msg.from_user.id}')
        bot.send_message(msg.chat.id, 'Permission denied')
    else:
        header, markup = drow_main_menu()
        bot.send_message(msg.chat.id, header, reply_markup=markup)

@bot.message_handler(commands=['temp'])
def menu_command_handler(msg: types.Message):
    if msg.from_user.id not in config.users_ID:
        bot.send_message(config.admin_ID, f'New User: {msg.from_user.id}')
        bot.send_message(msg.chat.id, 'Permission denied')
    else:
        bot.send_message(msg.chat.id, get_temp())

@bot.message_handler(commands=['boiler'])
def menu_command_handler(msg: types.Message):
    if msg.from_user.id not in config.users_ID:
        bot.send_message(config.admin_ID, f'New User: {msg.from_user.id}')
        bot.send_message(msg.chat.id, 'Permission denied')
    else:
        header, markup = drow_boiler_menu()
        bot.send_message(msg.chat.id, header, reply_markup=markup)

@bot.message_handler(commands=['wf'])
def menu_command_handler(msg: types.Message):
    if msg.from_user.id not in config.users_ID:
        bot.send_message(config.admin_ID, f'New User: {msg.from_user.id}')
        bot.send_message(msg.chat.id, 'Permission denied')
    else:
        header, markup = drow_wf_menu()
        bot.send_message(msg.chat.id, header, reply_markup=markup)

@bot.message_handler(commands=['pumps'])
def menu_command_handler(msg: types.Message):
    if msg.from_user.id not in config.users_ID:
        bot.send_message(config.admin_ID, f'New User: {msg.from_user.id}')
        bot.send_message(msg.chat.id, 'Permission denied')
    else:
        header, markup = drow_pump_menu()
        bot.send_message(msg.chat.id, header, reply_markup=markup)

@bot.message_handler(commands=['help'])
def menu_command_handler(msg: types.Message):
    if msg.from_user.id not in config.users_ID:
        bot.send_message(config.admin_ID, f'New User: {msg.from_user.id}')
        bot.send_message(msg.chat.id, 'Permission denied')
    else:
        help_msg = \
        'custom commads: \n\
        add user <users_ID> \n\
        get log\n\
        reboot\n\
        cmd <cmd> - call bash\n\
        '
        bot.send_message(msg.chat.id, 'Permission denied')

@bot.message_handler(func=lambda msg: True, content_types=['text'])
def msg_handler(msg):
    if msg.from_user.id not in config.users_ID:
        bot.send_message(config.admin_ID, f'New User: {msg.from_user.id}')
        bot.send_message(msg.chat.id, 'Permission denied')
    else:
        if 'add user' in msg.text:
            splt_msg = msg.text.split()
            try:
                uid = int(splt_msg[2])
                config.users_ID.append(uid)
                config.write_pass_list(config.users_ID)
            except ValueError:
                bot.send_message(config.admin_ID, 'wrong command')
                bot.send_message(config.admin_ID, 'add user xxx')

        if msg.text == 'get log':
            if os.path.isfile('log/log.txt'):
                send_file = open('log/log.txt', 'rb')
                bot.send_document(msg.chat.id, send_file)
            else:
                bot.send_message(msg.chat.id, 'Файл не найден')

        elif msg.text.split()[0] == 'rad':
            wl.toggle_gpio_wts(7)
            bot.send_message(msg.chat.id, 'Файл не найден')
            wts_conf['STATE'] == 'OK'

        elif msg.text == 'reboot':
            bot.send_message(msg.chat.id, 'Добби ушёл...')
            time.sleep(10)
            os.system('shutdown -r now')

        elif msg.text.split()[0] == 'cmd':
            f = subprocess.run(msg.text[5:].split(), stdout=subprocess.PIPE)
            bot.send_message(msg.chat.id, f.stdout)

        elif msg.text == 'clear log':
            f = open('log/clear', 'w')
            f.close()

        elif get_answer.waiting:
            bot.send_message(msg.chat.id, get_answer(msg.text))

@bot.callback_query_handler(func=lambda call: True)
def callback_inline(call):

    # ------------------------------------------------------------------------------------
    #                                        MAIN MENU
    # ------------------------------------------------------------------------------------
    if call.data == 'mainmenu':
        header, markup = drow_main_menu()
        bot.edit_message_text(header, call.message.chat.id, call.message.message_id,
                              reply_markup=markup)

    # ------------------------------------------------------------------------------------
    #                                   TEMPERATURE
    # ------------------------------------------------------------------------------------
    elif call.data == 'temp':
        temp_menu = types.InlineKeyboardMarkup()
        key1 = types.InlineKeyboardButton(text='Инф', callback_data='print_temp')
        key2 = types.InlineKeyboardButton(text='Настройки', callback_data='wts_select')
        key_back.callback_data = 'mainmenu'
        temp_menu.row(key1, key2)
        temp_menu.row(key_back, key_home)
        bot.edit_message_text('Температура', call.message.chat.id, call.message.message_id,
                              reply_markup=temp_menu)

    # ------------------------------------------------------------------------------------
    #                                 HEAT SELECT
    # ------------------------------------------------------------------------------------
    elif call.data == 'heat_select':
        heat_select_menu = types.InlineKeyboardMarkup()
        key1 = types.InlineKeyboardButton(text='Котёл', callback_data='boiler_options')
        key2 = types.InlineKeyboardButton(text='ТП', callback_data='wf_options')
        key3 = types.InlineKeyboardButton(text='Насосы', callback_data='pumps_options')
        key_back.callback_data = 'mainmenu'

        heat_select_menu.row(key1, key2, key3)
        heat_select_menu.row(key_back, key_home)
        bot.edit_message_text('Отопление', call.message.chat.id, call.message.message_id,
                              reply_markup=heat_select_menu)

    # ------------------------------------------------------------------------------------
    #                      TEMPERATURE -> INFO
    # ------------------------------------------------------------------------------------
    elif call.data.split('@')[0] == 'print_temp':

        bot.send_message(call.message.chat.id, get_temp())

    # ------------------------------------------------------------------------------------
    #            TEMPERATURE -> OPTIONS -> WTS SELECT
    # ------------------------------------------------------------------------------------
    elif call.data == 'wts_select':
        key_back.callback_data = 'temp'
        header, markup = drow_wts_select_menu()
        bot.edit_message_text(header, call.message.chat.id, call.message.message_id,
                              reply_markup=markup)

    # ------------------------------------------------------------------------------------
    #              TEMPERATURE -> OPTIONS -> WTS SELECT -> WTS CONFIG
    # ------------------------------------------------------------------------------------
    elif 'wts_options' in call.data:
        key_back.callback_data = 'wts_select'
        wts_num = int(call.data.split('@')[1])
        header, markup = drow_wts_menu(wts_num)
        bot.edit_message_text(header, call.message.chat.id, call.message.message_id,
                              reply_markup=markup)

    elif 'wts_gpio_toggle' in call.data:
        wts_num = int(call.data.split('@')[1])
        header, markup = drow_wts_menu(wts_num, '⏳')
        bot.edit_message_text(header, call.message.chat.id, call.message.message_id,
                              reply_markup=markup)
        wl.toggle_gpio_wts(wts_num)
        header, markup = drow_wts_menu(wts_num)
        bot.edit_message_text(header, call.message.chat.id, call.message.message_id,
                              reply_markup=markup)

    elif 'wts_update' in call.data:
        wts_num = int(call.data.split('@')[1])
        header, markup = drow_wts_menu(wts_num, '⏳')
        bot.edit_message_text(header, call.message.chat.id, call.message.message_id,
                              reply_markup=markup)
        wl.read_wts(wts_num)
        header, markup = drow_wts_menu(wts_num)
        bot.edit_message_text(header, call.message.chat.id, call.message.message_id,
                              reply_markup=markup)
        drow_wts_menu(wts_num, '⏳')

    elif 'set_wts_name' in call.data:
        bot.send_message(call.message.chat.id, 'Введите название датчика')
        get_answer.waiting = True
        get_answer.param = call.data

    elif call.data == 'wts_add':
        bot.send_message(call.message.chat.id, 'Напишите номер датчика')
        get_answer.waiting = True
        get_answer.param = call.data

    elif 'wts_delete' in call.data:
        wts_num = int(call.data.split('@')[1])
        config.delete_wts(wts_num)
        header, markup = drow_wts_menu(wts_num)
        bot.edit_message_text(header, call.message.chat.id, call.message.message_id,
                              reply_markup=markup)


    # ------------------------------------------------------------------------------------
    #                           HEAT SELECT -> BOILER OPTIONS
    # ------------------------------------------------------------------------------------
    elif call.data == 'boiler_options':
        key_back.callback_data = 'heat_select'
        header, markup = drow_boiler_menu()
        bot.edit_message_text(header, call.message.chat.id, call.message.message_id,
                              reply_markup=markup)

    elif call.data == 'boiler_onoff':
        if config.boiler['T_CTRL'] == '0':
            wl.set_boiler('T_CTRL', 1)
        elif config.boiler['T_CTRL'] == '1':
            wl.set_boiler('T_CTRL', 0)
        header, markup = drow_boiler_menu()
        bot.edit_message_text(header, call.message.chat.id, call.message.message_id,
                              reply_markup=markup)

    elif call.data == 'boiler_update':
        header, markup = drow_boiler_menu('⏳')
        bot.edit_message_text(header, call.message.chat.id, call.message.message_id,
                              reply_markup=markup)
        wl.update_boiler()
        header, markup = drow_boiler_menu()
        bot.edit_message_text(header, call.message.chat.id, call.message.message_id,
                              reply_markup=markup)

    # ------------------------------------------------------------------------------------
    #                         HEAT SELECT -> WF OPTIONS
    # ------------------------------------------------------------------------------------
    elif call.data == 'wf_options':
        key_back.callback_data = 'heat_select'
        header, markup = drow_wf_menu()
        bot.edit_message_text(header, call.message.chat.id, call.message.message_id,
                              reply_markup=markup)

    elif call.data == 'wf_onoff':
        if config.wf['STATE'] == wl.WL_STATE[0]:  # 'OK':
            if config.wf['T_CTRL'] == '0':
                wl.set_wf('T_CTRL', 1)
            elif config.wf['T_CTRL'] == '1':
                wl.set_wf('T_CTRL', 0)
            header, markup = drow_wf_menu()
            bot.edit_message_text(header, call.message.chat.id, call.message.message_id,
                              reply_markup=markup)

    elif call.data == 'wf_update':
        header, markup = drow_wf_menu('⏳')
        bot.edit_message_text(header, call.message.chat.id, call.message.message_id,
                              reply_markup=markup)
        wl.update_wf()
        header, markup = drow_wf_menu()
        bot.edit_message_text(header, call.message.chat.id, call.message.message_id,
                              reply_markup=markup)

    # ------------------------------------------------------------------------------------
    #                     HEAT SELECT -> PUMP OPTIONS
    # ------------------------------------------------------------------------------------
    elif call.data == 'pumps_options':
        key_back.callback_data = 'heat_select'
        header, markup = drow_pump_menu()
        bot.edit_message_text(header, call.message.chat.id, call.message.message_id,
                              reply_markup=markup)

    elif call.data.split('@')[0] == 'pump_toggle':
        pump = call.data.split('@')[1]
        header, markup = drow_pump_menu('⏳')
        bot.edit_message_text(header, call.message.chat.id, call.message.message_id,
                              reply_markup=markup)
        wl.toggle_pump(pump)
        wl.get_pump()
        header, markup = drow_pump_menu()
        bot.edit_message_text(header, call.message.chat.id, call.message.message_id,
                              reply_markup=markup)

    elif call.data.split('@')[0] == 'pump_update':
        header, markup = drow_pump_menu('⏳')
        bot.edit_message_text(header, call.message.chat.id, call.message.message_id,
                              reply_markup=markup)
        wl.get_pump()
        header, markup = drow_pump_menu()
        bot.edit_message_text(header, call.message.chat.id, call.message.message_id,
                              reply_markup=markup)

    # ------------------------------------------------------------------------------------
    #                     SET TEM BOILER / WF
    # ------------------------------------------------------------------------------------
    elif 'set_temp' in call.data:
        bot.send_message(call.message.chat.id, 'Введите температуру')
        get_answer.waiting = True
        get_answer.param = call.data

if os.path.isfile('update/update_state'):
    update_state_str = 'unknown'
    with open('update/update_state', 'r') as update_state:
        update_state_str = update_state.readline()
        update_state.close()
    bot.send_message(config.admin_ID, 'DOBBY UPDATE: ' + update_state_str)
    os.remove('update/update_state')

f = subprocess.run('date', stdout=subprocess.PIPE)
bot.send_message(config.admin_ID, f.stdout)

bot.polling(none_stop=True, interval=3, timeout=60)
# while True: # Don't let the main Thread end.
#     pass
