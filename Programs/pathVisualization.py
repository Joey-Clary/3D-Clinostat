import numpy as np
import matplotlib.pyplot as plt
import matplotlib.cm as cm
from mpl_toolkits.mplot3d import Axes3D

class PathVisualization:
    def __init__(self, ID, x, y, z, saveFile=''):
        self.ID = ID

        self.x = x
        self.y = y
        self.z = z

        self.pathCoords = list(zip(self.x, self.y, self.z))
        self.num_points = 1000

        self.saveFile = saveFile

    def __createSphere(self):
        """creates guide sphere with fibonnaci sequence on same plot as path"""
        golden_r = (np.sqrt(5.0) + 1.0) / 2.0            #golden ratio = 1.61803...
        golden_a = (2.0 - golden_r) * (2.0 * np.pi)      #golden angle + 2.39996...

        Xs, Ys, Zs = [], [], []
        
        for i in range(self.num_points):
            ys = 1 - (i / float(self.num_points - 1)) * 2
            radius = np.sqrt(1 - ys * ys)

            theta = golden_a * i

            xs = np.cos(theta) * radius
            zs = np.sin(theta) * radius

            Xs.append(xs)
            Ys.append(ys)
            Zs.append(zs)

        return(Xs, Ys, Zs)

    def __splitSphere(self, sphereCoords):
        octants = {'posI':[], 'posII':[], 'posIII':[], 'posIV':[], 'negI':[], 'negII':[], 'negIII':[], 'negIV':[]}
        
        for row in sphereCoords:
            #Coordinates: x = row[0], y = row[1], z = row[2]
            if (row[2] > 0):
                if (row[1] > 0):
                    if (row[0] > 0):
                        octants['posI'].append(row)
                    else:
                        octants['posII'].append(row)
                elif (row[0] > 0):
                    octants['posIV'].append(row)
                else: 
                    octants['posIII'].append(row)
            else:
                if (row[1] > 0):
                    if (row[0] > 0):
                        octants['negI'].append(row)
                    else:
                        octants['negII'].append(row)
                elif (row[0] > 0):
                    octants['negIV'].append(row)
                else:
                    octants['negIII'].append(row)
        
        return(octants)

    def __getPathOctant(self, pathRow):
        """"Checks what quadrant the tuple of coordinates is in"""
        if (pathRow[2] > 0):
            if (pathRow[1] > 0):
                if (pathRow[0] > 0):
                    return 'posI'
                else:
                    return 'posII'
            elif (pathRow[0] > 0):
                return 'posIV'
            else: 
                return 'posIII'
        else:
            if (pathRow[1] > 0):
                if (pathRow[0] > 0):
                    return 'negI'
                else:
                    return 'negII'
            elif (pathRow[0] > 0):
                return 'negIV'
            else:
                return 'negIII'

    def __getDistanceBetween(self, pathTupleCoords, sphereTupleCoords):
        """Calculates distance between two points (path point and sphere point"""
        pathX, pathY, pathZ = pathTupleCoords
        sphereX, sphereY, sphereZ = sphereTupleCoords

        diffX = pathX - sphereX
        diffY = pathY - sphereY
        diffZ = pathZ - sphereZ

        sumSquares = diffX ** 2 + diffY ** 2 + diffZ ** 2
        dist = np.sqrt(sumSquares)

        return dist

    def __getDistributionNum(self, sphereCoords):
        """Creates a dictionary of the three sphere coords that are closest to each path coord.
        The length of this dictionary will be the distribution score assigned to the combination.
        A higher distribution score means the path of the combination will better cover the entire sphere,
        thus the average orientation will be closer to zero and create a better simulation."""
        octants = self.__splitSphere(sphereCoords) #splits spheres into octants and returns dictionary with each octant separated
        
        #Every time the path passes between a new segment, the three vertices are added as keys. 
        #The value is a list of the indexes of the pathCoords to denote the how long it takes to repeat the entire path
        pathMap = {} 
        repeatTime = -1

        for pathRow in self.pathCoords:
            pathOctant = self.__getPathOctant(pathRow) #determines what octant this set of path coordinates is in
            sphereCoordsSplit = octants[pathOctant] #retrieves sphere coordinates in the octant that this set of path coordinates is in
            distDict = {}
            repeatTime += 1

            for sphereRow in sphereCoordsSplit:
                dist = self.__getDistanceBetween(pathRow, sphereRow) #gets distance between two points
                distDict[sphereRow] = dist #Updates dictionary (key:sphere coordinates, value: distance between path coordinate and that sphere coordinate)
                    
            rankedDist = sorted(distDict.items(), key=lambda x:x[1]) #takes dictionary of distances, sorts them, and makes it into a list of tuples
            segmentVertices = (rankedDist[0][0], rankedDist[1][0], rankedDist[2][0]) #the three closest sphere coordinates are the vertices of the segment that the path coordinate is in
            
            pathMap[segmentVertices] = pathMap.get(segmentVertices, []) + [repeatTime] # If the path has not passed through this segment, it creates a key and assigns the value as the first time the path passed through the segment
        
        return(len(pathMap))

    def getDistribution(self):
        #get sphere coords
        Xsphere, Ysphere, Zsphere = self.__createSphere()
        sphereCoords = list(zip(Xsphere, Ysphere, Zsphere))
        score = self.__getDistributionNum(sphereCoords)
        return score

    """
    Distribution Figure Types:
        Distribution     --> Shadow
        createPathFig       --> Path
        createSphereFig     --> Points
        createPathShadowFig --> Path, Shadow
        createCombinedFig   --> Path, Shadow, Points
    """
    def createPathShadowFig(self, mode='save', separated = False, title = True, legend = True):
        disScore = self.getDistribution()
        legTitle = 'Distribution: ' + str(disScore)
        if separated:
            fig = plt.figure(figsize=plt.figaspect(0.4)) #Separates Shadow and Path
            plt.xlim(-1.0, 1.0)
            plt.ylim(-1.0, 1.0)

            if title:
                fig.suptitle(self.ID + '  --  ' + 'Path and Shadow')

            ax = fig.add_subplot(1, 2, 1, projection='3d') 
            ax.plot(self.x, self.y, self.z, label = "Acceleration Vector Path", linewidth = 1) #Plots Path
            ax.legend()
            
            ax = fig.add_subplot(1, 2, 2, projection='3d')
            ax.plot(self.x, self.y, zs=-1, zdir='z', label='Projection in (x,y)') #Plots Shadow on x,y plane
            ax.plot(self.x, self.z, zs=1, zdir='y', label='Projection in (x,z)')  #Plots Shadow on x,z plane
            ax.plot(self.y, self.z, zs=-1, zdir='x', label='Projection in (y,z)') #Plots Shadow on y,z plane
            

            if legend:
                ax.legend(title=legTitle, loc='lower left')
            
        else:
            fig = plt.figure(figsize=plt.figaspect(0.85))
            plt.xlim(-1.0, 1.0)
            plt.ylim(-1.0, 1.0)

            if title:
                fig.suptitle(self.ID + '  --  ' + 'Path and Shadow')

            ax = fig.add_subplot(1, 1, 1, projection='3d') #Combines Shadow and Path (default)
            ax.plot(self.x, self.y, self.z, label = "Acceleration Vector Path", linewidth = 1) #Plots Path
            ax.plot(self.x, self.y, zs=-1, zdir='z', alpha = 0.3, label='Projection in (x,y)') #Plots Shadow on x,y plane
            ax.plot(self.x, self.z, zs=1, zdir='y', alpha = 0.3, label='Projection in (x,z)')  #Plots Shadow on x,z plane
            ax.plot(self.y, self.z, zs=-1, zdir='x', alpha = 0.3, label='Projection in (y,z)') #Plots Shadow on y,z plane
            
            if legend:
                ax.legend(title=legTitle, loc='lower left')
        
        if mode == 'save': 
            plt.savefig(self.saveFile + '-path.png')
        elif mode == 'show':
            plt.show()
        else:
            plt.savefig(self.saveFile + '-path.png')
            plt.show()
    
    def createCombinedFig(self, mode='save', separated = False, title = True, legend = True):
        pointSize = np.ones(self.num_points) * 2
        Xsphere, Ysphere, Zsphere = self.__createSphere()

        if separated:
            fig = plt.figure(figsize=plt.figaspect(0.4)) #Separates Shadow and Path
            plt.xlim(-1.0, 1.0)
            plt.ylim(-1.0, 1.0)

            if title:
                fig.suptitle(self.ID + '  --  ' + 'Combined')

            ax = fig.add_subplot(1, 2, 1, projection='3d')
            ax.scatter(Xsphere, Ysphere, Zsphere, s = pointSize, color = 'orange')  #Plots Sphere points
            ax.plot(self.x, self.y, self.z, label = "Acceleration Vector Path", linewidth = 1) #Plots Path
            
            if legend:
                ax.legend()
            
            ax = fig.add_subplot(1, 2, 2, projection='3d')
            ax.plot(self.x, self.y, zs=-1, zdir='z', label='Projection in (x,y)') #Plots Shadow on x,y plane
            ax.plot(self.x, self.z, zs=1, zdir='y', label='Projection in (x,z)')  #Plots Shadow on x,z plane
            ax.plot(self.y, self.z, zs=-1, zdir='x', label='Projection in (y,z)') #Plots Shadow on y,z plane
            
            if legend:
                ax.legend()
            
        else:
            fig = plt.figure(figsize=plt.figaspect(0.85))
            plt.xlim(-1.0, 1.0)
            plt.ylim(-1.0, 1.0)

            if title:
                fig.suptitle(self.ID + '  --  ' + 'Combined')

            ax = fig.add_subplot(1, 1, 1, projection='3d') #Combines Shadow and Path (default)
            ax.scatter(Xsphere, Ysphere, Zsphere, s = pointSize, color = 'goldenrod') #Plots Sphere points
            ax.plot(self.x, self.y, self.z, label = "Acceleration Vector Path", linewidth = 1) #Plots Path
            #ax.plot(self.x, self.y, zs=-1, zdir='z', alpha = 0.3, label='Projection in (x,y)') #Plots Shadow on x,y plane
            #ax.plot(self.x, self.z, zs=1, zdir='y', alpha = 0.3, label='Projection in (x,z)')  #Plots Shadow on x,z plane
            #ax.plot(self.y, self.z, zs=-1, zdir='x', alpha = 0.3, label='Projection in (y,z)') #Plots Shadow on y,z plane
            
            if legend:
                ax.legend()
        
        if mode == 'save': 
            plt.savefig(self.saveFile + '-combinedPathSphere.png')
        elif mode == 'show':
            plt.show()
        else:
            plt.savefig(self.saveFile + '-combinedPathSphere.png')
            plt.show()
        
    def createSphereFig(self, mode='save', title = True): 
        fig = plt.figure(figsize=plt.figaspect(0.85))
        plt.xlim(-1.0, 1.0)
        plt.ylim(-1.0, 1.0)

        if title:
            fig.suptitle("Number of Points: " + str(self.num_points)) 

        ax = fig.add_subplot(1, 1, 1, projection='3d') 

        pointSize = np.ones(self.num_points) * 2
        Xsphere, Ysphere, Zsphere = self.__createSphere()
        ax.scatter(Xsphere, Ysphere, Zsphere, s = pointSize, color = 'goldenrod')

        if mode == 'save': 
            plt.savefig(self.saveFile + '-sphere.png')
        elif mode == 'show':
            plt.show()
        else:
            plt.savefig(self.saveFile + '-sphere.png')
            plt.show()
    
    def createShadowFig(self, mode='save', title = True, legend = True):
        fig = plt.figure(figsize=plt.figaspect(0.85))
        plt.xlim(-1.0, 1.0)
        plt.ylim(-1.0, 1.0)

        if title:
            fig.suptitle(self.ID + '  --  ' + 'Shadow')

        ax = fig.add_subplot(1, 1, 1, projection='3d')
        ax.plot(self.x, self.y, zs=-1, zdir='z', label='Projection in (x,y)') #Plots Shadow on x,y plane
        ax.plot(self.x, self.z, zs=1, zdir='y', label='Projection in (x,z)')  #Plots Shadow on x,z plane
        ax.plot(self.y, self.z, zs=-1, zdir='x', label='Projection in (y,z)') #Plots Shadow on y,z plane
        
        if legend:
            ax.legend()
        
        if mode == 'save': 
            plt.savefig(self.saveFile + '-shadowFig.png')
        elif mode == 'show':
            plt.show()
        else:
            plt.savefig(self.saveFile + '-shadowFig.png')
            plt.show()

    def createPathFig(self, mode='save', title = True):
        fig = plt.figure(figsize=plt.figaspect(0.85))
        plt.xlim(-1.0, 1.0)
        plt.ylim(-1.0, 1.0)

        if title:
            fig.suptitle(self.ID + '  --  ' + 'Path')

        ax = fig.add_subplot(1, 1, 1, projection='3d')
        ax.plot(self.x, self.y, self.z, label = "Acceleration Vector Path", linewidth = 1) #Plots Path

        if mode == 'save': 
            plt.savefig(self.saveFile + '-pathFig.png')
        elif mode == 'show':
            plt.show()
        else:
            plt.savefig(self.saveFile + '-pathFig.png')
            plt.show()

    """'
    Acceleration Figure Types:
    createVectorFig  --> Figure with individual graphs of x, y, and z raw accel values over time
    createTimeAvgFig --> Figure with individual graphs of time averages of x, y, and z over time
    createMagFig     --> Figure with magnitude over time
    """

    def formatTime(self, time):
        startTime = time[0]
        fTime = []
        for t in time:
            fTime.append(t - startTime)
        return fTime

    def createVectorFig(self, time, mode='save', title=True):
        #fTime = self.formatTime(time)

        #Plot X Vector
        fig = plt.figure()
        ax = fig.add_subplot(1, 1, 1)
        ax.plot(time, self.x)
        
        if title:
            fig.suptitle(self.ID + '  --  ' + 'X Vector')

        if mode == 'save': 
            plt.savefig(self.saveFile + '-XvectorFig.png')
        elif mode == 'show':
            plt.show()
        else:
            plt.savefig(self.saveFile + '-XVectorFig.png')
            plt.show()
        
        #Plot Y Vector
        fig = plt.figure()
        ax = fig.add_subplot(1, 1, 1)
        ax.plot(time, self.y)
        
        if title:
            fig.suptitle(self.ID + '  --  ' + 'Y Vector')

        if mode == 'save': 
            plt.savefig(self.saveFile + '-YVectorFig.png')
        elif mode == 'show':
            plt.show()
        else:
            plt.savefig(self.saveFile + '-YVectorFig.png')
            plt.show()
        
        #Plot Z Vector
        fig = plt.figure()
        ax = fig.add_subplot(1, 1, 1)
        ax.plot(time, self.z)
        
        if title:
            fig.suptitle(self.ID + '  --  ' + 'Z Vector')

        if mode == 'save': 
            plt.savefig(self.saveFile + '-ZvectorFig.png')
        elif mode == 'show':
            plt.show()
        else:
            plt.savefig(self.saveFile + '-ZvectorFig.png')
            plt.show()
    
    def createTimeAvgFig(self, xTimeAvg, yTimeAvg, zTimeAvg, time, mode='save', legend=True, title=True):
        fTime = self.formatTime(time)

        fig = plt.figure()
        ax = fig.add_subplot(1, 1, 1)
        #plt.yscale('log')

        if title:
            fig.suptitle(self.ID + '  --  ' + 'Time Average')

        ax.plot(fTime, xTimeAvg, label='X')
        ax.plot(fTime, yTimeAvg, label='Y')
        ax.plot(fTime, zTimeAvg, label='Z')
        
        if legend:
            ax.legend()
        
        if mode == 'save': 
            plt.savefig(self.saveFile + '-timeAvgFig.png')
        elif mode == 'show':
            plt.show()
        else:
            plt.savefig(self.saveFile + '-timeAvgFig.png')
            plt.show()

    def createMagFig(self, magnitude, time, mode='save', title=True):
        fTime = self.formatTime(time)

        fig = plt.figure()
        ax = fig.add_subplot(1, 1, 1)
        plt.yscale('log')

        if title:
            fig.suptitle(self.ID + '  --  ' + 'Magnitude')

        ax.plot(fTime, magnitude)

        if mode == 'save': 
            plt.savefig(self.saveFile + '-timeMagFig.png')
        elif mode == 'show':
            plt.show()
        else:
            plt.savefig(self.saveFile + '-timeMagFig.png')
            plt.show()
