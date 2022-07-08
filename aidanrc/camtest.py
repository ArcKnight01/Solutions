
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


log_dir ='/home/pi/FlatSatChallenge/Images/'
image_dir = pathlib.Path(log_dir, 'aidanrc')
image_dir.mkdir(parents=True, exist_ok=True)
print(image_dir)


camera = PiCamera()
camera.resolution = (640, 480)
camera.framerate = 24
name = "pic"
camera.start_preview()
time.sleep(5) #warmup camera
camera.stop_preview()
imgname = str(image_dir) + f"/{name}.jpg"
print(imgname)
camera.capture(imgname)


