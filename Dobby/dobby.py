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

#wl_update_f=True
#======================================================================================================
#
#                                       FUNCTION DEF
#
#======================================================================================================
#def wl_update():
    #t=Timer(UPDATE_TIME, wl_update)
    #t.start()
    # wl.update_wf()
    # wl.update_boiler()
    # wl.update_wts()
    # wl.get_pump()
    # print('update wl')
    # if wl_update_f==False:
    #     print('stop wl_upate')
    #     t.cancel()

def drow_wts_menu(idle=' '):
    global gcall
    global wts_num
    config.read_wts()
    wts_check = config.wts[wts_num]["CHECK"]
    wts_name = config.wts[wts_num]["NAME"]
    wts_temp = config.wts[wts_num]["TEMP"]
    wts_state = config.wts[wts_num]["STATE"]
    wts_gpio = config.wts[wts_num]["GPIO"]

    if wts_check == '1':
        button_wts_onoff_text = '✅'
    else:
        button_wts_onoff_text = '⏹'  # not checked

    if wts_state == wl.WL_STATE[0]:  # 'OK'
        header_str = 'Д' + str(wts_num + 1) + '  ' + wts_name + '  ' + wts_temp + '°C' + idle
        if wts_gpio == '1':
            button_gpio_text = 'OFF'
        else:
            button_gpio_text = 'ON'

    elif wts_state == wl.WL_STATE[4]:  # 'OFFLINE'
        header_str = 'Д' + str(wts_num + 1) + '  ' + wts_name + ' OFFLINE' + idle
        button_gpio_text = '⚠'

    else:
        header_str = 'Д' + str(wts_num + 1) + '  ' + wts_state + idle
        button_gpio_text = '⚠'


    wts_options_menu = types.InlineKeyboardMarkup()
    key1 = types.InlineKeyboardButton(text='Имя', callback_data='set_wts_name')
    key2 = types.InlineKeyboardButton(text=button_wts_onoff_text, callback_data='wts_onoff')
    key3 = types.InlineKeyboardButton(text=button_gpio_text, callback_data='wts_gpio_toggle')
    key4 = types.InlineKeyboardButton(text='🔄', callback_data='wts_update')

    key_back.callback_data = 'wts_select'
    wts_options_menu.add(key1, key2, key3, key4)
    wts_options_menu.row(key_back, key_home)

    markup = wts_options_menu

    message_out = bot.edit_message_text(header_str, gcall.message.chat.id, gcall.message.message_id,
                                        reply_markup=markup)


def drow_boiler_menu(idle=' '):
    global gcall
    config.read_boiler()
    state = config.boiler[config.wf_blr_fieldnames[0]]
    temp_ctrl = config.boiler[config.wf_blr_fieldnames[1]]
    temp = config.boiler[config.wf_blr_fieldnames[2]]
    set_temp = config.boiler[config.wf_blr_fieldnames[3]]

    if state == wl.WL_STATE[0]:  # 'OK'
        if temp_ctrl == '1':
            button_onoff_text = '✅'
            header_str = 'Котёл ' + temp + '\t \t' + '[ ' + set_temp + '°C ]' + idle
        elif temp_ctrl == '0':
            button_onoff_text = '⏹'
            header_str = 'Котёл ' + temp + '\t \t' + '[ ' + set_temp + '°C ]' + idle
        else:
            button_onoff_text = '⚠️'
            header_str = 'Котёл ' + '[ ' + set_temp + '°C ]' + idle
    elif state == wl.WL_STATE[4]:  # 'OFFLINE'
        button_onoff_text = '🛑'  # offline
        header_str = 'Котёл - нет связи' + idle
    else:
        button_onoff_text = '⚠️'
        header_str = 'Котёл ' + state + idle

    boiler_options_menu = types.InlineKeyboardMarkup()
    key1 = types.InlineKeyboardButton(text=button_onoff_text, callback_data='boiler_onoff')
    key2 = types.InlineKeyboardButton(text='Уст.темп', callback_data='set_temp@boiler')
    key3 = types.InlineKeyboardButton(text='🔄', callback_data='boiler_update')
    key_back.callback_data = 'heat_select'

    boiler_options_menu.add(key1, key2, key3)
    boiler_options_menu.row(key_back, key_home)
    markup = boiler_options_menu
    message_out = bot.edit_message_text(header_str, gcall.message.chat.id, gcall.message.message_id,
                                        reply_markup=markup)


def drow_wf_menu(idle=' '):
    global gcall
    config.read_wf()
    state = config.wf[config.wf_blr_fieldnames[0]]
    temp_ctrl = config.wf[config.wf_blr_fieldnames[1]]
    temp = config.wf[config.wf_blr_fieldnames[2]]
    set_temp = config.wf[config.wf_blr_fieldnames[3]]

    if state == wl.WL_STATE[0]:  # 'OK'
        if temp_ctrl == '1':
            button_onoff_text = '✅'
            header_str = 'ТП  ' + temp + '  ' + '[ ' + set_temp + '°C ]' + idle
        elif temp_ctrl == '0':
            button_onoff_text = '⏹'
            header_str = 'ТП  ' + temp + '  ' + '[ ' + set_temp + '°C ]' + idle
        else:
            button_onoff_text = '⚠️'
            header_str = 'ТП  ' + '[ ' + set_temp + '°C ]'
    elif state == wl.WL_STATE[4]:  # 'OFFLINE'
        button_onoff_text = '🛑'  # offline
        header_str = 'ТП - нет связи' + idle
    else:
        button_onoff_text = '⚠️'
        header_str = 'ТП ' + state + idle

    wf_options_menu = types.InlineKeyboardMarkup()
    key1 = types.InlineKeyboardButton(text=button_onoff_text, callback_data='wf_onoff')
    key2 = types.InlineKeyboardButton(text='Уст.темп', callback_data='set_temp@wf')
    key3 = types.InlineKeyboardButton(text='🔄', callback_data='wf_update')
    key_back.callback_data = 'heat_select'

    wf_options_menu.add(key1, key2, key3)
    wf_options_menu.row(key_back, key_home)
    markup = wf_options_menu
    message_out = bot.edit_message_text(header_str, gcall.message.chat.id, gcall.message.message_id,
                                        reply_markup=markup)
def drow_pump_menu(idle=' '):
    global gcall
    config.read_pump()
    state = config.pump['STATE']
    button_pump =['00','00','00','00']
    button_pump_char={'10':'🛑','00':'Ⓜ','11':'⚠','01':'✅'}
    for x in range(4):
         button_pump[x] = config.pump[config.pump_fieldnames[x+5]] + config.pump[config.pump_fieldnames[x+1]]
         #PUMP_X_X_ST + PUMP_X_X_SW

    if state == wl.WL_STATE[0]:  # 'OK'
        header_str = 'Насосы ' + idle
    elif state == wl.WL_STATE[4]:  # 'OFFLINE'
        header_str = 'Насосы ' + 'нет связи' + idle
    else:
        header_str = 'Насосы ' + state + idle



    pumps_menu = types.InlineKeyboardMarkup()
    # key1 = types.InlineKeyboardButton(text=button5_text + '    ДОМ', callback_data='pump_toggle@PUMP_MAIN')
    # key2 = types.InlineKeyboardButton(text=button6_text + '    ХБ', callback_data='pump_toggle@PUMP_HB')
    key3 = types.InlineKeyboardButton(text=button_pump_char[button_pump[0]] + '  Кухня-гост', callback_data='pump_toggle@' + config.pump_fieldnames[1])
    key4 = types.InlineKeyboardButton(text=button_pump_char[button_pump[1]]  + '  Прихожая-сп.гост', callback_data='pump_toggle@' + config.pump_fieldnames[2])
    key5 = types.InlineKeyboardButton(text=button_pump_char[button_pump[2]]  + '  Спальная 2.1 -2.2.', callback_data='pump_toggle@' + config.pump_fieldnames[3])
    key6 = types.InlineKeyboardButton(text=button_pump_char[button_pump[3]]  + '  Спальная 2.3 -2.4.', callback_data='pump_toggle@' + config.pump_fieldnames[4])
    key7 = types.InlineKeyboardButton(text='🔄', callback_data='pump_update')

    key_back.callback_data = 'heat_select'
    # pumps_menu.row(key1)
    # pumps_menu.row(key2)
    pumps_menu.row(key3)
    pumps_menu.row(key4)
    pumps_menu.row(key5)
    pumps_menu.row(key6)
    pumps_menu.row(key7)
    pumps_menu.row(key_back, key_home)

    markup = pumps_menu
    message_out = bot.edit_message_text(header_str, gcall.message.chat.id, gcall.message.message_id, reply_markup=markup)

#======================================================================================================
#
#                                           MAIN
#
#======================================================================================================

config.init_dobby()
config.init()

bot = telebot.TeleBot(config.dobby['TOKEN'])
UPDATE_TIME = int(config.dobby['UPDATE_TIME'])
dbg.DEBUG = config.dobby['DBG'] == 'ON'
wl.EMULATION = config.dobby['EMULATION'] == 'ON'
wl.LOG_SX1278 = config.dobby['LOG'] == 'ON'

wts_num = 0
input_str_type = '0'
message_out = '0'
message_out_cnt = 0
gcall = '0'

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

    # print(a)


@bot.message_handler(content_types=['text'])
def inline_key(msg):
    global wts_num
    global input_str_type
    global message_out
    # global markup
    global gcall
    global set_dict
    global message_out_cnt
    print (msg.from_user.id)

    if msg.from_user.id not in config.users_ID:
        bot.send_message(config.admin_ID, "New User: " + str(msg.from_user.id))
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


# telegram commands
#menu - start menu
#temp - temperature info
#boiler - boiler settings
#wf - wf settings
#pumps - pumps settings
#help - help
        if msg.text == "/menu":
            input_str_type = '0'
            mainmenu = types.InlineKeyboardMarkup()
            key1 = types.InlineKeyboardButton(text='Прочее', callback_data='other')
            key2 = types.InlineKeyboardButton(text='Парник', callback_data='parn')
            key3 = types.InlineKeyboardButton(text='Отопление', callback_data='heat_select')
            key4 = types.InlineKeyboardButton(text='Температура', callback_data='temp')
            mainmenu.row(key4, key3)
            mainmenu.row(key2, key1)
            bot.send_message(msg.chat.id, '\t ГЛАВНОЕ МЕНЮ', reply_markup=mainmenu)
            # print(type(msg.text))
            bot.delete_message(msg.chat.id, msg.message_id)

        if msg.text == "/temp":
            config.read_wts()
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
                tempinfo = tempinfo  + config.boiler['STATE'] + '\r\n'

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
            tempinfo = tempinfo + 'Темп база: ' + t_base + '\r\n'
            tempinfo = tempinfo + "Данные датчиков:\r\n"
            for wts_conf in config.wts:
                if wts_conf["CHECK"] == '1':
                    if wts_conf['STATE'] == 'OK':
                        tempinfo = tempinfo + 'Д' + str(int(wts_conf["WTSN"]) + 1) + ' - ' + wts_conf["NAME"] + ': ' + \
                                   wts_conf[
                                       "TEMP"] + '\r\n'
                    else:
                        tempinfo = tempinfo + 'Д' + str(int(wts_conf["WTSN"]) + 1) + ' - ' + wts_conf["NAME"] + ': ' + \
                                   wts_conf[
                                       "STATE"] + '\r\n'
            bot.send_message(msg.chat.id, tempinfo)
            message_out_cnt += 1

        if msg.text == "get log":
            if os.path.isfile('log/log.txt'):
                send_file = open('log/log.txt', "rb")
                bot.send_document(msg.chat.id, send_file)
            else:
                bot.send_message(msg.chat.id, 'Файл не найден')

        if msg.text.split()[0] == "rad":
            wl.toggle_gpio_wts(7)
            bot.send_message(msg.chat.id, 'Файл не найден')
            wts_conf['STATE'] == 'OK':


        if msg.text == "reboot":
            bot.send_message(msg.chat.id,'Добби ушёл...')
            time.sleep(10)
            os.system('shutdown -r now')

        if msg.text.split()[0] == "call":
            f = subprocess.run(msg.text[5:].split(), stdout=subprocess.PIPE)
            bot.send_message(msg.chat.id,f.stdout)


        if msg.text == "clear log":
            f = open('log/clear', 'w')
            f.close()

        if input_str_type == 'wts_name':
            if (msg.text[0] == '#'):
                input_str_type = '0'
                message_out_cnt += 1
                wts_name = msg.text.strip('#')
                config.wts[wts_num]["NAME"] = wts_name
                config.write_wts()

                # msg=bot.send_message(msg.chat.id, 'Имя для Д1 - '+ wts_name )
                # bot.edit_message_text(get_WTS_state(wts_num), message_out.chat.id, message_out.message_id, reply_markup=markup)
                drow_wts_menu()
                #while message_out_cnt:
                #    bot.delete_message(msg.chat.id, msg.message_id + 1 - message_out_cnt)
                #    message_out_cnt -= 1
            else:
                bot.answer_callback_query(gcall.id, text="Неверно задано имя", show_alert=True)
                message_out_cnt += 1

            # print(message_out_cnt)


        if input_str_type.split('@')[0] == 'set_temp':
            temp_type = input_str_type.split('@')[1]

            if (msg.text.isdigit()):

                if temp_type == 'boiler':
                    if int(msg.text) >= config.temp['BOILER_MIN'] and int(msg.text) <= config.temp['BOILER_MAX']:
                        message_out_cnt += 1
                        # wl.set_boiler() return WL_CMD_STATE
                        if wl.set_boiler('TEMP_SET', int(msg.text)).cmd_state != wl.WL_CMD_STATE[0]:
                            bot.send_message(msg.chat.id, "Что-то пошло не так... Тут нужна магия")
                        else:
                            drow_boiler_menu()

                        input_str_type = '0'
                        #while message_out_cnt:
                        #    bot.delete_message(msg.chat.id, msg.message_id + 1 - message_out_cnt)
                        #    message_out_cnt -= 1

                    else:
                        bot.send_message(msg.chat.id, 'Значение должно быть в интервале\nMin: ' +
                                         str(config.temp['BOILER_MIN']) + '\n' +
                                         'Max: ' + str(config.temp['BOILER_MAX']))
                        message_out_cnt += 2

                elif temp_type == 'wf':
                    if int(msg.text) > config.temp['WF_MIN'] and int(msg.text) < config.temp['WF_MAX']:
                        message_out_cnt += 1

                        if wl.set_wf('TEMP_SET', int(msg.text)).cmd_state != wl.WL_CMD_STATE[0]:
                            bot.send_message(msg.chat.id, "Что-то пошло не так... Тут нужна магия")
                        else:
                            drow_wf_menu()

                        input_str_type = '0'
                        #while message_out_cnt:
                        #    bot.delete_message(msg.chat.id, msg.message_id + 1 - message_out_cnt)
                        #    message_out_cnt -= 1

                    else:
                        bot.send_message(msg.chat.id, 'Значение должно быть в интервале\nMin: ' +
                                         str(config.temp['BOILER_MIN']) + '\n' +
                                         'Max: ' + str(config.temp['BOILER_MAX']))
                        message_out_cnt += 2

                # bot.delete_message(msg.chat.id, msg.message_id)
                # bot.delete_message(msg.chat.id, msg.message_id-1)

            else:
                bot.send_message(msg.chat.id, "Неверно задано значение")
                message_out_cnt += 2


@bot.callback_query_handler(func=lambda call: True)
def callback_inline(call):
    global wts_num
    global input_str_type
    global message_out
    # global markup
    global gcall
    global message_out_cnt
    gcall = call

    # ------------------------------------------------------------------------------------
    #                                        MAIN MENU
    # ------------------------------------------------------------------------------------
    if call.data == "mainmenu":
        mainmenu = types.InlineKeyboardMarkup()
        key1 = types.InlineKeyboardButton(text='Прочее', callback_data='other')
        key2 = types.InlineKeyboardButton(text='Парник', callback_data='parn')
        key3 = types.InlineKeyboardButton(text='Отопление', callback_data='heat_select')
        key4 = types.InlineKeyboardButton(text='Температура', callback_data='temp')
        mainmenu.row(key4, key3)
        mainmenu.row(key2, key1)
        bot.edit_message_text('\t ГЛАВНОЕ МЕНЮ', call.message.chat.id, call.message.message_id,
                              reply_markup=mainmenu)
        # bot.edit_message_reply_markup(call.message.chat.id, call.message.message_id, reply_markup=mainmenu)
        input_str_type = '0'

    # ------------------------------------------------------------------------------------
    #                                   TEMPERATURE
    # ------------------------------------------------------------------------------------

    elif call.data == "temp":
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
    elif call.data == "heat_select":

        heat_select_menu = types.InlineKeyboardMarkup()
        key1 = types.InlineKeyboardButton(text='Котёл', callback_data='boiler_options')
        key2 = types.InlineKeyboardButton(text='ТП', callback_data='wf_options')
        key3 = types.InlineKeyboardButton(text='Насосы', callback_data='pumps')
        key_back.callback_data = 'mainmenu'

        heat_select_menu.row(key1, key2, key3)
        heat_select_menu.row(key_back, key_home)
        bot.edit_message_text('Отопление', call.message.chat.id, call.message.message_id,
                              reply_markup=heat_select_menu)

    # ------------------------------------------------------------------------------------
    #                                   PARNIC
    # ------------------------------------------------------------------------------------
    elif call.data == "parn":
        parn_menu = types.InlineKeyboardMarkup()
        key1 = types.InlineKeyboardButton(text='Передняя дв.', callback_data='front_door')
        key2 = types.InlineKeyboardButton(text='Задняя дв.', callback_data='back_door')
        key3 = types.InlineKeyboardButton(text='Инф', callback_data='print_parn_inf')
        key4 = types.InlineKeyboardButton(text='Настройки', callback_data='parn_options')
        key_back.callback_data = 'mainmenu'

        parn_menu.row(key1, key2)
        parn_menu.row(key3, key4)
        parn_menu.row(key_back, key_home)
        bot.edit_message_text('Парник', call.message.chat.id, call.message.message_id,
                              reply_markup=parn_menu)

    # ------------------------------------------------------------------------------------
    #                                   OTHER
    # ------------------------------------------------------------------------------------
    elif call.data == "other":
        other_menu = types.InlineKeyboardMarkup()
        key1 = types.InlineKeyboardButton(text='Септик', callback_data='front_door')

        key2 = types.InlineKeyboardButton(text='Настройки', callback_data='parn_options')
        key_back.callback_data = 'mainmenu'

        other_menu.row(key1, key2)
        other_menu.row(key_back, key_home)
        bot.edit_message_text('Прочее', call.message.chat.id, call.message.message_id,
                              reply_markup=other_menu)


    # ------------------------------------------------------------------------------------
    #                      TEMPERATURE -> INFO
    # ------------------------------------------------------------------------------------
    elif call.data.split('@')[0] == "print_temp":
        tempinfo = "Данные датчиков:\r\n"
        for wts_conf in config.wts:
            if wts_conf["CHECK"] == '1':
                if wts_conf['STATE'] == 'OK':
                    tempinfo = tempinfo + 'Д' + str(int(wts_conf["WTSN"])+1) + ' - ' + wts_conf["NAME"] + ': ' + wts_conf[
                        "TEMP"] + '\r\n'
                else:
                    tempinfo = tempinfo + 'Д' + str(int(wts_conf["WTSN"])+1) + ' - ' + wts_conf["NAME"] + ': ' + wts_conf[
                        "STATE"] + '\r\n'

        bot.send_message(call.message.chat.id, tempinfo)
        message_out_cnt += 1


    # ------------------------------------------------------------------------------------
    #            TEMPERATURE -> OPTIONS -> WTS SELECT
    # ------------------------------------------------------------------------------------

    elif call.data == "wts_select":
        wts_select_menu = types.InlineKeyboardMarkup()
        key1 = types.InlineKeyboardButton(text='Д1', callback_data='wts_options@1')
        key2 = types.InlineKeyboardButton(text='Д2', callback_data='wts_options@2')
        key3 = types.InlineKeyboardButton(text='Д3', callback_data='wts_options@3')
        key4 = types.InlineKeyboardButton(text='Д4', callback_data='wts_options@4')
        key5 = types.InlineKeyboardButton(text='Д5', callback_data='wts_options@5')
        key6 = types.InlineKeyboardButton(text='Д6', callback_data='wts_options@6')
        key7 = types.InlineKeyboardButton(text='Д7', callback_data='wts_options@7')
        key8 = types.InlineKeyboardButton(text='Д8', callback_data='wts_options@8')
        key9 = types.InlineKeyboardButton(text='Д9', callback_data='wts_options@9')
        key10 = types.InlineKeyboardButton(text='Д10', callback_data='wts_options@10')
        key11 = types.InlineKeyboardButton(text='Д11', callback_data='wts_options@11')
        key12 = types.InlineKeyboardButton(text='Д12', callback_data='wts_options@12')
        key13 = types.InlineKeyboardButton(text='Д13', callback_data='wts_options@13')
        key14 = types.InlineKeyboardButton(text='Д14', callback_data='wts_options@14')
        key15 = types.InlineKeyboardButton(text='Д15', callback_data='wts_options@15')
        key16 = types.InlineKeyboardButton(text='Д16', callback_data='wts_options@16')

        key_back.callback_data = 'temp'
        wts_select_menu.row(key1, key2, key3, key4)
        wts_select_menu.row(key5, key6, key7, key8)
        wts_select_menu.row(key9, key10, key11, key12)
        wts_select_menu.row(key13, key14, key15, key16)
        wts_select_menu.row(key_back, key_home)
        bot.edit_message_text('Настройки датчиков', call.message.chat.id, call.message.message_id,
                              reply_markup=wts_select_menu)


    # ------------------------------------------------------------------------------------
    #              TEMPERATURE -> OPTIONS -> WTS SELECT -> WTS COMFIG
    # ------------------------------------------------------------------------------------

    elif call.data.split('@')[0] == "wts_options":
        wts_num = int(call.data.split('@')[1]) - 1
        key_back.callback_data = 'wts_select'
        drow_wts_menu()

    elif call.data == "wts_onoff":
        config.wts_checking_toggle(wts_num)
        drow_wts_menu()

    elif call.data == "wts_gpio_toggle":
        drow_wts_menu("⏳")
        wl.toggle_gpio_wts(wts_num)
        drow_wts_menu()

    elif call.data == "wts_update":
        drow_wts_menu("⏳")
        #config.wts_checking_onoff(wts_num, 'on')  # turn wts ON
        wl.read_wts(wts_num)
        drow_wts_menu()

    elif call.data == "set_wts_name":
        input_str_type = 'wts_name';
        bot.send_message(call.message.chat.id, "Напишите название датчика\n Имя должно начинаться с #")
        message_out_cnt += 1


    # ------------------------------------------------------------------------------------
    #                           HEAT SELECT -> BOILER OPTIONS
    # ------------------------------------------------------------------------------------
    elif call.data == "boiler_options":
        drow_boiler_menu()

    elif call.data == "boiler_onoff":
        if config.boiler['T_CTRL'] == '0':
            wl.set_boiler('T_CTRL', 1)
        elif config.boiler['T_CTRL'] == '1':
            wl.set_boiler('T_CTRL', 0)
        drow_boiler_menu()

    elif call.data == "boiler_update":
        drow_boiler_menu("⏳")
        wl.update_boiler()
        drow_boiler_menu()

        # ------------------------------------------------------------------------------------
    #                         HEAT SELECT -> WF OPTIONS
    # ------------------------------------------------------------------------------------
    elif call.data == "wf_options":
        drow_wf_menu()

    elif call.data == "wf_onoff":
        if config.wf['STATE'] == wl.WL_STATE[0]:  # 'OK':
            if config.wf['T_CTRL'] == '0':
                wl.set_wf('T_CTRL', 1)
            elif config.wf['T_CTRL'] == '1':
                wl.set_wf('T_CTRL', 0)
            drow_wf_menu()

    elif call.data == "wf_update":
        drow_wf_menu("⏳")
        wl.update_wf()
        drow_wf_menu()

    elif call.data.split('@')[0] == "set_temp":
        input_str_type = call.data

        bot.send_message(call.message.chat.id, "Введите температуру")
        message_out_cnt += 1
    # ------------------------------------------------------------------------------------
    #                     HEAT SELECT -> PUMP OPTIONS
    # ------------------------------------------------------------------------------------
    elif call.data == "pumps":
        drow_pump_menu()
        key_back.callback_data = 'heat_select'

    elif call.data.split('@')[0] == 'pump_toggle':
        pump = call.data.split('@')[1]
        drow_pump_menu("⏳")
        wl.toggle_pump(pump)
        wl.get_pump()
        drow_pump_menu()

    elif call.data.split('@')[0] == 'pump_update':
        drow_pump_menu("⏳")
        wl.get_pump()
        drow_pump_menu()


    # ------------------------------------------------------------------------------------
    #                               PARNIC OPTIONS
    # ------------------------------------------------------------------------------------
    elif call.data == "front_door":
        front_door_menu = types.InlineKeyboardMarkup()

        key1 = types.InlineKeyboardButton(text='Открыть', callback_data='wts_options')
        key2 = types.InlineKeyboardButton(text='Закрыть', callback_data='wts_options')
        key_back.callback_data = 'parn'
        front_door_menu.row(key1, key2)
        front_door_menu.row(key_back, key_home)
        bot.edit_message_text('Передняя дверь', call.message.chat.id, call.message.message_id,
                              reply_markup=boiler_options)

    elif call.data == "back_door":
        back_door_menu = types.InlineKeyboardMarkup()

        key1 = types.InlineKeyboardButton(text='Открыть', callback_data='wts_options')
        key2 = types.InlineKeyboardButton(text='Закрыть', callback_data='wts_options')
        key_back.callback_data = 'parn'
        back_door_menu.row(key1, key2)
        back_door_menu.row(key_back, key_home)
        bot.edit_message_text('Задняя дверь', call.message.chat.id, call.message.message_id,
                              reply_markup=boiler_options)

    elif call.data == "parn_options":
        parn_options_menu = types.InlineKeyboardMarkup()

        key1 = types.InlineKeyboardButton(text='Передняя дв.', callback_data='wts_options')
        key2 = types.InlineKeyboardButton(text='Задняя дв.', callback_data='wts_options')
        key_back.callback_data = 'parn'
        parn_options_menu.row(key1, key2)
        parn_options_menu.row(key_back, key_home)
        bot.edit_message_text('Настройки парника', call.message.chat.id, call.message.message_id,
                              reply_markup=boiler_options)

    elif call.data == "front_door_options":
        front_door_options_menu = types.InlineKeyboardMarkup()

        key1 = types.InlineKeyboardButton(text='Темп', callback_data='wts_options')
        key2 = types.InlineKeyboardButton(text='Макс откр', callback_data='wts_options')
        key_back.callback_data = 'parn_options'
        front_door_options_menu.row(key1, key2)
        front_door_options_menu.row(key_back, key_home)
        bot.edit_message_text('Настр. передн. двери', call.message.chat.id, call.message.message_id,
                              reply_markup=boiler_options)

    elif call.data == "back_door_options":
        back_door_options_menu = types.InlineKeyboardMarkup()

        key1 = types.InlineKeyboardButton(text='Темп', callback_data='wts_options')
        key2 = types.InlineKeyboardButton(text='Макс откр', callback_data='wts_options')
        key_back.callback_data = 'parn_options'
        back_door_options_menu.row(key1, key2)
        back_door_options_menu.row(key_back, key_home)
        bot.edit_message_text('Настр. задн. двери', call.message.chat.id, call.message.message_id,
                              reply_markup=boiler_options)


if os.path.isfile('update/update_state'):
    update_state_str = "unknown"
    with open('update/update_state', 'r') as update_state:
        update_state_str = update_state.readline()
        update_state.close()
    bot.send_message(config.Alex_ID, "DOBBY UPDATE: " + update_state_str)
    os.remove('update/update_state')
#wl_update()

f = subprocess.run('date', stdout=subprocess.PIPE)
bot.send_message(config.Alex_ID, f.stdout)
#bot.send_message(config.Alex_ID, "привет")

bot.polling(none_stop=True, interval=3, timeout=60)
# while True: # Don't let the main Thread end.
#     pass
