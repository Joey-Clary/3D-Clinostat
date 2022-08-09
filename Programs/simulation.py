import math

class Sim:
    #Returns x-component of the G vector at a specific time for a specific inner and outer frame angular velocities
    def gVectorX(self, timeInSeconds, localInnerInRadSec, localOuterInRadSec):
        ret = math.sin(localOuterInRadSec*timeInSeconds)*math.cos(localInnerInRadSec*timeInSeconds)
        return ret
    #Returns z-component of the G vector at a specific time for a specific outer frame angular velocity
    def gVectorY(self, timeInSeconds, localOuterInRadSec):
        ret = math.cos(localOuterInRadSec*timeInSeconds)
        return ret
    #Returns y-component of the G vector at a specific time for a specific inner and outer frame angular velocities
    def gVectorZ(self, timeInSeconds, localInnerInRadSec, localOuterInRadSec):
        ret = math.sin(localOuterInRadSec*timeInSeconds)*math.sin(localInnerInRadSec*timeInSeconds)
        return ret

    #Converts and returns frame velocity from RPM to radians per second
    def RPMtoRadSec(self, RPM):
        ret = RPM * (math.pi / 30)
        return ret

    #Returns a Python dictionary containing value of g vector of each axis at specific times
    def gVectorData(self, startTimeInSeconds, endTimeInSeconds, innerRPM, outerRPM):
        innerInRadSec = self.RPMtoRadSec(innerRPM)
        outerInRadSec = self.RPMtoRadSec(outerRPM)
        timeArray, xArray, yArray, zArray = [], [], [], []
        for t in range(startTimeInSeconds, endTimeInSeconds + 1):
            timeArray.append(t)
            xArray.append(self.gVectorX(t, innerInRadSec, outerInRadSec))
            yArray.append(self.gVectorY(t, outerInRadSec))
            zArray.append(self.gVectorZ(t, innerInRadSec, outerInRadSec))
        data = timeArray, xArray, yArray, zArray
        return data
