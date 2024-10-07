import subprocess
import configparser
import net
from PyP100 import PyP100

config = configparser.ConfigParser()
config.read('dobby_login')

USER = config['TAPO']['user']
PASSWORD = config['TAPO']['pwd']
MAC_OUI = config['TAPO']['OUI']

#WIRELESS SOCKET TAPO P100
class WSP100:
    def __init__(self):
        self.dev = []
        self.ip = []
        self.mac = []
        self.dev_cnt = 0

    def scan_wsp100(self):
        self.dev.clear()
        self.ip.clear()
        self.mac.clear()
        self.dev_cnt = 0
        net_addr = net.scan_net()
        for host in net_addr:        
            if host['MAC']:
                if MAC_OUI == host['MAC'].replace(':', '')[0:6]:
                    self.dev.append(PyP100.P100(host['IP'], USER, PASSWORD))
                    self.ip.append(host['IP'])
                    self.mac.append(host['MAC'])
        self.dev_cnt = len(self.dev)
        
    def turnOn(self, ip):
        dev_num = self.getDevNumByIP(ip)
        if dev_num != None:
            self.dev[dev_num].turnOn()
            return 0
        else:
            return -1
    
    def turnOff(self, ip):
        dev_num = self.getDevNumByIP(ip)
        if dev_num != None:
            self.dev[dev_num].turnOff()
        
    def toggle(self, ip):
        dev_num = self.getDevNumByIP(ip)
        if dev_num != None:
            self.dev[dev_num].toggleState()
            return 0
        else:
            return -1
    
    def getDeviceName(self, ip):
        dev_num = self.getDevNumByIP(ip)
        if dev_num != None:
            return self.dev[dev_num].getDeviceName()
        else:
            return -1
    
    def getDeviceState(self, ip):
        dev_num = self.getDevNumByIP(ip)
        if dev_num != None:
            if self.dev[dev_num].getDeviceInfo()['device_on']:
                return 'on'
            else:
                return 'off'
        else:
            return -1
    
    def getDeviceIP(self, mac):
        dev_num = self.getDevNumByMAC(mac)
        if dev_num != None:
            return self.dev[dev_num].getDeviceInfo()['ip']
        else:
            return -1
    
    def getDeviceInfo(self, ip):
        dev_num = self.getDevNumByIP(ip)
        if dev_num != None:
            return self.dev[dev_num].getDeviceInfo()
        else:
            return -1
    
    def getDevNumByMAC(self, mac):
        if mac in self.mac:
            return self.mac.index(mac)
        else:
            return None
            
    def getDevNumByIP(self, ip):
        if ip in self.ip:
            return self.ip.index(ip)
        else:
            return None
        
        