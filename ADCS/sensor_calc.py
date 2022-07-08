 #sensor_calc.py
import time
import numpy as np
import adafruit_fxos8700
import adafruit_fxas21002c
import time
import os
import board
import busio

i2c = busio.I2C(board.SCL, board.SDA)
sensor1 = adafruit_fxos8700.FXOS8700(i2c)
sensor2 = adafruit_fxas21002c.FXAS21002C(i2c)


#Activity 1: RPY based on accelerometer and magnetometer
def roll_am(accelX,accelY,accelZ):
    if accelZ > 0:
        sign = 1
    else:
        sign = -1
    roll = (180/np.pi)*np.arctan2(accelY,sign*(accelX**2+accelZ**2)**0.5)
    

    roll_corrected = (180/np.pi)*np.arctan2(accelY,(accelX**2+accelZ**2)**0.5)
     # roll function using arctan2 - four quadrant answer
    if accelX >= 0 and accelZ >= 0 : 
        pass
    elif accelZ <= 0 and accelX >= 0 :
        roll_corrected = 180 - roll
    elif accelZ <= 0 and accelX < 0 :
        roll_corrected = 180 - roll
    elif accelZ >= 0 and accelX <= 0 :
        roll_corrected = roll + 360
    


    return roll # move to be 0 to 2pi from -pi to pi
    #print(roll)

def pitch_am(accelX,accelY,accelZ):
    if accelZ > 0:
        sign = 1
    else:
        sign = -1
    pitch = (180/np.pi)*np.arctan2(accelX,sign*(accelY**2+accelZ**2)**0.5) 
    # pitch function using arctan2 - four quadrant answer
    return pitch # 

def yaw_am(accelX,accelY,accelZ,magX,magY,magZ):
    #print(magX,magY,magZ)
    pitchR = (np.pi/180)*pitch_am(accelX,accelY,accelZ)
    rollR = (np.pi/180)*roll_am(accelX,accelY,accelZ) # change to radians for np functions to work
    magx = magX*np.cos(pitchR) + magY*np.sin(rollR)*np.sin(pitchR) + magZ*np.cos(rollR)*np.sin(pitchR)
    magy = magY*np.cos(rollR) - magZ*np.sin(rollR)
    yawR = np.arctan2(-magy,magx) # returning from - pi to pi for some reason (shift to 0-pi)
    return ((180/np.pi)*yawR*2 + 360) % 360  # changing to degrees at the end and moving to 0 to pi

#Activity 2: RPY based on gyroscope
def roll_gy(prev_angle, delT, gyro):
    roll = prev_angle + gyro*delT
    return np.mod(roll,360)
def pitch_gy(prev_angle, delT, gyro):
    pitch = prev_angle + gyro*delT
    return np.mod(pitch,360)
def yaw_gy(prev_angle, delT, gyro):
    yaw = prev_angle + gyro*delT
    return np.mod(yaw,360)

# SENSOR FUSION
def roll_F(prev_angle, delT, gyro,accelVal,weight):
    roll = weight*(prev_angle + gyro*delT) + (1-weight)*(accelVal)
    return np.mod(roll,360)
def pitch_F(prev_angle, delT, gyro,accelVal,weight):
    pitch = weight*(prev_angle + gyro*delT) + (1-weight)*(accelVal)
    return np.mod(pitch,360)
def yaw_F(prev_angle, delT, gyro,accelVal,weight):
    yaw = weight*(prev_angle + gyro*delT) + (1-weight)*(accelVal)
    return np.mod(yaw,360)

def set_initial(mag_offset = [0,0,0]):
    #Sets the initial position for plotting and gyro calculations.
    print("Preparing to set initial angle. Please hold the IMU still.")
    time.sleep(3)
    print("Setting angle...")
    accelX, accelY, accelZ = sensor1.accelerometer #m/s^2
    magX, magY, magZ = sensor1.magnetometer #gauss
    #Calibrate magnetometer readings. Defaults to zero until you
    #write the code
    magX = magX - mag_offset[0]
    magY = magY - mag_offset[1]
    magZ = magZ - mag_offset[2]
    roll = roll_am(accelX, accelY,accelZ)
    pitch = pitch_am(accelX,accelY,accelZ)
    yaw = yaw_am(accelX,accelY,accelZ,magX,magY,magZ)
    print("Initial angle set.")
    print([roll,pitch,yaw]) # display the initial position
    return [roll,pitch,yaw]

def calibrate_mag():
    rollList = [];
    pitchList = [];
    yawList = [];
    print("Preparing to calibrate magnetometer. Please wave around.")
    time.sleep(1) # pause before calibrating
    print("Calibrating...")
    numTestPoints = 0;
    while numTestPoints < 10:
        magX, magY, magZ = sensor1.magnetometer
        print(f"Mag(x,y,z)@{numTestPoints}: {(magX, magY, magZ)}")
        rollList.append(magX)
        pitchList.append(magY)
        yawList.append(magZ)
        numTestPoints += 1
        time.sleep(1)
    print("Calibration complete.")
    # print(rollList)
    time.sleep(1) # break after calibrating
    avgX = np.mean((np.min(rollList),np.max(rollList)))
    avgY = np.mean((np.min(pitchList), np.max(pitchList)))
    avgZ = np.mean((np.min(yawList), np.max(yawList)))
    calConstants = [avgX,avgY,avgZ]
    print(calConstants)
    return calConstants
    #return [0,0,0]

def calibrate_gyro():
    rollList = [];
    pitchList = [];
    yawList = [];
    print("Preparing to calibrate gyroscope. Please hold still.")
    time.sleep(1) # pause before calibrating
    print("Calibrating...")
    numTestPoints = 0;
    while numTestPoints < 10:
        gyroX, gyroY, gyroZ = sensor2.gyroscope
        rollList = rollList + [gyroX]
        pitchList = pitchList + [gyroY] 
        yawList = yawList + [gyroZ]
        numTestPoints += 1
        time.sleep(1)
    print("Calibration complete.")
    # print(rollList)
    time.sleep(1) # break after calibrating
    avgX = np.mean((np.min(rollList),np.max(rollList)))
    avgY = np.mean((np.min(pitchList), np.max(pitchList)))
    avgZ = np.mean((np.min(yawList), np.max(yawList)))
    calConstants = [avgX,avgY,avgZ]
    print(calConstants)
    return calConstants
    #return [0, 0, 0]

def find_north():
    # get gravity direction (down)
    accelX, accelY, accelZ = sensor1.accelerometer #m/s^2
    gravityVec = [accelX,accelY,accelZ]/np.sqrt(accelX**2+accelY**2+accelZ**2) # unit vector direction
    # get magnetic field direction
    magX, magY, magZ = sensor1.magnetometer #gauss
    magVec = [magX,magY,magZ]/np.sqrt(magX**2+magY**2+magZ**2) # unit vector direction
    # get East (cross gravity and mag field directions)
    east = np.cross(gravityVec,magVec)
    # get North (cross East and down)
    north = np.cross(east,gravityVec)
    rollN = np.arctan2(north[2],north[1])
    pitchN = np.arctan2(north[2],north[0])
    # assuming roll and pitch are zero - calculate the yaw from x and y values of North direction
    yawN = np.arctan2(north[0],north[1])
    return ([(180/np.pi)*rollN,(180/np.pi)*pitchN,(180/np.pi)*yawN])





