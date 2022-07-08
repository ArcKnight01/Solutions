#complete CAPITALIZED sections

#AUTHOR: 
#DATE:

#import libraries
import time
import os
import board
import busio
import adafruit_fxos8700

from git import Repo
from picamera import PiCamera
import numpy as np
# import math
# import cv2

# import sys
import pathlib
# import datetime

#setup imu and camera
i2c = busio.I2C(board.SCL, board.SDA)
sensor = adafruit_fxos8700.FXOS8700(i2c)
camera = PiCamera()
camera.resolution = (640, 480)
camera.framerate = 24

log_dir ='/home/pi/FlatSatChallenge/Images/'
image_dir = pathlib.Path(log_dir, 'aidanrc')
image_dir.mkdir(parents=True, exist_ok=True)
print(image_dir)

#function for uploading image to Github
def git_push():
    try:
        git_message = "New Photo"
        repo = Repo('/home/pi/FlatSatChallenge')
        repo.git.add('FlatSatChallenge/Images/aidanrc') #PATH TO YOUR IMAGES FOLDER, SHOULD BE LOCATED IN FlatSatChallenge/Images/YOURFOLDER
        
        repo.index.commit(git_message)
        print('made the commit')

        origin = repo.remote('origin')
        print('added remote')

        origin.push()
        print('pushed changes')
        
    except:
        print('Couldn\'t upload to git')

    
#SET THRESHOLD
threshold = (10.5978112954, 0.28713871199999996, 0.0646062102)


#read acceleration
while True:
    accelX, accelY, accelZ = sensor.accelerometer
    
     
    #CHECK IF READINGS ARE ABOVE THRESHOLD
    if ((abs(accelX) > threshold[0]) | (abs(accelY) > threshold[1]) | (abs(accelZ) > threshold[2])):
        print((accelX, accelY, accelZ))
        camera.start_preview()
        print("taking picture...")
        #PAUSE
        time.sleep(5) #warmup camera
        
        #TAKE/SAVE/UPLOAD A PICTURE
        
        name = "picture"     #Last Name, First Initial  ex. FoxJ
        
        
        
        
        if name:
            #path
            log_dir ='/home/pi/FlatSatChallenge/Images/'
            image_dir = pathlib.Path(log_dir, 'aidanrc')
            image_dir.mkdir(parents=True, exist_ok=True)

            print(image_dir)

            t = time.strftime("_%H%M%S")      # current time string
            imgname = (str(image_dir) + '/%s%s' % (name,t)) # change directory to your folder

            print(imgname)
             
            try:
                camera.capture(imgname + ".jpg")
            except:
                # restart the camera
                camera.resolution = (640, 480)
                camera.framerate = 24
                time.sleep(2) # camera warmup time
                
            camera.stop_preview()
            
    
    #PAUSE
    time.sleep(5)
    git_push()
