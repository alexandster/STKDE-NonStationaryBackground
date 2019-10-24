#ST_IB_3.py, by Alexander Hohl
#This script computes ST-IB based on kernel bandwidths (from ST_IB_1.py) and population within kernel (from ST_IB_2.py)

import numpy as np
from scipy import spatial
import math, sys, os

sim = sys.argv[1]			#simulation 0-99
neighThres = sys.argv[2]       # minimum number of ST neighbors threshold

#------------------------------------------------
#points_obs spatiotemporal envelope (domain)
xmin, xmax, ymin, ymax, tmin, tmax = 322896.6389, 337268.7369, 368748.6975, 387824.4062, 3, 658

# spatial and temporal resolution of output grid
xyRes, tRes = 100, 1
xyResHalf = xyRes/2.0

#------------------------------------------------

# function to convert coordinates to index for inArr
#--------------------------------------------------------------------------------------
def coordToIndex(x,y,t):

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

    tIndex2 = int(t)-tmin
    return [xIndex2, yIndex2, tIndex2]

#--------------------------------------------------------------------

# ST Kernel density estimation
#--------------------------------------------------------------------------------------
def densityF(x, y, t, xi, yi, ti, hs, ht):
    u = (x-xi) / hs
    v = (y-yi) / hs
    w = (t-ti) / ht
    Ks = 1 - pow(u, 2) - pow(v, 2)
    Kt = 1 - pow(w, 2)
    STKDE = [Ks,Kt]
    return STKDE

#--------------------------------------------------------------------

#number of points in each dimension
xDim = int((xmax - xmin)/xyRes)  
yDim = int((ymax - ymin)/xyRes)  
tDim = int((tmax - tmin)/tRes)  

#load regular grid: 3d grid of tuples: (x, y, t, nCount, pCount, ds, dt)
fullGridArr = np.load('outputs/ST_IB_2/sim_' + sim + os.sep + 'fullGrid_' + neighThres + '.npy')   

#------------------------------------------------
## read file containing case coordinates and bandwidths
## for each case, find spatiotemporal grid point neighbors and compute risk contribition

disFile = open('outputs/ST_IB_2' + os.sep + 'sim_' + sim + os.sep + 'peopleTime_' + neighThres + '.txt','r')

rCount = 0
for record in disFile:
    line = record.split(",")
	#coordinates of case point, bandwidths, population within kernel
    xC, yC, tC, hs, ht, pop = float(line[1]),float(line[2]),float(line[3]),float(line[4]),float(line[5]),float(line[6])

	#query point
    cIndex = coordToIndex(xC, yC, tC)
    qX, qY, qT = cIndex[0],cIndex[1],cIndex[2]  #query point index
    sDeg = int(hs / xyRes)
    tDeg = int(ht / tRes)
    #print coordToIndex(xC, yC, tC)
    if (qX < xDim and qX >= 0) and (qY < yDim and qY >= 0) and (qT < tDim and qT >= 0):
        fullGridArr[qX][qY][qT][3] += 1

	#find neighboring grid points
	count = 0

	for i in range(qX-sDeg,qX+sDeg+1):
	    if i < xDim and i >= 0:
	        for j in range(qY-sDeg,qY+sDeg+1):
	            if j < yDim and j >= 0:
	                for k in range(qT-tDeg,qT+tDeg+1):
	                    if k < tDim and k >= 0:

	                        #get neighbor coordinates
	                        nX, nY, nT = fullGridArr[i][j][k][0], fullGridArr[i][j][k][1], fullGridArr[i][j][k][2]

	                        #compute space-time distance between neighbor and query point
	                        sDist = pow(pow(xC-nX,2)+pow(yC-nY,2),0.5)
	                        tDist = abs(tC-nT)

	                        #if st-distance smaller than st-bandwidths
	                        if sDist <= hs and tDist <= ht:

	                            #compute density contribution
	                            STKDE = densityF(xC, yC, tC, nX, nY, nT, hs, ht)
	                            fullGridArr[i][j][k][5] += STKDE[0] / pop
	                            fullGridArr[i][j][k][6] += STKDE[1] / pop

    rCount += 1

disFile.close()

#initialize output array
nRows = xDim * yDim * tDim
nCols = 8   #columns ID, x, y, t, nCount, Ks, Kt
outArr = np.zeros((nRows,nCols))

ID = 0
xIndex = 0

while xIndex < xDim:
    yIndex = 0
    while yIndex < yDim:
        tIndex = 0
        while tIndex < tDim:

            outArr[ID][0] = ID                                      #id
            outArr[ID][1] = fullGridArr[xIndex][yIndex][tIndex][0]        #x
            outArr[ID][2] = fullGridArr[xIndex][yIndex][tIndex][1]        #y
            outArr[ID][3] = fullGridArr[xIndex][yIndex][tIndex][2]        #z
            outArr[ID][4] = fullGridArr[xIndex][yIndex][tIndex][3]     #nCount
            outArr[ID][5] = fullGridArr[xIndex][yIndex][tIndex][4]     #pCount
            outArr[ID][6] = fullGridArr[xIndex][yIndex][tIndex][5]     #s-density Ks
            outArr[ID][7] = fullGridArr[xIndex][yIndex][tIndex][6]     #t-density Kt

            ID += 1
            tIndex += 1
        yIndex += 1
    xIndex += 1

#scale Ks and Kt to 0-1
outArr[:,6]= outArr[:,6]/max(outArr[:,6])
outArr[:,7]= outArr[:,7]/max(outArr[:,7])
outArr[:,6]= outArr[:,6] * outArr[:,7]

#delete column
finalArr = np.delete(outArr, (7), 1)

outFile = open('outputs/ST_IB_3' + os.sep + 'density_' + neighThres + '.txt','w')

for i in finalArr:
    if i[1] == 0 and i[2] == 0 and i[3]  == 0:
        pass
    else:
        #write[x,y,t,nCount,pCount,density]
        outFile.write(str(i[1]) + "," + str(i[2]) + "," + str(i[3]) + "," + str(i[4]) + "," + str(i[5]) + "," + str(i[6]) + "\n")

outFile.close()
