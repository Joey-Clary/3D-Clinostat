from simulation import Sim
from accelDataProcessing import AccelDataProcesser
from pathVisualization import PathVisualization
import numpy as np

class HeatMapGen:
    innerMin = 0.125
    innerMax = 4
    outerMin = 0.125
    outerMax = 4

    vectorSim = Sim()
    magList = []
    distList = []
    mapOut = open('C:\\Users\\jclar\\Desktop\\School\\Clinostat Project\\Frontiers Paper\\Data\\Acceleration\\Simulations\\heatMap_v2.txt', 'w+')
    rankOut = open('C:\\Users\\jclar\\Desktop\\School\\Clinostat Project\\Frontiers Paper\\Data\\Acceleration\\Simulations\\ranking_v2.txt', 'w+') 
    for inV in range(int(innerMin * 8), int(innerMax * 8) + 1):
        magRow = []
        distRow = []
        for outV in range(int(outerMin * 8), int(outerMax * 8) + 1):
            timeArr, xArr, yArr, zArr = vectorSim.gVectorData(0, 10000, float(inV)/8, float(outV)/8)
            process = AccelDataProcesser(xArr, yArr, zArr, timeArr)
            xTimAvg, yTimAvg, zTimAvg = process.getTimeAvg()

            magArr = []
            for i in range(len(xTimAvg)):
                curX = xTimAvg[i]
                curY = yTimAvg[i]
                curZ = zTimAvg[i]
                curMag = (curX**2 + curY**2 + curZ**2)**0.5
                magArr.append(curMag)
            
            magRow.append(np.mean(magArr[5000:6000]))

            id = str(inV) + ":" + str(outV)
            pathVis = PathVisualization(id, xArr, yArr, zArr)
            distRow.append(pathVis.getDistribution())
            print(id)
        magList.append(magRow)
        distList.append(distRow)
        magRow = []
        distRow = []
    print(magList)
    print(distList)

    mapOut.write("Magnitude\n")
    for rowI in range(len(magList)):
        for colI in range(len(magList)):
            mapOut.write(str(magList[rowI][colI]) + "\t")
        mapOut.write("\n")
    
    mapOut.write("\Distribution\n")
    for rowI in range(len(distList)):
        for colI in range(len(distList)):
            mapOut.write(str(distList[rowI][colI]) + "\t")
        mapOut.write("\n")

    mapOut.close()

    rankOut.write("Combination\tMagnitude\Distribution\n")
    for rowI in range(len(magList)):
        for colI in range(len(magList)):
            inV = float(rowI + 1) / 8
            outV = float(colI + 1) / 8
            id = str(inV) + ":" + str(outV) + "\t"
            rankOut.write(id + str(magList[rowI][colI]) + "\t" + str(distList[rowI][colI]) + "\n")
    rankOut.close()
