# import stuff
import numpy as np
from matplotlib import pyplot as plt

# constants
minute = 60
second = 60
totalTimeSun = 15 # in hours
totalTimeDark = 24 - totalTimeSun # full day
angularRate = 180/totalTimeSun
runTime = 3 # time to run each thing
flatSatCurrent = 0.68
stressberryCurrent = 1
idleCurrent = 0.5
piV = 5.1 # voltage of the pi
solarV = 5.7 # voltage of the solar panel
batteryV = 5 # voltage of the battery
pi3Idle = 1.4

# Data from lab

# Function of power vs angle - measured
angleList = np.asarray([90,70,45,22.5,0])
angleListMod = angleList + 60
powerList = np.asarray([0.065,0.057,0.074,0.075,0.038])

# Function of power vs angle - guessed - should take this from the hardware docs
angleList_nice = np.asarray([0,40,90])
timeList_nice = angleList_nice/angularRate # time in hours
powerList_nice = np.asarray([0,0.04,0.075])*solarV # in watts (solar panel voltage times current)

# Plot power as function of angle to sun
# shift data by the angle the sun was at
plt.title("Power vs Angle (measured)")
plt.xlabel("Angle (degrees)")
plt.ylabel("Power (Watts)")
plt.plot(angleListMod,powerList)
plt.plot(angleList_nice,powerList_nice)
# plt.show()



# Power budget at 90 degrees
dayPowerGenerated = 2*np.trapz(powerList_nice,timeList_nice)# integrate - in amp hours
startPower = 10*batteryV # in amp hours (= 10000 mAhr)
powerUsed = flatSatCurrent*piV*runTime + stressberryCurrent*piV*runTime + idleCurrent*piV*(totalTimeSun - 2*runTime + totalTimeDark)
print(dayPowerGenerated)
print(powerUsed)
endPower = startPower + dayPowerGenerated - powerUsed
print(endPower)

# Power budget with solar tracking (pi 3)
dayPowerGenerated = 2*np.trapz(powerList_nice,timeList_nice)# integrate - in amp hours
startPower = 10*batteryV # in amp hours (= 10000 mAhr)
powerUsed = pi3Idle*runTime + stressberryCurrent*piV*runTime + pi3Idle*(totalTimeSun - 2*runTime + totalTimeDark)
print(dayPowerGenerated)
print(powerUsed)
endPower = startPower + dayPowerGenerated - powerUsed
print(endPower)





# Power budget with solar tracking
dayPowerGenerated = 0.075*solarV*totalTimeSun# integrate - in amp hours
startPower = 10*batteryV # in amp hours (= 10000 mAhr)
powerUsed = flatSatCurrent*piV*runTime + stressberryCurrent*piV*runTime + idleCurrent*piV*(totalTimeSun - 2*runTime + totalTimeDark)
print(dayPowerGenerated)
print(powerUsed)
endPower = startPower + dayPowerGenerated - powerUsed
print(endPower)


# Power budget with solar tracking (pi 3)
dayPowerGenerated = 0.075*solarV*totalTimeSun# integrate - in amp hours
startPower = 10*batteryV # in amp hours (= 10000 mAhr)
powerUsed = pi3Idle*runTime + stressberryCurrent*piV*runTime + pi3Idle*(totalTimeSun - 2*runTime + totalTimeDark)
print(dayPowerGenerated)
print(powerUsed)
endPower = startPower + dayPowerGenerated - powerUsed
print(endPower)


