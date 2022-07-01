
# IMPORTS
import time as t
import os
import board
import busio
import adafruit_fxos8700
import adafruit_fxas21002c
import numpy as np
import math
import imu
import RSTbluetooth as bt
from RSTbluetooth import *
import imu as imu
import ImageProcessor as ip
import camera_capture as cc

# BASIC CONSTANTS
bdaddrGS = "8C:85:90:A0:D6:84" # bluetooth address of ground station
bdaddrF = "8C:85:90:A0:D6:84" # bluetooth address of flight pi
dropboxpath = '/Users/sajivshah/Dropbox/BWSI2020Group5Images'
image_Path = '/home/pi/Solutions/FinalProject/2022/FlightImages/{}'.format(NAME) # path for where to save images

# INITIALIZATION
initial_time = t.time() # time that the code started
init_orbit = 0
orbitCount = 0 # number of the orbit that we are currently on


"""def startTime():
    global time
    while True:
        t.sleep(1)
        time += 1"""

#this keeps the names of the images from the last captureOrbit
img_names = []
def performOrbit(initial_time,orbit_count,image_path):
    """
    Takes pictures for one orbit and downlinks all telemetry at the end of the orbit.
    Each orbit will take sixty seconds. Run this for 60 seconds. At the end get the 
    yaw measurement and adjust so it is at 2pi

    param:
        initial_time = time that the code started
        orbit_count = number of the current orbit
        image_path = path to send images to when they are captured

    return:
        none - if we are past 10 orbit

    """

    # initialize orbit parameters
    img_names = [] # all image names for this orbit
    red_img_names = [] # all image names for this orbit with red in them
    orbit_count += 1 # increment the orbit counter for the start of a new orbit
    telem_data = '' # start with no telemetry data

    # loop until orbit is finished
    while True:
        # Get the orbit started
        t.sleep(1) # pause for 1 second to let you get set up 
        # print(starting orbit) # send message that the orbit is starting

        # if over 10 orbits return none to stop running
        if orbit_count > 10:
            return None

        # if under 10 orbits and within time for the first orbit (yaw not back to 360 deg)
        if ((t.time() - initial_time)%19 < 3):
            # take image 
            # TO DO: put this in serial port
            print('taking image')
            img_name = cc.take_picture(imu.getOrbitCount()+init_orbit, image_path, len(img_names))
            img_names.append(img_name) # add the image names to the list of image names

            # Try the image processor
            try:
                processor = ip.ImageProcessor(img_name, 'Sajiv')
            except:
                telem_data += "Image Processor Error "

            # Add image information to the telemetry data
            telem_data += processor.find_percentages()
            telem_data += 'Image taken at ' + str(t.time() - initial_time) + '\n' # add line describing image details

            t.sleep(5) # pause 5 seconds WHYYYYY

        # if it is the end of the orbit    
        if (((t.time() - initial_time)%60 < 5 and (t.time() - initial_time) > 60)  or len(img_names) >= 3):
            print('orbit end')

            # add ending to telemetry data
            telem_data += 'Orbit completed at ' + str(t.time() - initial_time) + '/n'
            # telem_data += 'ADCS good' WHYYYYY - how do you tell if ADCS is good

            # prepare everything to move to the next orbit
            transferOrbit()



def transferOrbit():
    """
    Transfer to the next orbit

    param:

    return:

    """
    print('enter transfer orbit')
    global telemData
    global img_names
    global init_orbit
    global orbitCount

    orbitCount += 2
    sendTelem()
    orbit_count = orbitCount + init_orbit
    #Resend image if no ground signal, put in a reboot
    #if 60 seconds have passed with no images transferred
    dt = send_images(img_names)
    if dt > 30:
        dt = send_images(img_names)
    if dt > 30:
        with open('data_transfer/Ground_Comms.txt', mode='w') as f:
            f.write(str(orbit_count)+'\n'+str(t.time() - intial_time()))
        os.system('sudo reboot')


# TO DO - why is the send images separate and have so many weird parts
def send_images(img_names, bdaddrGS, groundStationPath):
    """
    Send image to the ground station

    param:
        img_names = list of names of images to be sent to the groundstation
        bdaddrGS = address of ground station
        groundStationPath = place to send the file on the ground station pi
    return:
        nothing
    """

    print('sending images')

    # send images in list to the ground station
    for img_name in img_names:
        successfulTransfer, fileSize, sendTime = bt.sendFile(bdaddr, img_name, groundStationPath)
    t0 = t.process_time()
    dt = 0
    ground_signal = 0
    fail_count = 0
    while(ground_signal == 0 and dt <= 30):
        dt = t.process_time() - t0
        successfulDownload, fileSize, downloadTime = getFile(bdaddr, dropboxpath + '/ground_signal.txt', '/home/pi/Rubble_Space_Telescope/data_transfer/')
        if not successfulDownload:
            fail_count += 1
        if fail_count >= 9:
            #reboot?
            return dt
        #Put code receviing ground_signal from dropbox folder
        with open('/home/pi/Rubble_Space_Telescope/data_transfer/ground_signal.txt', mode='r') as f:
            signal = f.readline()
            if len(signal) > 0:
                ground_signal = int(signal)
        t.sleep(.05)
    return dt


def sendTelem(telem_data, bdaddrGS, groundStationPath):
    """
    Send telemetry packet to the ground stations

    param:
        telemData = telemetry data 
        bdaddrGS = address of ground station
        groundStationPath = place to send the file on the ground station pi
    return:
        nothing
    """
    # TO DO - make this serial connection
    print('sending telem')

    # write telemetry into full telemetry file
    with open('data_transfer/Flight_Telemetry.txt', mode='w') as f:
        f.write(telem_data)
    # send the file to the ground station
    successfulTransfer, fileSize, sendTime = bt.sendFile(bdaddrGS, 'data_transfer/Flight_Telemetry.txt', groundStationPath)

"""
Before running main code, you have to set Flight_Telemetry.txt to 0 and then next line to 0 as well so that the code
knows you are on the first orbit. After ground receives an image, they should write a one
or other number into ground_signal.txt, ground_signal.txt must only have an int or code will error.
"""
def main(initial_time, orbit_count, image_path):

    # with open('data_transfer/Flight_Telemetry.txt', mode='r') as f:
    #     init_orbit = f.readline()
    #     if len(init_orbit) > 0:
    #         init_orbit = int(init_orbit)

    # send initial telemetry packet
    sendTelem()

    hasStarted = False # start the process
    # loop to find north and start the orbit
    # TO DO - change this to sending a command to start the orbit
    while hasStarted == False:
        t.sleep(0.1)

        # Determine whether the orbit process has started
        if(imu.getyaw()):
            initial_time = t.time()
            performOrbit(initial_time, orbit_count, image_path) # start process for one orbit
            hasStarted = True

#Run code here
main(initial_time, orbit_count, image_path)
