import serial
import time

INIT = False
PORT = "COM11"

# First put next command on putty:
#   rx handler off
#   debug wl
#

def send_sPort(cmd_str):
    # ========  return code from wl_send_cmd	=========
    # 0	ok
    # 1	address fail
    # 2	bad crc
    # 3	error
    # 4	offline
    # 101 addr not specified
    # 102 wrong TX ADDR
    # 103 cmd not specified
    # 104 wrong TX CMD
    # 105 wrong TX VAR
    # 106 wrong TX VAL
    # ================================================

    wl_send_code =  4	#offline
    addr = 0
    cmd_state = 0
    cmd = '0'
    var = '0'
    val = '0'
    desc = '0'
    dev_error_code = '0'

    sPort = serial.Serial(port=PORT, baudrate=115200)
    result = sPort.write(b'\r\n')
    time.sleep(1)
    send_str = 'wlsend ' + cmd_str + '\r\n'
    result = sPort.write(send_str.encode('utf-8'))
    time.sleep(2)
    out = ''
    while sPort.inWaiting() > 0:
        out += sPort.read(1).decode('Ascii')
    sPort.close()

    if out != '':
        if 'Packet Received' in out:
            wl_send_code = 0  # ok

            s = out.replace('\r\n', '#')
            s = s.replace('##', '#', 10)
            s = s.replace('TX Packet Info', '@TX Packet Info', 2)
            s = s.replace('RX Packet Info', '@R'
                                            'X Packet Info', 2)
            packets=s.split('@')

            rx_pack_inf = packets[2].split('#')
            tx_pack_inf = packets[2].split('#')

            #print (rx_pack_inf)
            #print(tx_pack_inf)

            for fild in rx_pack_inf:
                if 'STATE: 0x' in fild:
                    cmd_state = int(fild.replace('STATE: ', ''), 16)
                if 'SRC ADDR: ' in fild:
                    addr = int(fild.replace('SRC ADDR: ', ''),16)
                if 'CMD' in fild:
                    cmd = fild.replace('CMD: ', '')
                if 'VAR' in fild:
                    var = fild.replace('VAR: ', '')
                if 'VAL' in fild:
                    val = str(int(fild.replace('VAL: ', ''),16))
                if 'DESC' in fild:
                    desc = fild.replace('DESC: ', '')
                if 'DEV ERROR CODE' in fild:
                    dev_error_code = str(int(fild.replace('DEV ERROR CODE: ', ''),16))

    return wl_send_code, addr, cmd_state, cmd, var, val, desc, dev_error_code
# STATE: 0x00
# DEV ERROR CODE: 0x00
# CMD: 0x01
# VAR: 0x00
# VAL: 0x0016
# PID: 0x10D6
# DEST ADDR: 0x53545701
# SRC ADDR: 0x52434657
# DESC: temp
# CRC: 0xBFED21FF
# CRC CALK: 0xBFED21FF
# CRC check: 4 / CRC OK
# ADDR check: 2 / ADDR MATCH#




#send_sPort('0x52434657 1 0 0')