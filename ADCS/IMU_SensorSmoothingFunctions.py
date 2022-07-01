import board
import adafruit_fxos8700
import adafruit_fxas21002c
from statistics import mean
import time

i2c = board.I2C()
accelMag = adafruit_fxos8700.FXOS8700(i2c)
gyro = adafruit_fxas21002c.FXAS21002C(i2c)
	
def getSmoothAccel(sensor, n):
	"""
		Eliminates noise from the accelerometer readings 
		using a moving average with an n-large window, and
		prints out values

		Args:
			sensor: the sensor being read
			n: the number of readings to be averaged

		Returns:
			Nothing

		Raises:
		AssertionError: sensor is not the accelerometer
	"""	

	assert type(sensor) is adafruit_fxos8700.FXOS8700

	xValues = []
	yValues = []
	zValues = []
	
	while len(xValues) < n:
		xValue, yValue, zValue = sensor.accelerometer
		xValues.append(xValue)
		yValues.append(yValue)
		zValues.append(zValue)
		
	print((sum(xValues)/n, sum(yValues)/n, sum(zValues)/n))
	
	while True:
		xValue, yValue, zValue = sensor.accelerometer
		xValues.append(xValue)
		yValues.append(yValue)
		zValues.append(zValue)
		xValues.pop(0)
		yValues.pop(0)
		zValues.pop(0)
		print((sum(xValues)/n, sum(yValues)/n, sum(zValues)/n))
		
def getSmoothMag(sensor, n):
	"""
		Eliminates noise from the magnetometer readings 
		using a moving average with an n-large window, and
		prints out values

		Args:
			sensor: the sensor being read
			n: the number of readings to be averaged

		Returns:
			Nothing

		Raises:
		AssertionError: sensor is not the magnetometer
	"""	

	assert type(sensor) is adafruit_fxos8700.FXOS8700
		
	xValues = []
	yValues = []
	zValues = []
	
	while len(xValues) < n:
		xValue, yValue, zValue = sensor.magnetometer
		xValues.append(xValue)
		yValues.append(yValue)
		zValues.append(zValue)
		
	print((sum(xValues)/n, sum(yValues)/n, sum(zValues)/n))
	
	while True:
		xValue, yValue, zValue = sensor.magnetometer
		xValues.append(xValue)
		yValues.append(yValue)
		zValues.append(zValue)
		xValues.pop(0)
		yValues.pop(0)
		zValues.pop(0)
		print((sum(xValues)/n, sum(yValues)/n, sum(zValues)/n))
		
def getSmoothGyro(sensor, n):	
	"""
		Eliminates noise from the gyroscope readings 
		using a moving average with an n-large window, and
		prints out values

		Args:
			sensor: the sensor being read
			n: the number of readings to be averaged

		Returns:
			Nothing

		Raises:
		AssertionError: sensor is not the gyroscope
	"""	

	assert type(sensor) is adafruit_fxas21002c.FXAS21002C
	
	xValues = []
	yValues = []
	zValues = []
	
	while len(xValues) < n:
		xValue, yValue, zValue = sensor.gyroscope
		xValues.append(xValue)
		yValues.append(yValue)
		zValues.append(zValue)
		
	print((sum(xValues)/n, sum(yValues)/n, sum(zValues)/n))
	
	while True:
		xValue, yValue, zValue = sensor.gyroscope
		xValues.append(xValue)
		yValues.append(yValue)
		zValues.append(zValue)
		xValues.pop(0)
		yValues.pop(0)
		zValues.pop(0)
		print((sum(xValues)/n, sum(yValues)/n, sum(zValues)/n))
