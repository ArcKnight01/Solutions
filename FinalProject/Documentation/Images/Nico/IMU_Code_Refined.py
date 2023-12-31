#Version 3
import time
import numpy as np
import adafruit_fxos8700
import adafruit_fxas21002c
import time
import os
import board
import busio
import math

#Initializing board
i2c = busio.I2C(board.SCL, board.SDA)
sensor1 = adafruit_fxos8700.FXOS8700(i2c)
sensor2 = adafruit_fxas21002c.FXAS21002C(i2c)

#Creating a continous loop
while True:
    accelX, accelY, accelZ = sensor1.accelerometer #m/s^2
    magX, magY, magZ = sensor1.magnetometer #gauss

    mag_offset = [25.300000000000004, 79.35, 80.05000000000001] #Insert mag_offset calibration values here
    mag_scale = [0.9513184584178499, 1.0695553021664768, 0.9863301787592009] #Insert mag_scale calibration values
    
    magX = (magX - mag_offset[0]) * mag_scale[0]
    magY = (magY - mag_offset[1]) * mag_scale[1]
    magZ = (magZ - mag_offset[2]) * mag_scale[2]
    
    #Calculating RPY
    roll = np.arctan2((accelY),(((accelX)**2 + (accelZ)**2)**0.5))
    

    pitch = np.arctan2((accelX),(((accelY)**2 + (accelZ)**2)**0.5))
    
    mag_x = (magX * np.cos(pitch)) + (magY * np.sin(roll)) + np.sin(pitch) + (magZ*np.cos(roll)*np.sin(pitch))
    mag_y = (magY*np.cos(roll)) - (magZ*np.sin(roll))
    #Original Yaw Eq: (180/np.pi)*np.arctan2(-mag_y, mag_x)
    yaw = (180/np.pi)*np.arctan2(-mag_x, mag_y)
    
    #Fixing coordinate direction
    yaw = (yaw + 360) % 360
    pitch = (((180/np.pi) * pitch) + 360) % 360
    roll = (((180/np.pi) * roll) + 360) % 360
    
    #Account for miniscule differences
    yaw += 113
    
    #Bounding Yaw to 0-360 deg
    if yaw > 360:
        yaw -= 360


    #Print RP Values
    print("roll: " + str(roll) + " degrees")
    print("pitch: " + str(pitch) + " degrees")
    
    #Print Yaw values with a cardinal direction

    if yaw >= 292 and yaw <= 337:
        _dir = str(yaw) + " degrees (NorthWest)"
    if yaw > 337 or yaw < 22:
        _dir = str(yaw) + " degrees (North)"
    if yaw > 248 and yaw < 292:
        _dir = str(yaw) + " degrees (West)"
    if yaw > 158 and yaw < 202:
        _dir = str(yaw) + " degrees (South)"
    if yaw > 68 and yaw < 112:
        _dir = str(yaw) + " degrees (East)"
    if yaw >= 22 and yaw <= 68:
        _dir = str(yaw) + " degrees (NorthEast)"
    if yaw >= 112 and yaw <= 158:
        _dir = str(yaw) + " degrees (SouthEast)"
    if yaw >= 202 and yaw <= 248:
        _dir = str(yaw) + " degrees (SouthWest)"
    
    print("yaw: " + _dir)
    
    #Delay for 1 second
    time.sleep(1)

