import os
import sys
import numpy as np
from pathVisualization import PathVisualization
from simulation import Sim

class DataProcessor:
    def __init__(self):
        #Uncomment machine type based on data source
        self.machineType = "sim"
        #self.machineType = "clinostat"
        #self.machineType = "rpm-integ"
        #self.machineType = "rpm-ard"

        #Set range for average magnitude (seconds)
        self.minSeg = 2000
        self.maxSeg = 3000 

        #Set data output path
        outParent = "C:\\FILEPATH\\" #SET OUTPUT FILE PATH

        if self.machineType != "sim": 
            self.inPath =  "C:\\FILEPATH\\" #SET INPUT FILE PATH 
            self.inName = "FILENAME.txt" #SET FILE NAME

            try:
                testOpen = open(self.inPath + self.inName, "r")
                testOpen.close()
            except FileNotFoundError:
                print("\nERROR: Input file not found: " + self.inPath + self.inName + "\n")
                sys.exit()
            if self.machineType != "sim":
                self.outPath = outParent + self.inName[:len(self.inName)-4] + "\\"
            else:
                self.outPath = outParent + self.inName + "\\"
            print(self.outPath)
        else: #Applies only for Computer Model
            self.innerV = 1.5 #SET INNER VELOCITY
            self.outerV = 3.875 #SET OUTER VELOCITY
            self.inName = str(self.innerV) + "-" + str(self.outerV)
            self.outPath = outParent + self.inName + "\\"

        if os.path.isdir(self.outPath) == False:
            os.makedirs(self.outPath)

    def outputDataFile(self):
        """Outputs processed data file"""
        self.__getVectors()
        xTimeAvg, yTimeAvg, zTimeAvg = self.__getTimeAvg()
        magList = self.__getMagnitude(xTimeAvg, yTimeAvg, zTimeAvg)
        avgMagSeg = self.__getMagSeg(magList)
        disScore = self.__getDisScore()

        fileOut = open(self.outPath + 'processedAccelData.txt', 'w+')
    
        if self.machineType != 'sim':
            fileOut.write(self.inName)
        else:
            fileOut.write('Inner: ' + str(self.innerV) + '\t' + 'Outer: ' + str(self.outerV) + '\n')

        fileOut.write('Segment: ' + str(self.minSeg) + ":" + str(self.maxSeg) + '\t' + str(avgMagSeg) + '\t' + '\t\t\t' + 'Dispersion: ' + '\t' + str(disScore) +'\n')
        fileOut.write('Time' + '\t' + 'X Vector' + '\t' + 'Y Vector' + '\t' + 'Z Vector' + '\t' + 'X Time Avg' + '\t' + 'Y Time Avg' + '\t' + 'Z Time Avg' + '\t' + 'Magnitude' + '\n')

        for i in range(len(self.x)):
            fileOut.write(str(self.time[i]) + '\t' + str(self.x[i]) + '\t' + str(self.y[i]) + '\t' + str(self.z[i]) + '\t' + str(xTimeAvg[i]) + '\t' + str(yTimeAvg[i]) + '\t' + str(zTimeAvg[i]) + '\t' + str(magList[i]) + '\n')
        
        fileOut.close()

        print("Average Magnitude: " + str(avgMagSeg))
        print("Distribution: " + str(disScore))

    def __getVectors(self):
        """Directs where to get data from"""
        if self.machineType == 'sim':
            self.time, self.x, self.y, self.z = self.__getSimAccelData()
        elif self.machineType == 'clinostat' or self.machineType == 'rpm-ard':
            self.time, self.x, self.y, self.z = self.__getArdAccelData()
        else:
            self.time, self.x, self.y, self.z = self.__getRPMAccelData()

    def __getArdAccelData(self):
        """Reads data from file formatted by the Arduino UNO Accelerometer"""
        dataIn = open(self.inPath + self.inName, 'r')
    
        x, y, z, time = [], [], [], []
        for line in dataIn.readlines():
            lineSplit = line.split('\t')
            if len(lineSplit) == 4:
                x.append(float(lineSplit[0]))
                y.append(float(lineSplit[1]))
                z.append(float(lineSplit[2]))
                unTime = float(lineSplit[3]) / 1000
                time.append(unTime)
        
        dataIn.close()
        return time, x, y, z

    def __getRPMAccelData(self):
        """Reads data from file formatted by the RPM 2.0"""
        dataIn = open(self.inPath + self.inName, 'r')

        x, y, z, time = [], [], [] ,[]
        for line in dataIn.readlines():
            lineFirstSplit = line.split('\t')
            splitVectors = lineFirstSplit[1]
            vectorList = splitVectors.split('   ')
        
            x.append(float(vectorList[0]))
            z.append(float(vectorList[1]))
            y.append(float(vectorList[2]))

        for i in range(len(x)):
            time.append(i)
        
        dataIn.close()
        return time, x, y, z

    def __getSimAccelData(self):
        """Gets data from computer model"""
        simInnerV = float(self.innerV)
        simOuterV = float(self.outerV)
        vectorSim = Sim()
        time, x, y, z = vectorSim.gVectorData(0, self.maxSeg, simInnerV, simOuterV)
        return time, x, y, z

    def __getTimeAvg(self):
        """Calculates Time Average"""
        xTimeAvg = []
        xTempList = []
        for xIter in self.x:
            xTempList.append(xIter)
            xTimeAvg.append(np.mean(xTempList))
        
        yTimeAvg = []
        yTempList = []
        for yIter in self.y:
            yTempList.append(yIter)
            yTimeAvg.append(np.mean(yTempList))

        zTimeAvg = []
        zTempList = []
        for zIter in self.z:
            zTempList.append(zIter)
            zTimeAvg.append(np.mean(zTempList))
        
        return xTimeAvg, yTimeAvg, zTimeAvg

    def __getMagnitude(self, xTimeAvg, yTimeAvg, zTimeAvg):
        """Calculates magnitude of time-averaged acceleration vector"""
        magList = []

        for i in range(len(self.x)):
            xIter = xTimeAvg[i]
            yIter = yTimeAvg[i]
            zIter = zTimeAvg[i]

            mag = (xIter ** 2 + yIter ** 2 + zIter ** 2) ** 0.5
            magList.append(mag)

        return magList
    
    def __getMagSeg(self, magList):
        """Calculates avergae magnitude between segmentd"""
        magSegList = magList[self.minSeg:self.maxSeg]
        if len(magList) < self.minSeg:
            print("\nERROR: Segment begins after data ends - " + str(len(magList)) + " sec\n")
            sys.exit()
        elif len(magSegList) < (self.maxSeg - self.minSeg):
            print("\nWARNING: Not enough data for segment - " + str(len(magList)) + " sec\n")
        return np.mean(magList[self.minSeg:self.maxSeg])
    
    def __getDisScore(self):
        xSeg = self.x[:self.maxSeg]
        ySeg = self.y[:self.maxSeg]
        zSeg = self.z[:self.maxSeg]
        path = PathVisualization(self.inName, xSeg, ySeg, zSeg)
        disScore = path.getDistribution()

        return disScore

    def copyRawData(self):
        if self.machineType == "sim":
            print("\nWARNING: Machine Type = Sim - No files were copied\n")
            return
        dataIn = open(self.inPath + self.inName, 'r')
        copyData = open(self.outPath + self.inName[:len(self.inName)-4] + '-Copy' + self.inName[len(self.inName)-4:], 'w+')

        copyData.write(self.inPath + self.inName + '\n\n')
        
        for line in dataIn.readlines():
            copyData.write(line)

        copyData.close()
        dataIn.close()
    
    def createGraphs(self):
        self.__getVectors()
        xTimeAvg, yTimeAvg, zTimeAvg = self.__getTimeAvg()
        magnitude = self.__getMagnitude(xTimeAvg, yTimeAvg, zTimeAvg)

        if self.machineType != 'sim':
            graphPath = PathVisualization(self.inName, self.x, self.y, self.z, saveFile=self.outPath + self.inName[:len(self.inName)-4])
        else:
            graphPath = PathVisualization(self.inName, self.x, self.y, self.z, saveFile=self.outPath + self.inName)
        
        graphPath.createPathShadowFig(mode='save', legend=False)

        graphPath.createVectorFig(self.time, mode='save')
        graphPath.createTimeAvgFig(xTimeAvg, yTimeAvg, zTimeAvg, self.time, mode='save')
        graphPath.createMagFig(magnitude, self.time, mode='save')
        
    def createSegGraphs(self):
        self.__getVectors()
        xSeg = self.x[2000:self.maxSeg]
        ySeg = self.y[2000:self.maxSeg]
        zSeg = self.z[2000:self.maxSeg]

        if self.machineType != 'sim':
            comparePaths = PathVisualization(self.inName, xSeg, ySeg, zSeg, saveFile=self.outPath + self.inName[:len(self.inName)-4] + '-Segment')
        else: 
            comparePaths = PathVisualization(self.inName, xSeg, ySeg, zSeg, saveFile=self.outPath + self.inName + '-Segment')
        comparePaths.createPathFig(mode='save')

if __name__ == "__main__":
    process = DataProcessor()
    process.outputDataFile()
    process.createGraphs()
    process.createSegGraphs()
    process.copyRawData()

