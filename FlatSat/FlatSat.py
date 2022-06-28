#complete CAPITALIZED sections

#AUTHOR: Emily McCarthy
#DATE: 6/27/22

#import libraries
import time
import os
import board
import busio
import adafruit_fxos8700
from git import Repo
from picamera import PiCamera

#setup imu and camera
i2c = busio.I2C(board.SCL, board.SDA)
sensor = adafruit_fxos8700.FXOS8700(i2c)
camera = PiCamera()

#function for uploading image to Github
def git_push():
#    try:
        repo = Repo('/home/pi/FlatSatChallenge')
        repo.git.add('/home/pi/FlatSatChallenge/Images/EmilyMcCarthy') #PATH TO YOUR IMAGES FOLDER, SHOULD BE LOCATED IN FlatSatChallenge/Images/YOURFOLDER
        repo.index.commit('New Photo')
        print('made the commit')
        origin = repo.remote('origin')
        print('added remote')
        origin.push()
        print('pushed changes')
#    except:
 #       print('Couldn\'t upload to git')

#SET THRESHOLD
threshold = 15


#read acceleration
while True:
	accelX, accelY, accelZ = sensor.accelerometer

    #CHECK IF READINGS ARE ABOVE THRESHOLD
        #PAUSE
	if accelX > threshold or accelY > threshold or accelZ > threshold:
        	print('Shake Detected')
        	print(accelX)
        	print(accelY)
        	print(accelZ)
        	time.sleep(4)
        	print('Image Taken')
        	camera.capture(imgname + '.jpg')
        	git_push()

    
        #TAKE/SAVE/UPLOAD A PICTURE 
	name = "McCarthyE"     #Last Name, First Initial  ex. FoxJ
	if name:
		t = time.strftime("_%H%M%S")      # current time string
		imgname = ('/home/pi/FlatSatChallenge/Images/EmilyMcCarthy/%s%s' % (name,t)) #change directory to your folder
    
            #<YOUR CODE GOES HERE>#
            
    
    #PAUSE
