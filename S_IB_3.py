import numpy as np
from scipy import spatial
import math, sys, os

sim = sys.argv[1]
neighThres = sys.argv[2]       # minimum number of ST neighbors threshold

#spatiotemporal domain
xmin, xmax, ymin, ymax = 323000, 337300, 369100, 387700

#spatiotemporal resolution
xyRes, tRes = 100, 1
xyResHalf = xyRes/2.0

# function to convert coordinates to index for inArr
#--------------------------------------------------------------------------------------
def coordToIndex(x,y):

    xindex1 = int((x-xmin) / xyRes)
    if x%xyRes < xyResHalf:
        xIndex2 = xindex1
    else:
        xIndex2 = xindex1 + 1

    yindex1 = int((y-ymin) / xyRes)
    if y%xyRes < xyResHalf:
        yIndex2 = yindex1
    else:
        yIndex2 = yindex1 + 1

    return [xIndex2, yIndex2]

#--------------------------------------------------------------------

# ST Kernel density estimation
#--------------------------------------------------------------------------------------
def densityF(x, y, xi, yi, hs):
    u = (x-xi) / hs
    v = (y-yi) / hs
    Ks = 1 - pow(u, 2) - pow(v, 2)
    return Ks

#--------------------------------------------------------------------

#number of points in each dimension
xDim = int((xmax - xmin)/xyRes)  
yDim = int((ymax - ymin)/xyRes)  

#load regular grid: 3d grid of tuples: (x, y, nCount, pCount, ds)
fullGridArr = np.load('outputs/S_IB_2/sim_' + sim + os.sep + 'fullGrid_' + neighThres + '.npy')

#------------------------------------------------
## read file containing case coordinates and bandwidths
## for each case, find spatiotemporal grid point neighbors and compute risk contribition

inDir = 'outputs/S_IB_2' + os.sep + 'sim_' + sim
disFile = open(inDir + os.sep + 'peopleTime_' + neighThres + '.txt','r')

rCount = 0
for record in disFile:
    line = record.split(',')
	#coordinates of case point, bandwidths, population within kernel
    xC, yC, hs, pop = float(line[1]),float(line[2]),float(line[3]),float(line[4])

	#query point
    cIndex = coordToIndex(xC, yC)
    qX, qY = cIndex[0],cIndex[1]  #query point index
    sDeg = int(hs / xyRes)
   
    #how many case points in pixel?
    if (qX < xDim and qX >= 0) and (qY < yDim and qY >= 0):
        fullGridArr[qX][qY][2] += 1

	#find neighboring grid points
	count = 0

    for i in range(qX-sDeg,qX+sDeg+1):
        if i < xDim and i >= 0:
            for j in range(qY-sDeg,qY+sDeg+1):
                if j < yDim and j >= 0:

                    nX, nY = fullGridArr[i][j][0], fullGridArr[i][j][1]

                    #compute distance between neighbor and query point
                    sDist = pow(pow(xC-nX,2)+pow(yC-nY,2),0.5)

                    #if distance smaller than bandwidth
                    if sDist <= hs:

                        #compute density contribution
                        KDE = densityF(xC, yC, nX, nY, hs)
                        #print KDE/pop
                        fullGridArr[i][j][4] += KDE / (pop+1)
                       
    rCount += 1

disFile.close()

#initialize output array
nRows = xDim * yDim
nCols = 6   #columns ID, x, y, nCount, pCount, Ks
outArr = np.zeros((nRows,nCols))

ID = 0
xIndex = 0
while xIndex < xDim:
    yIndex = 0
    while yIndex < yDim:
        outArr[ID][0] = ID                                      #id
        outArr[ID][1] = fullGridArr[xIndex][yIndex][0]        #x
        outArr[ID][2] = fullGridArr[xIndex][yIndex][1]        #y
        outArr[ID][3] = fullGridArr[xIndex][yIndex][2]     #nCount
        outArr[ID][4] = fullGridArr[xIndex][yIndex][3]     #pCount
        outArr[ID][5] = fullGridArr[xIndex][yIndex][4]     #s-density Ks
        
        ID += 1
        yIndex += 1
    xIndex += 1

#scale Ks to 0-1

outArr[:,5]= outArr[:,5]/max(outArr[:,5])

# create directory
outDir = 'outputs/S_IB_3/sim_' + sim
if not os.path.exists(outDir):
    os.makedirs(outDir)

outFile = open(outDir + os.sep + 'density_' + neighThres + '.txt','w')

for i in outArr:
    if i[1] == 0 and i[2] == 0:
        pass
    else:
        #write[x,y,nCount,pCount,density]
        outFile.write(str(i[1]) + ',' + str(i[2]) + ',' + str(i[3]) + ',' + str(i[4]) + ',' + str(i[5]) + '\n')

outFile.close()
