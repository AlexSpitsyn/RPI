import config
DS18B20_ID = '28-041750af62ff'
def get_temp():
    if config.dobby['OS'] == 'LIN':
        tfile = open("/sys/bus/w1/devices/"+DS18B20_ID+"/w1_slave")
        ttext = tfile.read()
        tfile.close()
        temp = ttext.split("\n")[1].split(" ")[9]
        temperature = float(temp[2:]) / 1000
        return temperature
    else:
        return 100

