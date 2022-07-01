import time
import serial
import os
from PIL import Image
from numpy import asarray
import numpy as np

ser = serial.Serial(
    port='/dev/rfcomm0',
    baudrate = 9600,
    parity=serial.PARITY_NONE,
    stopbits=serial.STOPBITS_ONE,
    bytesize=serial.EIGHTBITS,
    timeout=1
)

counter=0

if 1 > counter:
    pngArrayString = ''
    pngArray = bytearray(pngArrayString, 'utf-16')

#IMG NAME HERE
    img = Image.open("/home/pi/bwsi_achuscripts/test.jpg").convert("RGB")
    data = np.array(img)
    #data = [0,1,2,3,4]
    values = str(bytearray(data))


    print("Sending")
    ser.write("About to send".encode())
    ser.write(values)
    print("It has been written")
    ser.write("It was sent too".encode())
    time.sleep(1)
    counter += 1
