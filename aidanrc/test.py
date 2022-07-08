
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


log_dir ='./'
image_dir = pathlib.Path(log_dir, 'AIDANRC_TEMPORARY')
image_dir.mkdir(parents=True, exist_ok=True)
path = pathlib.Path(log_dir)
print(str(pathlib.Path.cwd()))

[print(child) for child in pathlib.Path('./').iterdir() if child.is_dir()]

if(image_dir.exists()):
    if(image_dir.is_dir()):
        print(image_dir)
        q = pathlib.Path('./') / image_dir
        print(q)
        p = pathlib.Path(q, 'file.py')
        p.open('w').write('text')
        print(p.read_text)
        with p.open() as f:
            print(f.readline())
            