#! /usr/bin/env python3
import time
import serial
import os

ser = serial.Serial(
#    port='/dev/ttyS0',
    port='/dev/rfcomm0',
    baudrate = 9600,
    parity=serial.PARITY_NONE,
    stopbits=serial.STOPBITS_ONE,
    bytesize=serial.EIGHTBITS,
    timeout=1
)
counter=0

while 1:
    #sendthis = (' ')
    sendthis = ('Write Counter %s \n' % counter)
    ser.write(sendthis.encode())
    time.sleep(1)
    counter += 1


