#ST_IB_MC_1.py, by Alexander Hohl
#This script

#import modules
import numpy as np
from scipy import spatial
import sys, os

#arguments
sim = sys.argv[1]				#simulation number
neighThres = int(sys.argv[2])	#number of neighbors threshold

#load simulated dataset 
disFile = open('data/case_rand_full/sim_' + sim + '.txt', "r")
inXYT = []
disFile.readline()
for record in disFile:
    inXYT.append([float(record.split(" ")[1]),float(record.split(" ")[2]),float(record.split(" ")[3])])
disFile.close()

#number of points
numPts = len(inXYT)

#sort dataset temporally
inXYT_s = np.array(sorted(inXYT, key=lambda a: a[2]))

#index dataset
sTree = spatial.cKDTree(inXYT_s[:,:2])
stNeighIndex = []

#maximum number of neighbors
mNN = np.inf

#current number of neighbors
NN = numPts

#outup path
outFile = open('outputs/ST_MC_1/sim_' + sim + os.sep + 'bandwidths_' + str(neighThres) + '.txt','w')

#loop through all data points
i = 200
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
    while inXYT_s[current,2] < inXYT_s[i,2]:
        tNeigh.insert(0,current)
        current += 1
		
    # intersect lists of spatial and temporal neighbors. check cardinality. If cardinality is lower than
    # minimum number of ST neighbors threshold, simultaneousely add the next spatial and temporal neighbor
    # from the spatial and temporal neighbor lists, interesect and check cardinality again.
    j = neighThres
    stNeigh = []
    sDistMax = 0
    tDistMax = 0
    while len(stNeigh) < neighThres:
        stNeigh = np.intersect1d(list(sNeigh[1][:j]), tNeigh[:j])
        sDist = sNeigh[0][j-1]
        if j < len(tNeigh):
            k = j
        else:
            k = len(tNeigh) - 1
        tDist = tCoord - inXYT_s[tNeigh[k],2]
        if sDist > sDistMax:
            sDistMax = sDist
        if tDist > tDistMax:
            tDistMax = tDist
        j += 1
    outFile.write(str(i) + "," + str(sCoord[0]) + "," + str(sCoord[1]) + "," + str(tCoord) + "," + str(sDistMax) + "," + str(tDistMax) + "\n")
    i += 1
outFile.close()
