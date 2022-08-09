import numpy as np

class AccelDataProcesser:
    def __init__(self, xList, yList, zList, time):
        self.xList = xList 
        self.yList = yList
        self.zList = zList
        self.time = time

    def getTimeAvg(self):
        """Calculates time averaged acceleration of individual vectors"""
        xTimeAvg = []
        xTempList = []
        for x in self.xList:
            xTempList.append(x)
            xTimeAvg.append(np.mean(xTempList))
        
        yTimeAvg = []
        yTempList = []
        for y in self.yList:
            yTempList.append(y)
            yTimeAvg.append(np.mean(yTempList))

        zTimeAvg = []
        zTempList = []
        for z in self.zList:
            zTempList.append(z)
            zTimeAvg.append(np.mean(zTempList))
        
        return xTimeAvg, yTimeAvg, zTimeAvg

    def getMag(self, xTimeAvg, yTimeAvg, zTimeAvg):
        """Calculates magnitude of time averaged acceleration"""
        magList = []
        timeAvgList = list(zip(xTimeAvg, yTimeAvg, zTimeAvg))

        for avg in timeAvgList:
            xAvg = avg[0]
            yAvg = avg[1]
            zAvg = avg[2]

            mag = (xAvg ** 2 + yAvg ** 2 + zAvg ** 2) ** 0.5
            magList.append(mag)
            self.magList = magList

        return magList
    
    def getIntervalAvg(self, minTim, maxTim, magnitudeL):
        """Calculates time averaged acceleration and magnitude for set range of time"""
        #if len(magnitudeL) < maxTim:
            #raise ValueError('Segment includes values that have not been recorded.')

        magSeg = magnitudeL[minTim:maxTim]
        avgMagSeg = np.mean(magSeg)
        stdMagSeg = np.std(magSeg)

        return avgMagSeg, stdMagSeg

    def formatTime(self):
        startTime = self.time[0]
        self.time = [(t - startTime) / 1000 for t in self.time]
        return self.time

def main():
    #Takes input from user to identify which file to process
    innerV = str(int(input('Inner Speed: ')))
    outerV = str(int(input('Outer Speed: ')))
    tNum = str(int(input('Trial Number: ')))

    #Reads data from file and appends x, y, and z values to their specific lists
    pathIn = 'C:\\Users\\jclar\\Documents\\Processing\\Acclerometer_Web_Socket\\'
    inName = innerV + '-' + outerV + '-T' + tNum + '-rawData.txt' 
    data = open(pathIn + inName, 'r')
    
    x = []
    y = []
    z = []
    time = []

    for line in data.readlines():
        lineSplit = line.split('\t')
        if len(lineSplit) == 4:
            x.append(float(lineSplit[0]))
            y.append(float(lineSplit[1]))
            z.append(float(lineSplit[2]))
            time.append(int(lineSplit[3]))

    
    process = AccelDataProcesser(x, y, z, time)

    t = process.formatTime()
    xTimeAvg, yTimeAvg, zTimeAvg = process.getTimeAvg()
    mag = process.getMag(xTimeAvg, yTimeAvg, zTimeAvg)

    print(t[5000], xTimeAvg[5000], yTimeAvg, zTimeAvg, mag[5000])
if __name__ == "__main__":
    main()
