import time
 
import board
import busio
 
import adafruit_fxos8700
 
 
# Initialize I2C bus and device.
i2c = busio.I2C(board.SCL, board.SDA)
sensor = adafruit_fxos8700.FXOS8700(i2c)
# Optionally create the sensor with a different accelerometer range (the
# default is 2G, but you can use 4G or 8G values):
# sensor = adafruit_fxos8700.FXOS8700(i2c, accel_range=adafruit_fxos8700.ACCEL_RANGE_4G)
# sensor = adafruit_fxos8700.FXOS8700(i2c, accel_range=adafruit_fxos8700.ACCEL_RANGE_8G)
 
# Main loop will read the acceleration and magnetometer values every second
# and print them out.
while True:
    # Read acceleration & magnetometer.
    accel_x, accel_y, accel_z = sensor.accelerometer
    mag_x, mag_y, mag_z = sensor.magnetometer
    # Print values.
   # print(
      #  "Acceleration (m/s^2): ({0:0.3f}, {1:0.3f}, {2:0.3f})".format(
        #    accel_x, accel_y, accel_z
        #)
    #)
    print(
        "Magnetometer (uTesla): ({0:0.3f}, {1:0.3f}, {2:0.3f})".format(
            mag_x, mag_y, mag_z
        )
    )
    print((mag_x*mag_x + mag_y*mag_y + mag_z*mag_z)*0.5)
    # Delay for a second.
    time.sleep(1.0)