#ST_IB_MC_2.py, by Alexander Hohl
#This script

import numpy as np
from scipy import spatial
import sys, os

sim = sys.argv[1]				#simulation 0-99
neighThres = sys.argv[2]       # minimum number of ST neighbors threshold

#------------------------------------------------
#spatiotemporal domain and resolution
xmin, xmax, ymin, ymax, tmin, tmax = 323000, 337300, 369100, 387700, 0, 730
xyRes, tRes = 100, 1
xyResHalf = xyRes/2.0

#number of points in each dimension
xDim = int((xmax - xmin)/xyRes)  
yDim = int((ymax - ymin)/xyRes)  
tDim = int((tmax - tmin)/tRes)  

#print xDim, yDim, yDim


# function to convert coordinates to index for inArr
#--------------------------------------------------------------------------------------
def coordToIndex(x,y,tStart,tEnd):

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

    tIndex2Start = int(tStart)-tmin
    tIndex2End = int(tEnd)-tmin

    return [xIndex2, yIndex2, tIndex2Start, tIndex2End]

#------------------------------------------------
#initialize regular grid: 3d grid of tuples: (x, y, t, nCount, pCount, ds, dt) |nCount: how many disease cases within voxel, pCount: how much population within voxel
fullGridArr = np.zeros((xDim, yDim, tDim, 7))

#populate the grid
xG = xmin
while xG < xmax:
    yG = ymin
    while yG < ymax:
        tG = tmin
        while tG < tmax:
            #create index
            gIndex = coordToIndex(xG, yG, tG, tG)
            xIndex, yIndex, tIndex = gIndex[0], gIndex[1], gIndex[2]

            #assign coordinates
            fullGridArr[xIndex][yIndex][tIndex][0] = xG
            fullGridArr[xIndex][yIndex][tIndex][1] = yG
            fullGridArr[xIndex][yIndex][tIndex][2] = tG
            tG += tRes
        yG += xyRes
    xG += xyRes

#------------------------------------------------
#read population files, add them to one array [x, y, tStart, tEnd, flag]	|flag: for avoiding double count (how many population  within voxel?)

i = 0
popList = []
while i <  334:
    popFile = open('outputs/pop_model/sim_0/barrio_" + str(i) + ".txt", "r")		#since uncertainty from population simulation is small, we can just pick the first dataset
    for record in popFile:
        x, y, tStart, tEnd = record.split(",")
        popList.append([float(x),float(y),float(tStart),float(tEnd.strip()), 0])
    popFile.close()
    i += 1
 
popArr = np.array(popList)

#------------------------------------------------
## read file containing case coordinates and bandwidths [ID, x, y, t, hs, ht]
disFile = open('outputs/ST_MC_1/sim_' + sim + os.sep + 'bandwidths_' + neighThres + '.txt', "r")
disList = []
for record in disFile:
    line = record.split(",")
    disList.append([float(line[0]),float(line[1]),float(line[2]),float(line[3]),float(line[4]),float(line[5])])
disFile.close()
numPts = len(disList)

#------------------------------------------------
# output directory
outDir = 'outputs/ST_MC_2' + os.sep + 'sim_' + sim

# open output File
outFile = open(outDir + os.sep + "peopleTime_" + neighThres + ".txt",'w')

#------------------------------------------------
# define get overlap function. returns overlap between two intervals.
def getOverlap(a, b):
    return max(0, min(a[1], b[1]) - max(a[0], b[0]))

#------------------------------------------------

#build kd tree
sTree = spatial.cKDTree(popArr[:,:2])

#printcounter = 0
count = 0
#for each disease case, compute populaiton inside kernel
for i in disList:

    sCoord = i[1:3]

    # query the tree: return all population points within bandwidth
    sNeigh = sTree.query_ball_point(sCoord, i[4])

    pt = 0      #people-time: how many people present inside kernel for how long? population adjustment.
    # for each population neighbor, calculate length of stay within kernel
    for j in sNeigh:
        #print("j: ", j)
        popStart = popArr[j,2]      #start of population column
        popEnd = popArr[j,3]        #end of population column
        kerEnd = i[3]               #end of kernel (=time of disase case)
        kerStart = kerEnd - i[5]    #start of kernel (=time of disease case minus temporal bandwidth)
        pt += getOverlap([popStart,popEnd],[kerStart,kerEnd])

        #add pop within voxel
        gIndex = coordToIndex(popArr[j,0],popArr[j,1],popStart,popEnd)      
        xIndex, yIndex, tIndex1, tIndex2 = gIndex[0], gIndex[1], gIndex[2], gIndex[3]

        if xIndex >= 0 and xIndex < xDim and yIndex >= 0 and yIndex < yDim and tIndex >= 0 and tIndex < tDim and popArr[j,4]==0:
            fullGridArr[xIndex,yIndex,tIndex1:tIndex2,4] += 1.0/(popEnd-popStart)	#add the proportion of the population column that is located inside the voxel
            popArr[j,4] = 1 

    #[ID, x, y, t, hs, ht, pt] |pt: people-time
    outFile.write(str(i[0]) + "," + str(i[1]) + "," + str(i[2]) + "," + str(i[3]) + "," + str(i[4]) + "," + str(i[5]) + "," + str(pt) + "\n")

    count += 1

outFile.close()

np.save(outDir + os.sep + "fullGrid_" + neighThres,fullGridArr)

