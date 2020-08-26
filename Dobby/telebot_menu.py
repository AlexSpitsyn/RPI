import telebot
from telebot import apihelper, types, util

import wl
import config


Alex_ID = 972228317

#https://hidemy.name/ru/proxy-list/?type=5#list
telebot.apihelper.proxy = {'https':'socks5://154.16.202.22:10879'}

TOKEN = '927942451:AAG7HMnzpyLVKcydJiEW0zGjOcnqi7_1EDE'

bot = telebot.TeleBot(TOKEN)
bot.send_message(Alex_ID, "привет")
#bot.edit_message_text( "Имя должно начинаться с #",message_out.chat.id, message_out.message_id, )
#bot.clear_step_handler_by_chat_id(chat_id=call.message.chat.id)
#bot.register_next_step_handler(message, send_text3)

config.init()

#print( config.wts)
print( config.boiler)
#print( config.wf)
#print( config.circ)

#print(wts_data)
wts_num=0
#wts_name =''
#wts_val=''
#wts_state=''
#wts_check=''
input_str_type='0'
message_out = '0'
message_out_cnt =0
#markup
gcall='0'


key_home = types.InlineKeyboardButton(text='🏠', callback_data='mainmenu')
key_back = types.InlineKeyboardButton(text='↩️', callback_data='back')

@bot.message_handler(content_types=['text'])

def inline_key(a):      
    global wts_num 
    global input_str_type
    global message_out
    #global markup
    global gcall
    global set_dict
    global message_out_cnt

    if a.text == "/menu":
        mainmenu = types.InlineKeyboardMarkup()
        key1 = types.InlineKeyboardButton(text='Прочее', callback_data='other')
        key2 = types.InlineKeyboardButton(text='Парник', callback_data='parn')
        key3 = types.InlineKeyboardButton(text='Отопление', callback_data='heat_select')
        key4 = types.InlineKeyboardButton(text='Температура', callback_data='temp')
        
        mainmenu.row(key4, key3)
        mainmenu.row(key2, key1)
        bot.send_message(a.chat.id, '\t ГЛАВНОЕ МЕНЮ', reply_markup=mainmenu)
        #print(type(a.text))   
        bot.delete_message(a.chat.id, a.message_id)
    

        
    if input_str_type == 'wts_name': 
        input_str_type = '0'
        if(a.text[0]=='#'):
            wts_name = a.text.strip('#')
            config.wts[wts_num]["NAME"]=wts_name
            config.write_wts() 
            
            #msg=bot.send_message(a.chat.id, 'Имя для Д1 - '+ wts_name )
            bot.edit_message_text(get_WTS_state(wts_num), message_out.chat.id, message_out.message_id, reply_markup=markup)            
            bot.delete_message(a.chat.id, a.message_id)
            bot.delete_message(a.chat.id, a.message_id-1)   
        else:
            bot.answer_callback_query(gcall.id, text="Неверно задано имя", show_alert=True)
            message_out_cnt+=1
            bot.delete_message(a.chat.id, a.message_id)
            bot.delete_message(a.chat.id, a.message_id-1)
            

    elif input_str_type.split('@')[0] == 'temp':        
        temp_type=input_str_type.split('@')[1]
                
        if(a.text.isdigit()):
            if temp_type == 'boiler':
                if int(a.text) > config.temp['BOILER_MIN'] and int(a.text) < config.temp['BOILER_MAX']:
                    
                    config.boiler['TEMP_SET']=a.text
                    config.write_boiler()
                    input_str_type='0'
                    drow_boiler_menu()
                    print (message_out_cnt)
                    #while message_out_cnt:                        
                    #    bot.delete_message(a.chat.id, a.message_id-message_out_cnt)
                    #    message_out_cnt-=1
                    
                else:
                    bot.answer_callback_query(gcall.id, text="Мин значение: "+str(config.temp['BOILER_MIN'])+'\n'+
                                              'Макс занчение: '+str(config.temp['BOILER_MAX'])+'n', show_alert=True)
                    message_out_cnt+=1
                     
            elif temp_type == 'wf':
                if int(a.text) > config.temp['WF_MIN'] and int(a.text) < config.temp['WF_MAX']:
                    drow_wf_menu()
                    config.wf['TEMP_SET']=a.text
                    config.write_wf() 
                    
                else:
                    bot.answer_callback_query(gcall.id, text="Мин значение: "+str(config.temp['WF_MIN'])+'\n'+
                                          'Макс занчение: '+str(config.temp['WF_MAX'])+'n', show_alert=True)
                    #message_out_cnt+=1
                           

            #bot.delete_message(a.chat.id, a.message_id)
            #bot.delete_message(a.chat.id, a.message_id-1)   
        else:
            bot.answer_callback_query(gcall.id, text="Неверно задано значение", show_alert=True)
            message_out_cnt+=1
     
     

            
        
@bot.callback_query_handler(func=lambda call: True)
def callback_inline(call):
    
   
    global wts_num
    global input_str_type
    global message_out
    #global markup
    global gcall    
    global message_out_cnt
    gcall=call
    
    if call.data == "mainmenu":
        mainmenu = types.InlineKeyboardMarkup()
        key1 = types.InlineKeyboardButton(text='Прочее', callback_data='other')
        key2 = types.InlineKeyboardButton(text='Парник', callback_data='parn')
        key3 = types.InlineKeyboardButton(text='Отопление', callback_data='heat_select')
        key4 = types.InlineKeyboardButton(text='Температура', callback_data='temp')
        mainmenu.row(key4, key3)
        mainmenu.row(key2, key1)
        bot.edit_message_reply_markup(call.message.chat.id, call.message.message_id, reply_markup=mainmenu)
        input_str_type='0'
        
    
    elif call.data == "temp":
        temp_menu = types.InlineKeyboardMarkup()
        key1 = types.InlineKeyboardButton(text='Инф', callback_data='print_temp')
        key2 = types.InlineKeyboardButton(text='Настройки', callback_data='wts_select')
        key_back.callback_data='mainmenu'

        temp_menu.row(key1, key2)

        temp_menu.row(key_back, key_home)
        bot.edit_message_text('Температура', call.message.chat.id, call.message.message_id,
                              reply_markup=temp_menu)

    elif call.data == "heat_select":

        heat_select_menu = types.InlineKeyboardMarkup()
        key1 = types.InlineKeyboardButton(text='Котёл', callback_data='boiler_options')
        key2 = types.InlineKeyboardButton(text='ТП', callback_data='wf_options')
        key3 = types.InlineKeyboardButton(text='Насосы', callback_data='circulators')
        key_back.callback_data='mainmenu'

        heat_select_menu.row(key1, key2, key3)
        heat_select_menu.row(key_back, key_home)
        bot.edit_message_text('Отопление', call.message.chat.id, call.message.message_id,
                              reply_markup=heat_select_menu)

    elif call.data == "parn":
        parn_menu = types.InlineKeyboardMarkup()
        key1 = types.InlineKeyboardButton(text='Передняя дв.', callback_data='front_door')
        key2 = types.InlineKeyboardButton(text='Задняя дв.', callback_data='back_door')
        key3 = types.InlineKeyboardButton(text='Инф', callback_data='print_parn_inf')
        key4 = types.InlineKeyboardButton(text='Настройки', callback_data='parn_options')
        key_back.callback_data='mainmenu'

        parn_menu.row(key1, key2)
        parn_menu.row(key3, key4)
        parn_menu.row(key_back, key_home)
        bot.edit_message_text('Парник', call.message.chat.id, call.message.message_id,
                              reply_markup=parn_menu)

    elif call.data == "other":
        other_menu = types.InlineKeyboardMarkup()
        key1 = types.InlineKeyboardButton(text='Септик', callback_data='front_door')
        
        key2 = types.InlineKeyboardButton(text='Настройки', callback_data='parn_options')
        key_back.callback_data='mainmenu'

        other_menu.row(key1, key2)
        other_menu.row(key_back, key_home)
        bot.edit_message_text('Прочее', call.message.chat.id, call.message.message_id,
                              reply_markup=other_menu)

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
        
        key_back.callback_data='temp'
        wts_select_menu.row(key1,key2,key3,key4)
        wts_select_menu.row(key5,key6,key7,key8)
        wts_select_menu.row(key9,key10,key11,key12)
        wts_select_menu.row(key13,key14,key15,key16)
        wts_select_menu.row(key_back, key_home)
        bot.edit_message_text('Настройки датчиков', call.message.chat.id, call.message.message_id,
                              reply_markup=wts_select_menu)

    
    elif call.data.split('@')[0] == "wts_options":
        wts_num=int(call.data.split('@')[1]) -1  
        drow_wts_options(wts_num)


    
    elif  call.data == "wts_onoff": 
        config.wts_toggle_check(wts_num)
        drow_wts_options(wts_num)
        
           
    
    elif  call.data == "wts_update":
        
        if wl.read_wts(wts_num) == 'FAIL' :
            bot.send_message(call.message.chat.id,  "Что-то пошло не так... Тут нужна магия")               
        else:
            drow_wts_options(wts_num)
 
    elif  call.data == "set_wts_name":
        input_str_type='wts_name';       
        bot.send_message(call.message.chat.id,  "Напишите название датчика\n Имя должно начинаться с #")   
        message_out_cnt+=1
        
    
    elif call.data == "boiler_options":        
        drow_boiler_menu()
        key_back.callback_data='heat_select'
        
    elif call.data == "boiler_onoff":
        if wl.toggle_boiler() == 'FAIL' :
            bot.send_message(call.message.chat.id,  "Что-то пошло не так... Тут нужна магия")               
        else:
            drow_boiler_menu()          

    elif call.data == "boiler_update": 
        if wl.update_boiler() == 'FAIL' :
            bot.send_message(call.message.chat.id,  "Что-то пошло не так... Тут нужна магия")               
        else:
            drow_boiler_menu()  
    
    elif call.data == "wf_options":        
        drow_wf_menu()
        key_back.callback_data='heat_select'
        
    elif call.data == "wf_onoff":
        if wl.toggle_wf() == 'FAIL' :
            bot.send_message(call.message.chat.id,  "Что-то пошло не так... Тут нужна магия")               
        else:
            drow_wf_menu()          

    elif call.data == "wf_update": 
        if wl.update_wf() == 'FAIL' :
            bot.send_message(call.message.chat.id,  "Что-то пошло не так... Тут нужна магия")               
        else:
            drow_wf_menu()  
    
    
    elif call.data.split('@')[0] == "set_temp": 
        temp_type=call.data.split('@')[1]
        input_str_type='temp@'+temp_type;      
       
        bot.send_message(call.message.chat.id,  "Введите температуру")   
        message_out_cnt+=1

    elif call.data == "circulators":
        drow_circ_menu()
        key_back.callback_data='heat_select'
        
    elif call.data.split('@')[0] == 'circ_toggle':
        circ=call.data.split('@')[1]
        wl.circ_toogle(circ)
        
        
    elif call.data == "front_door":
        front_door_menu = types.InlineKeyboardMarkup()

        key1 = types.InlineKeyboardButton(text='Открыть', callback_data='wts_options')
        key2 = types.InlineKeyboardButton(text='Закрыть', callback_data='wts_options')
        key_back.callback_data='parn'        
        front_door_menu.row(key1, key2)
        front_door_menu.row(key_back, key_home)
        bot.edit_message_text('Передняя дверь', call.message.chat.id, call.message.message_id,
                              reply_markup=boiler_options)

    elif call.data == "back_door":
        back_door_menu = types.InlineKeyboardMarkup()

        key1 = types.InlineKeyboardButton(text='Открыть', callback_data='wts_options')
        key2 = types.InlineKeyboardButton(text='Закрыть', callback_data='wts_options')
        key_back.callback_data='parn'        
        back_door_menu.row(key1, key2)
        back_door_menu.row(key_back, key_home)
        bot.edit_message_text('Задняя дверь', call.message.chat.id, call.message.message_id,
                              reply_markup=boiler_options)

    elif call.data == "parn_options":
        parn_options_menu = types.InlineKeyboardMarkup()

        key1 = types.InlineKeyboardButton(text='Передняя дв.', callback_data='wts_options')
        key2 = types.InlineKeyboardButton(text='Задняя дв.', callback_data='wts_options')
        key_back.callback_data='parn'        
        parn_options_menu.row(key1, key2)
        parn_options_menu.row(key_back, key_home)
        bot.edit_message_text('Настройки парника', call.message.chat.id, call.message.message_id,
                              reply_markup=boiler_options)

    elif call.data == "front_door_options":
        front_door_options_menu = types.InlineKeyboardMarkup()

        key1 = types.InlineKeyboardButton(text='Темп', callback_data='wts_options')
        key2 = types.InlineKeyboardButton(text='Макс откр', callback_data='wts_options')
        key_back.callback_data='parn_options'        
        front_door_options_menu.row(key1, key2)
        front_door_options_menu.row(key_back, key_home)
        bot.edit_message_text('Настр. передн. двери', call.message.chat.id, call.message.message_id,
                              reply_markup=boiler_options)

    elif call.data == "back_door_options":
        back_door_options_menu = types.InlineKeyboardMarkup()

        key1 = types.InlineKeyboardButton(text='Темп', callback_data='wts_options')
        key2 = types.InlineKeyboardButton(text='Макс откр', callback_data='wts_options')
        key_back.callback_data='parn_options'        
        back_door_options_menu.row(key1, key2)
        back_door_options_menu.row(key_back, key_home)
        bot.edit_message_text('Настр. задн. двери', call.message.chat.id, call.message.message_id,
                              reply_markup=boiler_options)



def drow_wts_options(wts_num):
    global gcall
    check = config.wts[wts_num]["CHECK"]    
    name = config.wts[wts_num]["NAME"]
    val = config.wts[wts_num]["VAL"]
    state = config.wts[wts_num]["STATE"]

    if check == '1':
        button_onoff_text = 'ВЫКЛ'
        if(state == '0'):
            state_sym='✅'

        elif(state == '1'):
            state_sym='🛑'#offline   
        else:
            state_sym='⚠️'+ wts_state 

        header_str = state_sym+'\t\t'+ 'Д'+ str(wts_num+1) +'\t\t'+ wts_name
    else:
        button_onoff_text = 'ВКЛ'
        state_sym='⏹'#not checked            
        header_str = state_sym +'\t\t'+ 'Д'+ str(wts_num+1) +'\t\t'+ name +'\t\t' + wts_val +'°C' 

    wts_options_menu = types.InlineKeyboardMarkup() 
    key1 = types.InlineKeyboardButton(text=button_onoff_text, callback_data='wts_onoff')
    key2 = types.InlineKeyboardButton(text='Имя', callback_data='set_wts_name')
    key3 = types.InlineKeyboardButton(text='🔄', callback_data='wts_update')
    #key_back.callback_data='wts_select'
    wts_options_menu.add(key1, key2, key3)
    wts_options_menu.row(key_back, key_home)

    markup = wts_options_menu
    message_out=bot.edit_message_text(header_str, gcall.message.chat.id, gcall.message.message_id,
                          reply_markup=wts_options_menu)

def drow_boiler_menu():
    global gcall   

    state = config.boiler["STATE"]
    temp = config.boiler["TEMP"]
    set_temp = config.boiler["TEMP_SET"]

    if state == '1':
        button_onoff_text = '✅'        
        header_str = '\t\tКотёл\t \t'+ temp +'\t \t'+ '[ '+set_temp+'°C ]'
    elif state == '1':        
        button_onoff_text = '🛑'                
        header_str = '\t\tКотёл\t \t'+ temp +'\t \t'+ '[ '+set_temp+'°C ]' 
    else:
        button_onoff_text = '⚠️'             
        header_str = '\t\tКотёл\t \t' + '[ '+set_temp+'°C ]'
    
    boiler_options_menu = types.InlineKeyboardMarkup() 
    key1 = types.InlineKeyboardButton(text=button_onoff_text, callback_data='boiler_onoff')
    key2 = types.InlineKeyboardButton(text='Уст.темп', callback_data='set_temp@boiler')
    key3 = types.InlineKeyboardButton(text='🔄', callback_data='boiler_update')
    
    #key_back.callback_data='heat_select'
    boiler_options_menu.add(key1, key2, key3)
    boiler_options_menu.row(key_back, key_home)

    markup = boiler_options_menu
    message_out=bot.edit_message_text(header_str, gcall.message.chat.id, gcall.message.message_id,
                          reply_markup=boiler_options_menu)
def drow_wf_menu():
    global gcall   

    state = config.wf["STATE"]
    temp = config.wf["TEMP"]
    set_temp = config.wf["SET_TEMP"]

    if state == '1':
        button_onoff_text = '✅'        
        header_str = '\t\tТП\t \t'+ temp +'\t \t'+ '[ '+set_temp+'°C ]'
    elif state == '1':        
        button_onoff_text = '🛑'                
        header_str = '\t\tТП\t \t'+ temp +'\t \t'+ '[ '+set_temp+'°C ]' 
    else:
        button_onoff_text = '⚠️'             
        header_str = '\t\tТПt \t' + '[ '+set_temp+'°C ]'
    
    wf_options_menu = types.InlineKeyboardMarkup() 
    key1 = types.InlineKeyboardButton(text=button_onoff_text, callback_data='wf_onoff')
    key2 = types.InlineKeyboardButton(text='Уст.темп', callback_data='set_temp@wf')
    key3 = types.InlineKeyboardButton(text='🔄', callback_data='wf_update')
    
    #key_back.callback_data='heat_select'
    wf_options_menu.add(key1, key2, key3)
    wf_options_menu.row(key_back, key_home)

    markup = wf_options_menu
    message_out=bot.edit_message_text(header_str, gcall.message.chat.id, gcall.message.message_id,
                          reply_markup=wf_options_menu)
    
def drow_circ_menu():
    global gcall   

    c1_1_state = config.circ["CIRC1_1"]
    c1_2_state = config.circ["CIRC1_2"]
    c2_1_state = config.circ["CIRC2_1"]
    c2_2_state = config.circ["CIRC2_2"]
    c_main_state = config.circ["CIRC_MAIN"]
    c_hb_state = config.circ["CIRC_HB"]

    if c1_1_state == '1':
        button1_text = '✅'  
    elif state == '0':        
        button1_text = '🛑'   
    else:
        button1_text = '⚠️'   
    
    if c1_2_state == '1':
        button2_text = '✅'  
    elif state == '0':        
        button2_text = '🛑'   
    else:
        button2_text = '⚠️' 
    
    if c2_1_state == '1':
        button3_text = '✅'  
    elif state == '0':        
        button3_text = '🛑'   
    else:
        button3_text = '⚠️'  

    if c2_2_state == '1':
        button4_text = '✅'  
    elif state == '0':        
        button4_text = '🛑'   
    else:
        button4_text = '⚠️'  
        
    if c_main_state == '1':
        button5_text = '✅'  
    elif state == '0':        
        button5_text = '🛑'   
    else:
        button5_text = '⚠️'  
        
    if c_hb_state == '1':
        button6_text = '✅'  
    elif state == '0':        
        button6_text = '🛑'   
    else:
        button6_text = '⚠️'  
      
    
    
    
    circulators_menu = types.InlineKeyboardMarkup()	
    key1 = types.InlineKeyboardButton(text=button5_text + ' ДОМ', callback_data='circ_toggle@CIRC_MAIN')
    key2 = types.InlineKeyboardButton(text=button6_text + ' ХБ', callback_data='circ_toggle@CIRC_HB')
    key3 = types.InlineKeyboardButton(text=button1_text + ' Кухня-гост', callback_data='circ_toggle@CIRC1_1')
    key3 = types.InlineKeyboardButton(text=button2_text + ' Прихожая-сп.гост', callback_data='circ_toggle@CIRC1_2')
    key5 = types.InlineKeyboardButton(text=button3_text + ' Спальная 2.1 -2.2.', callback_data='circ_toggle@CIRC2_1')
    key6 = types.InlineKeyboardButton(text=button4_text + ' Спальная 2.3 -2.4.', callback_data='circ_toggle@CIRC2_2')
    
   
    #key_back.callback_data='heat_select'        
    circulators_menu.row(key1)
    circulators_menu.row(key2)
    circulators_menu.row(key3)
    circulators_menu.row(key4)
    circulators_menu.row(key5)
    circulators_menu.row(key6)
    circulators_menu.row(key_back, key_home)
    
    markup = circulators_menu
    message_out=bot.edit_message_text('Насосы', gcall.message.chat.id, gcall.message.message_id,
                          reply_markup=circulators_menu)
    
bot.polling()
