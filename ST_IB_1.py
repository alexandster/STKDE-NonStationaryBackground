#ST_IB_1.py, by Alexander Hohl
#This script describes the computation of space-time bandwidths of kernels centered on data points

import numpy as np
from scipy import spatial
import sys

#------------------------------------------------
# read case points file
disFile = open('data/points_obs.csv', "r")
inXYT = []
disFile.readline()
for record in disFile:
    inXYT.append([float(record.split(",")[1]),float(record.split(",")[2]),float(record.split(",")[3])])
disFile.close()
numPts = len(inXYT)

#sort temporally
inXYT_s = np.array(sorted(inXYT, key=lambda a: a[2]))
#------------------------------------------------

#------------------------------------------------
#build k/d tree index on cases
sTree = spatial.cKDTree(inXYT_s[:,:2])

#------------------------------------------------
#initialize variables
stNeighIndex = []    #stores indexes of spatiotemporal neighbors
mNN = np.inf         # minimum number of neighbors
NN = numPts            # big number: number of nearest neighbors to search for

neighThresList = [25,30,35,40,45]       # minimum number of ST neighbors threshold

for neighThres in neighThresList:

    #------------------------------------------------
    # open output file
    outFile = open('outputs/ST_IB_1/bandwidths_' + str(neighThres) + '.txt','w')

    i = 200              # iterator variable. ignore first couple of datapoints because they are early in the study period and might not have enough teporal neighbors.

    #------------------------------------------------
    #loop through all data points
    while i < numPts:

        #query point
        sCoord = inXYT_s[i,:2]
        tCoord = inXYT_s[i,2]

        #query the tree, input number of neighbors to search for
        sNeigh = sTree.query(sCoord,NN)

        #temporal neighbors list
        tNeigh = []

        #number of temporal neighbors. procedure ensures that no negative
        #indexes are created.
        if i < NN:
            current = 0
        else:
            current = i - NN

        # append temporal neighbors to list. procedure ensures that only cases from the past are considered.
        # it also deals with cases that co-occur at the same time.
        #print(inXYT_s[current,2], inXYT_s[i,2])
        while inXYT_s[current,2] < inXYT_s[i,2]:
            tNeigh.insert(0,current)
            current += 1

        # intersect lists of spatial and temporal neighbors. check cardinality. If cardinality is lower than
        # minimum number of ST neighbors threshold, simultaneousely add the next spatial and temporal neighbor
        # from the spatial and temporal neighbor lists, interesect and check cardinality again.
        j = neighThres           #number of spatial and temporal nearest neighbors to consider. at least the minimum number of ST neighbors
        stNeigh = []
        sDistMax = 0            # record maximum distance of farthest spatial neighbor of the intersection set
        tDistMax = 0            # record maximum distance of farthest temporal neighbor of the intersection set
        while len(stNeigh) < neighThres:
            stNeigh = np.intersect1d(list(sNeigh[1][:j]), tNeigh[:j])

            # spatial distance
            sDist = sNeigh[0][j-1]

            # temporal distance. ensuring index k is within range of tNeigh
            if j < len(tNeigh):
                k = j
            else:
                k = len(tNeigh) - 1
            #print(tNeigh)
            tDist = tCoord - inXYT_s[tNeigh[k],2]

            if sDist > sDistMax:
                sDistMax = sDist
            if tDist > tDistMax:
                tDistMax = tDist

            j += 1
        #print(j, tCoord)

        outFile.write(str(i) + "," + str(sCoord[0]) + "," + str(sCoord[1]) + "," + str(tCoord) + "," + str(sDistMax) + "," + str(tDistMax) + "\n")

        i += 1

outFile.close()
