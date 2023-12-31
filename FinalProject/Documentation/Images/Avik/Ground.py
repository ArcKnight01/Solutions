import serial
import time
import threading
import os

def getNext(ser):
	while ser.in_waiting == 0: pass
	return ser.read()[0]

def serialreadfile(ser, filename, filesize):
    #Make sure to change your port

     buffer = 2048
     f = open(filename, "wb")

     #Read Size
     '''size = 0
     for i in range(4):
        size = size*256
        size += getNext(ser)'''
     text = b''

     #Read into File
     while filesize > buffer:
        while ser.in_waiting < buffer: pass
        text += ser.read(buffer)
        filesize -= buffer
     while ser.in_waiting < filesize: pass
     text += ser.read(filesize)
     f.write(text)
     f.close()
     print("File Received")

def serialreadsignal(ser):
    while True:
        print("reading")
        signal = getNext(ser)

        #Read file size
        filesize = 0
        for i in range(4):
            filesize = filesize*256
            filesize += getNext(ser)

	    #Read name siez
        namesize = 0
        for i in range(4):
            namesize = namesize*256
            namesize += getNext(ser)

		#Read name
        byt = ser.read(namesize)
        filename = str(byt, "utf-8")

		#Read file
        if signal == ord('i'):
            print("Receiving Image, " + filename)
        elif signal == ord('t'):
            print("Receiving Telemetry Packet, " + filename)
        serialreadfile(ser, filename, filesize)

#function for uploading image to Github
def git_push():
    try:
        repo = Repo('C:/Users/Super Sunny/Desktop/BWSI/Cubesat/GroundStation/AstroBeever/Images/Avik')
        repo.git.add('C:/Users/Super Sunny/Desktop/BWSI/Cubesat/GroundStation/AstroBeever/Images/Avik') #PATH TO YOUR IMAGES FOLDER, SHOULD BE LOCATED IN FlatSatChallenge/Images/YOURFOLDER
        repo.index.commit('New Photo')
        print('made the commit')
        origin = repo.remote('origin')
        print('added remote')
        origin.push()
        print('pushed changes')
    except:
        print('Couldn\'t upload to git')

def gitpull():
    while True:
        cmd = 'git pull'
        os.system(cmd)
        git_push()
        time.sleep(5)

print("Time to run!")
ser = serial.Serial(
    port='COM7',
    baudrate = 256000,
    parity=serial.PARITY_NONE,
    stopbits=serial.STOPBITS_ONE,
    bytesize=serial.EIGHTBITS,
    timeout=1
    )

serialreception=threading.Thread(target=serialreadsignal(ser))
gituploading=threading.Thread(target=gitpull())
serialreception.start()
gituploading.start()
