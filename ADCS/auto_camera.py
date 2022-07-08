import adafruit_fxos8700
import adafruit_fxas21002c
import time
import os
import board
import busio
from picamera import PiCamera
import numpy as np
import sys
from sensor_calc import *

i2c = busio.I2C(board.SCL, board.SDA)
sensor1 = adafruit_fxos8700.FXOS8700(i2c)
sensor2 = adafruit_fxas21002c.FXAS21002C(i2c)
camera = PiCamera()
name = "MaddieSchroeder"

#Code to take a picture at a given offset angle
def capture(dir ='yaw', target_angle = 110, epsilon = 5):
    #Calibration lines should remain commented out until you implement calibration
    offset_mag = calibrate_mag()
    offset_gyro = calibrate_gyro()
    initial_angle = set_initial(offset_mag) # [roll, pitch, yaw] in degrees
    print(initial_angle) # print to see what the initial angle is
    prev_angle = initial_angle # initialize previous angle to be the starting angle
    startTime = time.time() # get the initial startTime value
    print("Begin moving camera.")
    while True:
        accelX, accelY, accelZ = sensor1.accelerometer #m/s^2
        magX, magY, magZ = sensor1.magnetometer #gauss
	#Calibrate magnetometer readings
        magX = magX - offset_mag[0]
        magY = magY - offset_mag[1]
        magZ = magZ - offset_mag[2]
        gyroX, gyroY, gyroZ = sensor2.gyroscope #rad/s
        #Convert to degrees and calibrate
        gyroX = gyroX *180/np.pi - offset_gyro[0]
        gyroY = gyroY *180/np.pi - offset_gyro[1]
        gyroZ = gyroZ *180/np.pi - offset_gyro[2]
 
        #TODO: Everything else! Be sure to not take a picture on exactly a
        #certain angle: give yourself some margin for error. 
        # get roll, pitch, yaw
        roll_AM = roll_am(accelX,accelY,accelZ)
        pitch_AM = pitch_am(accelX,accelY,accelZ)
        yaw_AM = yaw_am(accelX,accelY,accelZ,magX,magY,magZ)
        
                
        # Calculate the time between gyro integrations
        endTime = time.time()
        delT = endTime-startTime
        # print(delT) - about 0.006 seconds
        startTime = time.time() # start the timer again for the next round
        roll_GY = roll_gy(prev_angle[0],delT,gyroX)
        pitch_GY = pitch_gy(prev_angle[1],delT,gyroY)
        yaw_GY = yaw_gy(prev_angle[2],delT,gyroZ)
        prev_angle = [roll_GY,pitch_GY,yaw_GY] # update the angle for the next measurement
        # print(prev_angle)
        # DEBUGGING PRINTS
        print(yaw_AM)
        #print(initial_angle)
        #print(target_angle)
        #print(yaw_AM - initial_angle - target_angle)

        # if the yaw angle is correct then initiate picture taking
        if np.absolute(yaw_AM - initial_angle[2] - target_angle) < epsilon:
            # print(yaw_GY - initial_angle[2] - target_angle)
            print("Taking a picture")
            t = time.strftime("_%H%M%S")      # current time string
            imgname = ('/home/pi/Labs/ADCS/Images/MaddieSchroeder/%s%s%s.jpg' % (name,t,target_angle)) #change directory to your fold>
            print(imgname)
            camera.start_preview()
            # Camera warm-up time
            time.sleep(0.05)
            camera.capture(imgname)


        

if __name__ == '__main__':
    capture(*sys.argv[1:])
