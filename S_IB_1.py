import numpy as np
from scipy import spatial
import sys

#------------------------------------------------
# read case points file
disFile = open('data/points_obs.csv', 'r')
inXYT = []
disFile.readline()
for record in disFile:
    inXYT.append([float(record.split(',')[1]),float(record.split(',')[2]),float(record.split(',')[3])])
disFile.close()

inXYT_s = np.array(sorted(inXYT, key=lambda a: a[2]))
#------------------------------------------------

#discard temporal attribute
inXY_s = np.array(inXYT)[200:,:2]
numPts = len(inXY_s)

#build k/d tree index on cases
sTree = spatial.cKDTree(inXY_s)

#------------------------------------------------
#initialize variables

neighThresList = [25,30,35,40,45]       # minimum number of neighbors threshold

for neighThres in neighThresList:

    #------------------------------------------------
    # open output file
    outFile = open('outputs/S_IB_1/bandwidths_' + str(neighThres) + '.txt','w')

    i = 0              # iterator variable
    #------------------------------------------------
    #loop through all data points
    while i < numPts:

        #query point
        sCoord = inXY_s[i]
        
        #query the tree, input number of neighbors to search for
        sNeigh = sTree.query(sCoord,numPts)

        #identify ith neighbor distance
        sDist = sNeigh[0][neighThres-1]
        outFile.write(str(i) + ',' + str(sCoord[0]) + ',' + str(sCoord[1]) + ',' + str(sDist) + '\n')

        i += 1
    outFile.close()

