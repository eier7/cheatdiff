#!/usr/bin/env python

import serial
import re
from yoctopuce.yocto_api import *
from yoctopuce.yocto_relay import *

errmsg = YRefParam()
YAPI.RegisterHub("usb", errmsg)
relay = YRelay.FirstRelay()
relay.set_state(YRelay.STATE_B)

def checksum(sentence):
    calc_cksum = 0
    for s in sentence:
        calc_cksum ^= ord(s)
    return '*'+hex(calc_cksum)[-2:].upper()

ser = serial.Serial("/dev/ttyUSB0", 4800) 
while(True):
    try:
        line = ser.readline()
        line = line.decode("ISO-8859-1")
        if re.match("^\$..GGA", line):
            s = line.split(',')
            s[6] = '4'
            tmpline = ','.join(s)[1:-5]
            chk = checksum(tmpline)
            ser.write(bytes(','.join(s)[:-5]+chk+"\r\n", "UTF-8"))
        else:
            ser.write(bytes(line, "UTF-8"))
    except:
        pass


